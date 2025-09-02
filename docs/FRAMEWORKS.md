# Frameworks and Tools Landscape

This matrix helps choose the right stack per task. It’s pragmatic: focus on tool-use reliability, Web3 integrations, and evaluation.

## Agent Frameworks (General)
| Framework        | Strengths | Web3 Fit | Notes |
|------------------|-----------|----------|-------|
| OpenAI Assistants | High-quality tool calling, code interp, retrieval | Good via tools | Great for deterministic tool flows; requires tool adapters for Web3 |
| LangGraph        | Graph-based control, memory, multi-step | Strong | Good for planner-executor patterns, simulation gates |
| Autogen          | Multi-agent orchestration | Medium | Powerful patterns; needs opinionated tooling for Web3 safety |
| LlamaIndex       | Retrieval + tool calling | Medium | Good for spec/ABI retrieval and structured tasks |
| CrewAI           | Role-based agents | Medium | Useful for larger workflows; watch cost/latency |
| Semantic Kernel  | Orchestration, plugins | Medium | Strong .NET/ecosystem integrations |
| Haystack         | RAG pipelines | Low | Great for retrieval, needs tool-use bolting |

## Web3 Libraries and Tooling (EVM)
| Category | Options | Notes |
|---------|---------|-------|
| Clients | ethers.js, viem, web3.py | viem has great typing; web3.py is convenient for Python agents |
| Toolchains | Foundry, Hardhat, ApeWorx, Brownie | Foundry is fast for local loops |
| Security | Slither, Mythril, Echidna | Automate in CI or via agent tools |
| Simulation | Anvil, Hardhat Network, Tenderly | Gate real tx with pre-sim |
| Storage | IPFS, web3.storage, Arweave | Prefer pinning CIDs + immutability |
| Governance | Snapshot, OpenZeppelin Governor, SAFE | Agents draft + submit with approvals |
| AA (4337) | Safe, Biconomy, Pimlico, StackUp | Start on testnet; strict spend rules |

## Solana and Others
| Chain | Tooling | Notes |
|------|---------|-------|
| Solana | Anchor, solana-web3.js, Solana CLI | Fast finality; different agent ops patterns |
| Cosmos | CosmJS, Ignite CLI | Modular app-chains; governance patterns differ |
| Polkadot | Substrate, Polkadot.js | Runtime dev; consider safety implications |

## Example Agent Kits
- Coinbase AgentKit — EVM onchain actions as tools
- thirdweb AgentKit — agent-friendly abstractions
- Base OnchainKit — UX and onchain patterns
- Autonolas — autonomous services

Selection advice
- Start with LangGraph or OpenAI Assistants for Day 001–003
- Use Foundry for local EVM and fast iteration
- Gate all writes with simulation (Anvil/Tenderly) + spend limits
- Prefer typed clients (viem) when using Node; web3.py for Python agents
