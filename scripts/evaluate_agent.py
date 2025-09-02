#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Minimal harness to record agent run metadata.")
    p.add_argument("--lab", required=True, help="lab folder name, e.g., day-001-wallets-and-rpc")
    p.add_argument("--framework", required=True, help="agent framework id")
    p.add_argument("--task", required=True, help="task id within the lab")
    p.add_argument("--success", action="store_true", help="mark success")
    p.add_argument("--cost", type=float, default=0.0)
    p.add_argument("--latency_ms", type=int, default=0)
    args = p.parse_args()

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lab_dir = Path(__file__).resolve().parents[1] / "labs" / args.lab / "runs"
    lab_dir.mkdir(parents=True, exist_ok=True)
    out = {
        "framework": args.framework,
        "task": args.task,
        "success": bool(args.success),
        "cost": args.cost,
        "latency_ms": args.latency_ms,
        "timestamp": ts,
    }
    (lab_dir / f"{ts}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out))

if __name__ == "__main__":
    main()

