# Day 001 — Wallets and RPC (EVM testnet)

## Goals
- Create and fund a test wallet
- Query balances and send a small transfer on a testnet
- Add an agent step that plans and executes RPC calls

## Prerequisites
- Anvil (local) or Goerli/SEPOLIA RPC (env var `EVM_RPC_URL`)
- Test private key in `.env` (excluded by git)

## Tasks
1) Generate a fresh test wallet (no reused keys)
2) If on testnet, fund via faucet (manual OK today)
3) Read ETH balance
4) Transfer minimal amount to a second wallet you control
5) Capture tx receipt and logs

## Acceptance criteria
- [ ] `runs/<timestamp>/wallet.json` with redacted pub info
- [ ] `runs/<timestamp>/transfer.json` receipt with status=1
- [ ] Notes on RPC, chainId, and gas estimation behavior

## Stretch
- Implement a dry-run/simulation on Anvil before testnet
- Add a spend limit policy in your agent/tool layer

## Runnable script (Python)
- Copy `.env.example` to `.env` and set `EVM_RPC_URL`, `PRIVATE_KEY`
- Optional: set `RECIPIENT` address to send to; defaults to self-transfer
- Install deps at repo root: `pip install -r requirements.txt`
- Run: `python labs/day-001-wallets-and-rpc/wallet_ops.py`

Artifacts will be written to `labs/day-001-wallets-and-rpc/runs/`.
