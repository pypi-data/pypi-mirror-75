# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['infrascrap']

package_data = \
{'': ['*']}

install_requires = \
['bitwarden-keyring>=0.3.0,<0.4.0',
 'keyring>=21.2.1,<22.0.0',
 'python-telegram-bot>=12.8,<13.0',
 'pyvirtualdisplay>=1.3.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'infrascrap',
    'version': '0.1.12',
    'description': 'Scraping infrastructure',
    'long_description': None,
    'author': 'Sivan Becker',
    'author_email': 'sivanbecker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
