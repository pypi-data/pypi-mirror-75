# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python_test']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'marshmallow>=3.7.1,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python-test = '
                     'hypermodern_python_test.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python-test',
    'version': '0.1.5',
    'description': 'The hypermodern Python project',
    'long_description': '# hypermodern-python test\n[![Tests](https://github.com/bluemania/hypermodern-python/workflows/Tests/badge.svg)](https://github.com/bluemania/hypermodern-python/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/bluemania/hypermodern-python/branch/master/graph/badge.svg)](https://codecov.io/gh/bluemania/hypermodern-python)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python-test.svg)](https://pypi.org/project/hypermodern-python-test/)\n\nLearning about task automation, linting, testing, static checking, documentation and CI!\n',
    'author': 'bluemania',
    'author_email': 'damnthatswack@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bluemania/hypermodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
