# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_message_channels']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'pyvarint>=0.0.1-alpha.2,<0.0.2']

setup_kwargs = {
    'name': 'simple-message-channels',
    'version': '0.0.1a2',
    'description': 'Sans I/O wire protocol for Hypercore',
    'long_description': '# simple-message-channels\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/simple-message-channels/status.svg)](https://drone.autonomic.zone/hyperpy/simple-message-channels)\n\n## Sans I/O wire protocol for Hypercore\n\n## Install\n\n```sh\n$ pip install simple-message-channels\n```\n\n## Example\n\n```python\nfrom simple_message_channels import SimpleMessageChannel\n\nsmc1 = SimpleMessageChannel()\nsmc2 = SimpleMessageChannel()\n\npayload = smc1.send(0, 1, b"foo")\nprint(f"sent: {payload}")\n\nfor idx in range(0, len(payload)):\n    smc2.recv(payload[idx : idx + 1])\nprint(f"received: {smc2.messages}")\n```\n\nOutput:\n\n```sh\nsent: b\'\\x04\\x01foo\'\nreceived: [(0, 1, b\'foo\')]\n```\n',
    'author': 'decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/simple-message-channels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
