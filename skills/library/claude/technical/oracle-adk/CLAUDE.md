# Oracle ADK Expert

Build production agentic applications on OCI using Oracle Agent Development Kit with multi-agent orchestration, function tools, and enterprise patterns.

## Quick Reference

**When to Use**: Building AI agents on Oracle Cloud Infrastructure
**Key Service**: OCI Generative AI Agents Service + ADK
**Language**: Python 3.10+

## Core Capabilities

1. **Multi-Turn Conversations** - Context-aware agents
2. **Multi-Agent Orchestration** - Routing, hierarchical, parallel patterns
3. **Function Tools** - Custom capabilities via decorators
4. **Deterministic Workflows** - Explicit control flow

## Key Patterns

```python
# Basic Agent
from oci_adk import Agent

agent = Agent(
    name="support_agent",
    model="cohere.command-r-plus",
    system_prompt="You are a helpful support agent"
)

# Function Tool
@FunctionTool(name="lookup_order")
def lookup_order(order_id: str):
    return db.get_order(order_id)
```

## Decision Guide

**Use Oracle ADK when**:
- Building on OCI infrastructure
- Integrating with Oracle Fusion/Cloud apps
- Need enterprise-grade security
- Want code-first agent development

**Consider alternatives**:
- Not on Oracle Cloud → Claude SDK or OpenAI Agents SDK
- Need visual builder → Google Agent Builder
- Framework-agnostic design → Oracle Agent Spec

## Related Skills
- `oci-services-expert` - OCI infrastructure
- `oracle-agent-spec` - Declarative agent definitions
- `oracle-database-expert` - ADB integration

---

*See SKILL.md for comprehensive documentation, patterns, and examples.*
