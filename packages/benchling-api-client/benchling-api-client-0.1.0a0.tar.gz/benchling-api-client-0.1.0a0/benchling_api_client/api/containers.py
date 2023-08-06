from typing import Any, cast, Dict

import httpx

from ..client import Client
from ..errors import ApiResponseError
from ..models.container import Container


def get_container(*, client: Client, container_id: str,) -> Container:

    """ get a container by id """
    url = "{}/containers/{container_id}".format(client.base_url, container_id=container_id)

    response = httpx.get(url=url, headers=client.get_headers(),)

    if response.status_code == 200:
        return Container.from_dict(cast(Dict[str, Any], response.json()))
    else:
        raise ApiResponseError(response=response)
