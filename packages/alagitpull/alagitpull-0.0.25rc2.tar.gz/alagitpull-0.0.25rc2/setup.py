# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alagitpull', 'alagitpull.writers']

package_data = \
{'': ['*'], 'alagitpull': ['static/*']}

install_requires = \
['alabaster<0.8']

entry_points = \
{'console_scripts': ['sphinx_themes = alagitpull:get_path']}

setup_kwargs = {
    'name': 'alagitpull',
    'version': '0.0.25rc2',
    'description': 'Cleverly-named alabaster sub-theme for git-pull projects',
    'long_description': None,
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
