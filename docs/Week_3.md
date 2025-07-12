좋습니다. 아래는 V11 단일 Full‑트랙 전략에 맞춘 **📅 Week 3 상세 로드맵**입니다.
` `2주차까지 KG(Neo4j)·RAG(FAISS) 기반 컨텍스트 시스템이 연결되었으므로, 이번 주는 **Arc → Beat → Scene 플롯 계층을 붙이고, Consistency Guard를 작동시키는 주간**입니다.

-----
## <a name="_phucrwd5n5j4"></a>**✅ Week 3 최종 목표**

|**모듈**|**목표**|
| :-: | :-: |
|Arc Planner|Arc Diff JSON 파일 생성 (A1\_detail\_diff\_v11.json)|
|Beat Maker|10개 비트 (A1\_beats.json) 생성 + JSON Schema 통과|
|Scene Maker|에피소드별 Scene Point 리스트 생성|
|Consistency Guard|설정 오류 검출 → 최초 Guard Fail 기록 확인|
|60화 배치 테스트|Beat+Scene+Guard 반영 상태에서 60화 완주|

-----
## <a name="_j14aq79481l9"></a>**🗓️ Day-by-Day 플래너**

|**Day**|**해야 할 일**|**상세**|
| :-: | :-: | :-: |
|D15|**Arc Planner 이슈 발행**• arc\_detail\_v11.py 스켈레톤 PR|GitHub Issue 예시:\n### Spec: arc\_detail\_v11.py CLI - Guide §3.2\n### Done:\n- [ ] A1\_diff\_v11.json 생성\n- [ ] pytest 녹색\nCopilot에: “30화 단위 Arc Diff 생성 CLI 스켈레톤 만들고, 출력은 memory/diffs/에 저장”|
|D16|**Arc Diff 작성 & 동기화**• 샘플 Arc YAML → JSON 변환• graph\_sync\_v11.py --source-file 실행|examples/demo\_project/A1\_diff.yaml 기반 Arc Diff 1개 수동 작성→ 변환: yaml2json→ KG 연동: graph\_sync\_v11.py --project Pilot --source-file memory/diffs/A1\_diff\_v11.json|
|D17|**Beat Maker CLI**• beat\_maker\_v11.py --arc-id A1• beats.json 출력 & Schema 통과|JSON Schema 예시 사용: schemas/beat\_package\_v11.schema.jsonCI 테스트 파일 tests/test\_beat\_maker\_basic.py 작성 & 통과 확인|
|D18|**Scene Maker PR + context에 삽입**• scene\_point\_maker\_v11.py• context\_builder\_v11.py 내부에서 Scene Point를 가져다 쓰도록 수정|CLI 인자 --scene-points-file 지원테스트: context\_builder\_v11.py에 Scene이 들어가는지 Markdown 텍스트 안에서 확인|
|D19|**Consistency Guard v11 구성**• consistency\_guard\_v11.py PR 발행• 스텁이 아닌 실제 검사 로직: 이름, 직업, 레벨 등|Guide §5.1 참조 – KG 기반의 Cypher 쿼리 검사 구현Fail 시 log/guard\_fail/YYYY-MM-DD.log 파일에 기록 남기기|
|D20|**60화 배치 테스트 (Guard 포함)**• run\_full\_pipeline\_v11.py에서 Beat+Scene+Guard 옵션 켜고 실행• 실패 로그 수집|--project Pilot --start-episode 1 --end-episode 60Guard Fail 횟수 로그 파일로 추출|
|D21|**정리 & 리포트 태그**• README 수정: Arc-Beat-Scene 구조 설명• git tag v11.0.0-beta.1|projects/Pilot/memory/diffs/, beats/, scenes/ 폴더 구성 완비CI 및 pytest -q 통과 여부 확인|

-----
## <a name="_4i2ls7p2rh3w"></a>**📂 Week 3 산출물 체크리스트**

|**파일**|**설명**|**예시 경로**|
| :-: | :-: | :-: |
|A1\_detail\_diff\_v11.json|Arc 계획 Diff 파일|projects/Pilot/memory/diffs/|
|A1\_beats.json|Beat 10개 배열|projects/Pilot/beats/|
|EP001\_scene\_points.json 등|1화당 장면 구성안|projects/Pilot/scenes/|
|context\_EP001.txt|Scene Point가 삽입된 컨텍스트|projects/Pilot/contexts/|
|guard\_fail/EP005.log|설정 오류 발생 로그|logs/guard\_fail/YYYY-MM-DD/|

-----
## <a name="_ncvzmba1m09f"></a>**🧯디버그 방지 팁**

|**이슈**|**대응**|
| :-: | :-: |
|Beat가 안 붙음|context\_builder\_v11.py에 episode\_id → beat\_id 매핑이 안 됐을 가능성 → 디렉토리/파일명 확인|
|Scene이 컨텍스트에 없음|--scene-points-file이 CLI에서 누락되었거나, scene\_point\_maker\_v11.py가 출력 파일을 생성하지 않음|
|Guard Fail 모두 0|검출 규칙이 아직 동작 안 함 → consistency\_guard\_v11.py에 Cypher 검사 로직 추가 필요|
|run\_full\_pipeline\_v11.py에서 Beat/Scene 적용 안 됨|파이프라인 내부에서 load\_beats(), load\_scene\_points() 호출 누락|

-----
## <a name="_3w7b2rwbfavb"></a>**✅ Week 3 Done 조건**
- CI 통과 (pytest, flake8)
- A1\_diff\_v11.json, A1\_beats.json, scene\_point\_n.json 생성
- 컨텍스트 파일에 Scene이 삽입됨
- consistency\_guard\_v11.py 가 최소 1회 이상 오류 탐지
- 60화 배치 후 평균 글자 수 ±10% / Guard Fail < 5%
-----
Week 3까지 완료하면 **“기획 → 플롯 → 씬 → 초고 → 검사” 전 파이프라인이 연결**됩니다.
` `Week 4부터는 **Editor Agent, Retry Controller, Streamlit UI** 모듈을 추가해 **출력 품질을 개선하고 생산성과 사용성을 올리는 단계**로 넘어갑니다. 다음 주도 필요하시면 준비해 드리겠습니다.

