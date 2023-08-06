from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SampleGroup:
    """  """

    id: Optional[str] = None
    samples: Optional[Dict[Any, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        samples = self.samples

        return {
            "id": id,
            "samples": samples,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> SampleGroup:
        id = d.get("id")

        samples = d.get("samples")

        return SampleGroup(id=id, samples=samples,)
