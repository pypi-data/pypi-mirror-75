# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graia', 'graia.template']

package_data = \
{'': ['*']}

install_requires = \
['graia-application-mirai>=0.0.5,<0.0.6', 'regex>=2020.7.14,<2021.0.0']

setup_kwargs = {
    'name': 'graia-template',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
