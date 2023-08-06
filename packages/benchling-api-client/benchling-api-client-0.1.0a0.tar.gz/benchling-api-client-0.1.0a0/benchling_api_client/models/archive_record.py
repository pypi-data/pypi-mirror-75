from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ArchiveRecord:
    """  """

    reason: str

    def to_dict(self) -> Dict[str, Any]:
        reason = self.reason

        return {
            "reason": reason,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ArchiveRecord:
        reason = d["reason"]

        return ArchiveRecord(reason=reason,)
