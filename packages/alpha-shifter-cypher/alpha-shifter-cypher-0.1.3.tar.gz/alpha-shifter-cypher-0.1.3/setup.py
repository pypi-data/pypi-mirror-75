# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpha_shifter_cypher']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['shifty = alpha_shifter_cypher:activate']}

setup_kwargs = {
    'name': 'alpha-shifter-cypher',
    'version': '0.1.3',
    'description': 'An example Python CLI program distributed via PyPI.',
    'long_description': None,
    'author': 'Benjamin Rosen',
    'author_email': 'ben@classy.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
