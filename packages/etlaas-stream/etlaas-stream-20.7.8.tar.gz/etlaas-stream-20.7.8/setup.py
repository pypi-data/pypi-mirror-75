# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etlaas_stream', 'etlaas_stream.bookmarker']

package_data = \
{'': ['*']}

install_requires = \
['fastjsonschema>=2.14.4,<3.0.0',
 'redis>=3.5.3,<4.0.0',
 'simplejson>=3.17.0,<4.0.0']

setup_kwargs = {
    'name': 'etlaas-stream',
    'version': '20.7.8',
    'description': 'Convenience classes for working with data streams.',
    'long_description': None,
    'author': 'Andrew Meier',
    'author_email': 'ameier38@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
