# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipver']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0', 'gitpython>=3.1.7,<4.0.0']

entry_points = \
{'console_scripts': ['pipver = bin.pipver:main']}

setup_kwargs = {
    'name': 'pipver',
    'version': '0.1.10',
    'description': 'Python package versioning made easy',
    'long_description': None,
    'author': 'John Shanahan',
    'author_email': 'shanahan.jrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
