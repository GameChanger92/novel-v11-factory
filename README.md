# novel-v11-factory

## Quick Start (3화 파일럿 실행)

```bash
# 1. Codespaces 환경에서, 필요한 패키지를 설치합니다.
pip install -r requirements.txt

# 2. .env 파일을 준비하고 API 키를 입력합니다.
cp .env.example .env
# nano .env  (또는 VS Code 편집기에서 직접 .env 파일을 열어 키를 입력)

# 3. 3화 분량의 파일럿 소설을 생성합니다.
python scripts/run_novel.py --total 3

# 4. 생성된 파일을 확인합니다.
ls -l projects/Pilot/episodes
```

## Week 1 Done Definition
- [x] GitHub repo & Codespace 정상 동작
- [x] `engine/`, `scripts/`, `ui/` 등 폴더 구조 생성
- [x] `requirements.txt` / `.env.example` 준비
- [x] 기본 CI 워크플로 **녹색**
- [x] README에 Quick Start 안내 추가
- [x] `run_novel.py` 150줄 MVP로 3화 파일럿 생성 성공

---