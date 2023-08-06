# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_prune']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['git-prune = git_prune.main:main']}

setup_kwargs = {
    'name': 'git-prune',
    'version': '0.0.6',
    'description': 'Clean up your local git branches to match the remote with one command.',
    'long_description': '# git-prune\n\nClean up your local git branches to match the remote with one command. This tool checks your remote location for current branches, compares this list against the local git branches, and gives you the option to remove all orphaned local branches. \n\n### Installation\n\n`pip3 install git-prune`\n\n### Usage\n\n    1. Navigate to the directory of your local repository copy\n    2. Enter the command "git-prune"\n    3. Confirm removal of branches found',
    'author': 'Richard Soper',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rsoper/git-prune',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
