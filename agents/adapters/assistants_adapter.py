"""
Stub adapter for OpenAI Assistants-style flows. Replace with real Assistants API
calls and registered tools (RPC, IPFS, deploy) when connecting the SDK.
"""
from typing import Any, Dict, List
from .base import AgentAdapter


class AssistantsAdapter(AgentAdapter):
    def plan(self, task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"tool": "rpc.transfer", "args": {"to": context.get("to"), "valueWei": 0}}]

    def act(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "step": step}

    def evaluate(self, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        return {"success": True, "latency_ms": 0, "cost": 0}

