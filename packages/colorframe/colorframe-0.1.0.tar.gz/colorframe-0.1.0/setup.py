# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colorframe']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0', 'joblib>=0.16.0,<0.17.0', 'loguru>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'colorframe',
    'version': '0.1.0',
    'description': 'Python utility to add borders to my photography pictures',
    'long_description': None,
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
