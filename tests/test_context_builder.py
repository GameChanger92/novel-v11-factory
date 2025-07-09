"""Context builder 테스트 모듈."""
import pytest
from engine.context_builder import build_context_for_episode


@pytest.mark.skip(reason="아직 실제 컨텍스트 생성 로직이 구현되지 않았습니다.")
def test_build_context_for_episode():
    """ContextBuilder가 기본 컨텍스트를 생성하는지 테스트합니다."""
    context = build_context_for_episode("Pilot", 1)
    assert "Pilot" in context
    assert "episode 1" in context
