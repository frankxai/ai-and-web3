"""
Stub adapter for LangGraph patterns. Fill in with actual LangGraph graph definitions
when integrating the dependency. Keeps to the common interface from base.AgentAdapter.
"""
from typing import Any, Dict, List
from .base import AgentAdapter


class LangGraphAdapter(AgentAdapter):
    def plan(self, task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"tool": "rpc.balance", "args": {"address": context.get("address")}}]

    def act(self, step: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder; wire to actual tool registry or MCP
        return {"ok": True, "step": step}

    def evaluate(self, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "latency_ms": 0, "cost": 0}

