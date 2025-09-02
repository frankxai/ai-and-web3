from dataclasses import dataclass
from typing import List


@dataclass
class SpendPolicy:
    max_value_wei: int
    allowlist: List[str]
    denylist: List[str]

    def check(self, to_addr: str, value_wei: int) -> None:
        ta = to_addr.lower()
        if ta in {a.lower() for a in self.denylist}:
            raise ValueError("Destination is denylisted")
        if self.allowlist and ta not in {a.lower() for a in self.allowlist}:
            raise ValueError("Destination not in allowlist")
        if value_wei > self.max_value_wei:
            raise ValueError("Transfer exceeds policy max value")

