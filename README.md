# AI + Web3: Agent Architect Playbook

Build, evaluate, and compare AI agents that reason about, interact with, and ship on Web3. Organized for daily, testable progression and repeatable experiments across chains, tools, and agent frameworks.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Scope](https://img.shields.io/badge/focus-AI%20agents%20%E2%86%94%EF%B8%8F%20Web3-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Table of contents
- Overview
- Repo Structure
- Quickstart
- Daily Labs
- Frameworks Matrix
- Evaluation
- MCP Servers
- Contributing

---

## Overview
- Turn research into runnable labs and production patterns
- Compare agent frameworks head‑to‑head on real Web3 tasks
- Reuse high‑quality scaffolds for new projects and demos
- Capture best practices for security, ops, and reliability

Mermaid overview
```mermaid
flowchart LR
  A[Agent Frameworks\n(LangGraph, Assistants, Autogen, LlamaIndex)] --> B{Tools}
  B --> C[Web3 Data\n(RPC, The Graph, Dune)]
  B --> D[State Change\n(ethers/web3.py/viem)]
  B --> E[Storage\n(IPFS/Arweave)]
  B --> F[Governance\n(DAOs/Snapshot)]
  A --> G[Evaluation\n(success, safety, cost, latency)]
  G --> H[Labs\n(day-by-day tasks)]
```

## Repo Structure
```
docs/                  # Getting started, patterns, security
resources/             # Curations: MCP, repos, papers
templates/             # Lab and agent project templates
labs/                  # Day-by-day, testable exercises
agents/                # Agent framework notes & adapters
examples/              # Example projects (stubs + links)
external/              # Vendored submodules (AgentKits, MCP)
scripts/               # Scaffold + evaluation utilities
ROADMAP.md             # Phased build-out plan
EVALS.md               # Evaluation rubric & task suite
```

## Quickstart
- Prereqs: Python 3.10+, Node 18+, Docker, Foundry or Hardhat (for EVM), Solana CLI (optional), Git
- Explore docs: `docs/GETTING_STARTED.md`
- Start with Day 001: `labs/day-001-wallets-and-rpc/README.md`
- Scaffold a new day: `python scripts/scaffold_lab.py --day 006 --name "intent-swap-aggregator"`

## Daily Labs
- Day 001: Wallets + RPC fundamentals (EVM, testnet)
- Day 002: On-chain data querying (RPC, The Graph, Dune)
- Day 003: Local contract deploy + agent planning loop
- Day 004: NFT mint pipeline (IPFS/Arweave + metadata)
- Day 005: DAO proposal drafting + submission (test DAO)
- Day 006: Account Abstraction (ERC-4337) + Safe policies
- Day 007: Intents + swap aggregator planning (simulated)
- Day 008: Cross-chain messaging (Axelar/LayerZero sim)
- Day 009: ZK pipeline primer (circom/snarkjs demo)
- Day 010: MEV-aware planning (simulation only)

See each day’s `README.md` for goals, acceptance criteria, and stretch tasks.

## Frameworks Matrix
- Agent frameworks: OpenAI Assistants, LangGraph, Autogen, LlamaIndex, CrewAI, Semantic Kernel, Haystack
- Web3 ops: Wallet mgmt, on-chain data, deploys, storage, governance, intents, AA
- Metrics: Task success, safety, cost, latency, reproducibility

Details live in `docs/FRAMEWORKS.md` and scoring in `EVALS.md`.

## Evaluation
- Per-lab `acceptance.md` checklists and artifacts
- Record runs with `scripts/evaluate_agent.py`
- Compare frameworks by lab using the shared rubric

## MCP Servers
We integrate general-purpose MCP servers (filesystem, git, web, sqlite) and design purpose-built Web3 servers (ethereum, solana, ipfs, thegraph, dune, tenderly). See `resources/mcp-servers.md` for the list and `mcp-specs/` for draft tool specs.

## External AgentKits
- Coinbase AgentKit is vendored under `external/coinbase-agentkit` (submodule)
- thirdweb AgentKit and Solana AgentKit: add-on submodules pending URL confirmation

## Contributing
- Keep examples minimal but runnable; link out to heavy stacks
- Prefer templates over one-offs; make it repeatable
- Security first: see `docs/SECURITY_MODEL.md`

---
Maintainers: AI Architects · Open to PRs and issue ideas.
