# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysparkrpc', 'pysparkrpc.server']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=1.5.0,<2.0.0',
 'findspark>=1.4.2,<2.0.0',
 'flask>=1.1.2,<2.0.0',
 'httpx>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['pysparkrpc = pysparkrpc.server.cli:main']}

setup_kwargs = {
    'name': 'pysparkrpc',
    'version': '0.3.0',
    'description': 'Seamlessly run Pyspark code on remote clusters.',
    'long_description': 'PysparkRPC |teststatus|\n========================\n\n.. |teststatus| image:: https://github.com/abronte/PysparkRPC/workflows/Tests/badge.svg\n\n\nSeamlessly run Pyspark code on remote clusters.\n',
    'author': 'Adam Bronte',
    'author_email': 'adam@bronte.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abronte/PysparkRPC',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
