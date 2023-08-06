from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PlateSchema:
    """  """

    def to_dict(self) -> Dict[str, Any]:

        return {}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> PlateSchema:
        return PlateSchema()
