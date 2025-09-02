# Getting Started

## Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (for local services like IPFS or Postgres if used)
- EVM toolchain: Foundry (recommended) or Hardhat
- Optional: Solana CLI + Anchor for Solana labs

## Install toolchains
- Foundry: https://book.getfoundry.sh/getting-started/installation
- Hardhat: https://hardhat.org
- Solana: https://docs.solana.com/cli/install-solana-cli
- IPFS Desktop/CLI: https://docs.ipfs.tech/install/

## Repo layout
See the root `README.md` for the high-level map. Labs are under `labs/`, each with clear goals, checklists, and acceptance criteria.

## Working locally
1) Create a Python virtualenv for scripts
2) Run Anvil (local EVM) for EVM labs: `anvil`
3) Copy `.env.example` to `.env` within a lab when present
4) Follow the lab’s `README.md` and `acceptance.md`

## MCP servers
We’ll use general-purpose servers (filesystem, git, web, sqlite) and design Web3-specific servers. If you have existing MCP servers (e.g., for Ethereum RPC or IPFS), link them in `resources/mcp-servers.md` and wire them in lab configs.

## Safety and keys
Never commit private keys. Use local test wallets and testnets. See `docs/SECURITY_MODEL.md`.
