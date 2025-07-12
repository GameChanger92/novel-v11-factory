## <a name="_l98akju8hv22"></a>**📅 Week 6 (Days 36 – 42) — “자동 배치 CI + Reward Scorer + 품질 대시보드”**
**이번 주 목표**\
` `1️⃣ GitHub Actions **full‑run 워크플로** (수동·예약 모두)\
` `2️⃣ **Reward Scorer v11** — LLM‑Eval로 긴장감·개연성 등 점수화\
` `3️⃣ **품질 대시보드** (Streamlit Metrics 탭)\
` `4️⃣ 300 화 배치 자동 트리거 + 품질 리포트 첨부\
` `5️⃣ 릴리스 후보 v11.0.0‑rc2

-----
### <a name="_14bplzythexj"></a>**🗓️ Day‑by‑Day 플래너**

|**Day**|**해야 할 일**|**세부 명령 & 검증**|**예상 h**|
| :-: | :-: | :-: | :-: |
|**D36 — GitHub Actions full‑run.yml**|□ .github/workflows/full\_run.yml PR → Copilot⦿ workflow\_dispatch + schedule: cron: '0 1 \* \* 0' (일요일 01:00 UTC)⦿ Job Steps:  1. Checkout repo  2. Set‑up Python 3.10  3. docker compose up -d neo4j redis  4. celery -A engine.tasks worker &  5. python scripts/queue\_full\_pipeline.py --project Pilot --episodes 300 --with-editor --use-retry|**Actions → full‑run → Run workflow** 테스트Job log에 ‘Task queued’ 문구 확인|2|
|**D37 — Reward Scorer 스켈레톤**|□ 이슈 feat(reward): reward\_scorer\_v11 skeleton⦿ 함수 score\_episode(text:str)->dict(score=[0,1])⦿ CLI reward\_scorer\_v11.py --project Pilot --episodes 1-300|` `Unit Test: tests/test\_reward\_scorer\_stub.py 녹색|2|
|**D38 — LLM‑Eval 프롬프트 & 평가 지표**|□ 프롬프트 요소: 긴장감·개연성·묘사력 0‑1 점수□ score\_episode() 구현 → OpenAI function‑call 반환□ 배치 스크립트: score\_all() → metrics/reward.csv|` `CLI python scripts/reward\_scorer\_v11.py --project Pilot --episodes 1-5 → csv 출력|2|
|**D39 — Pipeline과 연동 & 저장소 구조**|□ run\_full\_pipeline\_v11.py 마지막 단계: Reward Scorer 호출□ metrics/reward\_summary.csv 생성 (episode\_id, overall, failures)|시험: 10 화 배치 다시 실행 → csv 행 ≥ 10|1|
|**D40 — Streamlit Metrics 탭**|□ ui/app.py에 **“Metrics” Page** 추가⦿ st.file\_uploader CSV 선택 → st.dataframe 표시⦿ st.altair\_chart 3 선 (긴장감·개연성·묘사력)|브라우저 *Metrics* 클릭 → 그래프 랜더링 ✔|1\.5|
|**D41 — 자동 품질 리포트 & 메일**|□ engine/tasks.py 후크: 배치 종료→ Reward 평균이 0.8 미만이면 sendgrid 메일 발송 (옵션)□ Secrets: SENDGRID\_API\_KEY 저장|Actions full‑run 재실행 → Job Artifact reward\_summary.csv 업로드 확인|2|
|**D42 — 주간 QA & 태그**|□ Actions 스케줄(Job Sunday) → 디스패치 성공 여부만 확인□ CI 전체 녹색·k6 부하 재실행□ git tag v11.0.0-rc2 && git push|Script: python scripts/check\_quality.py --project Pilot --upto 300 --threshold 0.8 PASS|1|

-----
### <a name="_1gb1snp2s2p7"></a>**📂 Week 6 산출물 체크리스트**

|**파일 / 리소스**|**설명**|
| :-: | :-: |
|.github/workflows/full\_run.yml|자동/수동 전체 배치 CI|
|engine/reward\_scorer\_v11.py|LLM‑Eval 품질 스코어러|
|metrics/reward\_summary.csv|Episode 별 3지표·평균|
|ui/app.py Metrics 페이지|CSV 업로드 → 그래프|
|Git 태그 v11.0.0‑rc2|Release Candidate 2|

-----
### <a name="_cedx3cxhkwz5"></a>**🔧 디버그 & 운용 팁**

|**이슈**|**해결**|
| :-: | :-: |
|ModuleNotFound: altair|pip install altair + requirements.txt 업데이트|
|Actions Docker 권한 오류|services: 섹션으로 neo4j·redis 컨테이너 정의, network 적절히 연결|
|Reward Scorer 응답 시간 길다|score\_episode 에 max\_tokens=300 낮추기, 5개씩 batch 처리|
|SendGrid 메일 실패|Secrets 명 오타, to\_email 화이트리스트 여부 확인|

-----
### <a name="_1rv4p76xlfza"></a>**✅ Week 6 Done Definition**
- **GitHub Actions full‑run** 수동 실행 성공 & 300 화 Job 완주
- Reward Scorer가 **300 행 csv** 생성, 평균 ≥ 0.8
- Streamlit Metrics 탭에서 csv 시각화 OK
- Actions 스케줄(주 1) 트리거 설정 확인
- 릴리스 태그 **v11.0.0‑rc2**\


Week 6를 마치면 \*\*“클릭 없이 GitHub Actions+Celery로 300 화 배치 → 품질 스코어 → 대시보드”\*\*가 완전히 자동화됩니다.\
` `Week 7에는 **k6 부하 최적화, Chaos Day 자동 복구 테스트, Genre 팩·Plugin Loader**를 추가해 공장의 안정성과 다품종 생산성을 높일 예정입니다.

