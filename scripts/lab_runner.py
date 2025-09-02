#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


LAB_STEPS = {
    "day-001-wallets-and-rpc": [
        ["python", "labs/day-001-wallets-and-rpc/wallet_ops.py"]
    ],
    "day-002-onchain-data": [
        ["python", "labs/day-002-onchain-data/query_data.py"]
    ],
    "day-003-contract-deploy-local": [
        ["python", "labs/day-003-contract-deploy-local/interact.py"]
    ],
    "day-004-nft-minting": [
        ["python", "labs/day-004-nft-minting/mint_nft.py"]
    ],
}


def run_cmd(cmd, cwd=None):
    print("$ ", " ".join(cmd))
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit(res.returncode)


def main():
    p = argparse.ArgumentParser(description="Run a lab end-to-end")
    p.add_argument("lab", help="lab folder name, e.g., day-001-wallets-and-rpc")
    p.add_argument("--framework", default="manual")
    args = p.parse_args()

    steps = LAB_STEPS.get(args.lab)
    if not steps:
        raise SystemExit(f"Unknown lab: {args.lab}")
    for step in steps:
        run_cmd(step)

    # Record a minimal run metadata
    from scripts.evaluate_agent import datetime as _dt  # type: ignore
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    runs = Path("labs") / args.lab / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    meta = {"framework": args.framework, "task": "full", "success": True, "cost": 0, "latency_ms": 0, "timestamp": ts}
    (runs / f"{ts}.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta))


if __name__ == "__main__":
    main()

