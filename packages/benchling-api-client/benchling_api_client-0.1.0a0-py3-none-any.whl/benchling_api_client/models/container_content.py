from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast, Dict, Optional, Union

from .batch import Batch
from .custom_entity import CustomEntity
from .measurement import Measurement
from .protein import Protein
from .sequence import Sequence


@dataclass
class ContainerContent:
    """  """

    concentration: Measurement
    batch: Optional[Union[Optional[Batch]]] = None
    entity: Optional[Union[Optional[Sequence], Optional[Protein], Optional[CustomEntity]]] = None

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        if self.batch is None:
            batch = None
        else:
            batch = self.batch.to_dict() if self.batch else None

        if self.entity is None:
            entity = None
        elif isinstance(self.entity, Optional[Sequence]):
            entity = self.entity.to_dict() if self.entity else None

        elif isinstance(self.entity, Optional[Protein]):
            entity = self.entity.to_dict() if self.entity else None

        else:
            entity = self.entity.to_dict() if self.entity else None

        return {
            "concentration": concentration,
            "batch": batch,
            "entity": entity,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> ContainerContent:
        concentration = Measurement.from_dict(d["concentration"])

        def _parse_batch(data: Dict[str, Any]) -> Optional[Union[Optional[Batch]]]:
            batch: Optional[Union[Optional[Batch]]]
            batch = None
            if d.get("batch") is not None:
                batch = Batch.from_dict(cast(Dict[str, Any], d.get("batch")))

            return batch

        batch = _parse_batch(d.get("batch"))

        def _parse_entity(
            data: Dict[str, Any]
        ) -> Optional[Union[Optional[Sequence], Optional[Protein], Optional[CustomEntity]]]:
            entity: Optional[Union[Optional[Sequence], Optional[Protein], Optional[CustomEntity]]]
            try:
                entity = None
                if d.get("entity") is not None:
                    entity = Sequence.from_dict(cast(Dict[str, Any], d.get("entity")))

                return entity
            except:
                pass
            try:
                entity = None
                if d.get("entity") is not None:
                    entity = Protein.from_dict(cast(Dict[str, Any], d.get("entity")))

                return entity
            except:
                pass
            entity = None
            if d.get("entity") is not None:
                entity = CustomEntity.from_dict(cast(Dict[str, Any], d.get("entity")))

            return entity

        entity = _parse_entity(d.get("entity"))

        return ContainerContent(concentration=concentration, batch=batch, entity=entity,)
