# engine/story_bible_loader.py
import json  # yaml 대신 json을 임포트합니다.
import pathlib
import sys   # 에러 처리를 위해 sys를 임포트합니다.


from typing import Any


def load_story_bible(project_name: str) -> dict[str, Any]:
    """
    지정된 프로젝트의 story_bible_v11.json 파일을 로드합니다.

    Args:
        project_name (str): 로드할 프로젝트의 이름.

    Returns:
        dict[str, Any]: 로드된 Story Bible 데이터.
    """
    # 파일 경로를 Master Guide 표준인 story_bible_v11.json으로 변경합니다.
    file_path = pathlib.Path(f"projects/{project_name}/story_bible_v11.json")

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    try:
        with open(file_path, "r", encoding="utf8") as f:
            # yaml.safe_load 대신 json.load를 사용합니다.
            data: dict[str, Any] = json.load(f)
            data.setdefault("world", data.get("world_setting", {}))
            return data
    except json.JSONDecodeError as e:
        print(f"⛔️ ERROR: Failed to decode JSON from {file_path}. Error: {e}", file=sys.stderr)
        sys.exit(1)
