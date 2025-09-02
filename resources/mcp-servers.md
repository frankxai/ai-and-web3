# MCP Servers (Model Context Protocol)

This list tracks useful MCP servers today and proposed Web3-focused servers.

## General-purpose servers (ready to use)
- Model Context Protocol (org hub) — https://github.com/modelcontextprotocol
- Filesystem MCP: local file read/write
- Git MCP: clone, branch, diff, commit operations
- Web/Fetch MCP: HTTP requests, scraping with restrictions
- SQLite MCP: structured storage and simple analytics

## Web3-focused (proposed/spec)
- mcp-ethereum: JSON-RPC (read + safe-write), ABIs, ENS
- mcp-solana: RPC, program introspection, SPL token helpers
- mcp-ipfs: pin/add/get, directory ops, gateways
- mcp-thegraph: subgraph search + query execution
- mcp-dune: query run + cached result fetch (API)
- mcp-tenderly: simulation, fork actions, debug traces

## How to add as submodules
- Decide on the server repo under the MCP org or vendor
- Add as submodule under `external/mcp/<name>`
- Wire tool schemas under `mcp-specs/` and reference in labs

Each server should expose:
- Tool schema: clear input/output types; guardrails on write ops
- Simulation-first flows for state changes
- Config via env and per-lab config files

If you maintain or recommend an existing MCP server for any of the above, open a PR to add it here.
