from engine.story_bible_loader import load_story_bible
import pytest


def test_load_story_bible_success():
    """'Pilot' 프로젝트의 Story Bible을 성공적으로 로드하는지 테스트합니다."""
    project_name = "Pilot"
    bible_data = load_story_bible(project_name)
    assert isinstance(bible_data, dict)
    assert "world" in bible_data
    # characters가 배열 형태이므로 적절히 수정
    characters = bible_data["characters"]
    assert isinstance(characters, list)
    assert len(characters) > 0
    # 첫 번째 캐릭터가 성훈인지 확인
    sunghoon = next((char for char in characters if char["name"] == "성훈"), None)
    assert sunghoon is not None
    assert sunghoon["role"] == "주인공"


def test_load_story_bible_file_not_found():
    """존재하지 않는 프로젝트에 대해 FileNotFoundError를 발생하는지 테스트합니다."""
    with pytest.raises(FileNotFoundError):
        load_story_bible("NonExistentProject")
