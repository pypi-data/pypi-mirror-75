# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epymetheus',
 'epymetheus.benchmarks',
 'epymetheus.datasets',
 'epymetheus.exceptions',
 'epymetheus.helper',
 'epymetheus.history',
 'epymetheus.metrics',
 'epymetheus.strategy',
 'epymetheus.trade',
 'epymetheus.universe',
 'epymetheus.utils',
 'epymetheus.wealth']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.0,<2.0.0',
 'pandas-datareader>=0.8.1,<0.9.0',
 'pandas>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'epymetheus',
    'version': '0.5.0',
    'description': 'Python framework for multi-asset backtesting.',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
