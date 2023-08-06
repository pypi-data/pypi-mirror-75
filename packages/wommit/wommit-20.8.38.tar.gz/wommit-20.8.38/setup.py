# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wommit', 'wommit.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'emojis>=0.5.1,<0.6.0',
 'falcon>=2.0.0,<3.0.0',
 'gitpython>=3.1.3,<4.0.0',
 'keyring>=21.2.1,<22.0.0',
 'prompt_toolkit>=3.0.5,<4.0.0',
 'pycalver>=202007.36,<202008.0',
 'questionary>=1.5.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'webtest>=2.0.35,<3.0.0']

entry_points = \
{'console_scripts': ['commit = wommit.cli:c',
                     'shapeit = wommit.cli:cli',
                     'wmt = wommit.cli:c',
                     'wommit = wommit.cli:cli']}

setup_kwargs = {
    'name': 'wommit',
    'version': '20.8.38',
    'description': 'A tool for intuitively writing git commits that adhere to the Conventional Commits standards.',
    'long_description': "# Wommit\n\n**W**rite c**ommit** **t**ool\n\n---\n\n[![PyCalVer 20.08.0031-dev][version_img]][version_ref]\n[![PyPI Releases][pypi_img]][pypi_ref]\n\n#### A package for intuitively formatting appealing commmit messages with emojis, using an assortment of different methods.\n\n![CHECK ME OUT](https://i.imgur.com/VIXvQXY.png)\n\n---\n\n### Example usage:\n\n![EXAMPLE](https://i.imgur.com/EORqAkh.gif)\n\n---\n\n### Commands\n\n`wommit ...`:\n\n- `c`: Commit all staged files using an intuitive drop-down menu or a fast autocompletion prompt.\n\n  *Options:*\n  \n  - `-m`: Use menu mode, overriding default.\n\n  - `-e`: Use autocompletion mode, overriding default.\n  \n  - `-m [MESSAGE]`: Write a manual commit message, and commits if it's in the accepted format, as well as converting known types to emojis. \n  \n  - `-g`: Use global settings and data instead of local.\n\n  - `--test`:  Test either of the modes without commiting.\n  \n   - `--ic`:  Include staged files in the prompt display.\n  \n  \n- `check`: Manually check previously added commit. \n\n  *Options:*\n\n  - `-id [HASH]`: Check a commit message with the specified ID.\n  \n  - `-ids [HASH1] [HASH2]`: Check all commit messages between two IDs (newest ID first).\n\n  - `-m [MESSAGE]`:  Check if the given string passes the check.\n  \n  - `-l`:  Check all local commits that have not been pushed.\n\n- `configure ...`: Opens a prompt for adding/removing types and scopes.\n\n    - `e`: Edit current types and scopes.\n    \n    - `p`: Prints all types and scopes.\n    \n    - `s`: Edit settings.\n\n    *Options:*\n\n  - `-g`: Edit global settings.\n  \n  - `-t`: Manually test the functionality.\n  \n - `format`: Pastes the format a message needs to meet in order to pass the check.\n \n ---\n \n ## Info\n \n Use the [wommit-changelog-action](https://github.com/bkkp/wommit-changelog-action) in your wommit project to automatically release your project with appropriate changelogs.\n\n[version_img]: https://img.shields.io/static/v1.svg?label=Wommit&message=20.08.0031-dev&color=blue\n[version_ref]: https://pypi.org/project/wommit/\n[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg\n[pypi_ref]: https://pypi.org/project/wommit/\n\n",
    'author': 'Zylvian',
    'author_email': 'jovlisen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bkkp/wommit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
