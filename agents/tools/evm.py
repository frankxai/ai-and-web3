#!/usr/bin/env python3
import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3


@dataclass
class EVMContext:
    w3: Web3
    address: str
    pk: str


def load_ctx() -> EVMContext:
    load_dotenv()
    rpc = os.environ.get("EVM_RPC_URL")
    pk = os.environ.get("PRIVATE_KEY")
    if not rpc or not pk:
        raise SystemExit("Set EVM_RPC_URL and PRIVATE_KEY in .env or env")
    w3 = Web3(Web3.HTTPProvider(rpc))
    addr = Account.from_key(pk).address
    return EVMContext(w3=w3, address=addr, pk=pk)


def get_balance(address: str) -> Dict[str, Any]:
    ctx = load_ctx()
    bal = ctx.w3.eth.get_balance(Web3.to_checksum_address(address))
    return {"address": Web3.to_checksum_address(address), "wei": bal}


def simulate_transfer(to: str, value_wei: int) -> Dict[str, Any]:
    ctx = load_ctx()
    tx = {
        "from": ctx.address,
        "to": Web3.to_checksum_address(to),
        "value": int(value_wei),
        "data": b"",
    }
    try:
        gas = ctx.w3.eth.estimate_gas(tx)
        return {"ok": True, "estimated_gas": int(gas)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def send_transfer(to: str, value_wei: int, max_value_wei: int) -> Dict[str, Any]:
    if int(value_wei) > int(max_value_wei):
        raise SystemExit("Policy violation: value exceeds max_value_wei")
    ctx = load_ctx()
    sim = simulate_transfer(to, value_wei)
    if not sim.get("ok"):
        raise SystemExit(f"Simulation failed: {sim.get('error')}")
    tx = {
        "to": Web3.to_checksum_address(to),
        "value": int(value_wei),
        "nonce": ctx.w3.eth.get_transaction_count(ctx.address),
        "gas": max(21_000, int(sim.get("estimated_gas", 21_000))),
        "maxFeePerGas": ctx.w3.eth.gas_price,
        "maxPriorityFeePerGas": ctx.w3.eth.gas_price,
        "chainId": ctx.w3.eth.chain_id,
    }
    signed = ctx.w3.eth.account.sign_transaction(tx, private_key=ctx.pk)
    txh = ctx.w3.eth.send_raw_transaction(signed.rawTransaction)
    rcpt = ctx.w3.eth.wait_for_transaction_receipt(txh)
    return json.loads(Web3.to_json(rcpt))


def main():
    p = argparse.ArgumentParser(description="EVM tool CLI")
    sub = p.add_subparsers(dest="cmd")
    b = sub.add_parser("get_balance")
    b.add_argument("address")
    s = sub.add_parser("simulate_transfer")
    s.add_argument("to")
    s.add_argument("value_wei", type=int)
    t = sub.add_parser("send_transfer")
    t.add_argument("to")
    t.add_argument("value_wei", type=int)
    t.add_argument("max_value_wei", type=int)
    args = p.parse_args()

    if args.cmd == "get_balance":
        print(json.dumps(get_balance(args.address), indent=2))
    elif args.cmd == "simulate_transfer":
        print(json.dumps(simulate_transfer(args.to, args.value_wei), indent=2))
    elif args.cmd == "send_transfer":
        print(json.dumps(send_transfer(args.to, args.value_wei, args.max_value_wei), indent=2))
    else:
        p.print_help()


if __name__ == "__main__":
    main()

