#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv


def main():
    load_dotenv()
    rpc = os.environ.get("EVM_RPC_URL")
    pk = os.environ.get("PRIVATE_KEY")
    if not rpc or not pk:
        raise SystemExit("Set EVM_RPC_URL and PRIVATE_KEY in .env")

    w3 = Web3(Web3.HTTPProvider(rpc))
    acct = Account.from_key(pk)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    runs = Path("runs")
    runs.mkdir(parents=True, exist_ok=True)

    (runs / f"{ts}-wallet.json").write_text(
        json.dumps({"address": acct.address, "chain_id": w3.eth.chain_id}, indent=2)
    )

    bal = w3.eth.get_balance(acct.address)
    (runs / f"{ts}-balance.json").write_text(json.dumps({"wei": bal}, indent=2))

    # Prepare a small self-transfer (or set RECIPIENT env)
    to_addr = os.environ.get("RECIPIENT", acct.address)
    tx = {
        "to": Web3.to_checksum_address(to_addr),
        "value": Web3.to_wei(0, "ether"),
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 21_000,
        "maxFeePerGas": w3.eth.gas_price,
        "maxPriorityFeePerGas": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    }
    signed = w3.eth.account.sign_transaction(tx, private_key=pk)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    (runs / f"{ts}-transfer.json").write_text(Web3.to_json(receipt))
    print(f"Wrote artifacts under {runs} with timestamp {ts}")


if __name__ == "__main__":
    main()

