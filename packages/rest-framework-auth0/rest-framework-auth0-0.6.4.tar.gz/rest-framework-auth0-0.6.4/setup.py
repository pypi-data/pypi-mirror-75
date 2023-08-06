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
    'version': '0.6.4',
    'description': 'This library let you to authenticate an specific user on DRF based on the JWT Token returned by Auth0 Javascript libraries.',
    'long_description': "djangorestframework-auth0\n=====\n___\n\nThis library let you to **authenticate** an specific user on DRF based on the JWT Token returned by Auth0 Javascript libraries.\n\n![Logo](docs/logo.png)\n\nInstallation\n-----------\n\n1. Using `pip` to install current release:\n``` shell\npip install rest_framework_auth0\n```\n\n2. Using `pip` to install development version:\n``` shell\npip install git+https://github.com/mcueto/djangorestframework-auth0/\n```\n\n\nQuick start\n-----------\n\n1. Make sure `django.contrib.auth` in on INSTALLED_APPS setting, otherwise add it by your own:\n``` python\nINSTALLED_APPS = [\n    ...\n    'django.contrib.auth',\n    ...\n]\n```\nThis will allow us to login as an specific user as well as auto-creating users when they don't exist\n\n1. Add `rest_framework_auth0` to your `INSTALLED_APPS` setting:\n``` python\nINSTALLED_APPS = [\n    ...,\n    'rest_framework_auth0',\n]\n```\n\n2. Add `Auth0JSONWebTokenAuthentication` in your DEFAULT_AUTHENTICATION_CLASSES located at settings.py from your project:\n``` python\nREST_FRAMEWORK = {\n    ...,\n    'DEFAULT_AUTHENTICATION_CLASSES': (\n        ...,\n        'rest_framework_auth0.authentication.Auth0JSONWebTokenAuthentication',\n    ),\n}\n```\n\n3. Add your `CLIENTS` & `MANAGEMENT_API` settings in your settings.py file:\n```python\n# Import cryptography libraries\nfrom cryptography.x509 import load_pem_x509_certificate\nfrom cryptography.hazmat.backends import default_backend\n# Read the your Auth0 client PEM certificate\ncertificate_text = open('rsa_certificates/certificate.pem', 'rb').read()\ncertificate = load_pem_x509_certificate(certificate_text, default_backend())\n# Get your PEM certificate public_key\ncertificate_publickey = certificate.public_key()\n#\n#\n# AUTH0 SETTINGS\nAUTH0 = {\n  'CLIENTS': {\n      'default': {\n          'AUTH0_CLIENT_ID': '<YOUR_AUTH0_CLIENT_ID>',\n          'AUTH0_AUDIENCE': '<YOUR_AUTH0_CLIENT_AUDIENCE>',\n          'AUTH0_ALGORITHM': 'RS256',  # default used in Auth0 apps\n          'PUBLIC_KEY': certificate_publickey',\n      }\n  },\n  # Management API - For roles and permissions validation\n  'MANAGEMENT_API': {\n      'AUTH0_DOMAIN': '<YOUR_AUTH0_DOMAIN>',\n      'AUTH0_CLIENT_ID': '<YOUR_AUTH0_M2M_API_MANAGEMENT_CLIENT_ID>',\n      'AUTH0_CLIENT_SECRET': '<YOUR_AUTH0_M2M_API_MANAGEMENT_CLIENT_SECRET>'\n  },\n}\n```\n\n4. Add the `Authorization` Header to all of your REST API request, prefixing `Bearer` to your token(default in common REST clients & Postman):\n```\nAuthorization: Bearer <AUTH0_GIVEN_TOKEN>\n```\n\n5. That's it, now only your Auth0 users can request data to your DRF endpoints\n\n```\nNOTE: In order to get the token authentication, the 'django.contrib.auth' app models migrations must be applied(python manage.py migrate).\n```\n\nUse cases\n-----------\n- [Use cases can be found here](docs/use_cases.md)\n\nSample Project\n-----------\nA sample project can be found [here][sample]\n\n[sample]: https://github.com/mcueto/djangorestframework-auth0_sample\n",
    'author': 'Marcelo Cueto',
    'author_email': 'cueto@live.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
