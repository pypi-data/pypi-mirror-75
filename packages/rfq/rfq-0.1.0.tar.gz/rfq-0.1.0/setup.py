# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfq', 'rfq.scripts']

package_data = \
{'': ['*']}

install_requires = \
['hiredis>=1.0.1,<2.0.0', 'redis>=3.5.3,<4.0.0']

entry_points = \
{'console_scripts': ['rfq = rfq.scripts.__main__:main']}

setup_kwargs = {
    'name': 'rfq',
    'version': '0.1.0',
    'description': 'Simple language-agnostic message queues: tools, conventions, examples',
    'long_description': None,
    'author': 'Robofarm',
    'author_email': 'hello@robofarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
