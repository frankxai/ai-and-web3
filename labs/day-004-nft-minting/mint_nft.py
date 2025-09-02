#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv


ERC721_ABI = [
  {"inputs": [{"internalType":"address","name":"to","type":"address"},{"internalType":"string","name":"tokenURI","type":"string"}],"name":"safeMint","outputs":[],"stateMutability":"nonpayable","type":"function"}
]


def main():
    load_dotenv()
    rpc = os.environ.get("EVM_RPC_URL")
    pk = os.environ.get("PRIVATE_KEY")
    nft_addr = os.environ.get("ERC721_ADDRESS")
    token_uri = os.environ.get("TOKEN_URI")
    if not all([rpc, pk, nft_addr, token_uri]):
        raise SystemExit("Set EVM_RPC_URL, PRIVATE_KEY, ERC721_ADDRESS, TOKEN_URI in .env")

    w3 = Web3(Web3.HTTPProvider(rpc))
    acct = Account.from_key(pk)
    nft = w3.eth.contract(address=Web3.to_checksum_address(nft_addr), abi=ERC721_ABI)
    tx = nft.functions.safeMint(acct.address, token_uri).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 400_000,
        "maxFeePerGas": w3.eth.gas_price,
        "maxPriorityFeePerGas": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    })
    signed = w3.eth.account.sign_transaction(tx, pk)
    txh = w3.eth.send_raw_transaction(signed.rawTransaction)
    rcpt = w3.eth.wait_for_transaction_receipt(txh)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    runs = Path("runs"); runs.mkdir(exist_ok=True)
    (runs / f"{ts}-mint.json").write_text(Web3.to_json(rcpt))
    print(f"Minted NFT; receipt saved to runs/{ts}-mint.json")


if __name__ == "__main__":
    main()

