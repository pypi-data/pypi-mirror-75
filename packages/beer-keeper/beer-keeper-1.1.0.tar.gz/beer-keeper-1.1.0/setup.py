# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['beer_keeper']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0',
 'pydocstyle>=5.0.2,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'sphinx-automodapi>=0.12,<0.13']

entry_points = \
{'console_scripts': ['BeerKeeper = beer_keeper.cli:app']}

setup_kwargs = {
    'name': 'beer-keeper',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vlad David',
    'author_email': 'vlad.david@complyadvantage.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
