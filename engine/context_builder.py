# engine/context_builder.py
from engine.retriever import retrieve_unified_context
from engine.config import get_settings

# 여기에 Story Bible에서 다른 정보를 읽어오는 로직을 추가할 수 있습니다.
# from engine.story_bible_loader import load_story_bible


def build_final_prompt_context(project: str, episode_id: str, character_name: str, plot_query: str) -> str:
    """
    주어진 정보를 바탕으로 모든 소스에서 컨텍스트를 검색하고,
    LLM에 전달할 최종 프롬프트 문자열을 구성합니다.
    """
    print(f"Building final prompt context for {project} - {episode_id}...")

    # 1. 설정에서 안전한 토큰 예산을 가져옵니다.
    settings = get_settings()
    budget = settings.SAFE_TRIM_BUDGET

    # 2. 통합 리트리버를 호출하여 가장 중요한 정보 목록을 가져옵니다.
    #    - plot_query는 "주인공이 동굴에서 고대 유물을 발견한다"와 같은 현재 장면에 대한 설명입니다.
    #    - budget을 전달하여 토큰 제한을 적용합니다.
    top_k_contexts = retrieve_unified_context(
        project=project,
        character_name=character_name,
        query=plot_query,
        top_k=5,  # 최종적으로 5개의 가장 중요한 정보를 선택
        budget=budget
    )

    # 3. 검색된 정보 목록을 LLM이 이해하기 쉬운 형식으로 조합합니다.
    context_str = "[중요 배경 정보]\n"
    if not top_k_contexts:
        context_str += "- 현재 사용 가능한 배경 정보 없음."
    else:
        for i, context_item in enumerate(top_k_contexts, 1):
            context_str += f"{i}. {context_item}\n"

    # 4. (선택적) 여기에 추가적인 고정 정보나 지시문을 덧붙일 수 있습니다.
    # context_str += "\n[소설의 핵심 규칙]\n- 주인공은 절대 사람을 죽이지 않는다."

    print("Prompt context successfully built.")
    return context_str.strip()


# --- 스크립트 직접 실행 테스트용 ---
if __name__ == '__main__':
    # 이 테스트를 실행하려면 아래의 전제조건이 필요합니다:
    # 1. `memory/faiss_index/Pilot/` 에 FAISS 인덱스 파일이 있어야 함.
    # 2. Neo4j 데이터베이스가 실행 중이고, '성훈' 캐릭터 데이터가 있어야 함.
    # 3. `.env` 파일에 모든 접속 정보가 올바르게 설정되어 있어야 함.
    try:
        print("--- Running Context Builder Test ---")
        # 현재 에피소드의 줄거리를 가정한 쿼리
        current_plot_query = "성훈이 어두운 지하 던전의 입구를 발견하고 탐험을 시작하려 한다."

        final_context = build_final_prompt_context(
            project='Pilot',
            episode_id='EP001',
            character_name='성훈',
            plot_query=current_plot_query
        )

        print("\n--- Generated Final Prompt Context ---")
        print(final_context)

    except FileNotFoundError as e:
        print(f"\n[오류] 테스트를 위해 FAISS 인덱스가 먼저 필요합니다: {e}")
    except Exception as e:
        print(f"\n[오류] 예기치 못한 에러 발생: {e}")
