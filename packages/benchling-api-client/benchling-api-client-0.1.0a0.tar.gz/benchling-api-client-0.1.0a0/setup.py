# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchling_api_client',
 'benchling_api_client.api',
 'benchling_api_client.async_api',
 'benchling_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'benchling-api-client',
    'version': '0.1.0a0',
    'description': 'A client library for accessing Benchling API',
    'long_description': '# benchling-api-client\nA client library for accessing Benchling API\n\n## Usage\nFirst, create a client:\n\n```python\nfrom benchling_api_client import Client\n\nclient = Client(base_url="https://api.example.com")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom benchling_api_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom benchling_api_client.models import MyDataModel\nfrom benchling_api_client.api.my_tag import get_my_data_model\n\nmy_data: MyDataModel = get_my_data_model(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom benchling_api_client.models import MyDataModel\nfrom benchling_api_client.async_api.my_tag import get_my_data_model\n\nmy_data: MyDataModel = await get_my_data_model(client=client)\n```\n\nThings to know:\n1. Every path/method combo becomes a Python function with type annotations. \n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `benchling_api_client.api.default`\n1. If the API returns a response code that was not declared in the OpenAPI document, a \n    `benchling_api_client.api.errors.ApiResponseError` wil be raised \n    with the `response` attribute set to the `httpx.Response` that was received.\n    \n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`',
    'author': 'Benchling Customer Engineering',
    'author_email': 'ce-team@benchling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
