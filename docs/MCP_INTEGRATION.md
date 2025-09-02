# MCP Integration Guide

This repo uses MCP servers to standardize tool access for agents. Start with generic servers (filesystem, git, web, sqlite) and extend with Web3-focused servers.

## Steps
1) Install your MCP client/runtime per framework (e.g., Assistants/LangGraph plugin).
2) Configure server endpoints and auth in `.env` or per-lab configs.
3) Register tools with strict schemas (see `mcp-specs/*`).
4) Enforce simulation gates and spend policies for write ops.

## Recommended servers
- Filesystem MCP: local file read/write (scoped to repo)
- Git MCP: clone, branch, diff, commit
- Web MCP: HTTP fetch with domain allowlist
- SQLite MCP: local data storage
- Web3 (proposed): ethereum, solana, ipfs, thegraph, dune, tenderly

## Safety
- Use allowlists/denylists for network calls
- Require simulation and policy sign-off for state changes
