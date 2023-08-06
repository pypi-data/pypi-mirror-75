# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyutgenerator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pyutgen = pyutgenerator.run:main']}

setup_kwargs = {
    'name': 'pyutgenerator',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'shigeshige',
    'author_email': '5540474+shigeshige@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
