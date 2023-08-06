from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SchemaField:
    """  """

    is_requred: Optional[bool] = None
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        is_requred = self.is_requred
        name = self.name

        return {
            "isRequred": is_requred,
            "name": name,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> SchemaField:
        is_requred = d.get("isRequred")

        name = d.get("name")

        return SchemaField(is_requred=is_requred, name=name,)
