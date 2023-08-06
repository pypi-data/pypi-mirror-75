# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigmalint', 'sigmalint.schema']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pyrx>=0.3.0,<1.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['sigmalint = sigmalint.sigmalint:cli']}

setup_kwargs = {
    'name': 'sigmalint',
    'version': '0.2.0',
    'description': 'A simple linter for Sigma rules',
    'long_description': None,
    'author': 'Ryan Plas',
    'author_email': 'ryan.plas@stage2sec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
