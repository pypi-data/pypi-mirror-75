# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbrecon', 'bbrecon.api', 'bbrecon.models', 'bin']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0',
 'pydantic>=1.6.1,<2.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'typer[all]>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['bbrecon = bin.app:main']}

setup_kwargs = {
    'name': 'bbrecon',
    'version': '0.0.0.4',
    'description': 'A client library and CLI for accessing the Bug Bounty Recon API',
    'long_description': '# bbrecon\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
