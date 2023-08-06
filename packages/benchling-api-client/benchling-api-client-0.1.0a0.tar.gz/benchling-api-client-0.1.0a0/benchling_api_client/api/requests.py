from typing import Any, cast, Dict, Optional

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.request import Request
from ..models.request_status import RequestStatus
from ..models.requests_response_body import RequestsResponseBody


def list_requests(
    *,
    client: Client,
    schema_id: str,
    request_status: Optional[RequestStatus] = None,
    min_created_time: Optional[int] = None,
    max_created_time: Optional[int] = None,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> RequestsResponseBody:

    """ List requests """
    url = "{}/requests".format(client.base_url)

    json_request_status = request_status.value if request_status else None

    params: Dict[str, Any] = {
        "schemaId": schema_id,
    }
    if request_status is not None:
        params["requestStatus"] = json_request_status
    if min_created_time is not None:
        params["minCreatedTime"] = min_created_time
    if max_created_time is not None:
        params["maxCreatedTime"] = max_created_time
    if next_token is not None:
        params["nextToken"] = next_token
    if page_size is not None:
        params["pageSize"] = page_size

    response = httpx.get(url=url, headers=client.get_headers(), params=params,)

    if response.status_code == 200:
        return RequestsResponseBody.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)


def get_request(*, client: Client, request_id: str,) -> Request:

    """ Get a request by ID """
    url = "{}/requests/{request_id}".format(client.base_url, request_id=request_id)

    response = httpx.get(url=url, headers=client.get_headers(),)

    if response.status_code == 200:
        return Request.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
