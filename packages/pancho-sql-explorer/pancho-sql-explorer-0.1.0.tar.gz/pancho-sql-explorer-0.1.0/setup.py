# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['explorer', 'explorer.migrations', 'explorer.templatetags', 'explorer.tests']

package_data = \
{'': ['*'], 'explorer': ['static/explorer/*', 'templates/explorer/*']}

install_requires = \
['six>=1.15.0,<2.0.0', 'sqlparse>=0.3.1,<0.4.0', 'unicodecsv>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'pancho-sql-explorer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Francisco Ceruti',
    'author_email': 'hello@fceruti.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
