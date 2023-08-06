# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongoset']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=1.16.0,<2.0.0',
 'pymongo>=3.10.1,<4.0.0',
 'pytest-race>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'mongoset',
    'version': '0.2.3',
    'description': 'Pythonic wrapper around pymongo that can act as a drop-in replacement for dataset',
    'long_description': '## mongoset\n\n![Build](https://github.com/TadpoleTutoring/mongodb-dataset/workflows/Python%20testing%20and%20linting/badge.svg)\n[![codecov](https://codecov.io/gh/TadpoleTutoring/mongodb-dataset/branch/master/graph/badge.svg?token=kh26hWszR0)](https://codecov.io/gh/TadpoleTutoring/mongodb-dataset)\n\n\nPythonic wrapper around pymongo that can act as a drop-in replacement for dataset \n',
    'author': 'InnovativeInventor',
    'author_email': 'root@max.fan',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TadpoleTutoring/mongoset',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
