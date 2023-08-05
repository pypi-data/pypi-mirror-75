# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gflick']

package_data = \
{'': ['*']}

install_requires = \
['bottle>=0.12.18,<0.13.0',
 'gunicorn>=20.0.4,<21.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gflick-dev = gflick:dev',
                     'gflick-google = gflick:google',
                     'gflick-prod = gflick:prod',
                     'gflick-raw = gflick:raw']}

setup_kwargs = {
    'name': 'gflick',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Bùi Thành Nhân',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
