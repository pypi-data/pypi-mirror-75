# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crdatamgt']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=5.3.1,<6.0.0',
 'openpyxl>=3.0.4,<4.0.0',
 'pandas==1.1.0',
 'simplelogging>=0.10.0,<0.11.0',
 'toolz>=0.10.0,<0.11.0',
 'xlsxwriter>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'crdatamgt',
    'version': '3.0.5',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
