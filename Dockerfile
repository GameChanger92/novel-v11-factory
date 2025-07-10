# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 시스템 의존성 설치 (예: FAISS 빌드, 특정 라이브러리 실행에 필요한 경우)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential cmake libgomp1 \
#  && rm -rf /var/lib/apt/lists/*
# libgomp1는 일부 ML 라이브러리(예: faiss) 실행 시 필요할 수 있음

COPY requirements.txt .
# --no-cache-dir: Docker 이미지 크기 최적화
# --prefer-binary: 가능한 경우 pre-compiled 바이너리 사용 (빌드 시간 단축)
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# 우리가 만든 'engine' 패키지를 설치합니다.
# pyproject.toml이 있으므로, 아래 명령어로 설치할 수 있습니다.
COPY pyproject.toml .
COPY engine ./engine
RUN pip install -e .

# 나머지 애플리케이션 코드를 복사합니다.
# .dockerignore 파일을 사용하여 불필요한 파일(예: .git, .venv, __pycache__) 제외
COPY . .

# 기본 실행 명령어 (docker-compose.yml에서 오버라이드 가능)
CMD ["tail", "-f", "/dev/null"] # 기본적으로는 대기 상태로 실행