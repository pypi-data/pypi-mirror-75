from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Measurement:
    """  """

    units: Optional[str] = None
    value: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        units = self.units
        value = self.value

        return {
            "units": units,
            "value": value,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Measurement:
        units = d.get("units")

        value = d.get("value")

        return Measurement(units=units, value=value,)
