# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_hypercore_protocol']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.12.4,<4.0.0']

setup_kwargs = {
    'name': 'simple-hypercore-protocol',
    'version': '0.0.1a2',
    'description': 'The Hypercore protocol state machine',
    'long_description': '# simple-hypercore-protocol\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/simple-hypercore-protocol/status.svg)](https://drone.autonomic.zone/hyperpy/simple-hypercore-protocol)\n\n## The Hypercore protocol state machine\n\n## Install\n\n```sh\n$ pip install simple-hypercore-protocol\n```\n\n## Example\n\n```python\nfrom simple_hypercore_protocol import messages\n\nprint(messages.Request(index=0))\n```\n\nOutput:\n\n```sh\nindex: 0\n```\n',
    'author': 'decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/simple-hypercore-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
