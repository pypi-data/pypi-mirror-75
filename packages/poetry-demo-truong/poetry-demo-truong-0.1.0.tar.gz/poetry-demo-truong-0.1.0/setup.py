# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_truong']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-demo-truong',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Truong Nguyen',
    'author_email': 'truongnd0001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
