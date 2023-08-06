from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast, Dict, List, Optional, Union

from .archive_record import ArchiveRecord
from .checkout_record import CheckoutRecord
from .container_content import ContainerContent
from .fields import Fields
from .measurement import Measurement
from .user_summary import UserSummary


@dataclass
class Container:
    """  """

    barcode: str
    checkout_record: CheckoutRecord
    created_at: str
    creator: UserSummary
    fields: Fields
    id: str
    modified_at: str
    name: str
    parent_storage_id: str
    parent_storage_schema: Dict[Any, Any]
    schema: Dict[Any, Any]
    volume: Measurement
    archive_record: Optional[Union[Optional[ArchiveRecord]]] = None
    contents: Optional[List[ContainerContent]] = None
    project_id: Optional[str] = None
    web_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        barcode = self.barcode
        checkout_record = self.checkout_record.to_dict()

        created_at = self.created_at
        creator = self.creator.to_dict()

        fields = self.fields.to_dict()

        id = self.id
        modified_at = self.modified_at
        name = self.name
        parent_storage_id = self.parent_storage_id
        parent_storage_schema = self.parent_storage_schema
        schema = self.schema
        volume = self.volume.to_dict()

        if self.archive_record is None:
            archive_record = None
        else:
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        if self.contents is None:
            contents = None
        else:
            contents = []
            for contents_item_data in self.contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

        project_id = self.project_id
        web_url = self.web_url

        return {
            "barcode": barcode,
            "checkoutRecord": checkout_record,
            "createdAt": created_at,
            "creator": creator,
            "fields": fields,
            "id": id,
            "modifiedAt": modified_at,
            "name": name,
            "parentStorageId": parent_storage_id,
            "parentStorageSchema": parent_storage_schema,
            "schema": schema,
            "volume": volume,
            "archiveRecord": archive_record,
            "contents": contents,
            "projectId": project_id,
            "webURL": web_url,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Container:
        barcode = d["barcode"]

        checkout_record = CheckoutRecord.from_dict(d["checkoutRecord"])

        created_at = d["createdAt"]

        creator = UserSummary.from_dict(d["creator"])

        fields = Fields.from_dict(d["fields"])

        id = d["id"]

        modified_at = d["modifiedAt"]

        name = d["name"]

        parent_storage_id = d["parentStorageId"]

        parent_storage_schema = d["parentStorageSchema"]

        schema = d["schema"]

        volume = Measurement.from_dict(d["volume"])

        def _parse_archive_record(data: Dict[str, Any]) -> Optional[Union[Optional[ArchiveRecord]]]:
            archive_record: Optional[Union[Optional[ArchiveRecord]]]
            archive_record = None
            if d.get("archiveRecord") is not None:
                archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], d.get("archiveRecord")))

            return archive_record

        archive_record = _parse_archive_record(d.get("archiveRecord"))

        contents = []
        for contents_item_data in d.get("contents") or []:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        project_id = d.get("projectId")

        web_url = d.get("webURL")

        return Container(
            barcode=barcode,
            checkout_record=checkout_record,
            created_at=created_at,
            creator=creator,
            fields=fields,
            id=id,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            parent_storage_schema=parent_storage_schema,
            schema=schema,
            volume=volume,
            archive_record=archive_record,
            contents=contents,
            project_id=project_id,
            web_url=web_url,
        )
