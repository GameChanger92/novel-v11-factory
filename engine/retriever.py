# engine/retriever.py
import faiss
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import tiktoken

from engine.config import get_settings

# --- 전역 캐시: 모델, 인덱스, 드라이버 등 ---
# 이 객체들은 처음 호출될 때 한 번만 로드됩니다.
_model = None
_faiss_idx = {}
_meta = {}
_neo4j_driver = None

# --- Asset 로더들 ---


def get_embedding_model():
    """싱글턴 패턴으로 임베딩 모델을 로드합니다."""
    global _model
    if _model is None:
        settings = get_settings()
        print(f"Loading embedding model: {settings.EMBEDDING_MODEL}...")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        print("Model loaded.")
    return _model


def _load_faiss_assets(project: str):
    """프로젝트별 FAISS 인덱스와 메타데이터를 로드합니다."""
    if project in _faiss_idx:
        return
    settings = get_settings()
    root = Path(settings.FAISS_ROOT) / project
    index_path = root / "index.faiss"
    meta_path = root / "meta.pkl"

    if not index_path.exists() or not meta_path.exists():
        raise FileNotFoundError(f"FAISS index for project '{project}' not found at {root}")

    print(f"Loading FAISS index for project '{project}'...")
    _faiss_idx[project] = faiss.read_index(str(index_path))
    with open(meta_path, 'rb') as f:
        _meta[project] = pickle.load(f)
    print("FAISS index loaded.")


def get_neo4j_driver():
    """싱글턴 패턴으로 Neo4j 드라이버를 로드합니다."""
    global _neo4j_driver
    if _neo4j_driver is None:
        from neo4j import GraphDatabase
        settings = get_settings()
        print("Initializing Neo4j driver...")
        _neo4j_driver = GraphDatabase.driver(
            settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        print("Neo4j driver initialized.")
    return _neo4j_driver


# --- 개별 검색기 (Retrievers) ---


def search_rag_by_query(project: str, query: str, k: int = 5) -> list[tuple[float, str]]:
    """FAISS 벡터 검색을 수행하고, (유사도 점수, 텍스트 스니펫) 리스트를 반환합니다."""
    _load_faiss_assets(project)
    model = get_embedding_model()

    query_vector = model.encode([query])
    distances, indices = _faiss_idx[project].search(query_vector, k)

    results = []
    for i, dist in zip(indices[0], distances[0]):
        if i != -1:
            # Cosine distance를 similarity로 변환 (1 - distance)
            similarity = 1.0 - dist
            # 예시: 메타데이터에서 'content' 키를 가져옴
            content = _meta[project].get(i, {}).get('content', '내용 없음')
            results.append((similarity, content))
    return results


def search_kg_for_character_status(project: str, character_name: str) -> str | None:
    """Neo4j에서 캐릭터 상태를 조회하고, 포맷된 문자열로 반환합니다."""
    driver = get_neo4j_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Character {name: $name})
            RETURN c.name as name, c.status as status, c.summary as summary
        """, name=character_name).single()

        if not result:
            return None

        # 조회된 결과를 하나의 정보 덩어리(문자열)로 가공
        return (
            f"주인공 '{result['name']}' 정보: "
            f"현재 상태는 '{result['status']}'이며, "
            f"핵심 설정은 다음과 같음 - {result['summary']}"
        )


# --- 통합 검색기 (Retrieval Mixer) ---


def _count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """텍스트의 토큰 수를 계산합니다."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))
    except Exception:
        # tiktoken 오류 시 대략적인 추정치 사용 (단어 수 * 1.3)
        return int(len(text.split()) * 1.3)


def retrieve_unified_context(project: str, character_name: str, query: str,
                             top_k: int = 5, budget: int | None = None) -> list[str]:
    """
    KG와 RAG에서 정보를 검색하고, 가중치를 부여하여 가장 중요한 순서대로 정렬된 컨텍스트 목록을 반환합니다.
    budget이 지정된 경우, 누적 토큰 수가 예산을 초과하지 않도록 제한합니다.
    """
    # 1. 각 소스에서 정보 검색
    kg_result = search_kg_for_character_status(project, character_name)
    # RAG는 더 많은 후보군을 가져오기 위해 top_k의 2배수를 검색
    rag_results = search_rag_by_query(project, query, k=top_k * 2)

    # 2. 결과에 점수를 부여하여 통합 리스트 생성
    ranked_results = []

    # KG 결과는 가장 중요하므로 최상위 점수(1.0) 부여
    if kg_result:
        ranked_results.append((1.0, kg_result))

    # RAG 결과는 유사도 점수를 그대로 사용
    for similarity, content in rag_results:
        # 점수가 너무 낮은 결과는 제외 (예: 0.7 미만)
        if similarity >= 0.7:
            ranked_results.append((similarity, content))

    # 3. 점수 기준으로 내림차순 정렬
    ranked_results.sort(key=lambda x: x[0], reverse=True)

    # 4. 토큰 예산이 지정된 경우 예산 내에서만 결과 반환
    if budget is not None:
        final_context_list = []
        current_token_count = 0

        for score, text in ranked_results:
            text_tokens = _count_tokens(text)
            if current_token_count + text_tokens <= budget:
                final_context_list.append(text)
                current_token_count += text_tokens
            else:
                # 예산 초과 시 중단
                break

        return final_context_list
    else:
        # 예산이 지정되지 않은 경우 기존 로직 사용
        final_context_list = [text for score, text in ranked_results[:top_k]]
        return final_context_list
