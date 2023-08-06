from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .schema_field import SchemaField


@dataclass
class Schema:
    """  """

    field_definitions: Optional[List[SchemaField]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    prefix: Optional[str] = None
    registry_id: Optional[str] = None
    type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        if self.field_definitions is None:
            field_definitions = None
        else:
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        id = self.id
        name = self.name
        prefix = self.prefix
        registry_id = self.registry_id
        type = self.type

        return {
            "fieldDefinitions": field_definitions,
            "id": id,
            "name": name,
            "prefix": prefix,
            "registryId": registry_id,
            "type": type,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Schema:
        field_definitions = []
        for field_definitions_item_data in d.get("fieldDefinitions") or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        id = d.get("id")

        name = d.get("name")

        prefix = d.get("prefix")

        registry_id = d.get("registryId")

        type = d.get("type")

        return Schema(
            field_definitions=field_definitions, id=id, name=name, prefix=prefix, registry_id=registry_id, type=type,
        )
