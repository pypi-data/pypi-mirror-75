# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jotbox', 'jotbox.sessions', 'jotbox.whitelist']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2', 'pyjwt>=1,<2']

setup_kwargs = {
    'name': 'jotbox',
    'version': '0.1.1',
    'description': 'JWT library with support for revokable tokens',
    'long_description': '# Jotbox\n\nJWT library for python with support for revokable tokens and idle timeouts\n\nRead more here https://steinitzu.github.io/jotbox\n',
    'author': 'Steinthor Palsson',
    'author_email': 'steini90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
