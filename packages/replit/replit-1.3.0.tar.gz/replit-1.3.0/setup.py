# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['replit', 'replit.audio', 'replit.database', 'replit.maqpy']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'replit',
    'version': '1.3.0',
    'description': 'A library for interacting with features of repl.it',
    'long_description': '# replit-py\n\nReplit-py is a python library designed to be run from a repl on [repl.it](https://repl.it).\n\n### Features\n\n- Fully featured database client for Repl DB\n- Audio library which can play tones and files\n- Clear the terminal\n\n### Documentation\n\nThe documentation can be found [here](https://replit-python-docs.scoder12.repl.co).\n',
    'author': 'mat',
    'author_email': 'pypi@matdoes.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/replit/replit-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
