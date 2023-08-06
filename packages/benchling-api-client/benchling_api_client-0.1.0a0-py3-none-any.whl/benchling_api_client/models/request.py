from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, cast, Dict, List, Optional, Union

from .request_status import RequestStatus
from .sample_groups import SampleGroups
from .samples import Samples
from .schema_summary import SchemaSummary
from .team_summary import TeamSummary
from .user_summary import UserSummary


@dataclass
class Request:
    """  """

    assignees: Optional[List[Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]]] = None
    created_at: Optional[datetime] = None
    creator: Optional[UserSummary] = None
    display_id: Optional[str] = None
    fields: Optional[Dict[Any, Any]] = None
    id: Optional[str] = None
    need_by: Optional[date] = None
    project_id: Optional[str] = None
    request_status: Optional[RequestStatus] = None
    requestor: Optional[UserSummary] = None
    sample_groups: Optional[SampleGroups] = None
    samples: Optional[Samples] = None
    schema: Optional[SchemaSummary] = None
    web_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.assignees is None:
            assignees = None
        else:
            assignees = []
            for assignees_item_data in self.assignees:
                if assignees_item_data is None:
                    assignees_item = None
                elif isinstance(assignees_item_data, Optional[UserSummary]):
                    assignees_item = assignees_item_data.to_dict() if assignees_item_data else None

                else:
                    assignees_item = assignees_item_data.to_dict() if assignees_item_data else None

                assignees.append(assignees_item)

        created_at = self.created_at.isoformat() if self.created_at else None

        creator = self.creator.to_dict() if self.creator else None

        display_id = self.display_id
        fields = self.fields
        id = self.id
        need_by = self.need_by.isoformat() if self.need_by else None

        project_id = self.project_id
        request_status = self.request_status.value if self.request_status else None

        requestor = self.requestor.to_dict() if self.requestor else None

        sample_groups = self.sample_groups.to_dict() if self.sample_groups else None

        samples = self.samples.to_dict() if self.samples else None

        schema = self.schema.to_dict() if self.schema else None

        web_url = self.web_url

        return {
            "assignees": assignees,
            "createdAt": created_at,
            "creator": creator,
            "displayId": display_id,
            "fields": fields,
            "id": id,
            "needBy": need_by,
            "projectId": project_id,
            "requestStatus": request_status,
            "requestor": requestor,
            "sampleGroups": sample_groups,
            "samples": samples,
            "schema": schema,
            "webURL": web_url,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Request:
        assignees = []
        for assignees_item_data in d.get("assignees") or []:

            def _parse_assignees_item(
                data: Dict[str, Any]
            ) -> Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]:
                assignees_item: Optional[Union[Optional[UserSummary], Optional[TeamSummary]]]
                try:
                    assignees_item = None
                    if assignees_item_data is not None:
                        assignees_item = UserSummary.from_dict(cast(Dict[str, Any], assignees_item_data))

                    return assignees_item
                except:
                    pass
                assignees_item = None
                if assignees_item_data is not None:
                    assignees_item = TeamSummary.from_dict(cast(Dict[str, Any], assignees_item_data))

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        created_at = None
        if d.get("createdAt") is not None:
            created_at = datetime.fromisoformat(cast(str, d.get("createdAt")))

        creator = None
        if d.get("creator") is not None:
            creator = UserSummary.from_dict(cast(Dict[str, Any], d.get("creator")))

        display_id = d.get("displayId")

        fields = d.get("fields")

        id = d.get("id")

        need_by = None
        if d.get("needBy") is not None:
            need_by = date.fromisoformat(cast(str, d.get("needBy")))

        project_id = d.get("projectId")

        request_status = None
        if d.get("requestStatus") is not None:
            request_status = RequestStatus(d.get("requestStatus"))

        requestor = None
        if d.get("requestor") is not None:
            requestor = UserSummary.from_dict(cast(Dict[str, Any], d.get("requestor")))

        sample_groups = None
        if d.get("sampleGroups") is not None:
            sample_groups = SampleGroups.from_dict(cast(Dict[str, Any], d.get("sampleGroups")))

        samples = None
        if d.get("samples") is not None:
            samples = Samples.from_dict(cast(Dict[str, Any], d.get("samples")))

        schema = None
        if d.get("schema") is not None:
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], d.get("schema")))

        web_url = d.get("webURL")

        return Request(
            assignees=assignees,
            created_at=created_at,
            creator=creator,
            display_id=display_id,
            fields=fields,
            id=id,
            need_by=need_by,
            project_id=project_id,
            request_status=request_status,
            requestor=requestor,
            sample_groups=sample_groups,
            samples=samples,
            schema=schema,
            web_url=web_url,
        )
