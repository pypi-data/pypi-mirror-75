# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xraysink', 'xraysink.asgi']

package_data = \
{'': ['*']}

install_requires = \
['aws_xray_sdk>=2,<3']

setup_kwargs = {
    'name': 'xraysink',
    'version': '0.2.0',
    'description': 'Instrument asyncio Python for AWS X-Ray.',
    'long_description': '# xraysink (aka xray-asyncio)\nExtra AWS X-Ray instrumentation for asyncio Python libraries that are not\n(yet) supported by the official\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python)\nlibrary.\n\n\n## Integrations Supported\n* Generic ASGI-compatible tracing middleware for *any* ASGI-compliant web\n  framework. This has been tested with:\n  - [aiohttp](https://docs.aiohttp.org/en/stable/)\n  - [fastapi](https://fastapi.tiangolo.com/)\n\n\n## Licence\nThis project uses the Apache 2.0 licence, to make it compatible with\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python), the\nprimary library for integrating with AWS X-Ray.\n',
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
