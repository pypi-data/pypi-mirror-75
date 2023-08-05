# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbsearch', 'bbsearch.api', 'bbsearch.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'bbsearch',
    'version': '0.0.0',
    'description': 'A client library and CLI for accessing the Bug Bounty Search API',
    'long_description': '# bbsearch\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
