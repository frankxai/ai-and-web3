# Security Model

Principles for running agents that can transact and modify state on-chain.

## Core principles
- Least privilege: scoped keys, spend limits, allowlists
- Dry-run first: simulate transactions (Tenderly/Anvil) before submission
- Human-in-the-loop: approvals for high-impact actions
- Deterministic playbooks: narrow, testable flows over open-ended autonomy

## Key handling
- Use ephemeral test keys in `.env` files excluded by `.gitignore`
- Never commit secrets; prefer local key stores or env managers
- Consider per-lab wallets with zero shared balances

## Transaction policy
- Guardrails: max gas, max value, address allowlists/denylists
- Preflight checks: simulate locally; verify state diffs match expectations
- Logging: store receipts, RPCs, and diffs under `labs/<day>/runs/`

## Off-chain safety
- Respect API rate limits and costs
- Validate external data sources and handle failures explicitly

## Auditing
- Include `acceptance.md` per lab
- Capture artifacts: signed tx, simulation report, contract bytecode, metadata
