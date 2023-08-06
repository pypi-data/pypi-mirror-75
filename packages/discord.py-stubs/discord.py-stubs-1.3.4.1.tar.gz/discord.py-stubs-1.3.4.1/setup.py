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
    'version': '1.3.4.1',
    'description': 'discord.py stubs',
    'long_description': '# discord.py-stubs\n\n[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/bryanforbes/discord.py-stubs/blob/master/LICENSE)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nThis package contains type stubs to provide more precise static types and type inference for discord.py.\n\n## Installation\n\n```\npip install discord.py-stubs\n```\n',
    'author': 'Bryan Forbes',
    'author_email': 'bryan@reigndropsfall.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bryanforbes/discord.py-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
