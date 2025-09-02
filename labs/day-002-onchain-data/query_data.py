#!/usr/bin/env python3
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from web3 import Web3
from dotenv import load_dotenv


def get_rpc_transfers(w3: Web3, token: str, start_block: int, end_block: int) -> Dict[str, Any]:
    # Minimal ERC20 Transfer topic
    topic = w3.keccak(text="Transfer(address,address,uint256)").hex()
    logs = w3.eth.get_logs({
        "fromBlock": start_block,
        "toBlock": end_block,
        "address": Web3.to_checksum_address(token),
        "topics": [topic]
    })
    return {"count": len(logs), "logs": [dict(x) for x in logs[:50]]}


def main():
    load_dotenv()
    rpc = os.environ.get("EVM_RPC_URL")
    token = os.environ.get("ERC20_ADDRESS")
    if not rpc or not token:
        raise SystemExit("Set EVM_RPC_URL and ERC20_ADDRESS in .env")
    w3 = Web3(Web3.HTTPProvider(rpc))
    latest = w3.eth.block_number
    start = max(0, latest - 5_000)
    res = get_rpc_transfers(w3, token, start, latest)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    runs = Path("runs"); runs.mkdir(exist_ok=True)
    (runs / f"{ts}-rpc.json").write_text(json.dumps(res, indent=2, default=str))
    print(f"Saved RPC transfers to {runs}/{ts}-rpc.json")

    # Placeholder for The Graph / Dune: save config expectation for users
    graph_query = {
        "subgraph": os.environ.get("GRAPH_SUBGRAPH"),
        "query": "query { transfers(first: 10) { id from to value } }"
    }
    (runs / f"{ts}-subgraph.json").write_text(json.dumps(graph_query, indent=2))
    print("Wrote subgraph query placeholder; set GRAPH_SUBGRAPH and run externally.")


if __name__ == "__main__":
    main()

