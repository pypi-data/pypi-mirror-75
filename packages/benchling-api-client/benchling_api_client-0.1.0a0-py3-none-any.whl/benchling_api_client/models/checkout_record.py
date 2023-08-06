from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast, Dict, Optional, Union

from .status import Status
from .team_summary import TeamSummary
from .user_summary import UserSummary


@dataclass
class CheckoutRecord:
    """  """

    comment: str
    modified_at: str
    status: Status
    assignee: Optional[Union[Optional[UserSummary], Optional[TeamSummary]]] = None

    def to_dict(self) -> Dict[str, Any]:
        comment = self.comment
        modified_at = self.modified_at
        status = self.status.value

        if self.assignee is None:
            assignee = None
        elif isinstance(self.assignee, Optional[UserSummary]):
            assignee = self.assignee.to_dict() if self.assignee else None

        else:
            assignee = self.assignee.to_dict() if self.assignee else None

        return {
            "comment": comment,
            "modifiedAt": modified_at,
            "status": status,
            "assignee": assignee,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> CheckoutRecord:
        comment = d["comment"]

        modified_at = d["modifiedAt"]

        status = Status(d["status"])

        def _parse_assignee(data: Dict[str, Any]) -> Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]:
            assignee: Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]
            try:
                assignee = None
                if d.get("assignee") is not None:
                    assignee = UserSummary.from_dict(cast(Dict[str, Any], d.get("assignee")))

                return assignee
            except:
                pass
            assignee = None
            if d.get("assignee") is not None:
                assignee = TeamSummary.from_dict(cast(Dict[str, Any], d.get("assignee")))

            return assignee

        assignee = _parse_assignee(d.get("assignee"))

        return CheckoutRecord(comment=comment, modified_at=modified_at, status=status, assignee=assignee,)
