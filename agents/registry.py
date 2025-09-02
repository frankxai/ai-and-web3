#!/usr/bin/env python3
import argparse
import importlib
import json
from typing import Any, Dict


REGISTRY = {
    "evm.get_balance": ("agents.tools.evm", "get_balance"),
    "evm.simulate_transfer": ("agents.tools.evm", "simulate_transfer"),
    "evm.send_transfer": ("agents.tools.evm", "send_transfer"),
}


def run(tool: str, payload: Dict[str, Any]) -> Any:
    if tool not in REGISTRY:
        raise SystemExit(f"Unknown tool: {tool}")
    mod_name, fn_name = REGISTRY[tool]
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, fn_name)
    return fn(**payload)


def main():
    p = argparse.ArgumentParser(description="Simple tool registry CLI")
    p.add_argument("tool", help="e.g. evm.get_balance")
    p.add_argument("json_payload", help='JSON, e.g. {"address":"0x..."}')
    args = p.parse_args()
    payload = json.loads(args.json_payload)
    out = run(args.tool, payload)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

