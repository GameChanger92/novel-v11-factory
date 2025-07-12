## <a name="_4rrzdrm24ceh"></a>**📅 Week 2 (Days 8 – 14) — “Neo4j + FAISS 메모리 붙이고 10 화 파일럿”**
**주간 목표**
` `1️⃣ **Neo4j Graph 스키마 초기화** 2️⃣ **FAISS Lite 인덱스 구축** 3️⃣ **ContextBuilder에 RAG 연결**
` `4️⃣ **10 화 파일럿 완주 + CI 녹색 유지**

|**Day**|**해야 할 일 (체크박스)**|**세부 명령 & 검증 포인트**|**예상 h**|
| :-: | :-: | :-: | :-: |
|**D8 – Docker Compose 추가 & Neo4j 시동**|□ docker-compose.yml (부록 1) 루트에 복사 → 커밋□ Codespace 터미널 docker compose up -d neo4j|1\. docker ps → gamechanger\_neo4j\_v11 컨테이너 확인2. 브라우저 http://localhost:7474 접속 → 비밀번호 변경 화면 OK|1|
|**D9 – .env Neo4j 변수 맞추기**|□ .env 파일 NEO4J\_PASSWORD=neo4jpw와 docker‑compose 동일하게 유지|터미널 grep NEO4J\_PASSWORD .env 와 compose NEO4J\_AUTH 비교 → 일치|0\.5|
|**D10 – graph\_sync\_v11.py --init-schema**|□ 이슈 feat(graph): init schema 발행 → Copilot PR 병합□ 터미널: python scripts/graph\_sync\_v11.py --project Pilot --init-schema|출력에 🟢 Index & constraint creation completed 문구 확인|2|
|**D11 – Story Bible → KG 싱크 Smoke Test**|□ examples/demo\_project/story\_bible\_sample\_v11.json 복사 → projects/Pilot/story\_bible\_v11.json □ graph\_sync\_v11.py --project Pilot 실행|Neo4j Browser: MATCH (c:Character) RETURN c LIMIT 5 → 노드 ≥ 1|1|
|**D12 – FAISS Lite 인덱스 빌더**|□ scripts/build\_faiss\_index\_v11.py 40줄 Copilot PR□ pip install faiss-cpu sentence-transformers□ python scripts/build\_faiss\_index\_v11.py --project Pilot --source-bible|memory/faiss\_index/Pilot/index.faiss + meta.pkl 생성 확인|3|
|**D13 – ContextBuilder RAG 통합**|□ context\_builder\_v11.py 에 search\_rag(query, k=5) 라인 삽입 PR□ 테스트 `t|||
|ests/test\_context\_builder\_v11.py` 의 @skip 1개 해제 → CI 녹색|pytest -q 통과, CI Actions 녹색 확인|1\.5||
|**D14 – 10 화 파일럿 & 주간 태그**|□ python scripts/run\_novel.py --project Pilot --total 10 --use-kg□ projects/Pilot/episodes/EP010.md 존재 확인□ git tag v11.0.0-alpha.2 && git push origin v11.0.0-alpha.2|*Guard Stub* 경고 로그는 무시, Fatal 없으면 성공|1|

-----
### <a name="_vc8v3ngmz42h"></a>**🔍 Week 2 디버그 S.O.S**

|**증상**|**1‑분 해결 팁**|
| :-: | :-: |
|docker compose up 후 Neo4j healthcheck 실패|포트 이미 사용 → compose 7474:7475 식으로 호스트 포트 변경|
|graph\_sync … cannot connect|.env NEO4J\_URI=bolt://localhost:7687 인지 확인|
|faiss‑cpu 빌드 오류 (Windows)|conda install faiss-cpu -c pytorch 또는 WSL Ubuntu 이용|
|ContextBuilder RAG 검색 None 리턴|인덱스 경로 오타 · build\_faiss\_index 실행 누락 체크|
|10 화 실행 중  RateLimitError|.env OPENAI\_MAX\_RETRY=10  OPENAI\_BACKOFF=8 추가|

-----
### <a name="_qkwwzq1nr5w0"></a>**✅ Week 2 Done Definition**
- GitHub Actions **lint + pytest** 녹색
- neo4j 컨테이너 **healthy** & 노드 ≥ 1
- memory/faiss\_index/Pilot/index.faiss 존재
- projects/Pilot/episodes 안에 10개 파일
- 태그 v11.0.0-alpha.2 푸시

Week 2를 마치면 **KG·RAG 메모리 계층이 모두 연결**돼, Week 3부터 **Arc Planner → Beat Maker** 모듈을 붙일 안전한 기반이 완성됩니다. 

