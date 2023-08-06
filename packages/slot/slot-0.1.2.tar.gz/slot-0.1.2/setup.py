# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slot', 'slot.cli', 'slot.cli.stores']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'importlib-metadata>=1.7.0,<2.0.0',
 'python-box>=5.1.0,<6.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0',
 'use-dir>=0.1.4,<0.2.0']

entry_points = \
{'console_scripts': ['slt = slot.cli:cli']}

setup_kwargs = {
    'name': 'slot',
    'version': '0.1.2',
    'description': 'Rotate your files via symlink',
    'long_description': '# slot\n\nRotates a symlink between multiple different possible options.\n\n## Installation\n\n```bash\npip install slot\n```\n\n## Terminology\n\nA `target` is the file name that you are going to be turning into a symbolic link.\n\nA `store` is a repository of data files that act as potential options for a `target`.\n\nAn `option` is a data file inside of a store.\n\n## Usage\n\n### Create a new store\n\n(and optionally ingest current file as an `option`)\n\n```bash\nUsage: slt stores create [OPTIONS] NAME TARGET\n\nOptions:\n  --help  Show this message and exit.\n```\n\n### Add an option to a store\n\n```bash\nUsage: slt stores ingest [OPTIONS] STORE_NAME FILE_NAME\n\nOptions:\n  -n, --name TEXT       Name of the option this file becomes\n  -s, --silent BOOLEAN  Disable user interaction\n  --help                Show this message and exit.\n```\n\n### List stores\n\n```bash\nUsage: slt list [OPTIONS]\n\nOptions:\n  --help  Show this message and exit.\n```\n\n### See available options for a store\n\n```bash\nUsage: slt options [OPTIONS] STORE_NAME\n\nOptions:\n  --help  Show this message and exit.\n```\n',
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/markrawls/slot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
