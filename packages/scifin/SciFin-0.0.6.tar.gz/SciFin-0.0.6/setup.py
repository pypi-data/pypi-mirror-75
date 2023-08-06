# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scifin',
 'scifin.classifier',
 'scifin.fouriertrf',
 'scifin.geneticalg',
 'scifin.marketdata',
 'scifin.montecarlo',
 'scifin.neuralnets',
 'scifin.statistics',
 'scifin.timeseries']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.13,<8.0',
 'bs4>=4.7,<5.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.18,<2.0',
 'pandas>=1.0,<2.0',
 'pandas_datareader>=0.8,<0.9',
 'requests>=2.23,<3.0',
 'scipy>=1.4,<2.0',
 'sklearn>=0.22,<0.23',
 'statsmodels>=0.11,<0.12']

entry_points = \
{'console_scripts': ['scifin = scifin:main']}

setup_kwargs = {
    'name': 'scifin',
    'version': '0.0.6',
    'description': 'SciFin is a python package for Science and Finance.',
    'long_description': '\n<p align="center">\n  <img src="./docs/logos/logo_scifin_github.jpg" width=300 title="hover text">\n</p>\n\n\n\n# SciFin\n\nSciFin is a python package for Science and Finance.\n\n## Summary\n\nThe SciFin package is a Python package designed to gather and develop methods for scientific studies and financial services. It originates from the observation that numerous methods developed in scientific fields (such as mathematics, physics, biology and climate sciences) have direct applicability in finance and that, conversely, multiple methods developed in finance can benefit science.\n\nThe development goal of this package is to offer a toolbox that can be used to derive specific applications both in research and business. Its purpose is not only to bring these fields together, but also to increase interoperability between them, helping science turn into business and finance to get new insights from science. Some functions will thus be neutral to any scientific or economic fields, while others will be more specialized for precise tasks. The motivationg behind this design is to provide tools that perform advanced tasks without depending on too many parameters.\n\n\n## Contents\n\nThe current development is focused on the following topics:\n- `classifier`: Classification techniques\n- `fouriertrf`: Fourier transforms\n- `geneticalg`: Genetic algorithms\n- `marketdata`: Reading market data\n- `montecarlo`: Monte Carlo simulations\n- `neuralnets`: Neural networks\n- `statistics`: Basic statistics\n- `timeseries`: Time series analysis\n\nOther topics will later follow.\n\n\n## Installation\n\nInstalling SciFin on Linux or Mac is very easy, you can simply run `pip install SciFin` on the Terminal command line.\n\nIf you encounter problems during installation or after and think you know how the problem can be improved, please share it with me.\n\n\n## Contact\n\n- If you have comments or suggestions, you can reach Fabien Nugier.\n- If you wish to contribute, please contact me through GitHub.\n\n\n\n\n\n',
    'author': 'Fabien Nugier',
    'author_email': 'fabien.nugier@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SciFin-Team/SciFin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
