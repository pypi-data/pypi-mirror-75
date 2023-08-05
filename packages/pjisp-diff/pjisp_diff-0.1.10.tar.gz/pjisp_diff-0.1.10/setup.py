# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pjisp_diff']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pjisp_diff = pjisp_diff:diff']}

setup_kwargs = {
    'name': 'pjisp-diff',
    'version': '0.1.10',
    'description': 'PJISP diff check',
    'long_description': None,
    'author': 'Jelena Dokic',
    'author_email': 'jrubics@hacke.rs',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
