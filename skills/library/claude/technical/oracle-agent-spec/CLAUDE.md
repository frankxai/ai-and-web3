# Oracle Agent Spec Expert

Design framework-agnostic AI agents using Oracle's Open Agent Specification for portable, interoperable agentic systems with JSON/YAML definitions.

## Quick Reference

**When to Use**: Need agents that work across multiple frameworks
**Key Innovation**: Write once, deploy anywhere
**Format**: JSON/YAML declarative definitions

## Core Philosophy

**Problem**: Each framework requires different implementation
**Solution**: Unified representation that any runtime can execute
**Benefit**: Author once → Deploy across LangGraph, AutoGen, ADK, custom runtimes

## Key Components

```yaml
# Basic Agent Spec
version: "1.0"
agent:
  name: CustomerSupport
  components:
    classifier:
      type: LLMNode
      model: claude-haiku-4
    router:
      type: ConditionalNode
      conditions:
        - if: "type == 'technical'"
          then: tech_agent
```

## Node Types

| Node | Purpose |
|------|---------|
| `LLMNode` | Text generation |
| `AgentNode` | Multi-turn agent |
| `APINode` | External API calls |
| `WorkflowNode` | Orchestration |
| `ConditionalNode` | Routing |
| `ParallelNode` | Concurrent execution |

## Decision Guide

**Use Agent Spec when**:
- Need framework portability
- Want version-controlled agent definitions
- Building reusable components
- Team collaboration on design

**Combine with**:
- Oracle ADK (OCI deployment)
- LangGraph (state machines)
- MCP (tool standardization)

## Related Skills
- `oracle-adk` - Native OCI deployment
- `mcp-architecture` - Tool integration
- `langgraph-patterns` - Complex workflows

---

*See SKILL.md for comprehensive documentation, node library, and patterns.*
