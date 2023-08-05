# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cosmoplotian',
 'cosmoplotian.extern',
 'cosmoplotian.tests',
 'cosmoplotian.utils',
 'cosmoplotian.utils.tests']

package_data = \
{'': ['*'], 'cosmoplotian': ['data/*']}

install_requires = \
['astropy>=4.0.1,<5.0.0',
 'matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.17,<2.0',
 'reproject>=0.7.1,<0.8.0']

extras_require = \
{':extra == "docs"': ['sphinx-argparse>=0.2.5,<0.3.0'],
 ':python_version == "3.6"': ['importlib_resources>=2.0.1,<3.0.0'],
 u'docs': ['nbsphinx>=0.7.0,<0.8.0',
           'sphinx>=3.0.4,<4.0.0',
           'ipykernel>=5.3.0,<6.0.0',
           'pandoc>=1.0.2,<2.0.0',
           'sphinx-math-dollar>=1.1.1,<2.0.0',
           'sphinx-astropy>=1.3,<2.0'],
 u'test': ['pytest>=5.4.3,<6.0.0',
           'pytest-astropy>=0.8.0,<0.9.0',
           'tox>=3.15.1,<4.0.0']}

setup_kwargs = {
    'name': 'cosmoplotian',
    'version': '0.0.1',
    'description': 'cosmoplotian is for plotting',
    'long_description': 'Plotting of images related to cosmology\n---------------------------------------\n\n.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat\n    :target: http://www.astropy.org\n    :alt: Powered by Astropy Badge\n\n.. image:: https://coveralls.io/repos/github/bthorne93/cosmoplotian/badge.svg?branch=master\n    :target: https://coveralls.io/github/bthorne93/cosmoplotian?branch=master\n\n.. image:: https://travis-ci.org/bthorne93/cosmoplotian.svg?branch=master\n    :target: https://travis-ci.org/bthorne93/cosmoplotian\n\n``cosmoplotian`` provides additional projections and colormaps for the\nplotting of astronomical images.\n\n\nLicense\n-------\n\nThis project is Copyright (c) Ben Thorne and licensed under\nthe terms of the BSD 3-Clause license. This package is based upon\nthe `Astropy package template <https://github.com/astropy/package-template>`_\nwhich is licensed under the BSD 3-clause license. See the licenses folder for\nmore information.',
    'author': 'Ben Thorne',
    'author_email': 'bn.thorne@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bthorne93/cosmoplotian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
