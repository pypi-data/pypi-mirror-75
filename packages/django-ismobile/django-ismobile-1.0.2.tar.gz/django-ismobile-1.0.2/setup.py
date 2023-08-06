# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ismobile']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-ismobile',
    'version': '1.0.2',
    'description': 'Middleware for Django.',
    'long_description': '# django-ismobile\n\n\n"is_mobile" middleware for Django\n\n## Requirements\nRequires Django 2.0 or later.\n\n## Installing\n\nInstall with `pip` or your favorite PyPi package manager.\n\n```\npip install django-ismobile\n```\n\n## Using\n\nInclude MobileControlMiddleware into your MIDDLEWARE:\n\n```\nMIDDLEWARE = (\n    ...\n    \'ismobile.middleware.MobileControlMiddleware\',\n    ...\n)\n```\n\n## Config\n\nIn order to change request attribute name, \nset **IS_MOBILE_ATTR_NAME** in django **settings** file.\n\n```\nIS_MOBILE_ATTR_NAME="custom_name"\n```',
    'author': 'Can Sarigol',
    'author_email': 'ertugrulsarigol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cansarigol/django-ismobile',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
