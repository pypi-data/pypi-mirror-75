# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pjisp_template_name']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pjisp_template_name = pjisp_template_name:get_name']}

setup_kwargs = {
    'name': 'pjisp-template-name',
    'version': '0.2.3',
    'description': 'PJISP get template name from repository name',
    'long_description': 'About\n=====\n\nConsole app to chck if teachers gave the correct name to the github repository for student assignments when using https://github.com/petarmaric/pjisp-assignment-template.\n\nInstallation\n============\n\nTo install pjisp-template-name run::\n\n    $ pip install pjisp-template-name\n\nConsole app usage\n=================\n\n    $ pjisp_template_name <template_name>\n',
    'author': 'Jelena Dokic',
    'author_email': 'jrubics@hacke.rs',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JRubics/pjisp-template-name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
