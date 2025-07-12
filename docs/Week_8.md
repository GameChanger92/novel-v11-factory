## <a name="_dp4x4zgu55ow"></a>**📅 Week 8 (Days 50 – 56) — “오프사이트 백업 + 출판 패키지 + 운영 대시보드 & 정식 릴리스 v11.0.0”**
**이번 주 = ‘공장’ 준공 검사 & 배포 주간**\
` `1️⃣ **S3 오프사이트 백업** — Neo4j 덤프·Episode ZIP 주 1회 자동 업로드\
` `2️⃣ **Markdown → EPUB / PDF 변환 파이프라인** (전자책·제휴 플랫폼 용)\
` `3️⃣ **재무 Dashboard** — LLM 토큰비·플랫폼 매출 자동 집계·차트\
` `4️⃣ **백업 리스토어 테스트** — 새 Codespace에서 단일 스크립트로 복구\
` `5️⃣ 정식 태그 **v11.0.0 (GA)** + 릴리스 노트

-----
### <a name="_xiiq3ock84k0"></a>**🗓️ Day‑by‑Day 플래너**

|**Day**|**해야 할 일**|**세부 명령 & 검증**|**예상 h**|
| :-: | :-: | :-: | :-: |
|**D50 — AWS S3 버킷 준비 & Boto3 세팅**|□ S3 Bucket v11-factory-backup 생성□ GitHub Secrets AWS\_ACCESS\_KEY\_ID, AWS\_SECRET\_ACCESS\_KEY, AWS\_REGION 저장|Codespace:bash\npip install boto3\npython - <<'PY'\nimport boto3, os, json\ns3=boto3.client('s3')\nprint(s3.list\_buckets())\nPY|1|
|**D51 — backup\_upload\_v11.py 스크립트**|□ 기능:  • Neo4j dump 파일 이름 neo4j-YYYYMMDD.dump  • projects/<proj>/episodes.zip 선택 업로드□ Cron 등록 0 4 \* \* 0 (일요일 새벽)|CLI 시험:python backup\_upload\_v11.py --project Pilot → S3 Object 확인|2|
|**D52 — Markdown → EPUB/PDF 변환**|□ pip install ebooklib markdown pypandoc□ scripts/convert\_epub\_v11.py (Copilot PR)  • input dir episodes/ → output Pilot.epub  • 표지·목차 자동 생성|EPUB 검사: Kindle Previewer 열기 → 목차 OK|2|
|**D53 — 재무 데이터 파이프라인**|□ scripts/calc\_costs.py 토큰 usage → OpenAI billing API□ platform\_sales\_loader.py 문피아 CSV → 매출 합계□ metrics/finance.csv(date,cost,sales,profit)|Streamlit Metrics 탭에 ‘Finance’ 그래프 추가 (st.line\_chart)|2|
|**D54 — 백업 복구 E2E 테스트**|□ 새 Codespace 생성 → repo clone□ restore\_v11.sh <s3\_uri> 실행 >   • Neo4j 컨테이너 초기화  • dump 파일 복원  • episodes.zip 재압축 해제|run\_full\_pipeline\_v11.py --start 301 --end 305 정상 실행|2|
|**D55 — GA 릴리스 노트 & 버전 고정**|□ CHANGELOG.md 작성 (Features·Breaking·Upgrade guide)□ requirements.txt 버전 lock (pip freeze > requirements.lock)|git tag v11.0.0 → GitHub Release Draft 작성(+ ZIP Asset)|1\.5|
|**D56 — 최종 검수 & 정식 릴리스**|□ CI workflow dispatch → full‑run + chaos\_test + k6 모두 녹색□ GitHub Release Publish → v11.0.0 GA|README 헤더 버전·배지 업데이트|1|

-----
### <a name="_4ezafvvpuve6"></a>**📂 Week 8 산출물 체크리스트**

|**산출**|**경로·설명**|
| :-: | :-: |
|backup\_upload\_v11.py|S3 업로드 스크립트|
|.github/workflows/backup.yml|오프사이트 백업 CI|
|scripts/convert\_epub\_v11.py|Markdown → EPUB/PDF|
|metrics/finance.csv|날짜별 비용·매출|
|Streamlit Metrics “Finance” 그래프|재무 차트|
|restore\_v11.sh|원클릭 복구 스크립트|
|requirements.lock|버전 고정|
|Git Tag v11.0.0 GA|정식 릴리스|

-----
### <a name="_icfr68qrh4kp"></a>**🔧 디버그 & 운영 팁**

|**이슈**|**해결**|
| :-: | :-: |
|S3 SignatureDoesNotMatch|AWS\_REGION · bucket region 일치 확인|
|EPUB 이미지 깨짐|cover.jpg 경로 절대·상대 혼용 ⟶ os.path.abspath() 사용|
|OpenAI Billing API 401|사용자 org ID 미설정 → OPENAI\_ORG\_ID Secret 추가|
|neo4j-admin load 권한 오류|컨테이너 --env NEO4J\_ACCEPT\_LICENSE\_AGREEMENT=yes|

-----
### <a name="_igp4hakc41lg"></a>**✅ Week 8 Done Definition  → v11.0.0 GA**
- S3 오프사이트 백업 자동 업로드 & 리포트 PASS
- EPUB/PDF 변환 스크립트로 단일 클릭 전자책 생성
- Finance 대시보드 → 수익·비용 추이 시각화
- restore\_v11.sh 새 환경 복구 성공
- CI 전체 녹색, Chaos + k6 통과
- GitHub Release v11.0.0 퍼블리시 (릴리스 노트·ZIP Asset 포함)

**이제 ‘V11 소설 공장’은 생산·품질·배포·백업·재무 모니터링까지 모든 운영 루프가 닫힌 상태입니다.**\
` `앞으로는 **장르 YAML 작성, 플러그인 개발, RL 튜닝**만 추가해가며 다품종·고품질 작품을 무한 증식하시면 됩니다. 🎉

