# tests/test_config.py
import os
from unittest.mock import patch
from engine.config import get_settings, Settings


def test_get_settings_loads_from_env():
    """ .env 파일에서 설정을 올바르게 로드하는지 테스트 """
    # get_settings()는 lru_cache를 사용하므로, 캐시를 초기화해준다.
    get_settings.cache_clear()

    # .env 파일이 실제 존재한다고 가정하고 테스트
    # (CI 환경에서는 실제 .env 대신 GitHub Secrets를 사용)
    with patch.dict(os.environ, {
        "NEO4J_PASSWORD": "test_from_env",
        "EMBEDDING_MODEL": "test-model"
    }):
        # Pydantic이 환경 변수를 우선적으로 사용하도록 강제
        settings = Settings(_env_file=None)
        assert settings.NEO4J_PASSWORD == "test_from_env"
        assert settings.EMBEDDING_MODEL == "test-model"
