# Day 002 — On-chain Data Retrieval

## Goals
- Query token transfers and balances via RPC
- Use a subgraph (The Graph) or Dune for structured queries
- Compare latency, completeness, and cost

## Tasks
1) RPC: fetch last 100 transfers for a token
2) Subgraph: fetch holders and balances
3) Dune: run a query for top counterparties
4) Summarize differences and caveats

## Acceptance criteria
- [ ] `runs/<timestamp>/rpc.json` and `subgraph.json`
- [ ] Notes on pagination, rate limits, and schema drift
