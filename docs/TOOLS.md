# Tool Registry and Integration

This repo exposes a simple tool registry for EVM operations. Agents (Assistants, LangGraph, etc.) or MCP servers can call these uniformly.

## Tools
- `evm.get_balance` — input: `{ address }` — output: `{ address, wei }`
- `evm.simulate_transfer` — input: `{ to, value_wei }` — output: `{ ok, estimated_gas|error }`
- `evm.send_transfer` — input: `{ to, value_wei, max_value_wei }` — output: tx receipt

Schemas live in `agents/tools/schema/` for tool registration.

## CLI usage
- Balance: `python agents/registry.py evm.get_balance '{"address":"0x..."}'`
- Simulate: `python agents/registry.py evm.simulate_transfer '{"to":"0x...","value_wei":0}'`
- Send: `python agents/registry.py evm.send_transfer '{"to":"0x...","value_wei":1,"max_value_wei":1000}'`

Env: `EVM_RPC_URL`, `PRIVATE_KEY` must be set for transfer/simulate.

## Integration patterns
- Assistants: register these schemas as tools and route tool calls to `agents/registry.py`
- LangGraph: create nodes that invoke the registry and pass artifacts forward
- MCP: wrap these functions in a server with the same JSON schemas and add policy gates

## Safety
- Always simulate first; set `max_value_wei` to enforce spend limits
- Prefer local forks or testnets while developing
