# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['songmam',
 'songmam.api',
 'songmam.facebook',
 'songmam.facebook.entries',
 'songmam.facebook.entries.message',
 'songmam.facebook.messaging',
 'songmam.facebook.messaging.templates',
 'songmam.facebook.messaging.templates.airline',
 'songmam.facebook.messenger_profile']

package_data = \
{'': ['*']}

install_requires = \
['cacheout>=0.11.2,<0.12.0',
 'furl>=2.1.0,<3.0.0',
 'httpx>=0.13.3,<0.14.0',
 'loguru>=0.5.1,<0.6.0',
 'requests>=2.24.0,<3.0.0',
 'starlette>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'songmam',
    'version': '0.8.0',
    'description': 'a fork of FBMQ',
    'long_description': None,
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
