import argparse
import json
import sys
from importlib import resources
from pathlib import Path

from jsonschema import validate, ValidationError

# 우리 프로젝트의 'engine' 폴더에서 arc_planner 부품을 가져옵니다.
from engine.arc_planner import generate_diff

def main() -> None:
    # 1. 사용자의 명령(인자)을 해석할 준비
    parser = argparse.ArgumentParser(description="Generate Arc Diff JSON from a source YAML file.")
    parser.add_argument("--project", required=True, help="The project slug (e.g., Pilot).")
    parser.add_argument("--arc", required=True, help="The arc ID (e.g., A1, A2).")
    parser.add_argument("--source-yaml", type=Path, required=True, help="Path to the source arc detail YAML file.")
    args = parser.parse_args()

    # 2. 입력 파일이 진짜 있는지 확인 (방어 코드)
    if not args.source_yaml.is_file():
        sys.exit(f"[오류] 소스 파일을 찾을 수 없습니다: {args.source_yaml}")

    # 3. 엔진에 일 시키기
    diff_data = generate_diff(args.source_yaml)

    # 4. 결과물 검증하기
    try:
        # importlib.resources는 우리 패키지 안에 포함된 파일을 안전하게 찾도록 도와줍니다.
        schema_content = resources.files("schemas").joinpath("arc_diff_v11.schema.json").read_text(encoding="utf-8")
        schema = json.loads(schema_content)
        validate(diff_data, schema)
    except FileNotFoundError:
        sys.exit("[오류] 스키마 파일(schemas/arc_diff_v11.schema.json)을 찾을 수 없습니다.")
    except ValidationError as e:
        sys.exit(f"[오류] 생성된 데이터가 스키마와 맞지 않습니다:\n{e.message}")

    # 5. 최종 결과물 파일로 저장하기
    out_dir = Path(f"projects/{args.project}/memory/diffs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{args.arc}_detail_diff_v11.json"
    out_file.write_text(json.dumps(diff_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ Diff 파일이 성공적으로 생성되었습니다 → {out_file}")

if __name__ == "__main__":
    main()