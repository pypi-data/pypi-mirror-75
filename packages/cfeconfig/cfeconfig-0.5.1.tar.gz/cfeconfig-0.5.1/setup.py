# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfeconfig']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3,<6.0']

setup_kwargs = {
    'name': 'cfeconfig',
    'version': '0.5.1',
    'description': 'Manage app configuration with CLI options, Config File, or Env.',
    'long_description': None,
    'author': 'Matt Chapman',
    'author_email': 'Matt@NinjitsuWeb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matt2000/cfeconfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
