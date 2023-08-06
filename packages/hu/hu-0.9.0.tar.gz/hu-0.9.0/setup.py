# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hu',
    'version': '0.9.0',
    'description': 'Helpful utility software for open source programmers',
    'long_description': None,
    'author': 'Steve Holden',
    'author_email': 'steve@holdenweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
