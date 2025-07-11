
# Novel-V11 Factory 🚀
> "소설 공장" – V11 엔진 기반 웹소설 자동 제작 파이프라인

## 최종 목표: **10화 파일럿 자동 생성**

---

## 1. 개발 환경 설정 (최초 1회)

```bash
git clone https://github.com/GameChanger92/novel-v11-factory.git
cd novel-v11-factory

# 1. 가상환경 권장 (선택)
python -m venv .venv && source .venv/bin/activate

# 2. 필수 라이브러리
pip install -r requirements.txt --prefer-binary --no-cache-dir
pip install -e .    # 로컬 패키지(엔진) editable 설치

# 3. 환경 설정 파일 준비
cp .env.example .env          # API 키 / 비밀번호 편집
```

환경 파일 `.env`에 다음 항목들을 설정하세요:

```env
# Neo4j
NEO4J_PASSWORD=please_change_this
# OpenAI or Gemini 2.5
OPENAI_API_KEY=sk-...
```

---

## 2. 서비스 실행 (매 세션)

### Docker 사용 방식

| 환경 | 사용 방법 |
|----------|-----------|
| **GitHub Codespaces** | Devcontainer에 탑재된 **Docker-in-Docker**(DinD) 자동 사용.<br>재빌드 후 `docker compose ps`로 상태 확인하면 준비 완료. |
| **로컬 PC + Docker Desktop** | DinD 아니므로 `docker compose up -d --build`만 실행하면 됨. |

```bash
# GitHub Codespaces: 상태 확인만
docker compose ps

# 로컬 PC: 서비스 시작
docker compose up -d --build
```

Neo4j Browser → [http://localhost:7474](http://localhost:7474)
- Username: `neo4j`
- Password: `.env` 파일의 `NEO4J_PASSWORD` 값

---

## 3. 데이터 준비 (프로젝트별 1회)

```bash
# 스키마 초기화 및 데이터 동기화
docker compose exec gamechanger_worker_v11 \
  python scripts/graph_sync_v11.py --project Pilot --init-schema

docker compose exec gamechanger_worker_v11 \
  python scripts/graph_sync_v11.py --project Pilot

# FAISS 인덱스 빌드 (RAG용)
docker compose exec gamechanger_worker_v11 \
  python scripts/build_faiss_index_v11.py --project Pilot --source-bible projects/Pilot/story_bible_v11.json
```

---

## 4. 파일럿 10화 생성

```bash
docker compose exec gamechanger_worker_v11 \
  python scripts/run_novel.py --project Pilot --total 10
# → projects/Pilot/episodes/EP001.md ~ EP010.md
```

생성된 파일들은 `projects/Pilot/episodes/` 디렉토리에서 확인하세요.


## 🟢 Build FAISS Index

Build a FAISS index from story bible v11 for semantic search and RAG:

```bash
# Build FAISS index for the Pilot project
python scripts/build_faiss_index_v11.py --project Pilot --source-bible projects/Pilot/story_bible_v11.json

# Use a different embedding model (optional)
python scripts/build_faiss_index_v11.py --project Pilot --source-bible projects/Pilot/story_bible_v11.json --model sentence-transformers/paraphrase-MiniLM-L3-v2
```

This creates:
- `memory/faiss_index/Pilot/index.faiss` - The FAISS vector index
- `memory/faiss_index/Pilot/meta.pkl` - Metadata for each indexed text

---

## ✅ Roadmap Progress

| 주차 | 목표 | 상태 |
|------|------|------|
| **Week 1** | Foundation & 3-Episode MVP | ✅ |
| **Week 2** | Memory System Integration<br>(KG+RAG, 토큰 Budget) | ✅ `v11.0.0-week2-done` |
| **Week 3** | Plot & Consistency (Arc/Beat/Scene, Consistency Guard) | 🔜 진행 예정 |

### Week 1: Foundation & 3-Episode MVP
- ✅ GitHub repo & Codespace setup is working
- ✅ Basic folder structure (engine/, scripts/, etc.) is created
- ✅ requirements.txt is prepared
- ✅ Basic CI workflow passes (shows a green check)
- ✅ run_novel.py MVP successfully generates 3 pilot episodes

### Week 2: Memory System Integration
- ✅ Neo4j container is running successfully via Docker Compose
- ✅ Integrate Knowledge Graph (KG) and RAG into the pipeline

---

