### <a name="_7uy3u48k2nta"></a>**“소설 공장” — 프로젝트/장르마다 무제한으로 찍어내는 V11‑Factory 아키텍처**
**목표 재확인**
` `*단일 작품을 디버깅하며 키우는 엔진* 이 아니라
` `*▶ “딸깍 → 스카이림급 A, 딸깍 → GTA급 B …” 를 무한 증식*하는 **다품종 웹소설 자동화 공장**이 필요하다는 뜻입니다.

아래 설계는 **V11 핵심 모듈**(KG + RAG + Editor + Guard + RL) 을 \*\*“멀티‑프로젝트·멀티‑장르 공용 서비스”\*\*로 승격해, 클릭 한 번마다 *새 Story Bible 패키지 → 전체 200 ~ 300 화 완결*까지 풀파이프라인을 자동 배포·실행하도록 만든 **Factory‑grade** 구조입니다.

-----
## <a name="_4851rogtyr7e"></a>**1. 상위 개념도 — “생산 라인”을 분리한다**
┌─────────────── Web UI / CLI Frontend ───────────────┐

│ ① New‑Project Wizard  ② Run Queue  ③ Dashboard      │

└──────────────────┬───────────┬──────────────────────┘

`                   `│trigger    │monitor

`        `┌──────────▼───────────▼───────────┐

`        `│    Orchestrator (Service Bus)    │  ← Celery · Argo · Temporal

`        `└┬───────────┬────────┬───────────┬┘

`   `create│           │route    │events     │logs

┌────────▼───┐ ┌─────▼────┐ ┌──▼──────┐┌──▼──────┐

│ ProjectDB  │ │ K/V Meta │ │ Metrics ││ Logs   │   ← Postgres · Redis

└────────────┘ └──────────┘ └─────────┘└────────┘

`   `│namespaced volumes

`   `│

┌──▼──────────────────────────────────────────┐

│  Compute Pool (Worker Images)               │  ← k8s Jobs / Docker Swarm

│  ├─ ContextBuilder\_v11                      │

│  ├─ DraftGenerator\_v11                      │

│  ├─ EditorAgent\_v11                         │

│  ├─ ConsistencyGuard\_v11                    │

│  ├─ StoryBibleUpdater\_v11                   │

│  └─ (optional) RL\_Tuner\_v11                 │

└────┬────────────────────────────────────────┘

`     `│access

┌────▼───────────┐      ┌───────────────┐      ┌──────────────┐

│ Neo4j Cluster  │      │ FAISS Cluster │      │ ObjectStore  │

│ (multi‑tenant) │      │  (vector RAG) │      │ episodes/zip │

└────────────────┘      └───────────────┘      └──────────────┘

- **Frontend** — Streamlit·Gradio UI *또는* REST API.
- **Orchestrator** — 큐 기반(예 Celery)으로 **“프로젝트 단위 Job”** 스케줄.
- **Compute Pool** — 동일 이미지를 **수십 Worker**로 수평 확장 → 동시 다작.
- **스토리지** — Neo4j/FAISS는 **Project ID 네임스페이스**로 격리, 결과물은 S3‑호환 버킷.
-----
## <a name="_aq6vv1nymykk"></a>**2. 프로젝트‑팩 생성 → 완결 자동화 흐름**

|**단계**|**트리거 (한 줄)**|**내부 동작 (모듈)**|**산출물**|
| :-: | :-: | :-: | :-: |
|**① Wizard**|new\_project("⟪장르팩⟫",300)|*story\_bible\_init\_v11* + *graph\_sync --init*|/projects/PX/story\_bible.json|
|**② Queue In**|enqueue("PX", 300)|Orchestrator Job 등록|Row in Run Queue|
|**③ Arc Loop**|run\_full\_pipeline\_v11 Worker|Arc 1‑n (30 화씩) draft → editor → guard → update|/episodes/EP\*\*\*.md|
|**④ Packaging**|Post‑hook|전체 Markdown → ZIP/CSV, e‑book 변환|s3://outbox/PX.zip|
|**⑤ Publish Hook**|Platform API 키 존재 시|자동 예약 업로드, 통계 수집|Sales/Analytics|

*모듈 코드는 V11 사양 그대로, 단 **project‑slug** 인자를 받아 **네임스페이스 분리**만 추가.*

-----
## <a name="_5l9rdyhikywo"></a>**3. “장르 팩” 디자인 — 무한 변종을 찍는 템플릿 시스템**

|**레이어**|**역할**|**예시**|
| :-: | :-: | :-: |
|**Genre Template**|공통 톤·문체·장르 규칙 (ex. 현대 판타지, 서양 하이‑판타지, 게임 이식)|templates/genre/fantasy\_kr.yaml|
|**Theme Module**|작품 핵심 주제/갈등 쌍|“돈이 너무 쉽게 벌린다”, “복수, 정체성”|
|**Style Plugin**|대사체, 서술 뉘앙스, 1‑인칭↔3‑인칭|plugins/style/noir\_dialogue.py|
|**Constraint Set**|금기어, 길이, 플랫폼 룰|문피아 15세 규정, 노출어 필터|

**“딸깍”** 할 때마다 GenreTemplate + Theme + Style + Constraint 를 조합 → 새로운 Story Bible 씨앗 생성 → 동일 파이프라인 통과.

플러그인 매니페스트/엔트리포인트 구조는 Master Guide의 **plugins/manifest.yaml** 예시와 동일.

-----
## <a name="_rzqxm8aume9d"></a>**4. 리소스·비용 모델 — 동시 10 개 작품 공장 기준**

|**자원**|**스펙**|**산술 (10×300 화)**|**월 비용 가이드**|
| :-: | :-: | :-: | :-: |
|**LLM 토큰**|Draft=Gemini 2.5‑Pro, Editor=GPT‑4o‑mini|1\.6 M tok / 작품 ≈ $120|$1 200|
|**Neo4j AuraDS**|8 vCPU / 32 GB (HA)|~2 GB / 작품|$500|
|**FAISS (EC2 CPU)**|c7g.2xlarge × 2 spot|벡터 4 M|$350|
|**Worker Pool**|Docker‑GPU 단가 무관 (LLM API)|6 vCPU Node × 4|$400|
|**S3 Storage**|5 GB / 작품 마크다운, zip|50 GB|$10|
|**총합**|||**≈ $2 460 / 월**|

*ROI 계산*: 문피아 유료 200 화 × 평균 7 000 원 독자 400명 → ≈ $5 600 / 작품 ⇒ 50 % 수익률.

-----
## <a name="_ioeuy6il4nbk"></a>**5. 핵심 난제 & 해결책**

|**문제**|**공장‑스케일 해결책**|
| :-: | :-: |
|**① DB 동시 접속 폭주**|Neo4j Read‑Replica 추가, Cypher JOIN 최소화, Arc 단위 배치|
|**② 엇비슷한 스토리**|*Theme Module* 난수‑시드 + RL Reward Scorer → 중복 패턴 감점|
|**③ 모델 비용 급증**|Draft → Gemini Pro / Claude‑Haiku 혼합, Editor만 GPT‑4 고정|
|**④ 저작권 클레임**|PII/Similarity Scanner 플러그인 → 출력 전 7‑gram 겹침 < 20 % 검증|
|**⑤ 대규모 장애**|“Chaos Day” 시나리오 (Neo4j 다운, 429 폭주) 월 1회 자동 리허설|

-----
## <a name="_hi7ioic4ouj8"></a>**6. 90‑일 구축 로드맵 (비개발 1인 + GPT‑코파일럿)**

|**주**|**마일스톤**|**산출물**|
| :-: | :-: | :-: |
|1‑2주|**Mono‑project MVP** 배치 성공|300 화 1작품 완결|
|3‑4주|Orchestrator + Queue PoC|celery\_worker/, run\_queue DB|
|5‑6주|멀티‑Tenant Neo4j 스키마, Namespace VOLs|graph\_sync\_v11.py --tenant|
|7‑8주|GenreTemplate & StylePlugin SDK|templates/genre/\*, plugins/style/\*|
|9‑10주|Web Dashboard v1 (Streamlit)|New‑Project Wizard, Progress Board|
|11‑12주|Chaos Day 스크립트 & Auto‑Retry|chaos\_test/, retry\_controller\_v11.py|
|13주|**Factory α 런칭** — 동시 3 작품 운영|실매출 모니터링 시작|
|14‑‑‑|RL‑Scorer 데이터 수집 → PPO 파인튜닝|ppo\_tune\_v11.py, quality↑ 5 %|

-----
## <a name="_npgxbg42co2j"></a>**7. 실무 “한 줄 요약”**
**엔진을 리팩터하지 말고, “멀티‑Tenant 큐 + 플러그인 장르 팩” 구조로 감싸라.**
` `그러면 **마우스 딸깍 한 번**마다 *신규 Story Bible*이 스스로 **200 ~ 300 화 완결작**을 찍어내고, 당신은 **운영·마케팅·수익 확인**만 집중하면 됩니다.

