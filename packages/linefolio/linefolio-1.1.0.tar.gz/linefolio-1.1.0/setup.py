# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linefolio', 'linefolio.tests']

package_data = \
{'': ['*'], 'linefolio': ['examples/*'], 'linefolio.tests': ['test_data/*']}

install_requires = \
['empyrical>=0.5.3,<0.6.0',
 'ipython>=7.16.1,<8.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'pytz>=2020.1,<2021.0',
 'quantrocket-moonchart>=2.0.1,<3.0.0',
 'quantrocket-moonshot>=2.1.0,<3.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.5.1,<2.0.0',
 'seaborn>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'linefolio',
    'version': '1.1.0',
    'description': 'Backtest performance analysis and charting for MoonLine, but with pyfolio.',
    'long_description': None,
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
