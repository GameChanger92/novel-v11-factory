from engine.story_bible_loader import load_story_bible
import pytest

def test_load_story_bible_success():
    """'Pilot' 프로젝트의 Story Bible을 성공적으로 로드하는지 테스트합니다."""
    project_name = "Pilot"
    bible_data = load_story_bible(project_name)
    assert isinstance(bible_data, dict)
    assert "world" in bible_data
    assert bible_data["characters"]["성훈"]["role"] == "주인공"

def test_load_story_bible_file_not_found():
    """존재하지 않는 프로젝트에 대해 FileNotFoundError를 발생하는지 테스트합니다."""
    with pytest.raises(FileNotFoundError):
        load_story_bible("NonExistentProject")