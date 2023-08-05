# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsc', 'gsc.exercises']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['gsc = gsc.cli:main']}

setup_kwargs = {
    'name': 'gsc',
    'version': '1.0.2',
    'description': 'Git for Scientists practical exercise helper.',
    'long_description': '# gsc\n\nGit for Scientists practical exercise helper.\n\nSee https://www.gitscientist.com for more.\n',
    'author': 'Daniel Tipping',
    'author_email': 'daniel@gitscientist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.gitscientist.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
