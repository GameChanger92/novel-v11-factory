## <a name="_z54g0gx5nwq2"></a>**📅 Week 4 (Days 22 – 28) — “Editor Agent + Retry Controller + 120 화 품질 검증”**
**이번 주 목표**\
` `1️⃣ Editor Agent v11 (문체 / 길이 / 서스펜스 교정) \
` `2️⃣ Retry Controller v11 (Guard Fail 회차 자동 재시도) \
` `3️⃣ 120 화 배치 → Guard Fail ≤ 2 %·평균 글자 수 ±10 % 검증 \
` `4️⃣ Streamlit UI 0.5 스텁(버튼·progress 막대만) 준비

|**Day**|**해야 할 일**|**세부 명령 & 검증**|**예상 h**|
| :-: | :-: | :-: | :-: |
|**D22 — Editor Agent 스켈레톤 PR**|□ 이슈 feat(editor): editor\_agent\_v11 skeleton 발행 → Copilot PR□ 함수 refine\_episode(draft:str, targets:dict)->str·CLI editor\_agent\_v11.py --in --out|*Spec 인용*: Master‑Guide §4.2 “LLM Self‑Critique”pytest tests/test\_editor\_skeleton.py 녹색|2|
|**D23 — LLM Self‑Critique 로직 구현**|□ 프롬프트 템플릿(문체·길이 ±10 %) 삽입 PR□ 단위 테스트 길이 검증 추가|터미널:⟶ python scripts/editor\_agent\_v11.py --in examples/EP\_Sample.txt --out out.txt→ 글자 수 목표 충족 확인|2|
|**D24 — Pipeline 연결 & Mini test (5 화)**|□ run\_full\_pipeline\_v11.py 내 Draft → Editor 단계 삽입□ python run\_full\_pipeline\_v11.py --project Pilot --start 1 --end 5 --with-editor|출력 Markdown 실물 확인: ① 맞춤법 교정 ② 길이 ±10 % ③ 톤 변화 자연스러운지 육안 체크|1\.5|
|**D25 — Retry Controller v11**|□ 이슈 feat(retry): retry\_controller\_v11 PR  ‣ Guard Fail 회차만 최대 1회 재생성  ‣ 무한 루프 방지 Timeout 15 min|TEST: pytest tests/test\_retry\_controller.py → mock Guard Fail 발생 시 재시도 1회 기록|2|
|**D26 — 120 화 배치 + 로그 수집**|□ python run\_full\_pipeline\_v11.py --project Pilot --start 1 --end 120 --with-editor --use-retry□ 배치 중 progress CLI 확인|완료 후:‣ logs/guard\_summary.csv‣ 평균 글자 수 계산(scripts/stat\_len.py) 출력|2 (+배치 대기)|
|**D27 — Streamlit 0.5 스텁**|□ ui/app.py – Streamlit 120줄  ‣ 입력: 프로젝트·start/end·flags  ‣ 버튼 → subprocess run\_full\_pipeline\_v11.py  ‣ st.progress 갱신|streamlit run ui/app.py → 브라우저 열고 *Generate 5 Episodes* 성공|1\.5|
|**D28 — 주간 QA & 태그**|□ guard\_fail\_rate ≤ 2 % ? → Yes ✔ / No ✖ (버그 이슈 생성)□ README “Editor Agent + Retry” 절 추가□ git tag v11.0.0-beta.2 && git push|판별 스크립트:python scripts/check\_quality.py --project Pilot --upto 120 → PASS|1|

-----
### <a name="_iqvg6yy0wevu"></a>**🗂️ Week 4 산출물 체크리스트**

|**산출**|**경로 / 설명**|
| :-: | :-: |
|scripts/editor\_agent\_v11.py|Editor Agent CLI|
|tests/test\_editor\_skeleton.py|Self‑Critique 단위 테스트|
|engine/retry\_controller\_v11.py|Guard 재시도 로직|
|logs/guard\_summary.csv|EP별 Pass/Fail·Retry 기록|
|ui/app.py|Streamlit 버튼 + progress 스텁|
|v11.0.0-beta.2 Git 태그|주차 완료 스냅숏|

-----
### <a name="_d35mo39wobvy"></a>**🔧 자주 터지는 오류 & 즉시 처방**

|**증상**|**1‑분 해결**|
| :-: | :-: |
|**OpenAI: RateLimitError** (편집 단계)|.env OPENAI\_BACKOFF=8, OPENAI\_MAX\_RETRY=12|
|**재시도 무한 루프**|retry\_controller max\_retry=1 상수 확인|
|**에디터 출력 길이 제어 실패**|Editor 프롬프트에 {{desired\_chars}} 변수를 못 넘김 → run\_full\_pipeline\_v11.py arg 전달 체크|
|**Streamlit 버튼 클릭 무반응**|Codespace ports: 8501 exposed 여부 → *Ports* 탭에서 Public 설정|

-----
### <a name="_rj04q8ccfni"></a>**✅ Week 4 Done Definition**
- CI (lint + pytest) **녹색**\

- Editor Agent 적용 후 **평균 글자 수 ± 10 %**\

- guard\_fail\_rate ≤ 2 %, 재시도 성공률 ≥ 80 %
- Streamlit 버튼으로 5 화 생성 가능
- Git 태그 v11.0.0‑beta.2 푸시

Week 4가 끝나면 **“Draft → Editor → Guard → Retry”** 본선(品質) 루프가 완성되고, 간이 UI로 **원‑클릭 실행**까지 시험해 봅니다.\
` `Week 5부터는 Streamlit UI 정식 1.0, Celery Queue, 300 화 전량 배치, 부하·장애 테스트 단계로 넘어갑니다.

