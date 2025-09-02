#!/usr/bin/env python3
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

import yaml

from agents.registry import run as run_tool


VAR = re.compile(r"\$\{([A-Z0-9_]+)\}")


def resolve_env(obj):
    if isinstance(obj, str):
        def repl(m):
            key = m.group(1)
            val = os.environ.get(key)
            if val is None:
                raise SystemExit(f"Missing env var: {key}")
            return val
        return VAR.sub(lambda m: repl(m), obj)
    if isinstance(obj, list):
        return [resolve_env(x) for x in obj]
    if isinstance(obj, dict):
        return {k: resolve_env(v) for k, v in obj.items()}
    return obj


def main():
    p = argparse.ArgumentParser(description="Run a YAML playbook of tools")
    p.add_argument("playbook", help="Path to YAML playbook file")
    p.add_argument("--lab", default=None)
    args = p.parse_args()

    pb = yaml.safe_load(Path(args.playbook).read_text())
    steps = pb.get("steps", [])
    outputs = []
    for step in steps:
        tool = step["tool"]
        args_dict = resolve_env(step.get("args", {}))
        # Coerce number strings to ints for known fields
        for k, v in list(args_dict.items()):
            if isinstance(v, str) and v.isdigit():
                args_dict[k] = int(v)
        print(f"Running {tool} with {args_dict}")
        out = run_tool(tool, args_dict)
        outputs.append({"tool": tool, "args": args_dict, "output": out})

    # Save artifacts
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    if args.lab:
        runs = Path("labs") / args.lab / "runs"
    else:
        runs = Path("runs")
    runs.mkdir(parents=True, exist_ok=True)
    (runs / f"playbook-{ts}.json").write_text(json.dumps(outputs, indent=2))
    print(f"Saved outputs to {runs}/playbook-{ts}.json")


if __name__ == "__main__":
    main()

