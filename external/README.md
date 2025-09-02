# External Dependencies and Submodules

High-value repos vendored as submodules to accelerate examples:

## Agent Kits
- Coinbase AgentKit — external/coinbase-agentkit (submodule)
- thirdweb AgentKit — external/thirdweb-agentkit (submodule)
- Solana AgentKit — external/solana-agentkit (submodule)

## MCP Servers (TBD)
- Model Context Protocol org — add specific servers as submodules when selected

Initialize submodules after clone:
```
git submodule update --init --recursive
```

Note: If submodule add fails due to auth or repo moves, update the URLs in `.gitmodules` and re-run the init command.
