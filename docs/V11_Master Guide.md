-----
# <a name="_uze6vfoh5pso"></a>**PROJECT GAMECHANGER — Master Guide v11.2.0 (Full Edition for AI Learning)**
문서 버전: v11.2.0 (AI 학습 최적화판)
최종 수정일: 2025-05-15 (가상 날짜)
문서 목표: 이 문서는 AI가 PROJECT GAMECHANGER v11 엔진의 설계, 핵심 모듈, 구현 방법, 운영 전략 및 향후 확장성(V13 비전)을 심층적으로 학습하고 이해하는 것을 목표로 한다. 정보의 온전성과 탐색성을 극대화하여, AI가 V11 엔진 구축 및 개선에 대한 질문에 정확하고 포괄적인 답변을 생성할 수 있도록 지원한다.

-----
## <a name="_gf9a4mtqtn7o"></a>**# 0. TL;DR (Too Long; Didn't Read)**
PROJECT GAMECHANGER v11은 문피아 평균 이상의 고품질 웹소설(목표 240화 완결)을 자동으로 생성하기 위한 엔진입니다. 핵심 특징은 **동적 메모리 시스템** (Neo4j 그래프DB + FAISS 벡터 RAG), **지능형 품질 제어** (LLM 기반 Editor Agent, GraphDB 연동 Consistency Guard), 그리고 **강화학습(RL) 기반 품질 최적화 루프**입니다. v11은 모듈식 설계를 채택하여 각 컴포넌트의 독립적 개발, 테스트, 교체가 용이하며, 이는 향후 V13 "Zero-Touch, High-Fidelity" 완전 자동화 시스템으로의 단계적 확장을 염두에 둔 것입니다.

**주요 기능:**

- **지식 그래프(KG) 및 RAG:** story\_bible\_v11.json을 Neo4j에 동기화하고, 에피소드 요약 등을 FAISS에 저장하여 context\_builder\_v11.py가 풍부한 컨텍스트를 동적으로 생성합니다.
- **LLM 기반 편집 및 일관성 검증:** draft\_generator\_v11.py가 초고를 생성하면, editor\_agent\_v11.py가 이를 편집하고, consistency\_guard\_v11.py가 KG와 대조하여 설정 충돌을 검사합니다.
- **양방향 동기화 및 확장성:** graph\_sync\_v11.py는 Story Bible과 KG 간 양방향 동기화를 지원하며, 시스템 전반에 걸쳐 Semantic Versioning, JSON Schema 기반 입출력 표준화, 플러그인 아키텍처 준비 등 V13으로의 확장을 위한 기반이 마련되어 있습니다.
- **운영 및 개발자 지원:** Docker Compose를 통한 간편 배포, GitHub Actions 기반 CI/CD, Prometheus/Grafana 연동 모니터링, 구조화된 로깅, 상세한 Quick Start 가이드 및 샘플 데이터 제공으로 개발 편의성과 운영 안정성을 높였습니다.

**V11 엔진의 목표는** 단순 자동 생성을 넘어, 설정 오류를 최소화하고, 이야기의 깊이와 재미를 지속적으로 향상시키며, 개발자가 쉽게 시스템을 이해하고 기여할 수 있는 환경을 제공하는 것입니다. 본 문서는 이러한 V11 엔진의 모든 측면을 상세히 다룹니다.

-----
## <a name="_c2ppuywj3z01"></a>**# 1. 엔진 개요**
### <a name="_6d40lr9t8r4g"></a>**## 1.1. 프로젝트 목표 및 비전**
PROJECT GAMECHANGER의 최종 비전은 창작자와 협력하거나 독립적으로 고품질의 장편 서사를 생성할 수 있는 지능형 스토리텔링 AI를 구축하는 것입니다. V11 엔진은 이 비전을 향한 중요한 이정표로, 특히 다음과 같은 목표를 가집니다:

1. **고품질 장편 생성:** 문피아 등 웹소설 플랫폼에서 경쟁력 있는 수준의 240화 완결작 자동 생성.
1. **동적이고 일관된 세계관 관리:** Knowledge Graph(Neo4j)와 RAG(FAISS)를 결합한 동적 메모리 시스템을 통해, 이야기가 진행됨에 따라 발생하는 설정 변경 및 새로운 정보를 효과적으로 관리하고, 이를 바탕으로 일관성 있는 컨텍스트를 생성하여 LLM에 제공.
1. **지능형 품질 관리:** LLM 기반 Editor Agent를 통해 생성된 초고의 문체, 흐름, 표현력을 자동으로 개선하고, Consistency Guard를 통해 설정 오류를 능동적으로 감지 및 수정 유도.
1. **지속적인 품질 향상:** 강화학습(RL) 루프를 통해 생성된 결과물에 대한 평가(Reward Scorer)를 바탕으로, Draft 생성 LLM의 파라미터를 점진적으로 튜닝하여 장기적인 품질 향상 도모 (선택적 기능).
1. **개발 용이성 및 확장성 확보:** 각 기능을 모듈화하고 명확한 인터페이스를 정의하여, 개발자가 시스템을 쉽게 이해하고, 특정 모듈을 개선하거나 새로운 기능을 추가하는 작업을 용이하게 합니다. 이는 향후 V13 "Zero-Touch, High-Fidelity" 엔진으로의 자연스러운 진화를 위한 핵심 전략입니다.
1. **운영 안정성 및 효율성:** Docker, CI/CD, 모니터링, 구조화된 로깅, 상세한 가이드 및 샘플 데이터 제공을 통해 개발 및 운영 과정에서의 효율성과 안정성을 높입니다.

V11 엔진은 단순히 많은 양의 텍스트를 생성하는 것을 넘어, "잘 쓰인" 이야기를 만들어내는 데 중점을 둡니다. 이를 위해 기술적 도전 과제들을 해결하고, 창의성과 일관성 사이의 균형을 맞추며, 사용자(개발자 또는 최종 운영자)에게 투명하고 제어 가능한 시스템을 제공하고자 합니다.
### <a name="_rr19bwf69qlv"></a>**## 1.2. 핵심 아키텍처 철학**
V11 엔진의 아키텍처는 다음 네 가지 핵심 철학을 바탕으로 설계되었습니다:

1. **모듈성 (Modularity):**
   1. **설명:** 시스템을 기능적으로 독립적인 여러 모듈(예: 컨텍스트 빌더, 초고 생성기, 편집 에이전트, 일관성 검사기)로 분리합니다. 각 모듈은 명확히 정의된 입력과 출력을 가지며, 내부 구현은 다른 모듈로부터 숨겨집니다(캡슐화).
   1. **목표:** 각 모듈의 독립적인 개발, 테스트, 배포 및 업그레이드를 용이하게 합니다. 특정 모듈의 문제가 전체 시스템에 미치는 영향을 최소화하고, 필요에 따라 특정 모듈만 다른 구현으로 교체(Pluggability)할 수 있도록 합니다.
   1. **예시:** draft\_generator\_v11.py는 context\_builder\_v11.py로부터 컨텍스트를 받아 초고를 생성하며, 이 초고는 editor\_agent\_v11.py의 입력이 됩니다. 각 스크립트는 독립적으로 실행 가능하며, CLI 인터페이스를 가집니다.

1. **확장성 (Extensibility):**
   1. **설명:** 새로운 기능을 추가하거나 기존 기능을 변경/확장하는 것이 용이하도록 시스템을 설계합니다. 이는 잘 정의된 인터페이스, 플러그인 아키텍처 준비, 설정 파일의 유연성 등을 통해 달성됩니다.
   1. **목표:** V13과 같은 미래 버전의 고급 기능(예: Dual-Draft Generator, Auto-Fix Chain, Smart-Retry Orchestrator)을 V11 기반 위에 점진적으로 통합할 수 있도록 합니다. 외부 개발자나 다른 팀이 기여할 수 있는 여지를 마련합니다.
   1. **예시:** 플러그인 매니페스트 파일(plugins/manifest.yaml) 개념 도입, 주요 데이터 구조에 대한 JSON Schema 정의, 이벤트 기반 오케스트레이션 연동 준비 등이 확장성을 고려한 설계입니다.

1. **데이터 중심 (Data-Centric):**
   1. **설명:** 이야기의 모든 정보(세계관 설정, 캐릭터, 플롯, 에피소드 로그 등)를 구조화된 형태로 중앙에서 관리하고(Story Bible JSON, Neo4j GraphDB), 이를 각 모듈이 일관되게 활용하도록 합니다. 데이터의 흐름과 변환 과정을 명확히 추적합니다.
   1. **목표:** 데이터의 일관성과 무결성을 유지하고, 이를 바탕으로 고품질의 컨텍스트를 생성하며, 생성된 이야기의 모든 측면을 효과적으로 검증하고 관리합니다.
   1. **예시:** story\_bible\_v11.json을 "Single Source of Truth"로 활용하되, Neo4j와 FAISS를 통해 이 데이터를 더욱 동적이고 효율적으로 활용합니다. graph\_sync\_v11.py를 통한 양방향 동기화는 데이터 일관성 유지에 기여합니다.

1. **관찰 가능성 및 제어 가능성 (Observability & Controllability):**
   1. **설명:** 시스템의 현재 상태, 각 모듈의 동작 과정, 성능 지표, 발생 가능한 오류 등을 쉽게 파악하고(관찰 가능성), 필요한 경우 운영자가 개입하여 시스템의 동작을 조절하거나 문제를 해결할 수 있도록(제어 가능성) 합니다.
   1. **목표:** "블랙박스" 시스템이 아닌, 투명하고 예측 가능한 시스템을 구축합니다. 문제 발생 시 신속한 원인 파악 및 대응을 가능하게 하고, 시스템 최적화를 위한 근거 데이터를 제공합니다.
   1. **예시:** 구조화된 JSON 로깅, Trace ID를 통한 요청 추적, Prometheus/Grafana 연동 모니터링, 상세한 CLI 옵션 및 Feature Flag, "interactive" 모드 제공 등이 이에 해당합니다.

이러한 아키텍처 철학은 V11 엔진이 단순히 현재의 목표를 달성하는 것을 넘어, 장기적으로 발전하고 다양한 요구사항에 유연하게 대응할 수 있는 견고한 기반을 제공합니다.
### <a name="_3lvd9rjps8nw"></a>**## 1.3. 핵심 모듈 지도 (Pipeline Overview)**
V11 엔진의 전체 파이프라인은 여러 핵심 모듈들이 유기적으로 연동되어 작동합니다. 아래는 주요 모듈과 데이터 흐름을 나타낸 고수준 다이어그램입니다. 각 모듈에 대한 상세 설명은 이어지는 섹션에서 제공됩니다.

- **다이어그램:[ ](#2-전체-파이프라인-v1110---uml-ascii-다이어그램)[2. 전체 파이프라인 (v11.1.0) - UML ASCII 다이어그램 보기](#2-전체-파이프라인-v1110---uml-ascii-다이어그램)** (내부 앵커 링크)
  - *주석: 위 다이어그램은 주요 모듈 간의 상호작용을 보여줍니다. Season Init부터 시작하여 Arc Loop과 Draft Loop를 거치며 에피소드가 생성되고, 선택적으로 RL Scoring/Tuning Loop가 동작합니다. Knowledge Graph(Neo4j)와 Vector Index(FAISS)는 Context Builder를 통해 지속적으로 활용됩니다.*

**주요 단계 및 모듈 요약:**

1. **초기화 (Initialization):**
   1. story\_bible\_init\_v11.py: 프로젝트의 기본 뼈대인 story\_bible\_v11.json을 템플릿으로부터 생성합니다.
   1. graph\_sync\_v11.py --init-schema: Neo4j에 필요한 스키마(인덱스, 제약 조건)를 설정하고 FAISS 폴더를 준비합니다.

1. **아크 계획 (Arc Planning):**
   1. arc\_detail\_v11.py: 각 아크(보통 30화 단위)의 주요 플롯, 등장인물, 배경 등을 상세히 계획하여 Arc Diff JSON 파일을 생성합니다.

1. **컨텍스트 생성 (Context Building):**
   1. context\_builder\_v11.py: 현재 생성하려는 에피소드에 필요한 모든 정보를 Story Bible, Neo4j (KG), FAISS (RAG)로부터 수집하고 조합하여 LLM 프롬프트에 사용될 풍부한 컨텍스트를 구성합니다. CTX\_TOKEN\_BUDGET을 준수합니다.

1. **세부 플롯 생성 (Beat & ScenePoint Generation):**
   1. beat\_maker\_v11.py: 아크 계획과 현재 컨텍스트를 바탕으로 약 10화 단위의 세부적인 플롯 비트(줄거리 요점)를 생성합니다.
   1. scene\_point\_maker\_v11.py: 각 에피소드별로 더 상세한 장면 구성안(Scene Points)을 생성합니다.

1. **초고 생성 (Draft Generation):**
   1. draft\_generator\_v11.py: Scene Points와 풍부한 컨텍스트를 바탕으로 LLM을 호출하여 에피소드 초고를 생성합니다.

1. **품질 관리 (Quality Control):**
   1. editor\_agent\_v11.py: 생성된 초고를 LLM 기반의 편집 에이전트가 검토하고 문체, 흐름, 표현 등을 개선합니다.
   1. consistency\_guard\_v11.py: 편집된 초고를 Neo4j의 지식 그래프와 대조하여 설정 오류, 타임라인 모순 등을 검사합니다.
   1. retry\_controller\_v11.py: Consistency Guard 실패 시, 실패 원인을 바탕으로 프롬프트를 수정하여 초고 생성을 재시도합니다 (향후 V13의 Smart-Retry Orchestrator로 확장).

1. **데이터 업데이트 및 동기화 (Data Update & Sync):**
   1. story\_bible\_updater\_v11.py: 최종 통과된 에피소드 정보를 story\_bible\_v11.json에 반영하고, 변경 사항을 Neo4j 및 FAISS에 업데이트합니다.
   1. graph\_sync\_v11.py: Story Bible과 Neo4j 간의 데이터를 양방향으로 동기화합니다.

1. **피드백 및 튜닝 (Feedback & Tuning - 선택적):**
   1. reward\_scorer\_v11.py: 생성된 에피소드를 일관성, 긴장감, 캐릭터 표현 등의 기준으로 평가하여 점수를 매깁니다.
   1. ppo\_tune\_v11.py: 수집된 점수 데이터를 바탕으로 draft\_generator\_v11.py가 사용하는 LLM의 파인튜닝을 오프라인으로 수행합니다 (장기 목표).

각 모듈은 독립적으로 실행 가능한 Python 스크립트([[scripts/모듈명\_v11.py]])로 구현되며, CLI 인터페이스를 통해 제어됩니다. 전체 파이프라인은 [[scripts/run\_pilot\_v11.ps1]] (30화 파일럿) 또는 [[scripts/run\_full\_pipeline\_v11.py]] (240화 전체 - 가상)와 같은 오케스트레이션 스크립트에 의해 조율됩니다.

-----
## <a name="_m9qyr7jbopu2"></a>**# 2. 설치 및 환경 설정**
### <a name="_wels2l61t3w7"></a>**## 2.1. 시스템 요구사항**
- **Python:** 3.10 이상 권장.
- **운영체제:** Windows, Linux, macOS (PowerShell 또는 bash/zsh 쉘 환경 필요).
- **하드웨어:**
  - CPU: 최소 4코어 권장.
  - RAM: 최소 16GB 권장 (Neo4j, FAISS, LLM 로컬 실행 시 더 많이 필요할 수 있음).
  - Storage: 최소 50GB 여유 공간 (프로젝트 데이터, DB, 로그 등).

- **소프트웨어:**
  - Git: 버전 관리 시스템.
  - Docker Desktop: Neo4j 컨테이너 실행용 (또는 네이티브 Neo4j 설치).
  - C++ Build Tools: FAISS Python 패키지 설치 시 필요할 수 있음 (특히 Windows).

- **API Keys:**
  - OpenAI API Key 또는 다른 LLM 제공사 API Key.

- **네트워크:** LLM API 호출 및 패키지 다운로드를 위한 인터넷 연결.
### <a name="_oeoytvu053n7"></a>**## 2.2. 설치 절차**
상세 설치 절차는 [[docs/quickstart.md]] 문서의 "Prerequisites" 및 "Steps" 섹션을 참조하십시오.[ ](#12-부록-quick-start-가이드-docsquickstartmd)[부록 12: Quick Start 가이드 보기](#12-부록-quick-start-가이드-docsquickstartmd)

**요약:**

1. 프로젝트 Git 저장소 클론.
1. Python 가상환경 생성 및 활성화.
1. requirements.txt를 이용한 Python 패키지 설치 (pip install -r requirements.txt).
1. Neo4j 설치 및 실행 (Docker Compose 권장: docker-compose up -d neo4j).
1. .env.sample 파일을 .env로 복사 후, API 키 및 Neo4j 비밀번호 등 환경 변수 설정.
   1. .env 파일 예시:[ ](#3-단계별-cli-및-입출력-스펙-v1110---envsample-파일-예시)[3. 단계별 CLI 및 입출력 스펙 (v11.1.0) - .env.sample 파일 예시 보기](#3-단계별-cli-및-입출력-스펙-v1110---envsample-파일-예시) (내부 앵커 링크)

### <a name="_6r10osb8lgjh"></a>**## 2.3. 환경 변수 설정**
V11 엔진은 주요 설정을 환경 변수를 통해 관리합니다. .env 파일에 다음 주요 환경 변수를 설정해야 합니다:

- OPENAI\_API\_KEY: OpenAI API 사용 시 필수. (다른 LLM 사용 시 해당 키 변수 추가)
- NEO4J\_URI: Neo4j 데이터베이스 접속 주소 (기본값: bolt://localhost:7687).
- NEO4J\_USER: Neo4j 사용자명 (기본값: neo4j).
- NEO4J\_PASSWORD: Neo4j 비밀번호 (로컬 설치 시 초기 비밀번호 변경 권장).
- CTX\_TOKEN\_BUDGET: context\_builder\_v11.py가 생성하는 컨텍스트의 최대 토큰 예산 (기본값: 15000).
- CTX\_TOKEN\_MIN, CTX\_TOKEN\_MAX: 컨텍스트 토큰의 최소/최대 허용 범위.
- GC\_TRACE\_ID: (선택적) 분산 트레이싱을 위한 고유 ID. 비워두면 자동 생성.
- PROJECT\_NAME\_DEFAULT: 기본 프로젝트명.
- LOG\_LEVEL: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL). 기본값: INFO.

.env 파일은 프로젝트 루트 디렉토리에 위치해야 하며, .gitignore에 추가하여 Git 저장소에 포함되지 않도록 해야 합니다.
### <a name="_nsus3gi5mx6e"></a>**## 2.4. Docker Compose 설정 ([[docker-compose.yml]])**
V11 엔진은 Neo4j 데이터베이스와 향후 워커 애플리케이션 실행을 위해 Docker Compose를 활용합니다.

- **주요 서비스:**
  - neo4j: Neo4j Graph Database 컨테이너.
    - 이미지: neo4j:5-alpine (경량 이미지)
    - 포트: 7474 (HTTP Browser), 7687 (Bolt)
    - 볼륨: gamechanger\_neo4j\_data\_v11 (데이터 영속화)
    - 환경변수: NEO4J\_AUTH (인증), NEO4J\_PLUGINS (APOC 등 플러그인)
    - Healthcheck: Neo4j 서버 정상 실행 여부 확인.

  - gamechanger\_worker\_v11: (향후 전체 파이프라인 실행용 워커 서비스)
    - 빌드: 프로젝트 루트의 Dockerfile 사용.
    - 의존성: neo4j 서비스가 healthy 상태일 때 시작.
    - 볼륨: 프로젝트 데이터, FAISS 인덱스, 로그, 스키마 등 마운트.
    - 환경변수: .env 파일 로드.
    - 명령어: 기본 대기 상태, docker exec 또는 CI/CD에서 특정 스크립트 실행.


- **docker-compose.yml 전문:[ ](#부록-1-docker-composeyml)[부록 1: docker-compose.yml 보기](#부록-1-docker-composeyml)**
- **Dockerfile 예시:[ ](#부록-2-dockerfile)[부록 2: Dockerfile 보기](#부록-2-dockerfile)**

**실행 방법:**

- Neo4j 서비스 시작: docker-compose up -d neo4j
- 모든 서비스 시작: docker-compose up -d
- 로그 확인: docker-compose logs -f <service\_name>
- 서비스 중지 및 컨테이너 삭제: docker-compose down
### <a name="_feqmi0bb0l2h"></a>**### FAQ: 설치 및 환경 설정**
1. **Q: faiss-cpu 설치 시 C++ 빌드 오류가 발생합니다. 어떻게 해결하나요?**
   A: Windows 환경에서는 Visual Studio Build Tools (C++ 컴파일러 포함)가 필요합니다. Linux에서는 g++ 및 cmake 등이 필요할 수 있습니다. Anaconda 환경에서는 pre-compiled 바이너리를 제공하는 경우가 많으므로 conda install faiss-cpu -c pytorch 시도를 권장합니다.
1. **Q: .env 파일에 API 키를 넣었는데도 "API Key not found" 오류가 발생합니다.**
   A: .env 파일이 프로젝트 루트 디렉토리에 올바르게 위치하는지, 파일명에 오타가 없는지 확인하십시오. 또한, 스크립트가 python-dotenv 패키지를 사용하여 .env 파일을 정상적으로 로드하고 있는지 (일반적으로 load\_dotenv() 호출) 코드 확인이 필요할 수 있습니다.
1. **Q: Neo4j Docker 컨테이너는 정상 실행되지만, 애플리케이션에서 접속이 안 됩니다.**
   A: .env 파일의 NEO4J\_URI, NEO4J\_USER, NEO4J\_PASSWORD가 docker-compose.yml의 Neo4j 서비스 설정(특히 NEO4J\_AUTH 부분의 비밀번호)과 일치하는지 확인하십시오. 또한, 방화벽 설정이나 Docker 네트워크 설정을 점검해볼 필요가 있습니다. docker-compose logs -f neo4j로 Neo4j 서버 로그를 확인하여 오류 메시지가 있는지 살펴보십시오.
1. **Q: CTX\_TOKEN\_BUDGET은 어떤 기준으로 설정해야 하나요?**
   A: 사용하는 LLM 모델의 최대 컨텍스트 윈도우 크기와 비용을 고려하여 설정합니다. 일반적으로 4K~16K 토큰 사이에서 시작하며, Gemini 1.5 Pro와 같이 매우 큰 컨텍스트 윈도우를 가진 모델의 경우 100K 이상으로 설정할 수도 있습니다. 너무 작으면 정보가 부족하고, 너무 크면 비용이 증가하고 LLM의 처리 시간이 길어질 수 있습니다. 파일럿 실행을 통해 적절한 값을 찾아나가는 것이 좋습니다.
1. **Q: 여러 프로젝트를 동시에 관리하고 싶은데, Docker 볼륨명이나 컨테이너명이 충돌하지 않을까요?**
   A: docker-compose.yml 파일 내에서 볼륨명 (gamechanger\_neo4j\_data\_v11)이나 컨테이너명 (gamechanger\_neo4j\_v11)을 프로젝트별로 다르게 지정하거나, Docker Compose의 프로젝트명 기능(-p <project\_name>)을 활용하여 리소스명을 격리할 수 있습니다.
-----
## <a name="_6cwq5h8zg2r7"></a>**# 3. 핵심 모듈 상세 (Core Modules Deep Dive)**
이 섹션에서는 V11 엔진을 구성하는 각 핵심 모듈의 역할, 입출력, 주요 로직, 그리고 관련 스크립트 파일([[scripts/모듈명\_v11.py]])에 대해 상세히 설명합니다.
### <a name="_mnurf5xayjlp"></a>**## 3.1. Story Bible 관리 및 초기화**
Story Bible은 프로젝트의 모든 설정, 캐릭터, 플롯, 세계관 등을 담는 중앙 데이터 저장소 역할을 하는 JSON 파일입니다.
#### <a name="_yi9mpgg3cn9w"></a>**### 3.1.1. story\_bible\_template\_v11.json 스키마**
- **역할:** 새로운 프로젝트 시작 시 기반이 되는 Story Bible의 기본 구조와 필수 필드를 정의하는 템플릿 파일입니다.
- **주요 섹션:**
  - metadata: 소설 제목, 작가 페르소나, 장르, 로그라인, 버전 정보 등 프로젝트 전반의 메타데이터.
  - world\_setting: 세계관(우주관, 마법/기술 체계), 주요 지역 정보.
  - characters: 주요 등장인물의 상세 프로필 (역할, 설명, 동기, 관계 등).
  - plot\_arcs\_overview: 전체 이야기 아크들의 간략한 개요.
  - arc\_details: 각 아크별 상세 계획 (비어있음, arc\_detail\_v11.py가 채움).
  - episode\_log: 생성된 에피소드들의 요약 및 정보 기록.
  - themes\_and\_motifs: 작품의 핵심 주제 및 모티프.
  - rules\_and\_constraints: 작가가 설정한 규칙이나 제약사항 (예: 주인공은 회귀자 아님).
  - glossary: 작품 내 고유 용어 사전.

- **확장성 필드:** 각 엔티티(캐릭터, 지역 등)에는 graph\_id (Neo4j 노드 ID), kg\_node\_type (Neo4j 레이블) 필드가 포함되어 KG 연동을 지원합니다. foreshadow\_flags (캐릭터), discovered\_ep (지역) 등 향후 고급 기능 확장을 위한 필드도 고려되어 있습니다.
- **스키마 전문:[ ](#3-단계별-cli-및-입출력-스펙-v1110---templatesstory_bible_template_v11json-스니펫-20줄-예시)[3. 단계별 CLI 및 입출력 스펙 (v11.1.0) - templates/story_bible_template_v11.json 스니펫 보기](#3-단계별-cli-및-입출력-스펙-v1110---templatesstory_bible_template_v11json-스니펫-20줄-예시)** (내부 앵커 링크)
- **관련 JSON Schema:** [[schemas/story\_bible\_v11.schema.json]] (가상 경로)
#### <a name="_p60gv21in3dw"></a>**### 3.1.2. [[scripts/story\_bible\_init\_v11.py]]**
- **역할:** 지정된 프로젝트명으로 새로운 Story Bible 파일을 [[templates/story\_bible\_template\_v11.json]]을 복사하여 생성합니다. 필요시 프로젝트별 초기 설정을 주입할 수 있습니다.
- **주요 기능:**
  - 프로젝트 디렉토리 생성 (projects/{PROJECT\_NAME}/).
  - 템플릿 파일을 projects/{PROJECT\_NAME}/story\_bible\_v11.json으로 복사.
  - 생성 시각, 초기 버전 정보 등을 메타데이터에 기록.
  - --template-override <path\_to\_custom\_template.json> 옵션을 통해 기본 템플릿 대신 사용자 정의 템플릿 또는 샘플 Bible ([[examples/demo\_project/story\_bible\_sample\_v11.json]])을 사용할 수 있도록 지원 (Quick Start 및 테스트 용이성).

**CLI 예시:**
`      `python scripts/story\_bible\_init\_v11.py --project MyNewNovel

python scripts/story\_bible\_init\_v11.py --project MySampleNovel --template-override examples/demo\_project/story\_bible\_sample\_v11.json

   
- **입력:** --project <name>, --template <path> (선택적), --template-override <path> (선택적)
- **출력:** projects/{PROJECT\_NAME}/story\_bible\_v11.json 파일 생성.
#### <a name="_nfsmc1vhylz1"></a>**### FAQ: Story Bible 관리**
1. **Q: story\_bible\_v11.json 파일은 언제, 어떻게 수정되나요?**
   A: 초기화 시 story\_bible\_init\_v11.py에 의해 생성됩니다. 이후 각 에피소드가 성공적으로 생성되고 Consistency Guard를 통과하면, story\_bible\_updater\_v11.py가 해당 에피소드의 요약, 발생 이벤트, 캐릭터 상태 변화 등을 Story Bible에 업데이트(주로 episode\_log 및 관련 엔티티 필드 수정)합니다. 아크 계획 변경 시 arc\_detail\_v11.py의 결과물이 병합될 수도 있습니다. 수동 편집도 가능하지만, KG와의 동기화를 위해 graph\_sync\_v11.py --reverse 사용을 권장합니다.
1. **Q: graph\_id\_counter는 무엇인가요?**
   A: Story Bible 내에서 새로운 엔티티(캐릭터, 지역 등)가 생성될 때 고유한 graph\_id (예: char\_001, loc\_002)를 할당하기 위한 간단한 카운터입니다. 이는 Neo4j에서 노드를 식별하는 주요 키가 됩니다. graph\_sync\_v11.py 실행 시 이 카운터를 참조하여 ID를 생성하고 증가시킬 수 있습니다.
1. **Q: Story Bible 스키마를 변경하고 싶으면 어떻게 해야 하나요?**
   A: templates/story\_bible\_template\_v11.json 파일을 직접 수정하여 새로운 필드를 추가하거나 기존 필드 구조를 변경할 수 있습니다. 이후 해당 변경 사항을 사용하는 모든 관련 모듈(context\_builder\_v11.py, graph\_sync\_v11.py 등)의 로직도 함께 수정해야 합니다. 변경 후에는 [[schemas/story\_bible\_v11.schema.json]] (가상)도 업데이트하여 일관성을 유지하는 것이 좋습니다. Semantic Versioning에 따라 Bible 스키마 버전(metadata.bible\_version)도 적절히 변경해야 합니다.
1. **Q: metadata.settings 필드는 어떤 용도로 사용되나요?**
   A: 프로젝트별로 특정 환경 변수 설정을 오버라이드하거나, 해당 프로젝트에만 적용되는 특수 설정을 저장하는 용도로 사용할 수 있습니다. 예를 들어, CTX\_TOKEN\_BUDGET\_OVERRIDE 값을 설정하면, 해당 프로젝트에서는 .env 파일의 CTX\_TOKEN\_BUDGET 대신 이 값을 우선적으로 사용하도록 context\_builder\_v11.py에서 구현할 수 있습니다.
1. **Q: Story Bible이 너무 커지면 성능에 문제가 없을까요?**
   A: JSON 파일이 매우 커지면 로드 및 파싱 시간에 영향을 줄 수 있습니다. V11은 핵심 데이터를 Neo4j로 이전하고, Story Bible은 주로 초기 설정, 전체 개요, 그리고 최신 에피소드 로그 등을 담는 역할을 합니다. context\_builder\_v11.py는 Story Bible 전체를 항상 로드하기보다 필요한 부분만 선택적으로 읽거나, KG와 RAG를 우선적으로 활용하도록 설계하여 성능 문제를 완화합니다. 그럼에도 불구하고, 매우 긴 시리즈(수천 화)의 경우 Story Bible 분할 전략이나 DB 중심 관리로의 전환을 고려할 수 있습니다.
### <a name="_3lf5kdfttrob"></a>**## 3.2. Knowledge Graph (Neo4j) 및 Vector Store (FAISS) 연동**
V11 엔진은 정적인 JSON Story Bible의 한계를 극복하고, 이야기 정보를 더욱 동적이고 관계 중심으로 관리하기 위해 Neo4j 그래프 데이터베이스와 FAISS 벡터 저장소를 활용합니다.
#### <a name="_fwuy6e6ec6mh"></a>**### 3.2.1. Neo4j 스키마 설계 및 노드/관계 매핑**
- **역할:** Story Bible의 주요 엔티티(캐릭터, 지역, 아이템, 플롯 포인트, 에피소드 등)를 Neo4j의 노드로, 이들 간의 관계(방문, 소유, 상호작용, 다음 이벤트 등)를 관계로 모델링합니다. 이를 통해 복잡한 관계 추론, 설정 일관성 검증, 동적 컨텍스트 생성이 가능해집니다.
- **노드 레이블 및 속성:[ ](#41-neo4j-그래프-데이터베이스-설계---bible-필드--neo4j-노드-타입-매핑-표)[4.1. Neo4j 그래프 데이터베이스 설계 - Bible 필드 ↔ Neo4j 노드 타입 매핑 표 보기](#41-neo4j-그래프-데이터베이스-설계---bible-필드--neo4j-노드-타입-매핑-표)** (내부 앵커 링크)
  - 각 노드는 Story Bible의 해당 엔티티 graph\_id를 고유 식별자로 사용합니다.
  - 속성은 Story Bible 필드명과 최대한 일치시키되, 검색 및 필터링을 위해 일부 데이터 타입 변환이나 추가 속성(예: created\_at, updated\_at 타임스탬프)이 포함될 수 있습니다.

- **관계 타입 예시:**
  - (:Character)-[:APPEARED\_IN\_EPISODE]->(:EpisodeSummary)
  - (:Character)-[:VISITED\_LOCATION {episodes: [1,5], first\_visited\_episode: 1}]->(:Location)
  - (:Character)-[:HAS\_RELATIONSHIP {type: "FRIEND"}]->(:Character)
  - (:PlotPoint)-[:PRECEDES]->(:PlotPoint)

- **Cypher 예시 (MERGE 사용):[ ](#41-neo4j-그래프-데이터베이스-설계---기본-cypher-insert-예시-graph_sync_v11py-내)[4.1. Neo4j 그래프 데이터베이스 설계 - 기본 Cypher INSERT 예시 보기](#41-neo4j-그래프-데이터베이스-설계---기본-cypher-insert-예시-graph_sync_v11py-내)** (내부 앵커 링크)
  - MERGE를 사용하여 graph\_id 기준으로 노드/관계의 중복 생성을 방지하고, ON CREATE SET 및 ON MATCH SET으로 속성을 업데이트합니다.

#### <a name="_chcshnw70xf0"></a>**### 3.2.2. FAISS 벡터 인덱스 활용 (RAG)**
- **역할:** 에피소드 요약, 캐릭터 상세 설명, 세계관 설정의 특정 부분 등 긴 텍스트 정보를 고밀도 벡터로 임베딩하여 FAISS 인덱스에 저장합니다. 이를 통해 의미 기반 검색(Semantic Search)이 가능해져, 현재 컨텍스트와 가장 관련 높은 정보를 빠르게 찾아 LLM 프롬프트에 제공(Retrieval Augmented Generation - RAG)할 수 있습니다.
- **저장 대상:**
  - EpisodeSummary 노드의 summary\_long 또는 full\_text\_markdown (존재 시).
  - Character 노드의 description 및 주요 배경 이야기.
  - Location 노드의 상세 설명.
  - GlossaryTerm의 정의 등.

- **프로세스:**
  - 대상 텍스트를 문장 또는 단락 단위로 분할 (Chunking).
  - Transformer 기반 임베딩 모델(예: Sentence-BERT, OpenAI Embeddings API)을 사용하여 각 청크를 벡터로 변환.
  - 생성된 벡터와 원본 청크의 메타데이터(예: graph\_id, 에피소드 번호, 원본 노드 타입)를 FAISS 인덱스에 저장.
  - 인덱스 파일은 [[memory/faiss\_index/{PROJECT\_NAME}/]]에 저장됩니다.

- **검색:** 사용자 질의(또는 현재 생성 중인 내용)를 동일한 임베딩 모델로 벡터화한 후, FAISS 인덱스에서 코사인 유사도 등 거리 기반으로 가장 유사한 K개의 벡터(및 관련 텍스트 청크)를 검색합니다.
#### <a name="_x8qtjuw6jwqu"></a>**### 3.2.3. [[scripts/graph\_sync\_v11.py]]**
- **역할:** story\_bible\_v11.json의 내용과 Neo4j 그래프 데이터베이스 간의 데이터를 동기화합니다. 양방향 동기화를 지원합니다. 또한, FAISS 인덱스 업데이트 트리거 역할도 수행할 수 있습니다.
- **주요 기능:**
  - --init-schema: Neo4j에 필요한 인덱스(graph\_id에 대한 고유 제약 조건 등) 및 제약 조건 생성. FAISS 저장용 디렉토리 생성.
  - Bible → Graph 동기화 (기본 동작):
    - Story Bible을 읽어 각 엔티티(캐릭터, 지역 등)를 Neo4j 노드로, 관계 정보를 관계로 변환하여 MERGE 쿼리를 통해 생성/업데이트.
    - --source-file <path\_to\_diff.json>: 전체 Bible 대신 특정 Diff 파일(예: Arc Diff JSON)의 변경 사항만 선택적으로 동기화.

  - Graph → Bible 동기화 (--reverse):
    - Neo4j에서 데이터를 조회하여 story\_bible\_v11.json 형식으로 재구성하고, 기존 Bible 파일에 병합/업데이트.
    - --merge-policy <policy>: 충돌 발생 시 해결 정책 지정.
      - graph\_first (기본값): 그래프 데이터 우선.
      - bible\_first: Bible 데이터 우선.
      - interactive: 사용자에게 각 충돌 항목에 대해 선택 요청.[ ](#44-graph--bible-역동기화-graph_sync_v11py---reverse---interactive-모드-옵션)[4.4. Graph ↔ Bible 역동기화 - interactive 모드 옵션 보기](#44-graph--bible-역동기화-graph_sync_v11py---reverse---interactive-모드-옵션) (내부 앵커 링크)
      - smart-merge: (향후) 타임스탬프, 신뢰도 기반 자동 병합.
      - log-only: 충돌 로그만 기록.

    - --output-file <path\_to\_save\_bible.json>: 결과를 새 파일에 저장.

  - FAISS 인덱스 업데이트 트리거: Bible 또는 Graph 변경 시, 변경된 텍스트 데이터를 추출하여 FAISS 인덱싱 파이프라인 호출 (별도 모듈 또는 이 스크립트 내 함수).

**CLI 예시:**
`      `# 스키마 초기화

python scripts/graph\_sync\_v11.py --project MyNovel --init-schema

\# 전체 Bible을 Graph로 동기화

python scripts/graph\_sync\_v11.py --project MyNovel

\# Arc Diff 파일을 Graph로 동기화

python scripts/graph\_sync\_v11.py --project MyNovel --source-file projects/MyNovel/memory/diffs/A1\_detail\_diff\_v11.json

\# Graph를 Bible로 역동기화 (interactive 모드)

python scripts/graph\_sync\_v11.py --project MyNovel --reverse --merge-policy interactive --output-file projects/MyNovel/story\_bible\_from\_graph\_v11.json

   
  ` `IGNORE\_WHEN\_COPYING\_START
  ` `content\_copy download
  ` `Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Powershell
  IGNORE\_WHEN\_COPYING\_END
- **데이터 백업/복구:** Neo4j 데이터는 neo4j-admin dump/load 또는 Docker 볼륨 백업, FAISS 인덱스는 파일 시스템 백업으로 관리.[ ](#457-neo4j--faiss-데이터-관리-백업복구-gpt-⑦)[4.5.7. Neo4j & FAISS 데이터 관리 (백업/복구) 보기](#457-neo4j--faiss-데이터-관리-백업복구-gpt-⑦) (내부 앵커 링크)
#### <a name="_wvbi6vg0abx4"></a>**### FAQ: KG 및 RAG 연동**
1. **Q: Story Bible, Neo4j, FAISS 간에 데이터가 중복 저장되는 것 아닌가요? 비효율적이지 않나요?**
   A: 일부 정보(특히 텍스트 설명)는 여러 곳에 존재할 수 있지만, 각 저장소는 다른 목적과 강점을 가집니다. Story Bible(JSON)은 인간이 읽고 편집하기 쉬운 전체 개요 및 설정의 "원본 소스" 역할을 합니다. Neo4j는 이 정보를 관계 중심으로 구조화하여 복잡한 쿼리와 일관성 검증을 가능하게 합니다. FAISS는 긴 텍스트의 의미론적 검색에 특화되어 RAG 성능을 높입니다. 데이터 동기화(graph\_sync\_v11.py)를 통해 이들 간의 일관성을 유지하는 것이 중요하며, 각 모듈은 필요한 정보를 가장 효율적인 저장소에서 가져오도록 설계됩니다.
1. **Q: Neo4j 스키마를 변경하려면 어떻게 해야 하나요? (예: 새로운 노드 타입이나 관계 추가)**
   A: 1) story\_bible\_template\_v11.json 및 관련 JSON Schema에 변경 사항을 반영합니다. 2) graph\_sync\_v11.py의 노드/관계 매핑 로직 및 Cypher 쿼리를 수정합니다. 3) --init-schema 옵션 실행 시 새로운 인덱스나 제약 조건이 생성되도록 관련 Cypher 구문을 추가합니다. 4) 기존 데이터 마이그레이션이 필요한 경우 별도의 마이그레이션 스크립트를 작성하거나, graph\_sync\_v11.py에 관련 로직을 추가합니다. 5) 변경된 스키마를 활용하는 다른 모듈(예: context\_builder\_v11.py, consistency\_guard\_v11.py)도 업데이트해야 합니다.
1. **Q: FAISS 인덱스는 언제, 어떻게 업데이트되나요?**
   A: Story Bible이나 Neo4j의 텍스트 데이터(에피소드 요약, 캐릭터 설명 등)가 변경될 때마다 업데이트하는 것이 이상적입니다. story\_bible\_updater\_v11.py가 에피소드 정보를 저장한 후, 또는 graph\_sync\_v11.py가 동기화를 완료한 후, 변경된 텍스트에 대해 FAISS 인덱싱 파이프라인(텍스트 추출 → 청킹 → 임베딩 → FAISS 저장)을 호출하도록 구현할 수 있습니다. 모든 변경 시마다 전체 재인덱싱은 비효율적이므로, 변경된 부분만 선택적으로 업데이트(add/remove)하거나, 주기적으로 (예: 매 아크 완료 시) 재인덱싱하는 전략을 사용할 수 있습니다.
1. **Q: 어떤 임베딩 모델을 사용하는 것이 좋은가요?**
   A: 성능, 비용, 사용 편의성을 고려하여 선택합니다. OpenAI의 text-embedding-ada-002 와 같은 상용 API는 사용이 간편하고 성능이 우수하지만 비용이 발생합니다. Sentence-BERT (SBERT) 계열의 오픈소스 모델(예: all-MiniLM-L6-v2, paraphrase-multilingual-mpnet-base-v2)은 로컬에서 실행 가능하고 다양한 언어를 지원하며 성능도 준수합니다. 한국어 특화 모델(예: ko-sbert, ko-sroberta)도 좋은 선택이 될 수 있습니다. 모델 선택 시 임베딩 벡터의 차원 수(FAISS 인덱스 구성에 영향)와 처리 가능한 토큰 길이도 고려해야 합니다.
1. **Q: graph\_sync\_v11.py --reverse 실행 시 충돌은 어떤 경우에 발생하며, smart-merge는 어떻게 동작하나요?**
   A: 충돌은 Neo4j의 특정 노드/관계 속성값과 Story Bible의 해당 필드값이 서로 다를 때 발생합니다. 예를 들어, Neo4j에서는 캐릭터 레벨이 10인데 Bible에는 9로 되어 있는 경우입니다. smart-merge (향후 구현)는 각 데이터 소스의 마지막 수정 타임스탬프, 데이터 필드의 중요도(사전 정의), 또는 특정 필드는 특정 소스를 우선하는 규칙 등을 복합적으로 고려하여 자동으로 최적의 값을 선택하려고 시도합니다. 예를 들어, character.status는 항상 최신 정보가 반영된 KG를 우선하고, character.description은 인간이 직접 편집했을 가능성이 있는 Bible을 우선할 수 있습니다. 완벽한 자동 병합은 어려우므로, 중요한 충돌은 로그로 남기고 관리자 검토를 유도할 수 있습니다.
### <a name="_cd2g4ojomwu4"></a>**## 3.3. 컨텍스트 빌더 ([[scripts/context\_builder\_v11.py]])**
- **역할:** LLM이 다음 에피소드(또는 특정 내용)를 생성하는 데 필요한 모든 관련 정보를 수집, 필터링, 조합하여 최종 프롬프트에 포함될 "컨텍스트 패키지"를 동적으로 구성합니다. 정보 과다로 인한 LLM의 혼란을 막고, 토큰 예산을 효율적으로 사용하는 것이 핵심입니다.
- **주요 정보 소스:**
  - **Story Bible (story\_bible\_v11.json):**
    - 전체적인 세계관 설정 (world\_setting).
    - 현재 아크의 개요 (plot\_arcs\_overview, arc\_details).
    - 주요 등장인물 목록 및 핵심 프로필 (characters).
    - 작품의 테마 및 제약 조건 (themes\_and\_motifs, rules\_and\_constraints).

  - **Knowledge Graph (Neo4j):**
    - **현재 에피소드 관련 엔티티:** 주인공 및 주요 등장인물의 현재 상태(위치, 소지품, 감정 상태 추론 등), 최근 방문한 장소, 관련된 미해결 플롯 포인트.
    - **관계 정보:** 캐릭터 간의 현재 관계, 아이템 소유 관계, 특정 사건과 연루된 인물들.
    - **시간적 정보:** 최근 발생한 주요 이벤트 순서, 복선 회수 여부.
    - Cypher 쿼리를 통해 필요한 정보를 정밀하게 추출.

  - **Vector Store (FAISS - RAG):**
    - **관련 과거 에피소드 요약:** 현재 생성하려는 내용과 유사한 주제나 배경을 가진 과거 에피소드의 요약.
    - **캐릭터/지역 상세 정보:** 현재 등장하는 캐릭터나 배경 장소에 대한 상세한 설명 중, 현재 상황과 가장 관련 높은 부분.
    - 의미론적 검색을 통해 관련성 높은 텍스트 청크를 검색.

  - **현재 진행 중인 작업의 직접 입력:**
    - 이전 에피소드의 마지막 장면 또는 요약.
    - 현재 아크의 남은 목표 및 다음 예상 플롯 포인트.
    - scene\_point\_maker\_v11.py로부터 전달받은 현재 에피소드의 Scene Points.
    - (재시도 시) 이전 생성 실패 원인 및 수정 지침.


- **컨텍스트 구성 로직:**
  - **정보 수집:** 각 정보 소스로부터 관련 정보를 모두 가져옵니다.
  - **우선순위 부여 및 필터링:**
    - 정보의 중요도(예: 주인공 현재 상태 > 과거 아크 요약), 최신성, 직접적 관련성 등을 기준으로 우선순위 설정.
    - CTX\_TOKEN\_BUDGET 환경 변수 또는 metadata.settings.CTX\_TOKEN\_BUDGET\_OVERRIDE 값을 기준으로 전체 컨텍스트의 토큰양을 제한.

  - **정보 압축 및 요약:** 필요한 경우 긴 텍스트는 LLM을 사용하여 다시 요약하거나, 핵심 키워드만 추출.
  - **안전한 잘라내기 (Safe Trimming):** 토큰 예산 초과 시, 사전에 정의된 우선순위(예: 가장 오래된 정보, 가장 관련성 낮은 정보부터 제거)에 따라 정보를 안전하게 잘라냅니다. 핵심 엔티티 정보(주인공 상태 등)는 최대한 유지.[ ](#32-context-builder-context_builder_v11py-상세---토큰-초과-시-처리-알고리즘-3줄-설명)[3.2. Context Builder (context_builder_v11.py) 상세 - 토큰 초과 시 처리 알고리즘 보기](#32-context-builder-context_builder_v11py-상세---토큰-초과-시-처리-알고리즘-3줄-설명) (내부 앵커 링크)
  - **최종 컨텍스트 포맷팅:** LLM 프롬프트에 적합한 형태로 텍스트를 조합하고 구조화합니다 (예: Markdown, XML 태그 활용).

- **캐싱:** 동일하거나 유사한 입력(예: 동일 에피소드 재시도, 직전 에피소드 정보)에 대해 생성된 컨텍스트 또는 KG/RAG 쿼리 결과를 단기 캐시(인메모리 LRU, Redis 등)하여 LLM 호출 없이 재사용함으로써 비용 및 시간 절약 (--enable-context-cache 플래그).

**CLI 예시:**
`      `python scripts/context\_builder\_v11.py --project MyNovel --episode-id A1\_EP005 --output-file projects/MyNovel/contexts/A1\_EP005\_context.txt

   
  ` `IGNORE\_WHEN\_COPYING\_START
  ` `content\_copy download
  ` `Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Powershell
  IGNORE\_WHEN\_COPYING\_END
- **입력:** --project <name>, --episode-id <id>, (선택적) --arc-id <id>, --scene-points-file <path>, --previous-summary <text\_or\_path>
- **출력:** 생성된 컨텍스트 텍스트 파일 또는 JSON 객체.
- **관련 JSON Schema:** [[schemas/context\_package\_v11.schema.json]] (가상, 컨텍스트 출력 형식 정의)
#### <a name="_lpk3mzch33cq"></a>**### FAQ: 컨텍스트 빌더**
1. **Q: CTX\_TOKEN\_BUDGET을 초과하면 어떤 정보가 먼저 삭제되나요?**
   A: 삭제 우선순위는 구현에 따라 달라질 수 있지만, 일반적인 전략은 다음과 같습니다: 1) 가장 오래된 RAG 검색 결과 (예: 아주 예전 에피소드 요약), 2) 현재 에피소드와 직접 관련성이 낮은 일반 세계관 정보, 3) 덜 중요한 캐릭터의 상세 배경, 4) 현재 플롯과 직접 연결되지 않은 과거 아크의 상세 줄거리. 반면, 주인공의 현재 상태, 직전 에피소드의 마지막 장면, 현재 Scene Points 등은 최대한 유지하려고 노력합니다. "Safe Trimming" 알고리즘은 이러한 우선순위를 기반으로 정보를 단계적으로 제거합니다.
1. **Q: 컨텍스트에 너무 많은 정보가 들어가면 LLM이 혼란스러워하지 않을까요?**
   A: 맞습니다. 이것이 컨텍스트 빌더의 핵심 역할 중 하나입니다. 단순히 많은 정보를 모으는 것이 아니라, 현재 필요한 "핵심 정보"를 선별하고, LLM이 이해하기 쉬운 형태로 구조화하여 제공하는 것이 중요합니다. 정보 소스별 우선순위 설정, 관련성 기반 필터링, 그리고 필요시 정보를 요약하거나 가장 중요한 부분만 발췌하는 기법을 사용합니다. 또한, 프롬프트 엔지니어링을 통해 LLM에게 각 정보 섹션의 역할과 중요도를 안내할 수 있습니다.
1. **Q: KG 쿼리와 RAG 검색 중 어떤 것이 컨텍스트 생성에 더 중요한가요?**
   A: 둘 다 중요하며 상호 보완적입니다. KG 쿼리는 구조화된 데이터(예: 캐릭터 A는 아이템 B를 소유하고 있는가? 사건 C는 언제 발생했는가?)에 대한 정확하고 직접적인 답변을 얻는 데 유리합니다. RAG 검색은 비정형 텍스트 데이터(예: 캐릭터 A의 성격에 대한 상세 묘사, 과거 유사한 위기 상황에 대한 에피소드 내용)에서 현재 상황과 의미론적으로 관련된 정보를 찾는 데 효과적입니다. 컨텍스트 빌더는 이 둘을 적절히 조합하여 가장 풍부하고 정확한 컨텍스트를 만듭니다.
1. **Q: 컨텍스트 캐싱은 어떻게 구현되나요? 효과는 어느 정도인가요?**
   A: 캐싱은 컨텍스트 빌더의 입력값(프로젝트명, 에피소드 ID, 현재 KG/Bible 상태 해시 등)을 키로, 생성된 컨텍스트(또는 중간 KG/RAG 결과)를 값으로 하여 인메모리 LRU(Least Recently Used) 캐시나 Redis 같은 외부 캐시 저장소에 저장하는 방식으로 구현될 수 있습니다. 동일한 에피소드를 재시도하거나, 이전 에피소드와 매우 유사한 컨텍스트가 필요한 경우 캐시 히트율이 높아집니다. 효과는 사용 패턴에 따라 다르지만, LLM 호출이나 DB 쿼리 횟수를 줄여 10-30% 정도의 응답 시간 단축 및 비용 절감을 기대할 수 있습니다.
1. **Q: 컨텍스트 빌더의 성능 병목 지점은 어디인가요? 어떻게 최적화할 수 있나요?**
   A: 주요 병목 지점은 1) 복잡한 KG 쿼리 실행 시간, 2) 대량의 텍스트에 대한 RAG 임베딩 및 검색 시간, 3) (캐시 미스 시) 수집된 정보를 LLM으로 요약/압축하는 시간입니다. 최적화 방안으로는 1) Neo4j 쿼리 최적화 및 적절한 인덱싱, 2) FAISS 인덱스 최적화(예: IVFADC 사용) 및 임베딩 모델 경량화, 3) 효율적인 텍스트 청킹 및 요약 전략 사용, 4) 적극적인 캐싱 전략 도입 등이 있습니다.

...(이하 Draft Generator, Editor Agent, Consistency Guard 등 나머지 핵심 모듈에 대한 상세 설명 및 FAQ가 유사한 형식으로 이어집니다)...

-----
## <a name="_cyflp7g99ut6"></a>**# 4. 데이터 관리 및 동기화 (이전 4. 메모리/RAG 설계 내용 통합 및 재구성)**
...(Neo4j, FAISS, Graph Sync 등 상세 내용)...
### <a name="_kblz5140y1di"></a>**## 4.5. 모듈 API, 확장 지점 및 운영 고려 사항 (이전 4.5 내용 유지 및 확장)**
#### <a name="_86oq3v2mwywr"></a>**### 4.5.1. 모듈 인터페이스 및 확장성 원칙**
...
#### <a name="_f9nf89uf1zje"></a>**### 4.5.2. Semantic Versioning 및 모듈별 CHANGELOG ([[doc/CHANGELOG\_모듈명.md]])**
...

- **[[doc/CHANGELOG\_main.md]] (엔진 전체):[ ](#부록-3-docchangelog_mainmd-예시)[부록 3: CHANGELOG_main.md 예시 보기](#부록-3-docchangelog_mainmd-예시)**
#### <a name="_j1dvrkqm4gru"></a>**### 4.5.3. 플러그인 아키텍처 준비 ([[plugins/manifest.yaml]])**
...

- **[[plugins/sample\_echo/echo\_plugin.py]] PoC:[ ](#부록-4-pluginssample_echoecho_pluginpy-예시)[부록 4: echo_plugin.py 예시 보기](#부록-4-pluginssample_echoecho_pluginpy-예시)**
- **[[plugins/manifest.yaml]] PoC:[ ](#부록-5-pluginsmanifestyaml-예시)[부록 5: manifest.yaml 예시 보기](#부록-5-pluginsmanifestyaml-예시)**
#### <a name="_sop41e34f8o2"></a>**### 4.5.4. 입출력 스펙 표준화 (JSON Schema - [[schemas/]])**
...

- **[[schemas/arc\_diff\_v11.schema.json]] 예시:[ ](#부록-6-schemasarc_diff_v11schemajson-예시)[부록 6: arc_diff_v11.schema.json 예시 보기](#부록-6-schemasarc_diff_v11schemajson-예시)**
#### <a name="_usfx9c68b7zz"></a>**### 4.5.5. 이벤트 기반 오케스트레이션 연동 준비**
...
#### <a name="_ys1uhg7smc0z"></a>**### 4.5.6. 구조화된 로깅 및 트레이싱**
...

- 로그 예시:[ ](#11-부록-로그-예시-run_pilot_v11ps1-실행-결과)[11. 부록: 로그 예시 보기](#11-부록-로그-예시-run_pilot_v11ps1-실행-결과) (내부 앵커 링크)
#### <a name="_mvtdw0yky3uf"></a>**### 4.5.7. Neo4j & FAISS 데이터 관리 (백업/복구)**
...

- 백업 스크립트 예시 ([[scripts/backup\_neo4j.sh]]):[ ](#부록-7-scriptsbackup_neo4jsh-예시)[부록 7: backup_neo4j.sh 예시 보기](#부록-7-scriptsbackup_neo4jsh-예시)
-----
## <a name="_jj62a7s2k8ph"></a>**# 5. 품질 제어 파이프라인 (이전 5. 품질 제어 내용 통합)**
...

-----
## <a name="_okuc148oty34"></a>**# 6. 테스트 및 성능 검증 (이전 8. 테스트 자동화 내용 통합)**
### <a name="_nl4loagydnj9"></a>**## 6.1. 테스트 전략 (단위, 통합, E2E)**
...
### <a name="_nrain8us4hom"></a>**## 6.2. [[tests/]] 폴더 구조 및 pytest 활용**
...

- [[tests/test\_context\_builder\_v11.py]] 예시:[ ](#부록-8-teststest_context_builder_v11py-예시)[부록 8: test_context_builder_v11.py 예시 보기](#부록-8-teststest_context_builder_v11py-예시)
### <a name="_2hxuj3g2h8sc"></a>**## 6.3. 성능 목표(SLO) 및 부하 테스트 ([[tests/performance/]])**
...

- k6 스크립트 예시 ([[tests/performance/default\_load\_test.js]]):[ ](#부록-9-testsperformancedefault_load_testjs-예시)[부록 9: default_load_test.js 예시 보기](#부록-9-testsperformancedefault_load_testjs-예시)
- Makefile 부하 테스트 실행 예시:[ ](#부록-10-makefile-부하-테스트-부분-예시)[부록 10: Makefile (부하 테스트 부분) 예시 보기](#부록-10-makefile-부하-테스트-부분-예시)
-----
## <a name="_1ftdv5nyu6tm"></a>**# 7. 배포, 운영 및 유지보수 (이전 9. 배포 및 운영 가이드 내용 통합)**
### <a name="_tp4ttbjoglf5"></a>**## 7.1. CI/CD 파이프라인 ([[.github/workflows/main\_ci\_cd.yml]])**
...

- 워크플로 예시:[ ](#14-부록-cicd-파이프라인-상세-github-actions-예시-확장)[부록 14: GitHub Actions 워크플로 예시 보기](#14-부록-cicd-파이프라인-상세-github-actions-예시-확장) (내부 앵커 링크)
### <a name="_b6d4vzz4zmvq"></a>**## 7.2. Docker 기반 배포**
...
### <a name="_nkn3bvfsqwmb"></a>**## 7.3. 보안 관리 (비밀키, 접근 제어)**
...
### <a name="_ga8dgygbbldk"></a>**## 7.4. 데이터 거버넌스 (저작권, 개인정보 - PII Scanner Hook)**
...

- --pii-mode 플래그 및 처리 로직 예시.
### <a name="_eoooo625ovkf"></a>**## 7.5. 모듈 Deprecation Policy 및 마이그레이션 가이드 ([[docs/deprecations/]])**
...

- DeprecationWarning 사용 예시.
-----
## <a name="_rq9yphyj89mu"></a>**# 8. 고급 주제 및 향후 확장 (V13 비전)**
### <a name="_nb50qwt58zk8"></a>**## 8.1. 강화학습(RL) 루프 상세**
...
### <a name="_r3kzl27wkuy5"></a>**## 8.2. V13 "Zero-Touch, High-Fidelity" 확장 방향**
- Smart-Retry Orchestrator
- Auto-Fix Chain
- Dual-Draft Generator
- Adaptive Quality Ladder
- AutoForeshadow Manager
- Idempotent Check-pointing & Safe-Fallback Episode
### <a name="_9bakq4vvw9a7"></a>**## 8.3. 멀티-LLM 전략 및 비용 최적화 심화**
...

-----
## <a name="_kx5upb4c36y1"></a>**# 9. 튜토리얼 및 사용 예시**
### <a name="_cvh3d6qojua0"></a>**## 9.1. 30화 파일럿 실행 가이드 ([[scripts/run\_pilot\_v11.ps1]])**
- 스크립트 전문 및 설명:[ ](#7-30화-파일럿-체크리스트-및-실행-스크립트-scriptsrun_pilot_v11ps1)[7. "30화 파일럿" 체크리스트 및 실행 스크립트 보기](#7-30화-파일럿-체크리스트-및-실행-스크립트-scriptsrun_pilot_v11ps1) (내부 앵커 링크)
- Quick Start 가이드:[ ](#12-부록-quick-start-가이드-docsquickstartmd)[부록 12: Quick Start 가이드 보기](#12-부록-quick-start-가이드-docsquickstartmd) (내부 앵커 링크)
### <a name="_rme02lz6e2lk"></a>**## 9.2. 샘플 프로젝트 활용법 ([[examples/demo\_project/]])**
- 샘플 데이터 구조 및 로드 방법:[ ](#13-부록-샘플-데이터-세트-examplesdemo_project)[부록 13: 샘플 데이터 세트 보기](#13-부록-샘플-데이터-세트-examplesdemo_project) (내부 앵커 링크)
-----
## <a name="_d4j6vi3btbhd"></a>**# 10. 📜 변경 이력 (Changelog)**

|버전|날짜|주요 변경 사항|담당자|
| :- | :- | :- | :- |
|v11.2.0|2025-05-15|AI 학습 최적화 (계층적 목차, FAQ, 용어 사전, 부록 분리 등), Quick Start, 샘플 데이터, CI/k6 연동 강화, 플러그인 PoC, PII/Deprecation 예시 추가.|AI Assistant|
|v11.1.0|2025-05-13|V13 확장성 및 운영 안정성 강화 (Semantic Versioning, JSON Schema, 이벤트 기반 준비, 구조화 로깅, DR, 보안, 거버넌스, SLO, Deprecation 개념 도입).|AI Assistant|
|v11.0.1|2025-05-12|(가상) 초기 안정화 릴리스. 네이밍 통일, 템플릿 확장, Neo4j/Cypher 구체화, 토큰 가드 강화, 충돌 정책 보강, 테스트/보안/비용 팁, Docker, 모니터링, 로그 예시 추가.|User & AI|
|v11.0.0|(가상)|(가상) V11 엔진 핵심 기능 (KG/RAG, Editor Agent, RL 루프) 최초 통합 버전.|User|

-----
## <a name="_x4uibcko4dn6"></a>**# 11. 용어·약어 사전 (Glossary)**
- **CLI (Command Line Interface):** 명령줄 인터페이스. 사용자가 텍스트 명령으로 컴퓨터 프로그램과 상호작용하는 방식.
- **CTX\_TOKEN\_BUDGET:** 컨텍스트 빌더가 생성하는 LLM 프롬프트용 컨텍스트의 최대 토큰(단어 또는 하위 단어 단위) 예산.
- **Cypher:** Neo4j 그래프 데이터베이스를 위한 선언적 쿼리 언어.
- **Diff JSON:** 특정 변경 사항(예: 새로운 아크 계획, 에피소드 결과)을 나타내는 JSON 형식 데이터. Story Bible에 병합될 수 있음.
- **Docker:** 애플리케이션을 컨테이너라는 표준화된 단위로 패키징, 배포, 실행하기 위한 플랫폼.
- **Docker Compose:** 여러 Docker 컨테이너를 정의하고 실행하기 위한 도구. docker-compose.yml 파일 사용.
- **E2E (End-to-End) Test:** 전체 시스템 또는 주요 사용자 시나리오를 처음부터 끝까지 테스트하는 방식.
- **Editor Agent:** LLM을 활용하여 생성된 초고의 문체, 흐름, 표현 등을 자동으로 교정하고 개선하는 모듈.
- **FAISS (Facebook AI Similarity Search):** 고밀도 벡터의 효율적인 유사도 검색 및 클러스터링을 위한 라이브러리. RAG 시스템의 벡터 저장소로 활용.
- **Feature Flag:** 특정 기능을 켜고 끌 수 있도록 하는 소프트웨어 개발 기술. 점진적 배포나 A/B 테스트에 사용.
- **Git:** 분산 버전 관리 시스템. 소스 코드 변경 이력 관리.
- **GitHub Actions:** GitHub에서 직접 코드 빌드, 테스트, 배포 등의 워크플로를 자동화하는 CI/CD 서비스.
- **GraphDB (Graph Database):** 그래프 구조(노드, 관계, 속성)를 사용하여 데이터를 저장하고 탐색하는 데이터베이스. Neo4j가 대표적.
- **GUI (Graphical User Interface):** 그래픽 사용자 인터페이스. 사용자가 아이콘, 메뉴 등 시각적 요소로 프로그램과 상호작용하는 방식.
- **JSON (JavaScript Object Notation):** 사람이 읽기 쉬운 텍스트 기반의 데이터 교환 형식.
- **JSON Schema:** JSON 데이터의 구조를 정의하고 검증하기 위한 표준 명세.
- **k6:** 현대적인 부하 테스트 도구. 개발자 친화적이며 스크립트 기반 테스트 지원.
- **KG (Knowledge Graph):** 현실 세계의 엔티티와 그 관계를 그래프 형태로 표현한 지식 베이스. V11에서는 Neo4j를 사용.
- **LLM (Large Language Model):** 대규모 텍스트 데이터로 사전 학습된 거대 언어 모델 (예: GPT-4, Gemini, Claude).
- **Markdown:** 일반 텍스트 기반의 경량 마크업 언어. 읽고 쓰기 쉬우며 HTML로 변환 가능.
- **MERGE (Cypher):** Neo4j Cypher 명령어. 특정 패턴이 존재하면 일치시키고, 존재하지 않으면 새로 생성.
- **Neo4j:** 가장 널리 사용되는 그래프 데이터베이스 관리 시스템 중 하나.
- **오케스트레이션 (Orchestration):** 여러 개의 자동화된 작업이나 서비스를 조정하고 관리하여 하나의 통합된 프로세스나 워크플로를 만드는 것.
- **PII (Personally Identifiable Information):** 개인 식별 정보.
- **PoC (Proof of Concept):** 개념 증명. 새로운 아이디어나 방법의 실현 가능성을 검증하기 위한 소규모 시범 프로젝트.
- **PowerShell:** Microsoft에서 개발한 명령줄 셸 및 스크립트 언어.
- **Prometheus:** 오픈소스 시스템 모니터링 및 경고 도구.
- **pytest:** Python 프로그래밍 언어를 위한 테스트 프레임워크.
- **Python Entry Points:** Python 패키지가 다른 패키지에 플러그인이나 확장 기능을 제공할 수 있도록 하는 메커니즘.
- **RAG (Retrieval Augmented Generation):** 외부 지식 소스(예: 벡터 DB)에서 관련 정보를 검색하여 LLM의 프롬프트에 추가함으로써, 생성 결과의 정확성과 최신성을 향상시키는 기법.
- **Redis:** 인메모리 데이터 구조 저장소. 데이터베이스, 캐시, 메시지 브로커로 사용.
- **RL (Reinforcement Learning):** 강화학습. 에이전트가 환경과 상호작용하며 보상을 최대화하는 방향으로 학습하는 기계학습의 한 분야.
- **Semantic Versioning (SemVer):** MAJOR.MINOR.PATCH 형식의 버전 번호 지정 규칙. API 호환성 변경 여부를 명시.
- **SLO (Service Level Objective):** 서비스 수준 목표. 서비스가 달성해야 하는 특정 측정 가능한 목표치 (예: 응답 시간, 가용성).
- **Story Bible:** 소설의 모든 설정, 캐릭터, 플롯, 세계관 등을 담고 있는 핵심 문서 또는 데이터 저장소. V11에서는 JSON 파일 형태.
- **Stub:** 아직 완전히 구현되지 않은 코드 부분을 나타내는 임시 코드 조각. 인터페이스 정의나 테스트 목적으로 사용.
- **TL;DR (Too Long; Didn't Read):** 너무 길어서 읽지 않음. 긴 내용의 요약을 의미.
- **Token (LLM):** LLM이 텍스트를 처리하는 기본 단위. 단어, 하위 단어(subword), 또는 문자일 수 있음.
- **Trace ID (Correlation ID):** 분산 시스템에서 특정 요청이나 트랜잭션의 전체 경로를 추적하기 위해 사용되는 고유 식별자.
- **UML (Unified Modeling Language):** 소프트웨어 시스템을 시각적으로 모델링하기 위한 표준화된 언어.
- **UUID (Universally Unique Identifier):** 전역적으로 고유한 128비트 식별자.
- **YAML (YAML Ain't Markup Language):** 사람이 읽기 쉬운 데이터 직렬화 언어. 설정 파일 등에 많이 사용.
-----
## <a name="_3exb0cz8kp23"></a>**# 12. 부록: Quick Start 가이드 ([[docs/quickstart.md]])**
[부록 12: Quick Start 가이드 전문 보기](#부록-12-docsquickstartmd-전문)

-----
## <a name="_ntke5cxrgt4"></a>**# 13. 부록: 샘플 데이터 세트 ([[examples/demo\_project/]])**
[부록 13: 샘플 데이터 세트 구조 및 설명 보기](#부록-13-examplesdemo_project-구조-및-설명)

-----
## <a name="_nv7zhmocfjg2"></a>**# 14. 부록: CI/CD 파이프라인 상세 ([[.github/workflows/main\_ci\_cd.yml]])**
[부록 14: GitHub Actions 워크플로 예시 전문 보기](#부록-14-github-actions-워크플로-예시-전문)

-----
## <a name="_uuugxuemoebc"></a>**# 15. 부록: 릴리스 전략 및 시스템 검증 아이디어**
[부록 15: 릴리스 전략 및 검증 아이디어 상세 보기](#부록-15-릴리스-전략-및-시스템-검증-아이디어-상세)

----------
(여기까지가 본문입니다. 이제부터는 위 본문에서 링크로 참조된 부록 파일들의 내용을 코드펜스 블록으로 제공하겠습니다.)

-----
# <a name="_qik0ifyvtemc"></a>**부록 파일 목록**
## <a name="_pxq9up4aasky"></a>**부록 1: [[docker-compose.yml]]**
`     `# docker-compose.yml

version: '3.8'

services:

`  `neo4j:

`    `image: neo4j:5-alpine # 경량 이미지 사용

`    `container\_name: gamechanger\_neo4j\_v11 # 이전 버전과 구분

`    `ports:

`      `- "7474:7474" # Neo4j Browser

`      `- "7687:7687" # Bolt port

`    `volumes:

`      `- gamechanger\_neo4j\_data\_v11:/data # 볼륨명도 버전 명시

`      `- ./logs/neo4j:/logs # 로그 외부 마운트 (선택적)

`    `environment:

`      `# .env 파일에서 NEO4J\_PASSWORD를 가져오거나, 없으면 기본값 사용

`      `NEO4J\_AUTH: neo4j/${NEO4J\_PASSWORD:-please\_change\_this\_default\_password}

`      `NEO4J\_PLUGINS: '["apoc", "graph-data-science"]' # APOC, GDS 플러그인 사용 예시

`      `# JVM 힙 사이즈 설정 (메모리 사용량에 따라 조절)

`      `# NEO4J\_SERVER\_MEMORY\_HEAP\_INITIAL\_\_SIZE: 512m

`      `# NEO4J\_SERVER\_MEMORY\_HEAP\_MAX\_\_SIZE: 2G

`    `restart: unless-stopped

`    `healthcheck: # Neo4j 서버 상태 확인

`      `test: ["CMD-SHELL", "wget --quiet --tries=1 --spider http://localhost:7474 || exit 1"]

`      `interval: 10s

`      `timeout: 5s

`      `retries: 5

`  `gamechanger\_worker\_v11: # 서비스명도 버전 명시

`    `build:

`      `context: .

`      `dockerfile: Dockerfile # 프로젝트 루트에 Dockerfile 필요

`    `container\_name: gamechanger\_worker\_v11

`    `depends\_on:

`      `neo4j: # neo4j 서비스가 healthcheck를 통과한 후에 worker 시작

`        `condition: service\_healthy

`    `volumes:

`      `- ./projects:/app/projects # 프로젝트 데이터 마운트

`      `- ./memory/faiss\_index:/app/memory/faiss\_index # FAISS 인덱스 마운트

`      `- ./logs/app:/app/logs

`      `- ./schemas:/app/schemas # JSON Schema 마운트 (필요시)

`      `- ./plugins:/app/plugins # 플러그인 마운트 (필요시)

`      `- ./examples:/app/examples # 샘플 데이터 마운트 (필요시)

`    `env\_file:

`      `- .env # .env 파일 로드

`    `# 기본적으로는 실행하지 않고 대기 (exec로 명령어 전달 또는 CI에서 오버라이드)

`    `command: ["tail", "-f", "/dev/null"]

`    `restart: on-failure

volumes:

`  `gamechanger\_neo4j\_data\_v11: # 볼륨명도 버전 명시



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Yaml

IGNORE\_WHEN\_COPYING\_END
## <a name="_jm2112n4iiqh"></a>**부록 2: [[Dockerfile]]**
`     `# Dockerfile

FROM python:3.10-slim

WORKDIR /app

\# 시스템 의존성 설치 (예: FAISS 빌드, 특정 라이브러리 실행에 필요한 경우)

\# RUN apt-get update && apt-get install -y --no-install-recommends \

\#     build-essential cmake libgomp1 \

\#  && rm -rf /var/lib/apt/lists/\*

\# libgomp1는 일부 ML 라이브러리(예: faiss) 실행 시 필요할 수 있음

COPY requirements.txt .

\# --no-cache-dir: Docker 이미지 크기 최적화

\# --prefer-binary: 가능한 경우 pre-compiled 바이너리 사용 (빌드 시간 단축)

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

\# 애플리케이션 코드 복사

\# .dockerignore 파일을 사용하여 불필요한 파일(예: .git, .venv, \_\_pycache\_\_) 제외

COPY . .

\# 기본 포트 노출 (애플리케이션이 API 서버 등으로 동작할 경우)

\# EXPOSE 8000

\# 기본 실행 명령어 (docker-compose.yml에서 오버라이드 가능)

\# ENTRYPOINT ["python"]

\# CMD ["scripts/run\_full\_pipeline\_v11.py", "--project", "DefaultDockerProject"]

CMD ["tail", "-f", "/dev/null"] # 기본적으로는 대기 상태로 실행



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Dockerfile

IGNORE\_WHEN\_COPYING\_END
## <a name="_u1djzgiuoz2u"></a>**부록 3: [[doc/CHANGELOG\_main.md]] 예시**
`     `# Project GameChanger - Main Engine Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

\## [v11.2.0] - 2025-05-15

\### Added

\- AI 학습 최적화를 위한 문서 구조 전면 개편 (계층적 목차, 모듈별 상세 기술, FAQ, 용어 사전, 부록 분리).

\- `docs/quickstart.md` 추가: 10줄 내외의 즉시 실행 가능한 명령어 블록 제공.

\- `examples/demo\_project/` 샘플 데이터 세트 개념 명시 및 구조 권고.

\- CI/CD 파이프라인 (GitHub Actions)에 k6 부하 테스트 실행 스텁 및 결과 리포팅 개념 추가.

\- 플러그인 레지스트리 PoC (`plugins/sample\_echo/`) 및 실행 로그 예시 추가.

\- PII Scanner Hook (`--pii-mode` 플래그) 예외 처리 및 기본값 설정 권고.

\- Deprecation Policy 실행 테스트 (`warnings.warn`) 예시 코드 추가.

\- 릴리스 전략, 파일럿 멀티-모델 매트릭스 수집, 장애 복구 테스트, E2E 왕복 테스트 개념 도입 (부록 15).

\### Changed

\- 문서 버전을 v11.1.0에서 v11.2.0으로 변경.

\- 문서 목표에 "개발자가 즉시 프로젝트를 실행하고 검증"할 수 있도록 하는 내용 명시.

\- TL;DR 업데이트하여 v11.1.0 -> v11.2.0 핵심 변화 요약.

\## [v11.1.0] - 2025-05-13

\### Added

\- V13 확장성 및 운영 안정성 강화를 위한 기반 마련:

`  `- Semantic Versioning 도입 권고.

`  `- 입출력 스펙 표준화 (JSON Schema) 개념 도입.

`  `- 이벤트 기반 오케스트레이션 연동 개념 도입.

`  `- 구조화된 로깅 및 Trace ID 활용 강화.

`  `- Neo4j & FAISS 데이터 백업/복구 절차 권고.

`  `- 보안 관리 (비밀키, 접근 제어) 가이드라인 추가.

`  `- 데이터 거버넌스 (저작권, 개인정보) 고려 사항 언급.

`  `- 성능 목표(SLO) 및 부하 테스트 개념 도입.

`  `- 모듈 Deprecation Policy 및 마이그레이션 가이드 개념 도입.

\- Docker Compose Healthcheck 추가 (Neo4j).

\- `story\_bible\_template\_v11.json`에 `engine\_version\_used`, `settings` 등 확장 필드 예시 추가.

\- Neo4j 스키마 매핑 표에 확장성 고려 사항 추가.

\### Changed

\- 문서 버전을 v11.0.1에서 v11.1.0으로 변경.

\- 문서 목표에 "향후 확장성" 및 "운영 안정성 확보" 명시.

\- 전체 파이프라인 UML 다이어그램에 확장 지점(Hook Point) 명시.

\- `.env.sample`에 `GC\_TRACE\_ID`, `PLUGIN\_DIR` (주석 처리) 등 추가.

\- `run\_pilot\_v11.ps1`에 `GC\_TRACE\_ID` 자동 생성 예시 추가.

\- 로그 예시를 구조화된 JSON 형태로 변경.

\## [v11.0.1] - 2025-05-12 (가상)

\### Added

\- (내용은 v11.2.0 본문에 통합되었으므로 상세 생략, 이전 버전의 주요 변경점 섹션 참조)

\- 네이밍 및 버전 통일, 템플릿 예시 확장, Neo4j 스키마 및 Cypher 구체화, 컨텍스트 토큰 가드 강화, Graph↔Bible 충돌 정책 보강, 테스트 템플릿 개선, 보안 및 비용 절감 팁 추가, Docker Compose 초안 추가, 성능 및 모니터링 가이드라인 추가, 로그 예시 추가, 문서 구조 개선 (TL;DR 요약표).

\### Fixed

\- (가상) 초기 버그 수정 및 안정화.

\## [v11.0.0] - (가상)

\### Added

\- V11 엔진 핵심 기능 최초 통합:

`  `- 동적 메모리 시스템 (Neo4j GraphDB + FAISS RAG) 도입.

`  `- 지능형 품질 제어 (LLM 기반 Editor Agent + Consistency Guard v11).

`  `- 강화학습(RL) 기반 품질 최적화 루프 (선택적).

`  `- 모듈화 및 Feature Flag 도입.

`  `- 양방향 동기화 (Graph ↔ Bible).



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Markdown

IGNORE\_WHEN\_COPYING\_END
## <a name="_57hdtck7pvc"></a>**부록 4: [[plugins/sample\_echo/echo\_plugin.py]] 예시**
`     `# plugins/sample\_echo/echo\_plugin.py

import logging

\# 로거 설정 (플러그인 개별 로깅을 위해)

logger = logging.getLogger(\_\_name\_\_)

\# 기본 로깅 레벨 설정 (필요시 외부에서 주입 가능)

\# logging.basicConfig(level=logging.DEBUG) # 테스트 시 로깅 확인용

class EchoPlugin:

`    `"""

`    `간단한 에코 플러그인 예시.

`    `입력된 텍스트에 설정된 접두사를 붙여 반환하고 로그를 남깁니다.

`    `"""

`    `def \_\_init\_\_(self, config=None):

`        `self.config = config if config is not None else {}

`        `self.prefix = self.config.get("prefix", "EchoPlugin: ")

`        `logger.debug(f"EchoPlugin initialized with config: {self.config}, prefix: '{self.prefix}'")

`    `def process(self, text: str) -> str:

`        `"""

`        `주어진 텍스트를 처리합니다.

`        `:param text: 처리할 입력 텍스트.

`        `:return: 접두사가 추가된 텍스트.

`        `"""

`        `if not isinstance(text, str):

`            `logger.error(f"Invalid input type for EchoPlugin.process: expected str, got {type(text)}")

`            `return "[Error: Invalid input type]"

`        `processed\_text = f"{self.prefix}{text}"

`        `logger.info(f"EchoPlugin processing: Input='{text}', Output='{processed\_text}'")

`        `return processed\_text

`    `def get\_status(self) -> dict:

`        `"""

`        `플러그인의 현재 상태나 설정을 반환합니다. (선택적 메소드)

`        `"""

`        `return {

`            `"name": "SampleEcho",

`            `"version": self.config.get("version", "0.1.0"), # manifest에서 주입 가능

`            `"prefix\_used": self.prefix,

`            `"is\_active": True

`        `}

def get\_plugin\_instance(config: dict = None): # 이 함수가 Entry Point로 사용됨

`    `"""

`    `EchoPlugin의 인스턴스를 생성하여 반환합니다.

`    `플러그인 로더가 이 함수를 호출하여 플러그인을 가져옵니다.

`    `:param config: 플러그인 설정 딕셔너리.

`    `:return: EchoPlugin 인스턴스.

`    `"""

`    `return EchoPlugin(config)

\# 직접 실행하여 테스트하기 위한 예시 (선택적)

if \_\_name\_\_ == "\_\_main\_\_":

`    `# 로깅 핸들러 추가 (직접 실행 시 콘솔 출력용)

`    `if not logger.handlers:

`        `handler = logging.StreamHandler()

`        `formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

`        `handler.setFormatter(formatter)

`        `logger.addHandler(handler)

`        `logger.setLevel(logging.DEBUG)

`    `# 기본 설정으로 플러그인 인스턴스 생성

`    `default\_plugin\_config = {"prefix": "DefaultEcho: "}

`    `plugin\_instance\_default = get\_plugin\_instance(default\_plugin\_config)

`    `result\_default = plugin\_instance\_default.process("Hello from default config!")

`    `# print(f"Default Test: {result\_default}")

`    `# print(f"Default Status: {plugin\_instance\_default.get\_status()}")

`    `# Manifest 파일과 유사한 커스텀 설정으로 플러그인 인스턴스 생성

`    `custom\_plugin\_config\_from\_manifest = {

`        `"prefix": "GameChanger Custom Echo: ",

`        `"version": "0.1.1-custom"

`    `}

`    `plugin\_instance\_custom = get\_plugin\_instance(custom\_plugin\_config\_from\_manifest)

`    `result\_custom = plugin\_instance\_custom.process("Hello from custom manifest config!")

`    `# print(f"Custom Test: {result\_custom}")

`    `# print(f"Custom Status: {plugin\_instance\_custom.get\_status()}")



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Python

IGNORE\_WHEN\_COPYING\_END
## <a name="_dy157kv5aoxk"></a>**부록 5: [[plugins/manifest.yaml]] 예시**
`     `# plugins/manifest.yaml

\# Project GameChanger v11 - Plugin Manifest File

\# 이 파일은 시스템에 로드할 플러그인들을 정의합니다.

\# 플러그인 로더는 이 파일을 파싱하여 각 플러그인을 초기화하고 등록합니다.

plugins:

`  `- name: "SampleEcho"  # 플러그인의 고유한 이름

`    `# Python 모듈 경로. 'plugins' 디렉토리를 기준으로 상대 경로 또는 절대 경로.

`    `# 예: 'sample\_echo.echo\_plugin' -> plugins/sample\_echo/echo\_plugin.py

`    `module: "sample\_echo.echo\_plugin"

`    `# 모듈 내에서 플러그인 인스턴스를 반환하는 함수 또는 클래스 생성자 이름.

`    `# 이 함수/클래스는 선택적으로 config 딕셔너리를 인자로 받을 수 있어야 함.

`    `entry\_point\_func: "get\_plugin\_instance"

`    `version: "0.1.0"    # 플러그인의 버전 (Semantic Versioning 권장)

`    `description: "A simple echo plugin for demonstration purposes." # 플러그인 설명

`    `enabled: true       # true 이면 로드 시도, false 이면 무시.

`    `# 이 플러그인에 전달될 설정값들.

`    `# entry\_point\_func 호출 시 이 딕셔너리가 인자로 전달됨.

`    `config:

`      `prefix: "GameChanger Echo (from Manifest): "

`      `# log\_level: "DEBUG" # 플러그인별 로그 레벨 설정 등

`  `# - name: "AnotherExamplePlugin"

`  `#   module: "another\_plugin.main\_module"

`  `#   entry\_point\_func: "create\_plugin" # 또는 클래스명 "AnotherPluginClass"

`  `#   version: "1.2.3"

`  `#   description: "Does something more complex."

`  `#   enabled: false # 현재 비활성화된 플러그인

`  `#   config:

`  `#     api\_key\_env\_var: "ANOTHER\_PLUGIN\_API\_KEY" # 환경 변수 이름을 참조하도록 할 수도 있음

`  `#     timeout\_seconds: 30

\# 플러그인 로더는 다음 사항을 고려하여 구현될 수 있습니다:

\# 1. 'enabled: true'인 플러그인만 로드.

\# 2. 'module'과 'entry\_point\_func'를 사용하여 플러그인 인스턴스 동적 임포트 및 생성.

\#    (예: importlib.import\_module, getattr 사용)

\# 3. 'config' 딕셔너리를 플러그인 인스턴스 생성 시 전달.

\# 4. 로드된 플러그인들을 이름으로 관리하는 레지스트리(딕셔너리 등)에 저장.

\# 5. 버전 충돌 또는 의존성 관리 (고급 기능).



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Yaml

IGNORE\_WHEN\_COPYING\_END
## <a name="_7h2m26lh4rag"></a>**부록 6: [[schemas/arc\_diff\_v11.schema.json]] 예시**
`     `{

`  `"$schema": "http://json-schema.org/draft-07/schema#",

`  `"title": "Arc Diff v11",

`  `"description": "Schema for an Arc Detail Diff JSON file in Project GameChanger v11. This defines the plan for a single story arc.",

`  `"type": "object",

`  `"properties": {

`    `"arc\_id": {

`      `"description": "Unique identifier for the arc (e.g., A1, A2).",

`      `"type": "string",

`      `"pattern": "^A[1-9]\\d\*$"

`    `},

`    `"title": {

`      `"description": "The title of this story arc.",

`      `"type": "string",

`      `"minLength": 1

`    `},

`    `"summary\_logline": {

`      `"description": "A short, compelling logline summarizing the arc.",

`      `"type": "string",

`      `"minLength": 10

`    `},

`    `"target\_episode\_start": {

`      `"description": "The intended starting episode number for this arc within the entire series.",

`      `"type": "integer",

`      `"minimum": 1

`    `},

`    `"target\_episode\_end": {

`      `"description": "The intended ending episode number for this arc.",

`      `"type": "integer",

`      `"minimum": 1

`      `// "exclusiveMinimum": { "$ref": "#/properties/target\_episode\_start" } // 시작보다 커야 함 (주의: JSON Schema 표준 문법 아님, 구현 시 로직으로 처리)

`    `},

`    `"main\_characters\_in\_arc": {

`      `"description": "List of main character graph\_ids appearing or central to this arc. Can include new character definitions.",

`      `"type": "array",

`      `"items": {

`        `"oneOf": [

`          `{ "type": "string", "description": "Existing character graph\_id." },

`          `{

`            `"type": "object",

`            `"properties": {

`              `"id": { "type": "string", "description": "New character graph\_id (e.g., char\_new\_villain\_a1)" },

`              `"name": { "type": "string", "description": "New character's name" },

`              `"role": { "type": "string", "description": "New character's role (e.g., villain, ally)" },

`              `"is\_new": { "type": "boolean", "const": true }

`            `},

`            `"required": ["id", "name", "role", "is\_new"]

`          `}

`        `]

`      `}

`    `},

`    `"new\_locations\_in\_arc": {

`      `"description": "List of new locations introduced in this arc.",

`      `"type": "array",

`      `"items": {

`        `"type": "object",

`        `"properties": {

`          `"id": { "type": "string", "description": "New location graph\_id (e.g., loc\_secret\_lab\_a1)" },

`          `"name": { "type": "string" },

`          `"type": { "type": "string", "description": "Type of location (e.g., dungeon, city, lab)" },

`          `"description\_short": { "type": "string" }

`        `},

`        `"required": ["id", "name", "type"]

`      `}

`    `},

`    `"key\_plot\_points": {

`      `"description": "A sequence of key plot points planned for this arc.",

`      `"type": "array",

`      `"items": {

`        `"$ref": "#/definitions/plotPoint"

`      `}

`    `},

`    `"arc\_theme\_focus": {

`      `"description": "The main thematic focus of this arc.",

`      `"type": "string"

`    `},

`    `"items\_introduced": {

`      `"description": "List of new significant items introduced in this arc.",

`      `"type": "array",

`      `"items": {

`        `"type": "object",

`        `"properties": {

`          `"graph\_id": { "type": "string" },

`          `"name": { "type": "string" },

`          `"description": { "type": "string" },

`          `"type": { "type": "string", "description": "Type of item (e.g., weapon, artifact, consumable)" }

`        `},

`        `"required": ["graph\_id", "name", "description"]

`      `}

`    `},

`    `"foreshadows\_planted": {

`      `"description": "List of foreshadowing elements to be planted in this arc.",

`      `"type": "array",

`      `"items": {

`        `"type": "object",

`        `"properties": {

`          `"graph\_id": {"type": "string", "description": "Unique ID for this foreshadowing element"},

`          `"description": {"type": "string"},

`          `"target\_reveal\_arc\_id": {"type": "string", "description": "Arc ID where this foreshadow is intended to be revealed/resolved"}

`        `},

`        `"required": ["graph\_id", "description"]

`      `}

`    `},

`    `"foreshadows\_resolved": {

`      `"description": "List of graph\_ids of foreshadowing elements from previous arcs to be resolved in this arc.",

`      `"type": "array",

`      `"items": { "type": "string" }

`    `}

`  `},

`  `"required": [

`    `"arc\_id",

`    `"title",

`    `"summary\_logline",

`    `"target\_episode\_start",

`    `"target\_episode\_end",

`    `"main\_characters\_in\_arc",

`    `"key\_plot\_points"

`  `],

`  `"definitions": {

`    `"plotPoint": {

`      `"type": "object",

`      `"properties": {

`        `"graph\_id": {

`          `"type": "string",

`          `"description": "Unique identifier for this plot point (e.g., plot\_A1\_001)."

`        `},

`        `"kg\_node\_type": {

`          `"type": "string",

`          `"const": "PlotPoint",

`          `"description": "Knowledge Graph node type."

`        `},

`        `"summary": {

`          `"type": "string",

`          `"description": "A concise summary of the plot point."

`        `},

`        `"episode\_target": {

`          `"type": "integer",

`          `"description": "Target episode number within the arc for this plot point to occur (relative to arc start or absolute in series)."

`        `},

`        `"status": {

`          `"type": "string",

`          `"enum": ["PLANNED", "IN\_PROGRESS", "RESOLVED", "DROPPED"],

`          `"default": "PLANNED"

`        `},

`        `"related\_character\_ids": {

`          `"type": "array",

`          `"items": { "type": "string" }

`        `},

`        `"related\_location\_ids": {

`          `"type": "array",

`          `"items": { "type": "string" }

`        `}

`      `},

`      `"required": ["graph\_id", "kg\_node\_type", "summary", "episode\_target"]

`    `}

`  `}

}



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Json

IGNORE\_WHEN\_COPYING\_END
## <a name="_6tidq9g7ddx8"></a>**부록 7: [[scripts/backup\_neo4j.sh]] 예시**
`     `#!/bin/bash

\# scripts/backup\_neo4j.sh

\# Neo4j 데이터베이스를 백업하는 스크립트 예시.

\# docker exec를 사용하여 실행 중인 Neo4j 컨테이너에서 dump를 수행합니다.

\# --- 설정 변수 ---

\# 백업 파일을 저장할 디렉토리

BACKUP\_DIR="/srv/gamechanger/neo4j\_backups"

\# Neo4j Docker 컨테이너 이름 (docker-compose.yml에 정의된 이름)

NEO4J\_CONTAINER\_NAME="gamechanger\_neo4j\_v11"

\# 백업할 데이터베이스 이름 (Neo4j 5.x 기본값은 'neo4j')

DATABASE\_NAME="neo4j"

\# 보관할 최근 백업 파일 수 (오래된 파일 자동 삭제용)

RETENTION\_DAYS=7

\# 로그 파일 경로

LOG\_FILE="${BACKUP\_DIR}/backup\_neo4j.log"

\# --- ---

\# 로그 함수

log\_message() {

`    `echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" | tee -a "$LOG\_FILE"

}

\# 백업 디렉토리 생성 (없으면)

mkdir -p "$BACKUP\_DIR"

if [ $? -ne 0 ]; then

`    `log\_message "ERROR: Failed to create backup directory: $BACKUP\_DIR"

`    `exit 1

fi

\# 현재 타임스탬프 (파일 이름용)

TIMESTAMP=$(date +"%Y%m%d\_%H%M%S")

DUMP\_FILENAME="${DATABASE\_NAME}\_backup\_${TIMESTAMP}.dump"

DUMP\_PATH\_IN\_CONTAINER="/backups/${DUMP\_FILENAME}" # 컨테이너 내 임시 경로

FINAL\_DUMP\_PATH="${BACKUP\_DIR}/${DUMP\_FILENAME}"

log\_message "Starting Neo4j backup for database '$DATABASE\_NAME' from container '$NEO4J\_CONTAINER\_NAME'..."

\# 1. Docker 컨테이너 내에 dump 파일 생성

\#    neo4j-admin database dump <database\_name> --to-path=<path\_in\_container>

\#    Neo4j 5.x 에서는 '--name' 옵션 대신 바로 데이터베이스 이름을 사용.

log\_message "Executing: docker exec $NEO4J\_CONTAINER\_NAME neo4j-admin database dump $DATABASE\_NAME --to-path=$DUMP\_PATH\_IN\_CONTAINER"

docker exec "$NEO4J\_CONTAINER\_NAME" neo4j-admin database dump "$DATABASE\_NAME" --to-path="$DUMP\_PATH\_IN\_CONTAINER"

if [ $? -ne 0 ]; then

`    `log\_message "ERROR: Neo4j dump command failed inside container."

`    `exit 1

fi

log\_message "Dump created inside container: $DUMP\_PATH\_IN\_CONTAINER"

\# 2. 생성된 dump 파일을 로컬 호스트로 복사

log\_message "Copying dump file from container to host: $FINAL\_DUMP\_PATH"

docker cp "${NEO4J\_CONTAINER\_NAME}:${DUMP\_PATH\_IN\_CONTAINER}" "$FINAL\_DUMP\_PATH"

if [ $? -ne 0 ]; then

`    `log\_message "ERROR: Failed to copy dump file from container."

`    `# 컨테이너 내 임시 파일 삭제 시도 (실패해도 계속 진행)

`    `docker exec "$NEO4J\_CONTAINER\_NAME" rm "$DUMP\_PATH\_IN\_CONTAINER"

`    `exit 1

fi

\# 3. 컨테이너 내 임시 dump 파일 삭제

log\_message "Removing temporary dump file from container."

docker exec "$NEO4J\_CONTAINER\_NAME" rm "$DUMP\_PATH\_IN\_CONTAINER"

if [ $? -ne 0 ]; then

`    `log\_message "WARNING: Failed to remove temporary dump file from container. Manual cleanup might be needed."

fi

\# 4. (선택적) 오래된 백업 파일 삭제

if [ "$RETENTION\_DAYS" -gt 0 ]; then

`    `log\_message "Cleaning up old backups older than $RETENTION\_DAYS days in $BACKUP\_DIR..."

`    `find "$BACKUP\_DIR" -name "${DATABASE\_NAME}\_backup\_\*.dump" -type f -mtime +"$RETENTION\_DAYS" -exec rm -f {} \;

`    `log\_message "Old backup cleanup finished."

fi

log\_message "Neo4j backup successful: $FINAL\_DUMP\_PATH"

log\_message "----------------------------------------------------"

exit 0



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Bash

IGNORE\_WHEN\_COPYING\_END
## <a name="_hd2bvr7asns0"></a>**부록 8: [[tests/test\_context\_builder\_v11.py]] 예시**
`     `# tests/test\_context\_builder\_v11.py

import pytest

import json

import os

from unittest.mock import patch, MagicMock

\# 테스트 대상 모듈 임포트 (실제 경로에 맞게 수정 필요)

\# from scripts.context\_builder\_v11 import ContextBuilder, CTX\_TOKEN\_BUDGET\_DEFAULT

\# 프로젝트 루트 경로를 기준으로 상대 경로 설정 (필요시)

\# SCRIPT\_DIR = os.path.dirname(os.path.dirname(os.path.abspath(\_\_file\_\_)))

\# SCHEMAS\_DIR = os.path.join(SCRIPT\_DIR, "schemas")

\# # JSON Schema 로드 (예시, 실제 파일 경로 및 스키마 필요)

\# try:

\#     with open(os.path.join(SCHEMAS\_DIR, "context\_package\_v11.schema.json")) as f:

\#         context\_output\_schema = json.load(f)

\# except FileNotFoundError:

\#     context\_output\_schema = None # 스키마 파일이 없으면 테스트 스킵 또는 다른 처리


\# --- Mock Objects and Fixtures ---

@pytest.fixture

def mock\_neo4j\_driver():

`    `"""Neo4j 드라이버를 모킹합니다."""

`    `mock\_driver = MagicMock()

`    `# mock\_session.run().data() 등의 반환값 설정

`    `# 예: mock\_driver.session().run().data.return\_value = [{"character\_name": "Test Character"}]

`    `return mock\_driver

@pytest.fixture

def mock\_faiss\_index():

`    `"""FAISS 인덱스를 모킹합니다."""

`    `mock\_index = MagicMock()

`    `# mock\_index.search()... 등의 반환값 설정

`    `# 예: mock\_index.search.return\_value = (distances\_mock, ids\_mock, metadatas\_mock)

`    `return mock\_index

@pytest.fixture

def sample\_story\_bible\_data():

`    `"""테스트용 Story Bible 데이터 예시."""

`    `return {

`        `"metadata": {"title": "Test Novel", "CTX\_TOKEN\_BUDGET\_OVERRIDE": 10000},

`        `"characters": [{"graph\_id": "char\_001", "name": "Hero", "description": "The main protagonist."}],

`        `"world\_setting": {"magic\_system": "Mana-based"},

`        `# ... 기타 필요한 최소 데이터 ...

`    `}

@pytest.fixture

def mock\_context\_builder\_dependencies(mock\_neo4j\_driver, mock\_faiss\_index, sample\_story\_bible\_data, tmp\_path):

`    `"""ContextBuilder의 의존성을 모킹하고 기본 환경을 설정합니다."""

`    `# .env 파일 모킹 (필요시)

`    `# with patch.dict(os.environ, {"CTX\_TOKEN\_BUDGET": "12000"}):

`    `#     pass

`    `# Story Bible 파일 모킹

`    `project\_name = "TestProject"

`    `projects\_dir = tmp\_path / "projects"

`    `project\_dir = projects\_dir / project\_name

`    `project\_dir.mkdir(parents=True, exist\_ok=True)

`    `story\_bible\_path = project\_dir / "story\_bible\_v11.json"

`    `with open(story\_bible\_path, "w") as f:

`        `json.dump(sample\_story\_bible\_data, f)

`    `# ContextBuilder 인스턴스 생성에 필요한 mock 객체들

`    `# 실제 ContextBuilder 생성자 및 메소드 호출 방식에 맞춰 mock 설정

`    `# with patch("scripts.context\_builder\_v11.Neo4jDriver", return\_value=mock\_neo4j\_driver), \

`    `#      patch("scripts.context\_builder\_v11.FaissIndexLoader", return\_value=mock\_faiss\_index), \

`    `#      patch("scripts.context\_builder\_v11.load\_story\_bible", return\_value=sample\_story\_bible\_data):

`    `#     builder = ContextBuilder(project\_name=project\_name, projects\_base\_dir=str(projects\_dir))

`    `#     yield builder # 테스트 함수에서 사용하도록 builder 반환

`    `yield MagicMock() # 임시로 MagicMock 반환 (실제 ContextBuilder 임포트 후 수정)


\# --- Test Cases ---

@pytest.mark.skip(reason="ContextBuilder 모듈 및 실제 의존성 로직 구현 후 작성")

def test\_context\_builder\_initialization(mock\_context\_builder\_dependencies):

`    `"""ContextBuilder 초기화 테스트."""

`    `builder = mock\_context\_builder\_dependencies # fixture로부터 builder (또는 mock) 가져옴

`    `assert builder is not None

`    `# assert builder.project\_name == "TestProject"

`    `# assert builder.token\_budget == 10000 # Bible의 오버라이드 값 확인

@pytest.mark.skip(reason="Not fully implemented yet.")

def test\_build\_context\_simple\_scenario(mock\_context\_builder\_dependencies):

`    `"""간단한 시나리오에 대한 컨텍스트 생성 테스트."""

`    `builder = mock\_context\_builder\_dependencies

`    `episode\_id = "A1\_EP001"

`    `# Mock KG/RAG 반환값 설정

`    `# builder.neo4j\_driver.session().run().data.return\_value = [...]

`    `# builder.faiss\_index.search.return\_value = (...)

`    `# context = builder.build\_context\_for\_episode(episode\_id)

`    `context\_str = "This is a sample context." # 임시 결과

`    `assert isinstance(context\_str, str)

`    `assert len(context\_str) > 0

`    `# if context\_output\_schema:

`    `#     from jsonschema import validate

`    `#     # context가 JSON 객체로 반환된다면 스키마 검증

`    `#     # validate(instance=json.loads(context\_str), schema=context\_output\_schema)


@pytest.mark.skip(reason="Token budget logic not fully tested.")

def test\_context\_trimming\_when\_over\_budget(mock\_context\_builder\_dependencies):

`    `"""토큰 예산 초과 시 정보 잘라내기 로직 테스트."""

`    `# builder = mock\_context\_builder\_dependencies

`    `# builder.token\_budget = 50 # 매우 작은 예산으로 설정

`    `# 매우 긴 정보를 반환하도록 KG/RAG 모킹

`    `# ...

`    `# context = builder.build\_context\_for\_episode("A1\_EP002")

`    `# 여기서 context의 토큰 수를 계산하고, builder.token\_budget 이하인지 확인

`    `# (실제 토큰 계산 로직 필요, 예: tiktoken 라이브러리 사용)

`    `# num\_tokens = calculate\_tokens(context)

`    `# assert num\_tokens <= builder.token\_budget

`    `pass

@pytest.mark.skip(reason="Caching logic to be implemented and tested.")

def test\_context\_caching\_logic(mock\_context\_builder\_dependencies, tmp\_path):

`    `"""컨텍스트 캐싱 로직 테스트."""

`    `# builder = mock\_context\_builder\_dependencies

`    `# builder.enable\_cache = True

`    `# builder.cache\_dir = tmp\_path / "cache" # 캐시 디렉토리 설정

`    `episode\_id = "A1\_EP003"

`    `# 첫 번째 호출: 실제 빌드 로직 수행 (내부적으로 KG/RAG 호출 mock 필요)

`    `# context1 = builder.build\_context\_for\_episode(episode\_id)

`    `# 두 번째 호출: 캐시에서 로드되어야 함 (KG/RAG mock이 다시 호출되지 않음을 확인)

`    `# with patch.object(builder.neo4j\_driver.session(), 'run', side\_effect=AssertionError("DB should not be called")) as mock\_db\_run, \

`    `#      patch.object(builder.faiss\_index, 'search', side\_effect=AssertionError("FAISS should not be called")) as mock\_faiss\_search:

`    `#     context2 = builder.build\_context\_for\_episode(episode\_id)

`    `# assert context1 == context2

`    `# mock\_db\_run.assert\_not\_called() # 고급: 첫 호출 이후 DB 접근 없었는지 확인

`    `# mock\_faiss\_search.assert\_not\_called()

`    `pass

\# 추가 테스트 케이스:

\# - 특정 정보 소스(KG, RAG, Bible) 부재 시 처리

\# - 다양한 입력 파라미터 조합에 대한 테스트

\# - 재시도 시 컨텍스트에 실패 정보 추가 여부 테스트



## <a name="_eibyriftis8i"></a>**부록 9: [[tests/performance/default\_load\_test.js]] 예시**
`     `// tests/performance/default\_load\_test.js

import http from 'k6/http';

import { check, sleep, group, Trend } from 'k6'; // Trend 추가

import { SharedArray } from 'k6/data'; // 외부 데이터 로딩용 (선택적)

// --- Configuration ---

const API\_BASE\_URL = \_\_ENV.API\_BASE\_URL || 'http://localhost:8000/api/v1'; // API 서버 주소

const PROJECT\_NAME\_FOR\_TEST = \_\_ENV.PROJECT\_NAME || "PerfTestProject";

const EPISODES\_TO\_GENERATE = parseInt(\_\_ENV.EPISODES\_TO\_GENERATE || "3");

// 사용자 시나리오별 지연 시간 측정을 위한 Trend 객체

const generateEpisodeLatency = new Trend('generate\_episode\_latency', true);

const contextBuilderLatency = new Trend('context\_builder\_latency', true); // 가상

export const options = {

`  `// 시나리오 정의 (VU: Virtual User)

`  `scenarios: {

`    `// 시나리오 1: 일반적인 에피소드 생성 부하

`    `generate\_episodes\_load: {

`      `executor: 'ramping-vus', // 점진적으로 VU 증가

`      `startVUs: 1,

`      `stages: [

`        `{ duration: '30s', target: 5 },  // 30초 동안 VU 5명까지 증가

`        `{ duration: '1m', target: 5 },   // VU 5명으로 1분간 유지

`        `{ duration: '30s', target: 0 },  // 30초 동안 VU 0명으로 감소

`      `],

`      `gracefulRampDown: '10s', // 테스트 종료 시 부드럽게 VU 감소

`      `exec: 'generateSingleEpisodeScenario', // 이 시나리오에서 실행할 함수

`    `},

`    `// 시나리오 2: 특정 고부하 API 스트레스 테스트 (선택적)

`    `// stress\_context\_api: {

`    `//   executor: 'constant-vus',

`    `//   vus: 10,

`    `//   duration: '30s',

`    `//   exec: 'callContextBuilderDirectly', // 가상의 직접 호출 함수

`    `//   gracefulStop: '5s',

`    `// }

`  `},

`  `// 전역 성능 목표 (Thresholds)

`  `thresholds: {

`    `http\_req\_failed: ['rate<0.02'],              // HTTP 실패율 2% 미만

`    `http\_req\_duration: ['p(95)<15000'],          // 전체 HTTP 요청의 95%가 15초 이내

`    `'generate\_episode\_latency{scenario:generate\_episodes\_load}': ['p(90)<20000'], // 에피소드 생성 90%가 20초 이내

`    `// 'context\_builder\_latency{scenario:stress\_context\_api}': ['avg<1000'], // 컨텍스트 빌더 평균 응답 1초 이내

`    `checks: ['rate>0.98'],                       // 모든 check 성공률 98% 이상

`  `},

`  `// 전역 태그 (리포팅 시 구분용)

`  `tags: {

`    `test\_type: 'load\_test',

`    `system\_version: \_\_ENV.SYSTEM\_VERSION || 'v11.2.0', // CI에서 주입 가능

`  `},

};

// --- Helper Functions (선택적) ---

// 테스트 데이터 로딩 (예: 에피소드 ID 목록)

// const episodeIds = new SharedArray('episodeIDs', function () {

//   // return JSON.parse(open('./data/episode\_ids\_for\_test.json'));

//   let ids = [];

//   for (let i = 1; i <= EPISODES\_TO\_GENERATE; i++) {

//     ids.push(`A1\_EP${String(i).padStart(3, '0')}`);

//   }

//   return ids;

// });


// --- Test Execution Functions (Scenarios) ---

// 시나리오 1: 단일 에피소드 생성 요청

export function generateSingleEpisodeScenario() {

`  `group('Generate Single Episode Flow', function () {

`    `const episodeNum = (\_\_VU \* options.scenarios.generate\_episodes\_load.stages.length + \_\_ITER) % EPISODES\_TO\_GENERATE + 1;

`    `const episodeId = `A1\_EP${String(episodeNum).padStart(3, '0')}`;

`    `const payload = JSON.stringify({

`      `project\_name: PROJECT\_NAME\_FOR\_TEST,

`      `episode\_id: episodeId,

`      `use\_kg: true,

`      `with\_editor: true,

`      `// ... 기타 필요한 파라미터 ...

`    `});

`    `const params = {

`      `headers: {

`        `'Content-Type': 'application/json',

`        `'X-Trace-Id': `k6-${\_\_VU}-${Date.now()}`, // 각 요청에 트레이스 ID 추가

`      `},

`      `timeout: '60s', // 개별 요청 타임아웃 (60초)

`    `};

`    `// 실제로는 GameChanger의 에피소드 생성 API 엔드포인트 호출

`    `// 여기서는 가상의 엔드포인트 '/generate\_episode' 사용

`    `const res = http.post(`${API\_BASE\_URL}/generate\_episode`, payload, params);

`    `// 응답 시간 기록

`    `generateEpisodeLatency.add(res.timings.duration);

`    `// 응답 검증 (Checks)

`    `check(res, {

`      `'status is 200 (episode generated)': (r) => r.status === 200,

`      `'response body contains episode\_id': (r) => {

`        `try {

`          `return r.json('episode\_id') === episodeId;

`        `} catch (e) { return false; }

`      `},

`      `'response time is acceptable': (r) => r.timings.duration < 30000, // 30초 이내

`    `}) || errorRate.add(1); // 체크 실패 시 에러율 증가 (별도 Metric 필요 시)

`    `// 요청 간 약간의 지연 (Think time)

`    `sleep(Math.random() \* 3 + 1); // 1~4초 사이 랜덤 대기

`  `});

}

// 시나리오 2: 컨텍스트 빌더 직접 호출 (가상)

export function callContextBuilderDirectly() {

`  `group('Context Builder Stress Test', function () {

`    `const res = http.get(`${API\_BASE\_URL}/debug/build\_context?episode\_id=A2\_EP010&project\_name=${PROJECT\_NAME\_FOR\_TEST}`);

`    `contextBuilderLatency.add(res.timings.duration);

`    `check(res, { 'status is 200 (context built)': (r) => r.status === 200 });

`    `sleep(0.5);

`  `});

}

// --- Setup and Teardown (선택적) ---

export function setup() {

`  `// 테스트 시작 전 초기화 작업 (예: 테스트 프로젝트 생성, 인증 토큰 획득)

`  `console.log('k6 load test setup: Initializing test environment...');

`  `// const loginRes = http.post(`${API\_BASE\_URL}/auth/login`, { user: 'test', pass: 'test' });

`  `// const authToken = loginRes.json('token');

`  `// return { authToken: authToken }; // 다음 단계(VU 실행)로 데이터 전달

`  `// 만약 setup에서 프로젝트 생성이 오래 걸린다면,

`  `// 해당 로직은 CI 파이프라인의 별도 스텝으로 분리하는 것이 나을 수 있음.

`  `// 여기서는 간단히 로그만 남김.

`  `// 실제 GameChanger는 CLI 기반이므로, 이 setup/teardown은

`  `// API 서버를 별도로 구축했을 때 더 유용합니다.

`  `// CLI 부하 테스트는 k6보다 다른 도구(예: 직접 스크립트 루프)가 적합할 수 있습니다.

`  `// 이 k6 스크립트는 GameChanger가 HTTP API를 제공한다고 가정합니다.

}

export function teardown(data) {

`  `// 테스트 종료 후 정리 작업 (예: 테스트 데이터 삭제)

`  `console.log('k6 load test teardown: Cleaning up test environment...');

}

// (별도 Metric 정의가 필요하면 여기에 추가)

// import { Rate } from 'k6/metrics';

// export const errorRate = new Rate('errors');



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). JavaScript

IGNORE\_WHEN\_COPYING\_END
## <a name="_d6czq374q345"></a>**부록 10: [[Makefile]] (부하 테스트 부분) 예시**
`     `# Makefile (일부 발췌)

\# --- Docker ---

DOCKER\_COMPOSE = docker-compose

NEO4J\_SERVICE\_NAME = neo4j # docker-compose.yml 내 Neo4j 서비스 이름

WORKER\_IMAGE\_NAME = gamechanger-worker-v11 # 빌드할 워커 이미지 이름

WORKER\_IMAGE\_TAG ?= latest # 태그 기본값, 외부에서 오버라이드 가능 (예: make test-perf WORKER\_IMAGE\_TAG=v11.2.0)

\# --- k6 Performance Testing ---

K6\_SCRIPT\_DIR = tests/performance

K6\_DEFAULT\_SCRIPT = default\_load\_test.js

K6\_DOCKER\_IMAGE = ghcr.io/grafana/k6:latest # k6 공식 Docker 이미지

\# CI 환경 여부 (GitHub Actions 등에서 CI=true로 설정)

CI ?= false

.PHONY: help build-worker start-neo4j stop-neo4j test-perf test-perf-ci

help:

`	`@echo "Available commands:"

`	`@echo "  build-worker           Build the GameChanger worker Docker image."

`	`@echo "  start-neo4j            Start Neo4j service using Docker Compose."

`	`@echo "  stop-neo4j             Stop Neo4j service."

`	`@echo "  test-perf              Run k6 performance test locally against a running application."

`	`@echo "  test-perf-ci           Run k6 performance test in CI mode (expects services to be set up by CI workflow)."


build-worker:

`	`@echo "Building GameChanger worker Docker image: $(WORKER\_IMAGE\_NAME):$(WORKER\_IMAGE\_TAG)..."

`	`docker build -t $(WORKER\_IMAGE\_NAME):$(WORKER\_IMAGE\_TAG) .

start-neo4j:

`	`@echo "Starting Neo4j service..."

`	`$(DOCKER\_COMPOSE) up -d $(NEO4J\_SERVICE\_NAME)

`	`@echo "Waiting for Neo4j to be healthy..."

`	`@# 간단한 health check 대기 (실제로는 더 견고한 방법 사용 권장)

`	`@timeout 60s bash -c 'while ! curl -s -I http://localhost:7474 | grep -q "200 OK"; do sleep 5; done' || \

`		`(echo "Neo4j did not become healthy in time." && exit 1)

`	`@echo "Neo4j is up and running."

stop-neo4j:

`	`@echo "Stopping Neo4j service..."

`	`$(DOCKER\_COMPOSE) down

\# 로컬에서 성능 테스트 실행 (애플리케이션이 별도로 실행 중이라고 가정)

\# 예: python scripts/api\_server\_v11.py 실행 후 이 명령어 호출

test-perf:

`	`@echo "Running k6 performance test locally..."

`	`@echo "Ensure your GameChanger application (API server) is running and accessible at $(API\_BASE\_URL)."

`	`@echo "Using k6 script: $(K6\_SCRIPT\_DIR)/$(K6\_DEFAULT\_SCRIPT)"

`	`docker run --rm -i --network="host" \

`		`-v $(shell pwd)/$(K6\_SCRIPT\_DIR):/scripts \

`		`-e API\_BASE\_URL=$(API\_BASE\_URL) \

`		`-e PROJECT\_NAME=$(PROJECT\_NAME) \

`		`-e EPISODES\_TO\_GENERATE=$(EPISODES\_TO\_GENERATE) \

`		`$(K6\_DOCKER\_IMAGE) run /scripts/$(K6\_DEFAULT\_SCRIPT)

\# CI 환경에서 성능 테스트 실행 (GitHub Actions 워크플로에서 호출)

\# CI 워크플로는 Neo4j 및 테스트 대상 애플리케이션(워커)을 별도로 설정해야 함.

test-perf-ci:

`	`@echo "Running k6 performance test for CI..."

`	`@echo "This target assumes Neo4j and the application worker are already running in the CI environment."

`	`@echo "API\_BASE\_URL for CI: $(API\_BASE\_URL\_CI)"

`	`docker run --rm -i \

`		`--network="host" `# CI 환경의 네트워크 설정에 따라 변경될 수 있음` \

`		`-v $(shell pwd)/$(K6\_SCRIPT\_DIR):/scripts \

`		`-e API\_BASE\_URL=$(API\_BASE\_URL\_CI) \

`		`-e PROJECT\_NAME=$(PROJECT\_NAME\_CI) \

`		`-e EPISODES\_TO\_GENERATE=$(EPISODES\_TO\_GENERATE\_CI) \

`		`-e SYSTEM\_VERSION=$(WORKER\_IMAGE\_TAG) \

`		`-e K6\_PROMETHEUS\_RW\_SERVER\_URL=$(K6\_PROMETHEUS\_RW\_SERVER\_URL) `# 선택적: CI에서 설정된 경우` \

`		`-e K6\_OUT=influxdb=http://myinfluxdb:8086/k6 `# 선택적: 결과 DB` \

`		`$(K6\_DOCKER\_IMAGE) run /scripts/$(K6\_DEFAULT\_SCRIPT) \

`		`--summary-export=/scripts/k6\_summary\_$(WORKER\_IMAGE\_TAG).json `# 결과를 스크립트 폴더(볼륨 마운트된)에 저장`

\# 환경 변수 기본값 (로컬 테스트용, 외부에서 오버라이드 가능)

API\_BASE\_URL ?= http://localhost:8000/api/v1

PROJECT\_NAME ?= PerfTestLocal

EPISODES\_TO\_GENERATE ?= 2

\# CI용 환경 변수 (CI 시스템에서 이 값들을 설정해야 함)

API\_BASE\_URL\_CI ?= http://localhost:8001/api/v1 # CI 환경의 앱 주소

PROJECT\_NAME\_CI ?= PerfTestCI

EPISODES\_TO\_GENERATE\_CI ?= 5

K6\_PROMETHEUS\_RW\_SERVER\_URL ?= ""



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Makefile

IGNORE\_WHEN\_COPYING\_END
## <a name="_3n0bu08tzqds"></a>**부록 11: 로그 예시 (내용은 이전과 동일하나, 참조용으로 유지)**
- [11.1. 성공 로그 일부 (구조화된 JSON 로그 예시) 보기](#111-성공-로그-일부-구조화된-json-로그-예시---powershell-출력은-가독성-위해-포맷될-수-있음)
- [11.2. 실패 및 재시도 로그 예시 (일부, 구조화 JSON) 보기](#112-실패-및-재시도-로그-예시-일부-구조화-json)
## <a name="_rl2gkj2x6mue"></a>**부록 12: [[docs/quickstart.md]] 전문**
`     `# Project GameChanger v11 - Quick Start Guide

This guide helps you get a sample pilot project running quickly using Project GameChanger v11.

The goal is to generate a few episodes and verify the basic pipeline.

\## Prerequisites

1\.  \*\*Git:\*\* Install from [git-scm.com/downloads](https://git-scm.com/downloads).

2\.  \*\*Python:\*\* Version 3.10 or higher. Install from [python.org/downloads](https://python.org/downloads/).

`    `\*   Ensure Python and pip are added to your system's PATH.

3\.  \*\*Docker Desktop:\*\* Required for running Neo4j. Install from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).

`    `\*   Ensure Docker Desktop is running before proceeding.

4\.  \*\*Shell:\*\* PowerShell (Windows) or a bash-compatible shell (Linux/macOS).

\## Steps

\### 1. Clone the Repository

Open your terminal or PowerShell and run:

\```bash

git clone https://github.com/your\_repo/project\_gamechanger.git

cd project\_gamechanger



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Markdown

IGNORE\_WHEN\_COPYING\_END

(Replace https://github.com/your\_repo/project\_gamechanger.git with the actual repository URL)
### <a name="_1wpl92l959lj"></a>**2. Set Up Python Virtual Environment & Install Dependencies**
`     `# Create a virtual environment

python -m venv .venv

\# Activate the virtual environment

\# On Windows (PowerShell):

.\.venv\Scripts\Activate.ps1

\# On Linux/macOS (bash/zsh):

\# source .venv/bin/activate

\# Install required Python packages

pip install -r requirements.txt

pip install pytest # For running tests (optional for quick start)



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Bash

IGNORE\_WHEN\_COPYING\_END
### <a name="_bhqyxl2w5wui"></a>**3. Configure Environment Variables**
Copy the sample environment file and edit it with your actual API keys and passwords.

`     `# On Windows (PowerShell):

copy .env.sample .env

notepad .env # Opens .env in Notepad for editing

\# On Linux/macOS (bash/zsh):

\# cp .env.sample .env

\# nano .env # Opens .env in nano editor

\# --- Key fields to edit in .env ---

\# OPENAI\_API\_KEY="sk-your\_openai\_api\_key\_here"

\# NEO4J\_PASSWORD="your\_chosen\_neo4j\_password" # This password will be used by Neo4j container



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Bash

IGNORE\_WHEN\_COPYING\_END

**Important:** The NEO4J\_PASSWORD in .env **must match** the password you intend for Neo4j to use. The docker-compose.yml reads this (or a default) for Neo4j's NEO4J\_AUTH setting.
### <a name="_2rm30qz3dc4w"></a>**4. Start Neo4j Database using Docker Compose**
In the project root directory (where docker-compose.yml is located):

`     `docker-compose up -d neo4j



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Bash

IGNORE\_WHEN\_COPYING\_END

- This command starts the Neo4j service in detached mode (-d).
- Wait about 1-2 minutes for Neo4j to fully initialize. You can check its logs: docker-compose logs -f neo4j.
- Once running, you can access the Neo4j Browser at http://localhost:7474.
  - Connect with:
    - Connect URL: bolt://localhost:7687 (usually default)
    - Username: neo4j
    - Password: The NEO4J\_PASSWORD you set in your .env file (or please\_change\_this\_default\_password if not set and docker-compose.yml used its default).


### <a name="_pgls7blbfgaj"></a>**5. Run the Pilot Script (Using Sample Project Data)**
This command will initialize a new project but use a pre-configured sample Story Bible to generate a few episodes. This allows for a quicker first run without needing to create all initial data manually.

`     `# Ensure your virtual environment (.venv) is still active.

\# This example uses PowerShell syntax.

\# Generate a unique Trace ID for this run

$env:GC\_TRACE\_ID = [guid]::NewGuid().ToString()

Write-Host "Using Trace ID: $env:GC\_TRACE\_ID"

\# Run the pilot script for 3 episodes using a sample template

\# The 'MyQuickStartPilot' project will be created if it doesn't exist.

\# The '--template-override' flag tells story\_bible\_init\_v11.py (called by run\_pilot)

\# to use the specified sample file instead of the default empty template.

\# (This assumes run\_pilot\_v11.py or story\_bible\_init\_v11.py supports --template-override)

python scripts/run\_pilot\_v11.py --project "MyQuickStartPilot" --num-episodes 3 --use-kg --with-editor --use-rl-scoring --template-override "examples/demo\_project/story\_bible\_sample\_v11.json"

\# If --template-override is not directly supported by run\_pilot\_v11.py,

\# you might need to initialize the project first:

\# python scripts/story\_bible\_init\_v11.py --project "MyQuickStartPilot" --template-override "examples/demo\_project/story\_bible\_sample\_v11.json"

\# python scripts/run\_pilot\_v11.py --project "MyQuickStartPilot" --num-episodes 3 --use-kg --with-editor --use-rl-scoring



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Powershell

IGNORE\_WHEN\_COPYING\_END

*(**Note:** The run\_pilot\_v11.ps1 or run\_pilot\_v11.py script needs to be adapted to correctly handle the --template-override logic, potentially by passing it down to story\_bible\_init\_v11.py.)*
### <a name="_y5n9s7kmyoq4"></a>**6. Check Results**
After the script finishes:

- **Generated Episodes:** Look in projects/MyQuickStartPilot/episodes/ for the generated .txt or .md files.
- **Updated Story Bible:** Check projects/MyQuickStartPilot/story\_bible\_v11.json. It should now contain logs for the generated episodes.
- **Neo4j Data:** Open Neo4j Browser (http://localhost:7474) and run Cypher queries like MATCH (n) RETURN n LIMIT 25 to see if data (nodes, relationships) was created.
- **Logs:** Application logs can be found in logs/app/. Look for files related to MyQuickStartPilot or the GC\_TRACE\_ID.
### <a name="_orvb85eh4wn2"></a>**7. (Optional) Run Automated Tests**
If you installed pytest:

`     `pytest



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Bash

IGNORE\_WHEN\_COPYING\_END

This will run all automated tests in the tests/ directory.
### <a name="_mua3tte5y1go"></a>**8. Stop Neo4j**
When you are done:

`     `docker-compose down



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Bash

IGNORE\_WHEN\_COPYING\_END

This stops and removes the Neo4j container. Your Neo4j data will persist in the Docker volume (gamechanger\_neo4j\_data\_v11) unless you explicitly remove the volume.

-----
Congratulations! You have successfully run a pilot for Project GameChanger v11.
For more details, refer to the full Master Guide.

`     `## \*\*부록 13: `[[examples/demo\_project/]]` 구조 및 설명\*\*



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487).

IGNORE\_WHEN\_COPYING\_END

examples/
└── demo\_project/
├── README.md # (This file) 설명 및 사용 방법.
|
├── story\_bible\_sample\_v11.json # 3~5화 분량의 핵심 설정, 캐릭터, 초기 아크 개요가 포함된 Story Bible.
| # Neo4j/FAISS 초기화의 기반 데이터로 사용 가능.
|
├── neo4j\_init\_data/ # Neo4j 초기 데이터 로드용 파일들 (선택적).
│ ├── 00\_constraints\_indexes.cypher # graph\_id 고유 제약 조건 및 인덱스 생성 Cypher.
│ ├── 01\_characters\_sample.cypher # story\_bible\_sample\_v11.json 기반 캐릭터 노드 생성 Cypher.
│ ├── 02\_locations\_sample.cypher # 샘플 지역 노드 생성 Cypher.
│ └── (기타 필요한 엔티티 및 관계 생성 Cypher 파일들)
|
├── faiss\_sample\_data/ # FAISS 인덱스 샘플 및 관련 데이터 (선택적).
│ ├── sample\_texts\_for\_faiss.jsonl # FAISS에 인덱싱할 텍스트 데이터 (줄당 JSON 객체).
│ # 각 객체는 text와 metadata (graph\_id 등) 포함.
│ ├── (Optional) prebuilt\_sample.faiss # 미리 빌드된 FAISS 인덱스 파일 (테스트 시간 단축용).
│ └── (Optional) prebuilt\_sample\_meta.pkl # 위 인덱스 파일의 메타데이터.
|
└── sample\_run\_config.yaml # (선택적) 이 샘플 프로젝트를 실행하기 위한
\# run\_pilot\_v11.py 또는 run\_full\_pipeline\_v11.py 용 설정 파일 예시.
\# (예: 사용할 LLM 모델, 특정 기능 플래그 등)

`     `\*\*`README.md` (in `examples/demo\_project/`) 내용 예시:\*\*

\```markdown

\# Demo Project for GameChanger v11

This directory contains sample data to quickly get started with Project GameChanger v11 and test its core functionalities.

\## Contents

\-   \*\*`story\_bible\_sample\_v11.json`\*\*:

`    `A minimal but functional Story Bible JSON file. It includes:

`    `-   Basic metadata for a fictional story.

`    `-   1-2 fully defined main characters.

`    `-   1 sample location.

`    `-   An overview for the first story arc (e.g., "A1: The Awakening").

`    `-   1-2 planned key plot points for the first arc.

`    `This file can be used with `story\_bible\_init\_v11.py --template-override path/to/this/file.json`

`    `or referenced by `run\_pilot\_v11.py` to initialize a new project with this data.

\-   \*\*`neo4j\_init\_data/`\*\*:

`    `Contains Cypher scripts to populate Neo4j with data corresponding to `story\_bible\_sample\_v11.json`.

`    `-   `00\_constraints\_indexes.cypher`: Essential for creating unique `graph\_id` constraints and indexes for performance. Run this first.

`    `-   `01\_characters\_sample.cypher`, `02\_locations\_sample.cypher`, etc.: Create sample nodes and relationships.

`    `These can be executed against your Neo4j instance (e.g., via Neo4j Browser or `cypher-shell`) after starting the Neo4j service.

`    `Alternatively, `graph\_sync\_v11.py --project DemoProject --init-schema` (for constraints) and then

`    ``graph\_sync\_v11.py --project DemoProject --source-file examples/demo\_project/story\_bible\_sample\_v11.json`

`    `can achieve a similar result by syncing the sample Bible to an empty graph.

\-   \*\*`faiss\_sample\_data/`\*\*:

`    `Contains sample text data that can be used to build a FAISS index for RAG.

`    `-   `sample\_texts\_for\_faiss.jsonl`: Each line is a JSON object like `{"id": "char\_001\_desc", "text": "Detailed description of character 001...", "metadata": {"graph\_id": "char\_001", "type": "character\_description"}}`.

`    `-   A script (e.g., `scripts/build\_faiss\_index\_v11.py` - not part of this sample, but a conceptual V11 utility) would read this `jsonl` file, generate embeddings, and save the FAISS index to `memory/faiss\_index/DemoProject/`.

`    `-   Pre-built `.faiss` and `.pkl` files are optional and can speed up testing if provided.

\-   \*\*`sample\_run\_config.yaml`\*\* (Conceptual):

`    `If the main execution scripts support a YAML configuration file, this would provide an example for running this demo project.

`    ````yaml

`    `# project\_name: DemoProjectFromSample

`    `# num\_episodes\_to\_generate: 3

`    `# use\_knowledge\_graph: true

`    `# use\_editor\_agent: true

`    `# llm\_settings:

`    `#   draft\_generator\_model: "gpt-3.5-turbo" # Cheaper model for quick test

`    `#   editor\_agent\_model: "gpt-3.5-turbo"

`    `# context\_builder\_token\_budget: 8000

`    ````

\## How to Use

1\.  \*\*Follow the main `docs/quickstart.md` guide.\*\*

2\.  When initializing the project or running the pilot, use the `--template-override examples/demo\_project/story\_bible\_sample\_v11.json` option if your script supports it.

`    `Example:

`    ````powershell

`    `python scripts/run\_pilot\_v11.py --project "MyDemoRun" --num-episodes 2 --template-override "examples/demo\_project/story\_bible\_sample\_v11.json" --use-kg

`    ````

3\.  (Optional) If providing Neo4j Cypher scripts, manually execute them in Neo4j Browser or using `cypher-shell` after starting Neo4j and before running the main GameChanger scripts that depend on KG data. Start with `00\_constraints\_indexes.cypher`.

4\.  (Optional) If providing FAISS sample texts, you would need a separate script to build the FAISS index from `sample\_texts\_for\_faiss.jsonl` and place it in the correct `memory/faiss\_index/MyDemoRun/` directory.

This demo project aims to provide a tangible starting point for understanding and testing Project GameChanger v11.



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487).

IGNORE\_WHEN\_COPYING\_END
## <a name="_hboie96w2nac"></a>**부록 14: GitHub Actions 워크플로 예시 전문**
`     `# .github/workflows/main\_ci\_cd.yml

name: GameChanger CI/CD Pipeline

on:

`  `push:

`    `branches: [ main, develop ]

`    `tags: [ 'v\*' ] # Example: v11.2.0, v11.2.1-alpha

`  `pull\_request:

`    `branches: [ main ] # Run on PRs targeting main

env:

`  `PYTHON\_VERSION: '3.10'

`  `# Docker Image Naming (GitHub Packages: ghcr.io/OWNER/REPO/IMAGE\_NAME)

`  `# Ensure github.repository\_owner is lowercase for ghcr.io if needed, or use a static name.

`  `DOCKER\_IMAGE\_NAME\_BASE: gamechanger-worker # Base name for the image

`  `# For ghcr.io, it's often ghcr.io/$(echo ${{ github.repository\_owner }} | tr '[:upper:]' '[:lower:]')/${{ github.event.repository.name }}

`  `# Simpler static example:

`  `DOCKER\_REGISTRY: ghcr.io

`  `DOCKER\_IMAGE\_OWNER: ${{ github.repository\_owner }} # Keep original case for display/logic

`  `# Final image name will be constructed later

jobs:

`  `lint-and-test:

`    `name: Lint, Schema Validation & Unit Tests

`    `runs-on: ubuntu-latest

`    `steps:

`      `- name: Checkout code

`        `uses: actions/checkout@v4

`      `- name: Set up Python ${{ env.PYTHON\_VERSION }}

`        `uses: actions/setup-python@v4

`        `with:

`          `python-version: ${{ env.PYTHON\_VERSION }}

`          `cache: 'pip' # Cache pip dependencies

`      `- name: Install dependencies

`        `run: |

`          `python -m pip install --upgrade pip

`          `pip install -r requirements.txt

`          `pip install pytest pytest-cov flake8 jsonschema ajv-cli # Testing & linting tools

`      `- name: Lint with Flake8

`        `run: |

`          `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

`          `flake8 . --count --exit-zero --max-complexity=12 --max-line-length=119 --statistics

`      `- name: Validate JSON Schemas (using ajv-cli)

`        `run: |

`          `echo "Validating JSON Schemas in ./schemas directory..."

`          `# Example: Validate all \*.schema.json files. Fails workflow if any schema is invalid.

`          `# Ensure your schemas are self-contained or correctly reference $id for external $refs.

`          `# For more complex validation (e.g., against data files), a custom script might be needed.

`          `find ./schemas -name '\*.schema.json' -print -exec ajv validate -s {} --valid \;

`          `# If ajv is not found or this fails, consider a Python script using jsonschema library.

`      `- name: Run Pytest (Unit & Integration Tests)

`        `run: |

`          `pytest -v --cov=scripts --cov-report=xml --cov-report=term-missing

`          `# -v for verbose output

`          `# --cov for coverage, reporting to xml (for Codecov/SonarQube) and terminal

`      `- name: Upload coverage reports to Codecov

`        `uses: codecov/codecov-action@v3

`        `with:

`          `token: ${{ secrets.CODECOV\_TOKEN }} # Optional: for private repos

`          `files: ./coverage.xml # Coverage file generated by pytest-cov

`          `fail\_ci\_if\_error: true # Optional

`  `build-and-push-docker:

`    `name: Build & Push Docker Image

`    `needs: lint-and-test # Run only if lint-and-test job succeeds

`    `# Run on push to main/develop or on version tags

`    `if: github.event\_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop' || startsWith(github.ref, 'refs/tags/'))

`    `runs-on: ubuntu-latest

`    `permissions:

`      `contents: read

`      `packages: write # Needed to push to GitHub Packages (ghcr.io)

`    `steps:

`      `- name: Checkout code

`        `uses: actions/checkout@v4

`      `- name: Set up Docker Buildx

`        `uses: docker/setup-buildx-action@v3

`      `- name: Log in to GitHub Container Registry

`        `uses: docker/login-action@v3

`        `with:

`          `registry: ${{ env.DOCKER\_REGISTRY }}

`          `username: ${{ github.actor }}

`          `password: ${{ secrets.GITHUB\_TOKEN }}

`      `- name: Determine Image Tags

`        `id: meta

`        `run: |

`          `IMAGE\_NAME="${{ env.DOCKER\_REGISTRY }}/$(echo ${{ env.DOCKER\_IMAGE\_OWNER }} | tr '[:upper:]' '[:lower:]')/${{ env.DOCKER\_IMAGE\_NAME\_BASE }}"

`          `TAGS=""

`          `# SHA tag

`          `SHA\_TAG="${IMAGE\_NAME}:${{ github.sha }}"

`          `TAGS="$SHA\_TAG"

`          `# Latest tag for main branch

`          `if [ "${{ github.ref }}" == "refs/heads/main" ]; then

`            `TAGS="$TAGS,${IMAGE\_NAME}:latest"

`          `fi

`          `# Develop tag for develop branch

`          `if [ "${{ github.ref }}" == "refs/heads/develop" ]; then

`            `TAGS="$TAGS,${IMAGE\_NAME}:develop"

`          `fi

`          `# Version tag if git ref is a tag

`          `if [[ "${{ github.ref }}" == refs/tags/v\* ]]; then

`            `VERSION\_TAG=$(echo ${{ github.ref }} | sed 's/refs\/tags\///')

`            `TAGS="$TAGS,${IMAGE\_NAME}:${VERSION\_TAG}"

`          `fi

`          `echo "DOCKER\_IMAGE\_NAME\_FULL=${IMAGE\_NAME}" >> $GITHUB\_ENV

`          `echo "DOCKER\_IMAGE\_TAGS=${TAGS}" >> $GITHUB\_ENV

`          `echo "Determined tags: ${TAGS}"

`      `- name: Build and push Docker image

`        `uses: docker/build-push-action@v5

`        `with:

`          `context: .

`          `file: ./Dockerfile

`          `push: true

`          `tags: ${{ env.DOCKER\_IMAGE\_TAGS }}

`          `cache-from: type=gha

`          `cache-to: type=gha,mode=max

`          `# build-args: | # Optional build arguments

`          `#   SOME\_BUILD\_ARG=value

`  `# Optional: Performance Test Job (using k6)

`  `performance-test-k6:

`    `name: k6 Performance Test

`    `needs: build-and-push-docker # Run after Docker image is built and pushed

`    `# Run only on push to main or version tags (not on develop to save resources)

`    `if: github.event\_name == 'push' && (github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/'))

`    `runs-on: ubuntu-latest

`    `env:

`      `# Use the image built in the previous job

`      `TEST\_DOCKER\_IMAGE: ${{ env.DOCKER\_IMAGE\_NAME\_FULL }}:${{ github.sha }}

`      `# Neo4j test instance configuration (example)

`      `NEO4J\_TEST\_CONTAINER\_NAME: gamechanger\_neo4j\_k6test

`      `NEO4J\_TEST\_PASSWORD: k6testpassword

`      `# API base URL for the application started by this job

`      `APP\_API\_BASE\_URL: http://localhost:8001/api/v1 # Example port

`      `K6\_SCRIPT\_PATH: tests/performance/default\_load\_test.js

`    `services: # Optional: Spin up dependent services like a test Neo4j

`      `neo4j-for-k6test:

`        `image: neo4j:5-alpine

`        `# container\_name: ${{ env.NEO4J\_TEST\_CONTAINER\_NAME }} # Service name acts as hostname

`        `ports:

`          `- 7475:7474 # Use different host port to avoid conflict if local Neo4j is running

`          `- 7689:7687

`        `environment:

`          `NEO4J\_AUTH: neo4j/${{ env.NEO4J\_TEST\_PASSWORD }}

`        `options: >- # Healthcheck for service readiness

`          `--health-cmd "wget --quiet --tries=1 --spider http://localhost:7474 || exit 1"

`          `--health-interval 10s

`          `--health-timeout 5s

`          `--health-retries 5

`    `steps:

`      `- name: Checkout code (for k6 scripts)

`        `uses: actions/checkout@v4

`      `- name: Start Application for Test (using the built Docker image)

`        `run: |

`          `echo "Starting application container: ${{ env.TEST\_DOCKER\_IMAGE }}"

`          `docker run -d --name gamechanger\_app\_k6test \

`            `--network="host" `# Or use Docker bridge network and service name 'neo4j-for-k6test:7687'` \

`            `-e NEO4J\_URI="bolt://localhost:7689" `# Points to the service 'neo4j-for-k6test' host port` \

`            `-e NEO4J\_USER="neo4j" \

`            `-e NEO4J\_PASSWORD="${{ env.NEO4J\_TEST\_PASSWORD }}" \

`            `-e API\_PORT=8001 `# Port the app inside container listens on` \

`            `-p 8001:8001 `# Map host port to container port` \

`            `${{ env.TEST\_DOCKER\_IMAGE }} \

`            `python scripts/api\_server\_v11.py `# Assume there's an API server script`

`          `echo "Waiting for application to start..."

`          `sleep 20 # Adjust as needed, or implement a proper health check for the app

`      `- name: Run k6 load test

`        `uses: grafana/k6-action@v0.3.1 # Official k6 GitHub Action

`        `with:

`          `filename: ${{ env.K6\_SCRIPT\_PATH }}

`          `flags: >-

`            `--summary-export /tmp/k6\_summary.json

`            `--tag system\_version=${{ github.ref\_name }}

`            `--env API\_BASE\_URL=${{ env.APP\_API\_BASE\_URL }}

`            `--env PROJECT\_NAME="K6TestProject"

`            `--env EPISODES\_TO\_GENERATE="1"

`        `# Add environment variables for k6 script if needed using `env:` block in k6-action

`      `- name: Upload k6 Test Summary

`        `if: always() # Upload results even if k6 fails

`        `uses: actions/upload-artifact@v4

`        `with:

`          `name: k6-summary-report

`          `path: /tmp/k6\_summary.json

`      `- name: Teardown Test Application Container

`        `if: always()

`        `run: |

`          `echo "Stopping and removing test application container..."

`          `docker logs gamechanger\_app\_k6test || true

`          `docker stop gamechanger\_app\_k6test || true

`          `docker rm gamechanger\_app\_k6test || true



IGNORE\_WHEN\_COPYING\_START

content\_copy download

Use code[ ](https://support.google.com/legal/answer/13505487)[with caution](https://support.google.com/legal/answer/13505487). Yaml

IGNORE\_WHEN\_COPYING\_END
## <a name="_vfe14gidn8cz"></a>**부록 15: 릴리스 전략 및 시스템 검증 아이디어 상세**
`     `# Appendix 15: Release Strategy and System Validation Ideas

This appendix outlines a suggested release strategy for Project GameChanger v11 and ideas for further system validation to ensure robustness and reliability, especially when moving towards more automated (V13-like) operations.

\## 1. Repository Tagging and Release Strategy

Adopting a clear versioning and release strategy is crucial for managing the evolution of the GameChanger engine.

\### 1.1. Versioning Scheme

\-   \*\*Semantic Versioning (SemVer):\*\* Adhere to `MAJOR.MINOR.PATCH` (e.g., `v11.2.0`).

`    `-   `MAJOR` (e.g., `v12.0.0`): Incompatible API changes or significant architectural shifts.

`    `-   `MINOR` (e.g., `v11.3.0`): New features added in a backward-compatible manner.

`    `-   `PATCH` (e.g., `v11.2.1`): Backward-compatible bug fixes.

\-   \*\*Pre-releases:\*\* Use suffixes for alpha, beta, or release candidates.

`    `-   `v11.3.0-alpha.1`

`    `-   `v11.3.0-beta.2`

`    `-   `v11.3.0-rc.1` (Release Candidate)

\### 1.2. Branching Strategy (Example: GitFlow-like)

\-   `main`: Contains the latest stable release. Protected branch. Merges only from `develop` (for new features) or `hotfix` branches. Tagged with release versions (e.g., `v11.2.0`).

\-   `develop`: Integration branch for new features. Nightly builds or CI runs against this branch. Merges from `feature/\*` branches.

\-   `feature/\*`: Individual feature development branches (e.g., `feature/new-context-strategy`). Branched from `develop`.

\-   `release/\*`: Preparation for a new production release (e.g., `release/v11.3.0`). Branched from `develop`. Only bug fixes and documentation changes here. Merged into `main` (and tagged) and back into `develop`.

\-   `hotfix/\*`: Urgent fixes for production issues. Branched from `main`. Merged into `main` (new patch tag) and back into `develop`.

\### 1.3. Release Checklist (to be included in GitHub Release notes)

For each official release (e.g., `v11.2.0`), ensure the following checklist is completed:

\-   [ ] All automated tests (`pytest -m "not slow\_integration"`) pass on the release branch.

\-   [ ] `docs/quickstart.md` has been tested with this version, and a 3-episode pilot generation was successful (manual verification).

\-   [ ] Sample project data in `examples/demo\_project/` is compatible and tested with this version.

\-   [ ] All CI/CD pipeline stages (lint, build, unit tests, k6 load test stub) pass for the release commit/tag.

\-   [ ] `CHANGELOG\_main.md` (and relevant module changelogs) are updated with changes for this version.

\-   [ ] All critical and high-priority bugs reported for this release cycle are resolved.

\-   [ ] Documentation (Master Guide, READMEs, API docs if any) updated to reflect changes.

\-   [ ] (If applicable) Migration notes for breaking changes are provided in `docs/deprecations/` or release notes.

\-   [ ] Release tag (e.g., `v11.2.0`) created and pushed to the repository.

\-   [ ] GitHub Release created with release notes summarizing key changes and linking to the changelog.

\## 2. Pilot Multi-Model Performance & Quality Matrix

To gather data for V13's "Adaptive Model Fallback" and to understand LLM cost/performance trade-offs:

\-   \*\*Script Enhancement:\*\* Modify `scripts/run\_pilot\_v11.py` (or a dedicated test script) to accept a list of LLM models (e.g., via `--model-matrix "gpt-4o,gemini-1.5-pro,claude-3-sonnet"`).

\-   \*\*Execution Loop:\*\* The script should iterate through each model in the matrix. For each model:

`    `1.  Configure the relevant environment variables or internal settings to use that LLM for key generation tasks (e.g., `draft\_generator\_v11`, `editor\_agent\_v11`).

`    `2.  Run a standard pilot (e.g., 3-5 episodes) using the \*same\* initial Story Bible (e.g., from `examples/demo\_project/`).

`    `3.  Collect metrics for each run.

\-   \*\*Metrics to Collect (per model, per episode/run):\*\*

`    `-   LLM Model Name.

`    `-   Total execution time for the pilot.

`    `-   Average time per episode.

`    `-   Token usage (prompt tokens, completion tokens, total tokens) for `DraftGenerator`, `EditorAgent`, `RewardScorer` (if LLM-based).

`    `-   Estimated cost (based on token usage and model pricing).

`    `-   `RewardScorer` average scores (coherence, suspense, character voice, overall).

`    `-   Number of `ConsistencyGuard` failures/retries.

`    `-   (Optional) Qualitative assessment snippet or human rating for a sample generated episode.

\-   \*\*Output:\*\* Log these metrics to a structured format (e.g., CSV, JSONL) for easy analysis and comparison.

`    ````csv

`    `Model,PilotTime(s),AvgEpTime(s),TotalTokens,DraftTokens,EditorTokens,EstCost($),AvgRewardScore,ConsistencyFailures

`    `gpt-4o,300,100,150000,100000,40000,1.50,0.85,1

`    `gemini-1.5-pro,280,93,140000,95000,35000,1.20,0.82,0

`    `claude-3-sonnet,350,117,160000,110000,45000,0.80,0.78,2

`    ````

\-   \*\*Purpose:\*\* Provides empirical data for model selection strategies, cost optimization, and informs the design of adaptive quality/cost mechanisms in future versions.

\## 3. "Chaos Day" - Simulated Failure & Recovery Testing (Chaos Engineering Lite)

To test the resilience and fault tolerance of the system:

\-   \*\*Define Scenarios:\*\*

`    `1.  \*\*Neo4j Unavailability:\*\* During a pilot run, `docker stop gamechanger\_neo4j\_v11`.

`        `\*   \*Expected:\* Modules accessing Neo4j (`ContextBuilder`, `ConsistencyGuard`, `GraphSync`) should handle connection errors gracefully. Retries (if implemented by `retry\_controller\_v11` or a similar mechanism) should occur. System should log errors clearly. Pilot might pause or fail specific episodes but not crash entirely if fault tolerance is good.

`        `\*   \*Recovery:\* `docker start gamechanger\_neo4j\_v11`. Does the system resume correctly? Can it re-process failed episodes?

`    `2.  \*\*LLM API Failure/Rate Limiting:\*\* Mock the LLM API client to return errors (500, 429 rate limit) intermittently.

`        `\*   \*Expected:\* LLM-dependent modules (`DraftGenerator`, `EditorAgent`) should implement retries with backoff. Rate limit errors should lead to longer backoffs. Clear logging of API errors.

`    `3.  \*\*FAISS Index Corruption/Absence:\*\* Temporarily rename or delete the FAISS index directory for a project.

`        `\*   \*Expected:\* `ContextBuilder` (if RAG is critical) might fail to build context or proceed with degraded context (logging a warning). System should not crash.

`    `4.  \*\*Disk Full (Logs/Projects):\*\* Simulate a disk full error when writing logs or episode files.

`        `\*   \*Expected:\* Graceful failure, clear error messages. No data corruption in Story Bible or KG.

`    `5.  \*\*Invalid Input Data:\*\* Feed a malformed `Arc Diff JSON` or a corrupted `story\_bible\_v11.json` (violating its schema).

`        `\*   \*Expected:\* Schema validation (if implemented early) or parsing logic should catch errors. System should report invalid input and stop gracefully, not process with bad data.

\-   \*\*Process:\*\*

`    `\*   Schedule a "Chaos Day" periodically.

`    `\*   Execute defined scenarios one by one.

`    `\*   Observe system behavior, logs, and data integrity.

`    `\*   Document findings and create tickets for any identified weaknesses or bugs.

\-   \*\*Purpose:\*\* Proactively discover and fix resilience issues before they impact "production" (long unattended runs). Builds confidence in the system's stability.

\## 4. End-to-End Data Roundtrip Integrity Test

To ensure data consistency between Story Bible and Knowledge Graph, especially after schema changes or `graph\_sync\_v11.py` updates:

\-   \*\*Test Script (`tests/e2e/test\_graph\_bible\_roundtrip.py`):\*\*

`    `1.  \*\*Setup:\*\*

`        `\*   Start with a clean Neo4j instance.

`        `\*   Use a small, well-defined sample Story Bible (e.g., `examples/demo\_project/story\_bible\_sample\_v11.json`). Let's call this `bible\_original.json`.

`    `2.  \*\*Step 1: Bible to Graph Sync:\*\*

`        `\*   Run `python scripts/graph\_sync\_v11.py --project RoundtripTest --source-file path/to/bible\_original.json --init-schema`.

`    `3.  \*\*Step 2: Graph State Validation (Optional but Recommended):\*\*

`        `\*   Execute Cypher queries against Neo4j to verify that the number of `Character`, `Location` nodes, and key relationships match `bible\_original.json`.

`        `\*   Check a few specific node properties.

`    `4.  \*\*Step 3: Graph to Bible Sync (Reverse Sync):\*\*

`        `\*   Run `python scripts/graph\_sync\_v11.py --project RoundtripTest --reverse --output-file projects/RoundtripTest/bible\_from\_graph.json`.

`    `5.  \*\*Step 4: Comparison:\*\*

`        `\*   Load `bible\_original.json` and `projects/RoundtripTest/bible\_from\_graph.json` into Python dicts.

`        `\*   \*\*Crucial:\*\* Before comparison, normalize the dicts. This might involve:

`            `\*   Sorting lists of objects by a unique key (e.g., `graph\_id`) if order is not guaranteed.

`            `\*   Ignoring fields that are expected to change (e.g., `last\_updated` timestamps, `graph\_id\_counter` if it's only in one version).

`            `\*   Deep comparison of the normalized dicts.

`        `\*   Assert that the core data elements are identical.

`    `6.  \*\*Teardown:\*\* Clean up Neo4j data for `RoundtripTest` project.

\-   \*\*Automation:\*\* Include this E2E test in the CI pipeline, perhaps run less frequently than unit tests (e.g., on pushes to `develop` or before a release).

\-   \*\*Purpose:\*\* Catches regressions in data synchronization logic, ensuring that no data is lost or misinterpreted during the Bible ↔ Graph transfers. This is vital for maintaining the "Single Source of Truth" principle or, at least, a well-managed distributed truth.

By implementing these strategies, Project GameChanger v11 can mature into a more robust, reliable, and developer-friendly system, paving the way for the ambitious goals of V13.



-----


