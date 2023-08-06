# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crashtest', 'crashtest.contracts', 'crashtest.solution_providers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crashtest',
    'version': '0.3.1',
    'description': 'Manage Python errors with ease',
    'long_description': '# Crashtest\n\nCrashtest is a Python library that makes exceptions handling and inspection easier.\n',
    'author': 'Sébastien Eustace',
    'author_email': 'sebastien@eustace.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdispater/crashtest',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
