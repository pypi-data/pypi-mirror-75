from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Samples:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        return {}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Samples:
        return Samples()
