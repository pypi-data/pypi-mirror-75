# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['owoify']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'owoify',
    'version': '0.3.0',
    'description': 'Cutting edge technologies to owoify your texts',
    'long_description': None,
    'author': 'crinny',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
