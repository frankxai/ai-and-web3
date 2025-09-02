#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv


ABI = [
  {"inputs": [], "name": "count", "outputs": [{"internalType":"uint256","name":"","type":"uint256"}], "stateMutability": "view", "type": "function"},
  {"inputs": [], "name": "increment", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]


def main():
    load_dotenv()
    rpc = os.environ.get("EVM_RPC_URL", "http://127.0.0.1:8545")
    pk = os.environ.get("PRIVATE_KEY")
    addr = os.environ.get("COUNTER_ADDRESS")
    if not pk or not addr:
        raise SystemExit("Set PRIVATE_KEY and COUNTER_ADDRESS in .env")

    w3 = Web3(Web3.HTTPProvider(rpc))
    acct = Account.from_key(pk)
    c = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=ABI)

    before = c.functions.count().call()
    tx = c.functions.increment().build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 200_000,
        "maxFeePerGas": w3.eth.gas_price,
        "maxPriorityFeePerGas": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    })
    signed = w3.eth.account.sign_transaction(tx, pk)
    txh = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(txh)
    after = c.functions.count().call()

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    runs = Path("runs"); runs.mkdir(exist_ok=True)
    (runs / f"{ts}-calls.json").write_text(json.dumps({
        "before": before, "after": after, "receipt": Web3.to_json(receipt)
    }, indent=2))
    print(f"Incremented from {before} to {after}. Artifacts under {runs}.")


if __name__ == "__main__":
    main()

