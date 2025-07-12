# engine/arc_planner.py

from pathlib import Path
import yaml
# === 이 부분을 추가합니다 ===
from typing import Any, Dict, List
# ==========================

# === 이 부분을 수정합니다: dict -> Dict[str, Any] ===
def generate_diff(source_yaml: Path) -> Dict[str, Any]:
# ===================================================
    """
    YAML Arc detail 파일을 읽어, 모든 내용을 'add'하는 ops 리스트를 포함한
    딕셔너리로 변환합니다.
    
    Args:
        source_yaml (Path): 읽어올 소스 YAML 파일의 경로 객체.

    Returns:
        Dict[str, Any]: arc_id와 'ops' 리스트를 포함하는 딕셔너리.
    """
    after = yaml.safe_load(source_yaml.read_text(encoding="utf-8"))

    # === 이 부분을 수정합니다: ops 타입을 명시적으로 지정 ===
    ops: List[Dict[str, Any]] = [
    # ==================================================
        {
            "op": "add",
            "path": "",
            "value": after
        }
    ]

    return {
        "arc_id": after.get("arc_id", "UNKNOWN_ARC"),
        "ops": ops
    }