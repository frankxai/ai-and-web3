# AgentKits Integration

This repo uses AgentKits to accelerate onchain actions for agents.

## Included as submodules
- Coinbase AgentKit — `external/coinbase-agentkit`

## Pending add (confirm URLs)
- thirdweb AgentKit — `external/thirdweb-agentkit`
- Solana AgentKit — `external/solana-agentkit`

## Integration steps (generic)
1) Initialize submodules: `git submodule update --init --recursive`
2) Follow AgentKit README to install dependencies
3) Expose tool-like wrappers (e.g., `wallet.transfer`, `nft.mint`) as MCP tools or framework-native tools
4) Add policy gates (spend limits, allowlists) and simulation-first flows
5) Write minimal adapters per framework using the common interface in `agents/adapters/`

## Safety notes
- Use testnets or local forks; never commit private keys
- Prefer dry-run (Anvil/Tenderly) before real submissions
- Apply explicit policies from `agents/policies.py`
