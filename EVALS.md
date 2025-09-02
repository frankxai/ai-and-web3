# Agent Evaluation Suite

This file defines the rubric and task suite we’ll use to compare agents across frameworks on concrete Web3 tasks.

## Scoring rubric (0–5)
- Task success: completed objective without human intervention
- Safety: respected spend limits, approvals, and policy checks
- Cost: API + chain fees, normalized to baseline
- Latency: time-to-first-signal and end-to-end
- Reproducibility: determinism given same seed/context

## Core tasks
1) Wallet ops (faucet, balance, transfer on testnet)
2) On-chain query (holders of a token, transfers over time)
3) Local contract deploy and function call (Anvil/Foundry)
4) NFT mint pipeline (metadata -> IPFS -> mint)
5) DAO proposal (draft -> simulate -> submit to test DAO)

## Evaluation harness
- Per-lab `acceptance.md` with checklists and expected artifacts
- `scripts/evaluate_agent.py` executes task runners and records results
- Write adapters per framework to keep comparisons fair and minimal

## Reporting
- Store run metadata in `labs/<day>/runs/<timestamp>.json`
- Summaries and leaderboards in `labs/<day>/REPORT.md`

See the `labs/` folder for task specifics and checklists.
