from pathlib import Path
from engine.arc_planner import generate_diff

# pytest는 'tmp_path'라는 마법의 인자를 제공합니다.
# 이 인자는 테스트가 실행되는 동안에만 존재하는 임시 폴더를 만들어줘서,
# 테스트를 위해 파일을 만들고 지우는 작업을 깔끔하게 처리할 수 있습니다.
def test_generate_diff_returns_correct_structure(tmp_path: Path):
    """
    generate_diff 함수가 'arc_id'와 'ops' 키를 포함하는
    올바른 구조의 딕셔너리를 반환하는지 테스트합니다.
    """
    # 1. 준비 (Arrange): 테스트에 필요한 가짜 YAML 파일을 임시 폴더에 만듭니다.
    source_yaml_file = tmp_path / "test_arc.yaml"
    source_yaml_file.write_text("arc_id: A1\ntitle: 'The First Arc'")
    
    # 2. 실행 (Act): 테스트하려는 함수를 실행합니다.
    result = generate_diff(source_yaml_file)
    
    # 3. 단언 (Assert): 결과가 우리가 기대한 것과 같은지 확인합니다.
    assert isinstance(result, dict)
    assert "arc_id" in result
    assert "ops" in result
    assert result["arc_id"] == "A1"
    assert isinstance(result["ops"], list)
    assert len(result["ops"]) > 0