# engine/story_bible_loader.py
import json  # yaml 대신 json을 임포트합니다.
import pathlib
import sys   # 에러 처리를 위해 sys를 임포트합니다.


def load_story_bible(project_name: str) -> dict:
    """
    지정된 프로젝트의 story_bible_v11.json 파일을 로드합니다.

    Args:
        project_name (str): 로드할 프로젝트의 이름.

    Returns:
        dict: 로드된 Story Bible 데이터.
    """
    # 파일 경로를 Master Guide 표준인 story_bible_v11.json으로 변경합니다.
    file_path = pathlib.Path(f"projects/{project_name}/story_bible_v11.json")

    if not file_path.exists():
        # 에러 메시지를 좀 더 명확하게 하고, sys.exit로 프로그램을 종료시킵니다.
        print(f"⛔️ ERROR: Story Bible file not found at: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf8") as f:
            # yaml.safe_load 대신 json.load를 사용합니다.
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"⛔️ ERROR: Failed to decode JSON from {file_path}. Error: {e}", file=sys.stderr)
        sys.exit(1)
