# engine/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    프로젝트의 모든 설정을 관리하는 클래스.
    .env 파일, 환경 변수, 또는 기본값 순서로 설정을 로드합니다.
    """
    # Neo4j 설정
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    # 임베딩 및 FAISS 설정
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    FAISS_ROOT: str = "memory/faiss_index"

    # 토큰 예산 설정 (대형 컨텍스트 모델용)
    MAX_CTX_WINDOW: int = 1_000_000
    CTX_TOKEN_BUDGET: int = 200_000

    # Pydantic 설정
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'  # .env 파일에 추가 필드가 있어도 무시
    )

    @property
    def SAFE_TRIM_BUDGET(self) -> int:
        """10% 안전 마진을 적용한 효율적인 예산을 계산합니다."""
        return min(self.CTX_TOKEN_BUDGET, int(self.MAX_CTX_WINDOW * 0.9))


@lru_cache
def get_settings() -> Settings:
    """
    설정 객체를 반환하는 함수.
    lru_cache를 사용하여 처음 호출 시 한 번만 객체를 생성하고 캐싱합니다.
    """
    return Settings()


# 스크립트 직접 실행 시 설정값 확인용
if __name__ == "__main__":
    settings = get_settings()
    print("--- Project Settings ---")
    print(f"Neo4j URI: {settings.NEO4J_URI}")
    print(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    # 비밀번호는 보안을 위해 출력하지 않습니다.
    print("Settings loaded successfully.")
