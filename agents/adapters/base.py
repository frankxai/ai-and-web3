from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AgentAdapter(ABC):
    @abstractmethod
    def plan(self, task: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return a sequence of steps the agent intends to execute."""

    @abstractmethod
    def act(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one step and return artifacts."""

    @abstractmethod
    def evaluate(self, artifacts: Dict[str, Any]) -> Dict[str, Any]:
        """Map artifacts to metrics (success, safety, cost, latency)."""

