# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sprinkles']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2', 'boto3', 'click', 'tomlkit']

setup_kwargs = {
    'name': 'sprinkles-config',
    'version': '0.1.0',
    'description': 'Generate config files from AWS Secrets',
    'long_description': None,
    'author': 'Okal Otieno',
    'author_email': 'okal@justokal.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
