# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brishgarden']

package_data = \
{'': ['*']}

install_requires = \
['brish>=0.2.2,<0.3.0',
 'fastapi[all]>=0.60.1,<0.61.0',
 'passlib[bcrypt,argon2]>=1.7.2,<2.0.0',
 'python-jose[cryptography]>=3.1.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6']

entry_points = \
{'console_scripts': ['brishgarden = brishgarden:main']}

setup_kwargs = {
    'name': 'brishgarden',
    'version': '0.1.0',
    'description': "BrishGarden uses Brish to serve an HTTP API that can execute interpreted code (that would otherwise need expensive startup costs) fast. It's also useful as a remote code executor.",
    'long_description': None,
    'author': 'NightMachinary',
    'author_email': 'rudiwillalwaysloveyou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
