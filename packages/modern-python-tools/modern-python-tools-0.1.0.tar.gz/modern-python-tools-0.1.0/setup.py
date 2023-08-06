# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modern_python_tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.7.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['modern-python-tools = modern_python_tools.console:main']}

setup_kwargs = {
    'name': 'modern-python-tools',
    'version': '0.1.0',
    'description': 'Playing with modern Python tools',
    'long_description': '# modern-python-tools\n\n[![Tests](https://github.com/taquitochowder/modern-python-tools/workflows/Tests/badge.svg)](https://github.com/taquitochowder/modern-python-tools/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/taquitochowder/modern-python-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/taquitochowder/modern-python-tools)\n\n\nPlaying with modern Python tools (<https://cjolowicz.github.io/posts/hypermodern-python-01-setup/>)\n',
    'author': 'Thakee Chowdhury',
    'author_email': 'thakeechow@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taquitochowder/modern-python-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
