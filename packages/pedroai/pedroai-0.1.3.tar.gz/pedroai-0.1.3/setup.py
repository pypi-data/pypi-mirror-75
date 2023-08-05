# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pedroai']

package_data = \
{'': ['*']}

install_requires = \
['plotnine>=0.6,<0.7', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pedroai',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Pedro Rodriguez',
    'author_email': 'me@pedro.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
