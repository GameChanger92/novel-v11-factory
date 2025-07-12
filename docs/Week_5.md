## <a name="_jhc9nhnspwpz"></a>**📅 Week 5 (Days 29 – 35) — “UI 1.0 + 큐 오케스트레이터 + 300 화 본격 배치”**
**주간 목표**\
` `1️⃣ **Streamlit UI 1.0** — 프로젝트 생성 위저드·실시간 로그·ZIP 다운로드\
` `2️⃣ **Celery + Redis** 작업 큐 — 대기 작업·동시 여러 시즌 처리\
` `3️⃣ **300 화 전체 배치** — Editor + Guard + Retry 켜고 완주\
` `4️⃣ Neo4j/Bible **Round‑Trip 통합 테스트** + 백업 스크립트\
` `5️⃣ 버전 준비: **v11.0.0‑rc1** 태그

-----
### <a name="_wq1a03kclvxd"></a>**🗓️ Day‑by‑Day 플래너**

|**Day**|**해야 할 일**|**세부 명령 & 검증**|**예상 h**|
| :-: | :-: | :-: | :-: |
|**D29 — Streamlit UI 1.0 업그레이드**|□ ui/app.py 확장 PR → Copilot|` `기능:  • New Project Wizard (Story Bible 업로드 / 장르선택)  • 실행 파라미터: start EP, end EP, with‑editor, use‑retry  • st.text\_area 실시간 로그 스트림  • st.download\_button ZIP 다운로드|streamlit run ui/app.py → 브라우저: ① 필드 표시 ② “Generate 1 Episode” 시험 ✔|
|**D30 — Redis + Celery 컨테이너 추가**|□ docker-compose.yml 에 redis 서비스 추가□ 이슈 feat(queue): celery\_worker\_v11 PR → Copilot|` `파일들:  • engine/tasks.py — generate\_episodes\_task()  • celeryconfig.py — broker redis:// docker compose up -d redis 후 celery -A engine.tasks worker -l INFO|터미널 로그에 ready 표시|
|**D31 — UI↔큐 연결 & 300 화 작업 등록**|□ ui/app.py에서 버튼 클릭 ➜ generate\_episodes\_task.delay() 호출□ st.progress Poll loop 3 s|브라우저에서 **Generate 300 Episodes** ↗ “Task queued” 출력|1\.5|
|**D32 — 300 화 Celery 배치 모니터링**|□ 작업 실행 중 로그 실시간 표시 확인□ 완료 후 projects/<proj>/episodes/EP300.md 존재|logs/guard\_summary.csv → Guard Fail ≤ 2 % / Retry Success ≥ 80 %|2 (+ 실행 대기)|
|**D33 — Neo4j ↔ Story Bible Round‑Trip 테스트**|□ 이슈 test(e2e): test\_graph\_bible\_roundtrip PR → Copilot|` `테스트 로직:  1. Bible → KG graph\_sync --source-file  2. KG → Bible --export-bible  3. filecmp.cmp True|pytest -k roundtrip 녹색|
|**D34 — Backup & Chaos Day 스크립트**|□ scripts/backup\_neo4j.sh 작성: docker exec neo4j neo4j-admin database dump neo4j --to /backups/$(date)+dump□ Codespace crontab -e → 0 3 \* \* 0 주 1회 등록□ Chaos Day: docker stop neo4j 5 분 → 큐가 재시도 대기?|재가동: docker start neo4j 후 작업 자동 재개 로그 확인|2|
|**D35 — 부하 (k6) & 릴리스 태그**|□ tests/k6\_load.js — 10 RPS → UI POST 엔드포인트□ npm k6 run tests/k6\_load.js → 95p latency < 15 s|모든 스텝 녹색 후:git tag v11.0.0-rc1 && git push --tags|1\.5|

-----
### <a name="_i7swk560oaop"></a>**📂 Week 5 산출물 체크리스트**

|**파일 / 리소스**|**설명**|
| :-: | :-: |
|ui/app.py v1.0|Wizard + 실행 + 실시간 로그 + ZIP|
|docker-compose.yml (redis 추가)|Celery broker|
|engine/tasks.py, celeryconfig.py|Celery worker 코드|
|projects/<proj>/episodes/EP300.md|300 화 산출 확인|
|logs/guard\_summary.csv|Quality 메트릭|
|tests/test\_graph\_bible\_roundtrip.py|E2E 테스트 파일|
|scripts/backup\_neo4j.sh|DB 덤프 백업 스크립트|
|tests/k6\_load.js|부하 테스트 스크립트|
|Git 태그 v11.0.0-rc1|Release Candidate|

-----
### <a name="_qr73uvompk5j"></a>**🔧 디버그 & 운용 팁**

|**이슈**|**해결**|
| :-: | :-: |
|Celery worker가 작업 못 찾음|CELERY\_IMPORTS = ['engine.tasks'] 설정 확인|
|Streamlit 로그가 안 올라옴|Queue.get\_nowait Poll 주기 3 s, stdout → WebSocket 전송 여부|
|Redis 연결 오류 ECONNREFUSED|docker-compose network 이름 mismatch → redis: 호스트 확인|
|Guard Fail > 2 %|Scene/Beat 엮인 설정 불일치 → Arc Diff 재검 · Guard 규칙 추가|
|k6 95p latency > 15 s|Codespace CPU 한계 → 동시 10요청 스레드 낮추고 Celery worker 2개로 확장|

-----
### <a name="_4wq7i51i1mrx"></a>**✅ Week 5 Done Definition**
- CI 녹색 + k6 부하 pass
- Streamlit UI 1.0 → 버튼으로 300 화 큐 등록·모니터링·ZIP 다운로드 성공
- Guard Fail ≤ 2 %, 평균 글자 수 ± 10 %
- Neo4j 백업 덤프 파일 생성, Chaos Day 복구 OK
- 릴리스 태그 v11.0.0‑rc1 푸시

Week 5를 마치면 **“원‑클릭(UI) → 큐 → 300 화 완결”** 전 과정이 실전 환경으로 돌아갑니다.\
` `Week 6에서는 **GitHub Actions 자동 배치, Reward Scorer, 품질 대시보드**를 붙여 운영 자동화와 품질 피드백 루프를 완성하게 됩니다.

