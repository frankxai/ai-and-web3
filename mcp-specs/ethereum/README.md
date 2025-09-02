# MCP Ethereum (Draft Spec)

Goal: Provide safe, typed tools for Ethereum JSON-RPC that prioritize read operations and enforce simulation and policy checks for writes.

## Tools (proposed)
- eth_getBalance(addr) -> wei
- eth_call(call) -> returnData
- resolve_abi(address | name) -> abi
- simulate_tx(tx, policy) -> simReport
- send_tx(tx, policy, require_sim_hash) -> txHash

## Policy
- Spend limits (max value, max gas)
- Address allowlist/denylist
- Required simulation hash binding

## Config
- `EVM_RPC_URL`, `CHAIN_ID`, `SIMULATOR` (tenderly/anvil)

See `send_tx.schema.json` for example input/output shapes.
