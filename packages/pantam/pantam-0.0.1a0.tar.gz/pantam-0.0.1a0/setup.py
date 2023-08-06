# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pantam', 'pantam.services']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'colored>=1.4.2,<2.0.0',
 'shellingham>=1.3.2,<2.0.0',
 'starlette>=0.13.6,<0.14.0',
 'typer>=0.3.1,<0.4.0',
 'uvicorn>=0.11.6,<0.12.0']

entry_points = \
{'console_scripts': ['pantam = cli:run']}

setup_kwargs = {
    'name': 'pantam',
    'version': '0.0.1a0',
    'description': 'The microframework for microservices',
    'long_description': None,
    'author': 'Matt Davies',
    'author_email': 'matt@filament.so',
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
