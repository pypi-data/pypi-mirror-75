# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpwebpay']

package_data = \
{'': ['*']}

install_requires = \
['cryptography==2.8',
 'invoke>=1.4.1,<2.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'requests==2.23',
 'tox>=3.17.1,<4.0.0']

setup_kwargs = {
    'name': 'gpwebpay',
    'version': '0.1.0',
    'description': 'GPWebPay Gateway access with python',
    'long_description': None,
    'author': 'Filipa Andrade',
    'author_email': 'filipa.andrade@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
