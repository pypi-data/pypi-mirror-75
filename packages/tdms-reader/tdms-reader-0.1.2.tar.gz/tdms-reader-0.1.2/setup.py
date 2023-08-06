# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tdms_reader']

package_data = \
{'': ['*'], 'tdms_reader': ['CSV DATA/*', 'PLOT DATA/*']}

install_requires = \
['bokeh>=2.1.1,<3.0.0',
 'nptdms>=0.27.0,<0.28.0',
 'pandas>=1.1.0,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'simplelogging>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'tdms-reader',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@front.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
