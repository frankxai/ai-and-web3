# Day 006 — Account Abstraction (ERC-4337) + Safe

## Goals
- Create a Safe or 4337 smart account on testnet
- Execute a user operation with strict spend limits

## Tasks
1) Set up bundler/provider (e.g., Pimlico/StackUp)
2) Create account and deposit minimal funds
3) Execute a transfer via AA or Safe module
4) Log userOp hash, receipts, and policy checks

## Acceptance criteria
- [ ] `runs/<ts>/aa_account.json` and `userop.json`
- [ ] Spend limit + allowlist enforced
