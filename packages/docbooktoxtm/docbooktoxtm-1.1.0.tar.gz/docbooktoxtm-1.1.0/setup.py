# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docbooktoxtm']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.51,<2.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'lxml>=4.5.1,<5.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.24.0,<3.0.0',
 'typer[all]>=0.3.0,<0.4.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['docbooktoxtm = docbooktoxtm.main:app']}

setup_kwargs = {
    'name': 'docbooktoxtm',
    'version': '1.1.0',
    'description': '',
    'long_description': "# `docbooktoxtm`\n\nUtility for prepping DocBook XML packages for use as XTM source files.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.\n\n## Prerequisites\n\nInstall docbooktoxtm with ```pip```.\n\n```\n$ pip install docbooktoxtm\n```\nor\n\n```\n$ python3 -m pip install docbooktoxtm\n```\nThe script also requires a GitHub API token be exported as an environment variable named ```github_token```. The script will automatically pick up the token if correctly configured and will route things properly. For information on creating a personal access token, [visit GitHub's help article on the subject for more information.](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)\n\n## Usage\n\n```console\n$ docbooktoxtm [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `resource`: Restructures source file structure for more...\n* `unsource`: Restores target files exported from XTM to...\n\n## `docbooktoxtm resource`\n\nRestructures source file structure for more efficient parsing in XTM.\n\n**Usage**:\n\n```console\n$ docbooktoxtm resource [OPTIONS] TARGET_FNAME\n```\n\n**Options**:\n\n* `TARGET_FNAME`: name of target .zip package  [required]\n* `--help`: Show this message and exit.\n\n## `docbooktoxtm unsource`\n\nRestores target files exported from XTM to original source file structure.\n\n**Usage**:\n\n```console\n$ docbooktoxtm unsource [OPTIONS] COURSE\n```\n\n**Options**:\n\n* `COURSE`: course name or name of source .zip package  [required]\n* `-r, --release-tag TEXT`: optional GitHub release tag\n* `--help`: Show this message and exit.\n\n## Authors\n\n* **Ryan O'Rourke**\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n",
    'author': "Ryan O'Rourke",
    'author_email': 'ryan.orourke@welocalize.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
