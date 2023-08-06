# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xraysink', 'xraysink.asgi']

package_data = \
{'': ['*']}

install_requires = \
['aws_xray_sdk>=2,<3', 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'xraysink',
    'version': '1.0.0',
    'description': 'Instrument asyncio Python for AWS X-Ray.',
    'long_description': '# xraysink (aka xray-asyncio)\nExtra AWS X-Ray instrumentation for asyncio Python libraries that are not\n(yet) supported by the official\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python) library.\n\n\n## Integrations Supported\n* Generic ASGI-compatible tracing middleware for *any* ASGI-compliant web\n  framework. This has been tested with:\n  - [aiohttp server](https://docs.aiohttp.org/en/stable/)\n  - [FastAPI](https://fastapi.tiangolo.com/)\n\n\n## Installation\nxraysink is distributed as a standard python package through\n[pypi](https://pypi.org/), so you can install it with your favourite Python\npackage manager. For example:\n\n    pip install xraysink \n\n\n## How to use\n\n### FastAPI\nInstrument incoming requests in your FastAPI web server by adding the `xray_middleware`. For example:\n\n    # Basic asyncio X-Ray configuration\n    xray_recorder.configure(context=AsyncContext(), service="my-cute-little-service")\n    \n    # Create a FastAPI app with various middleware\n    app = FastAPI()\n    app.add_middleware(MyTracingDependentMiddleware)  # Any middleware that is added earlier will have the X-Ray tracing context available to it\n    app.add_middleware(BaseHTTPMiddleware, dispatch=xray_middleware)\n\n\n## Licence\nThis project uses the Apache 2.0 licence, to make it compatible with\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python), the\nprimary library for integrating with AWS X-Ray.\n',
    'author': 'Gary Donovan',
    'author_email': 'gazza@gazza.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garyd203/xraysink',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
