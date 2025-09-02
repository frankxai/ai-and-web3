# Agent Patterns for Web3

Reusable patterns for agents that read, reason, and act on-chain.

## Patterns
- Retriever-Toolformer: retrieve on-chain/off-chain context; plan tools; act
- Planner-Executor: separate high-level plan from tool execution steps
- Critic-Refiner: self-critique outputs before irreversible actions
- Simulator-Gate: simulate tx and only continue on policy-compliant results

## Tooling
- Data: RPC, The Graph, Dune
- State change: ethers.js / web3.py / viem / Foundry scripts
- Storage: IPFS/Arweave
- Governance: Snapshot/Compound/SAFE modules

## Framework notes
See `agents/README.md` for framework comparisons and adapters.
