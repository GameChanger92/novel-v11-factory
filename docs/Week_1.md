## <a name="_8hqmby8wfxmb"></a>**📅 Week 1 (Days 1 – 7) — “엔진 뼈대 + 첫 3 화 파일럿”**
❏ 총 투입 시간 : 약 10 h (하루 1 ~ 2 h)
` `❏ 주간 목표 : **리포 구조·CI 녹색·150줄 MVP 실행 → 3 화 생성 확인**

|**Day**|**당신이 할 일 (✓ 표시하며 진행)**|**상세 명령 & 검증 포인트**|
| :-: | :-: | :-: |
|**D1 — Repo & Codespaces 개통**|□ GitHub 신규 repo gamechanger‑v11-factory 생성□ “Use this template?” NO → 빈 repo□ **Codespaces ↗** 버튼 → *Create*|1\. 리포 페이지 > **Settings → Codespaces** 60 h 쿼터 확인.2. Codespace 생기면 좌측 터미널에python --version → 3.10 ↑ 확인.|
|**D2 — 패키지 스캐폴딩**|□ 터미널: pip install cookiecutter□ cookiecutter gh:audreyr/cookiecutter-pypackage --no-input project\_slug=engine|*outputs*: engine/\_\_init\_\_.py, setup.py 등.□ git add . && git commit -m "chore:init cookiecutter"□ git push origin main|
|**D3 — CI 골격 & 종속성**|□ .github/workflows/main\_ci\_cd.yml 복사 (Master‑Guide 부록 14) □ requirements.txt 작성: openai, pytest, flake8, python-dotenv|Codespace 터미널에서 pip install -r requirements.txt.**GitHub Actions → lint‑and‑test** 잡가서 녹색인지 확인.|
|**D4 — 환경 변수 & Secrets**|□ Repo Root: cp .env.sample .env 후 편집 OPENAI\_API\_KEY=sk-... NEO4J\_PASSWORD=myneo4jpw (임시)□ GitHub > Settings > Secrets → 두 값 입력|Codespace 터미널: printenv OPENAI\_API\_KEY 는 비어 있고,cat .env 로컬엔 값 존재 → OK.|
|**D5 — 이슈 #1 Story‑Bible Loader**|□ GitHub Issues → New *Title*: feat(loader): load\_story\_bible() *Template*:md\n### Spec\nMaster‑Guide §3.1 요약\n### Done\n- [ ] pytest tests/test\_story\_bible\_loader.py green\n- [ ] flake8 0\n|Copilot PR 뜨면1) 파일 경로 projects/{project}/story\_bible\_v11.json 하드코딩 여부 확인.2) pytest -q 통과 → 머지.|
|**D6 — 이슈 #2 ContextBuilder 스텁**|□ New Issue feat(ctx): context\_builder skeleton build\_context\_for\_episode() 빈 구현 + env CTX\_TOKEN\_BUDGET 사용 명시|PR 병합 후: pytest -q 녹색 유지.Flake8 E501(긴 줄) 발생 시 댓글 “줄바꿈” 지시.|
|**D7 — 150줄 MVP & 3 화 테스트**|□ scripts/run\_novel.py 복붙 (Guide Quick Start 8줄 변형) □ examples/demo\_project/story\_bible\_sample\_v11.json 복사 → projects/Pilot/story\_bible\_v11.json□ examples/demo\_project/outline.csv 3줄 샘플 작성|bash\npython scripts/run\_novel.py --project Pilot --total 3\n☑ projects/Pilot/episodes/EP001.md 등 3 개 생성.☑ CI 다시 녹색.|
|**주말 정리**|□ README.md > “Quick Start (3 화)” 블록 삽입□ git tag v11.0.0-alpha → push|**Week 1 Done Definition**• CI 녹색 • 3 화 파일 존재 • Neo4j 아직 미사용|

-----
### <a name="_r1byc0kosvxa"></a>**🔒 디버그 지옥 방지 5‑포인트 체크**
1. **CI 실패 시 개발 중단** – 새 코드 넣기 전에 반드시 녹색 복구.
1. **.env 는 커밋 금지** – 캡쳐된 키 유출 원천 차단.
1. **테스트 @skip 는 하루 하나씩 해제** – 에러 범위 최소화.
1. **로그 디렉터리 고정** logs/full/YYYY‑MM‑DD.log – 문제 발생 시 파일째 ChatGPT에 전달.
1. **보라색 STOP(Fri)** – GuardFail·CI OK 아니면 기능 추가 금지.
-----
#### <a name="_wyvpashb0u4d"></a>**Week 1 완료 시 얻는 것**
- **작동하는 뼈대** : repo·CI·패키지·150줄 MVP
- **Copilot 워크플로** : Issue → PR → CI 녹색 루틴 체득
- **첫 결과물** : 3 화 텍스트 (품질은 무관)
  ` `→ 이제 Week 2부터 Neo4j 스키마ㆍFAISS Lite를 안전하게 붙일 준비가 끝났습니다.

