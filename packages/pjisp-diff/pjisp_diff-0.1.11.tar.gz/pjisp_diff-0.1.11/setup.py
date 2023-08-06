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
    'version': '0.1.11',
    'description': 'PJISP diff check',
    'long_description': 'About\n=====\n\nConsole app to help teachers check if they changed all the necessary files when making an assignment for students using https://github.com/petarmaric/pjisp-assignment-template.\n\nInstallation\n============\n\nTo install pjisp_diff run::\n\n    $ pip install pjisp-diff\n\nConsole app usage\n=================\n\n    $ pjisp_diff <template>\nTemplate can be T12, T34 or SOV\n',
    'author': 'Jelena Dokic',
    'author_email': 'jrubics@hacke.rs',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JRubics/pjisp-diff/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
