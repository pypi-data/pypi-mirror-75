# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elegy',
 'elegy.callbacks',
 'elegy.data',
 'elegy.losses',
 'elegy.metrics',
 'elegy.nn',
 'elegy.regularizers']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.5.0,<2.0.0',
 'deepdish>=0.3.6,<0.4.0',
 'deepmerge>=0.1.0,<0.2.0',
 'dm-haiku>=0.0.1,<0.0.2',
 'jaxlib>=0.1.51,<0.2.0',
 'numpy>=1.19.0,<2.0.0',
 'pytest-cov>=2.10.0,<3.0.0',
 'pytest>=5.4.3,<6.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'tables>=3.6.1,<4.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tensorboardx>=2.1,<3.0',
 'toolz>=0.10.0,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'elegy',
    'version': '0.1.5',
    'description': 'Elegy is a Neural Networks framework based on Jax and Haiku.',
    'long_description': None,
    'author': 'Cristian Garcia',
    'author_email': 'cgarcia.e88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
