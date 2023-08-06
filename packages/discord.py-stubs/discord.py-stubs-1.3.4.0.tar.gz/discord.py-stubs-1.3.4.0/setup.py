# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord-stubs']

package_data = \
{'': ['*'], 'discord-stubs': ['ext/*', 'ext/commands/*', 'ext/tasks/*']}

install_requires = \
['mypy>=0.782,<0.783', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'discord.py-stubs',
    'version': '1.3.4.0',
    'description': 'discord.py stubs',
    'long_description': None,
    'author': 'Bryan Forbes',
    'author_email': 'bryan@reigndropsfall.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
