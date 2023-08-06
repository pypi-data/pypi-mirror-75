# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsets', 'dsets.downloader', 'dsets.storage']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0']

setup_kwargs = {
    'name': 'dsets',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Alexander Hungenberg',
    'author_email': 'alexander.hungenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
