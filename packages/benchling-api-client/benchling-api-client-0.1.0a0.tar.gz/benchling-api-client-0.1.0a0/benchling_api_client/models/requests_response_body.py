from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .request import Request


@dataclass
class RequestsResponseBody:
    """  """

    next_token: Optional[str] = None
    requests: Optional[List[Request]] = None

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        if self.requests is None:
            requests = None
        else:
            requests = []
            for requests_item_data in self.requests:
                requests_item = requests_item_data.to_dict()

                requests.append(requests_item)

        return {
            "nextToken": next_token,
            "requests": requests,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> RequestsResponseBody:
        next_token = d.get("nextToken")

        requests = []
        for requests_item_data in d.get("requests") or []:
            requests_item = Request.from_dict(requests_item_data)

            requests.append(requests_item)

        return RequestsResponseBody(next_token=next_token, requests=requests,)
