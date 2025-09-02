#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from jsonschema import validate, ValidationError


SCHEMAS = {
    "evm.get_balance": Path("agents/tools/schema/evm_get_balance.schema.json"),
    "evm.send_transfer": Path("agents/tools/schema/evm_send_transfer.schema.json"),
}


def main():
    p = argparse.ArgumentParser(description="Validate lab artifacts against known schemas")
    p.add_argument("lab", help="labs/day-XXX-... path")
    args = p.parse_args()
    lab = Path(args.lab)
    runs = lab / "runs"
    if not runs.exists():
        print("No runs folder to validate.")
        return
    # Basic heuristic: open all json artifacts and check they are valid JSON
    errors = 0
    for f in runs.glob("*.json"):
        try:
            data = json.loads(f.read_text())
        except Exception as e:
            print(f"Invalid JSON: {f}: {e}")
            errors += 1
            continue
        # Optional: if file name includes a tool, validate payload
        for tool, schema_path in SCHEMAS.items():
            if tool.replace(".", "_") in f.name and schema_path.exists():
                schema = json.loads(schema_path.read_text())
                try:
                    validate(instance=data, schema=schema)
                except ValidationError as e:
                    print(f"Schema mismatch for {tool} in {f}: {e.message}")
                    errors += 1
    if errors:
        raise SystemExit(1)
    print("All artifacts valid.")


if __name__ == "__main__":
    main()

