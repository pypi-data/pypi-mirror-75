# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unusualvolume']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'joblib>=0.16.0,<0.17.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'tqdm>=4.48.2,<5.0.0',
 'yfinance>=0.1.54,<0.2.0']

entry_points = \
{'console_scripts': ['unusualvolume = unusualvolume.cli:cli']}

setup_kwargs = {
    'name': 'unusualvolume',
    'version': '0.1.0',
    'description': 'Monitor stock market transactions for unusual volume and (possibly) make millions',
    'long_description': '# unusualvolume\n\nMonitor stock market transactions for unusual volume and (possibly) make millions.\n\n## Demo\n\n![](unusualvolume_demo.gif)\n\n## About\n\nA simple command line tool to retrieve stock market data (US-only) and analyze trading volumes for anomalies.\n\n## Use Cases\n\n1. Mining valuable trading information and getting ahead of possible large changes in stock prices\n2. Transaction monitoring for OSINT (open source intelligence) purposes\n3. Collecting data to train your own ML model\n\n\n## Installation\n\n```shell script\n$ pip install unusualvolume --upgrade\n```\n\n## Usage\n\n```shell script\n$ unusualvolume scan\n```',
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfdeux/unusualvolume',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
