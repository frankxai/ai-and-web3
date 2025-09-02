#!/usr/bin/env bash
set -euo pipefail

if [ -z "${FORK_RPC_URL:-}" ]; then
  echo "Set FORK_RPC_URL to a mainnet/testnet RPC URL" >&2
  exit 1
fi

anvil --fork-url "$FORK_RPC_URL" --chain-id 1

