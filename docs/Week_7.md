## <a name="_nes7p58umtj0"></a>**📅 Week 7 (Days 43 – 49) — “안정성 최적화 + 다품종 생산 지원”**
**이번 주 목표**\
` `1️⃣ **부하 최적화** – k6 95‑퍼센타일 < 10 s, Celery Worker 오토스케일\
` `2️⃣ **Chaos Day 자동 복구** – Neo4j·Redis 장애 시 5 분 내 자가 회복\
` `3️⃣ **Genre Template 팩 3종** – 장르 선택만으로 새 Bible 씨앗 생성\
` `4️⃣ **Plugin Loader v11** – 스타일·금기어 플러그인 핫스왑 구조\
` `5️⃣ 릴리스 후보 **v11.0.0‑rc3**

-----
### <a name="_gg7jda39zkm9"></a>**🗓️ Day‑by‑Day 플래너**

|**Day**|**해야 할 일**|**세부 명령 & 검증**|**예상 h**|
| :-: | :-: | :-: | :-: |
|**D43 — k6 부하 스크립트 확장**|□ tests/k6\_load.js → 50 VU·RPS 20 시나리오 추가□ npm run k6 (Codespace) → 95p < 10 s 미달 시 튜닝|조치: Celery --autoscale 4,1, prefetch\_multiplier=1 설정 → 재시험|2|
|**D44 — Celery 오토스케일 & 모니터링**|□ celeryconfig.py worker\_autoscale=(4,1)□ flower (모니터) 컨테이너 추가 → docker-compose.yml|브라우저 :5555 꽃 모니터 페이지 열림 확인|1\.5|
|**D45 — Chaos Day 스크립트 자동화**|□ scripts/chaos\_day\_v11.sh  • 무작위로 docker stop neo4j 60 s  • 작업 큐 pause → resume□ GitHub Actions chaos\_test.yml (cron 월 1회)|Actions job 로그에 “Recovered within 300 s ✅” 메시지|2|
|**D46 — Genre Template 팩 3종 작성**|□ templates/genre/fantasy\_kr.yaml□ templates/genre/modern\_noir.yaml□ templates/genre/romance\_comedy.yaml|Streamlit Wizard → 드롭다운 장르 선택 → Bible 씨앗 생성 OK|2|
|**D47 — Plugin Loader v11 구현**|□ 이슈 feat(plugin): plugin\_loader\_v11 PR → Copilot⦿ Entry‑point spec: plugins/{name}/\_\_init\_\_.py with register()⦿ 핫로딩: importlib + .enabled YAML|샘플 플러그인 plugins/style/noir\_dialogue.py 등록 → Editor 단계 적용 확인|2|
|**D48 — E2E 다품종 테스트**|□ 장르 3종 × 플러그인 2개 → 총 6 프로젝트 5 화씩 큐 등록□ 결과 ZIP 확인 → 장르/톤 차이 수동 리뷰|Guard/Reward 통계: 5 화 평균 점수 ≥ 0.8, Fail < 5 %|2 (+대기)|
|**D49 — QA & 릴리스 태그 rc3**|□ k6·Chaos job 성공, 로그 보관□ README “Genre 팩 & Plugin” 섹션 추가□ git tag v11.0.0-rc3 && git push --tags|pytest, flake8, k6, chaos\_test.yml 모두 녹색|1|

-----
### <a name="_mvitbe8wjblw"></a>**📁 Week 7 산출물 체크리스트**

|**산출**|**파일·리소스**|
| :-: | :-: |
|tests/k6\_load.js (개선)|50 VU 부하 시나리오|
|docker-compose.yml (flower 추가)|Celery 모니터링|
|scripts/chaos\_day\_v11.sh|장애 시뮬레이터|
|.github/workflows/chaos\_test.yml|월 1회 Chaos CI|
|templates/genre/\*.yaml (3종)|장르 팩|
|plugins/style/noir\_dialogue.py 등|플러그인 예시|
|engine/plugin\_loader\_v11.py|동적 로더|
|Git 태그 v11.0.0‑rc3|Release Candidate 3|

-----
### <a name="_q4objr1lsn19"></a>**🔧 디버그 & 운영 팁**

|**이슈**|**해결**|
| :-: | :-: |
|Flower 접속 ×|compose 포트 5555 expose 확인, Codespace Port Public 설정|
|Chaos Day 후 작업 유실|Celery acks\_late=True, visibility\_timeout=3600 설정|
|Plugin ImportError|\_\_init\_\_.py 에 def register(pipeline): 시그니처 확인|
|장르 PDF 생성 실패|Wizard 업로드 파일명 비영어 → slugify() 사용|

-----
### <a name="_usxdtytaqpy6"></a>**✅ Week 7 Done Definition**
- k6 95p latency < 10 s (20 RPS)
- Chaos Day 자동 스크립트 → “Recovered within 5 min”
- Wizard → 3 장르 템플릿으로 새 Project 생성 OK
- Plugin Loader 활성화 + 샘플 플러그인 적용됨
- E2E 6 프로젝트 시험: Guard Fail ≤ 5 %, Reward ≥ 0.8
- 태그 v11.0.0‑rc3 푸시

Week 7까지 완료하면 **부하·장애 내성 + 다장르/스타일 변환**이 확보되어 “소설 공장” 가동 준비가 사실상 끝납니다.\
` `Week 8에서는 **백업 자동검증 → S3 오프사이트 전송, Markdown→EPUB 변환, 재무 대시보드** 등을 마무리해 v11.0.0 정식 릴리스를 찍게 됩니다.

