#!/usr/bin/env python3
"""
Minimal agent runner that plans -> acts using our tool registry.
This keeps a deterministic shape for comparison without external deps.
"""
from typing import Any, Dict, List
from agents.registry import run as run_tool


def plan(task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
    if task == "balance_and_transfer":
        return [
            {"tool": "evm.get_balance", "args": {"address": context["address"]}},
            {"tool": "evm.simulate_transfer", "args": {"to": context["to"], "value_wei": context["value_wei"]}},
            {"tool": "evm.send_transfer", "args": {"to": context["to"], "value_wei": context["value_wei"], "max_value_wei": context.get("max_value_wei", 0)}}
        ]
    raise ValueError("Unknown task")


def run(task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
    steps = plan(task, context)
    out = []
    for s in steps:
        out.append({"step": s, "result": run_tool(s["tool"], s["args"])})
    return out


if __name__ == "__main__":
    import os, json
    ctx = {
        "address": os.environ.get("FROM_ADDRESS"),
        "to": os.environ.get("TO_ADDRESS"),
        "value_wei": int(os.environ.get("VALUE_WEI", "0")),
        "max_value_wei": int(os.environ.get("MAX_VALUE_WEI", "0")),
    }
    print(json.dumps(run("balance_and_transfer", ctx), indent=2))

