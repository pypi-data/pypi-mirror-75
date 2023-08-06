# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cervo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cervo',
    'version': '0.0.1.dev0',
    'description': 'Serving machine learning pipelines as APIs',
    'long_description': None,
    'author': 'KelvinSP',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
