# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_single_element_destructuring']

package_data = \
{'': ['*']}

install_requires = \
['astroid>=2.3.3,<3.0.0', 'pylint>=2.4.4,<3.0.0', 'pytest-cov>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'pylint-single-element-destructuring',
    'version': '0.1.2a2',
    'description': '',
    'long_description': None,
    'author': 'd1618033',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
