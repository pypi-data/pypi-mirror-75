from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SchemaSummary:
    """  """

    id: Optional[str] = None
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        return {
            "id": id,
            "name": name,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> SchemaSummary:
        id = d.get("id")

        name = d.get("name")

        return SchemaSummary(id=id, name=name,)
