import os


def build_context_for_episode(project_name: str, episode_number: int) -> str:
    """
    주어진 에피소드를 생성하기 위한 컨텍스트를 구성합니다.
    (현재는 스텁이며, 환경 변수만 읽는 기능만 구현합니다.)

    Args:
        project_name (str): 프로젝트 이름.
        episode_number (int): 생성할 에피소드 번호.

    Returns:
        str: 구성된 컨텍스트 문자열 (현재는 더미 텍스트).
    """
    # .env 파일 등에서 CTX_TOKEN_BUDGET을 읽어오는 로직 (예시)
    token_budget = os.getenv("CTX_TOKEN_BUDGET", "8192")
    print(f"ContextBuilder: Using token budget of {token_budget}")

    # 나중에 실제 컨텍스트 구성 로직이 여기에 들어갑니다.
    dummy_context = (
        f"This is a dummy context for {project_name}, episode {episode_number}."
    )
    return dummy_context
