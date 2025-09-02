# Day 007 — Intents + Swap Aggregator (Simulated)

## Goals
- Model an intent (best-price swap) and plan across aggregators
- Simulate outcomes and choose a path within constraints

## Tasks
1) Define intent schema (tokenIn, tokenOut, slippage, maxCost)
2) Query 1inch/CoW routes (API or sim)
3) Simulate top 2 paths locally or on a fork
4) Pick and justify the chosen path

## Acceptance criteria
- [ ] `runs/<ts>/intent.json` and `simulation.json`
- [ ] Rationale with cost/latency comparison
