# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_extract']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.7,<4.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['git-extract = git_extract.cli:cli']}

setup_kwargs = {
    'name': 'git-extract',
    'version': '1.1.3',
    'description': 'Extract files or directories from a git repository',
    'long_description': '[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n[![PyPI version fury.io](https://badge.fury.io/py/git-extract.svg)](https://pypi.org/project/git-extract/)\n\n# git-extract\n\nExtract files or directories from a git repository\n\n\n## Installation\n\n```shell script\n$ pip install git-extract --upgrade\n```\n[Official PyPi Repository]((https://pypi.org/project/git-extract/))\n\n## Usage\n\nExtract files with multiple patterns:\n```shell script\n$ git-extract file https://github.com/mfdeux/git-extract --pattern "*.md" --pattern "*.py" --dest ~/Downloads/test --recursive\n```\n\nExtract directory with pattern:\n```shell script\n$ git-extract dir https://github.com/mfdeux/git-extract --pattern "tests" --dest ~/Downloads/test\n```\n\n## Patterns\n\nMultiple patterns are acceptable -- as many as you want!\n\nYou can think of patterns as filters.  When git-extract is looking throughout the git repository, it will match files or directories based on the patterns supplied.\n\nAll patterns are based on standard Python glob patterns.\n\nYou can read more about how to construct the patterns at:\n[https://docs.python.org/3/library/glob.html](https://docs.python.org/3/library/glob.html)',
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfdeux/git-extract',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
