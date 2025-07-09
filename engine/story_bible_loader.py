import yaml
import pathlib


def load_story_bible(project_name: str) -> dict:
    """
    지정된 프로젝트의 story_bible.yaml 파일을 로드합니다.

    Args:
        project_name (str): 로드할 프로젝트의 이름.

    Returns:
        dict: 로드된 Story Bible 데이터.
    """
    file_path = pathlib.Path(f"projects/{project_name}/story_bible.yaml")
    if not file_path.exists():
        raise FileNotFoundError(f"Story Bible을 찾을 수 없습니다: {file_path}")

    with open(file_path, "r", encoding="utf8") as f:
        return yaml.safe_load(f)
