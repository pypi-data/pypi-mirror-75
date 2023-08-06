# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hello_smr39_rasa']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'gunicorn>=20.0.4,<21.0.0', 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'hello-smr39-rasa',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
