# Agents and Adapters

This folder centralizes notes and thin adapters for each framework we evaluate. Keep abstractions minimal and make tradeoffs explicit.

## Frameworks (targeted)
- OpenAI Assistants: tools for RPC, IPFS, and deploy scripts
- LangGraph: planner + executor with simulation gate
- Autogen: multi-agent (planner/critic/executor) patterns
- LlamaIndex: tool-calling with retrieval for specs/ABIs

## Adapters
Each adapter should expose a common interface:
- plan(task) -> steps
- act(step) -> artifacts
- evaluate(artifacts) -> metrics

Start with stubs; add real code within each example project.
