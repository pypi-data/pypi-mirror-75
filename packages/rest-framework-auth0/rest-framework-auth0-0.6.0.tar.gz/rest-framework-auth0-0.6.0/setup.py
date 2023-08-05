# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_framework_auth0', 'rest_framework_auth0.migrations']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=3.12', 'cryptography>=3', 'django>2.2', 'pyjwt>=1.7']

setup_kwargs = {
    'name': 'rest-framework-auth0',
    'version': '0.6.0',
    'description': 'This library let you to authenticate an specific user on DRF based on the JWT Token returned by Auth0 Javascript libraries.',
    'long_description': None,
    'author': 'Marcelo Cueto',
    'author_email': 'cueto@live.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
