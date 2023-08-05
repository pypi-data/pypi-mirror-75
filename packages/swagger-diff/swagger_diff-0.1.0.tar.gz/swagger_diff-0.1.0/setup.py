# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swagger_diff']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dictdiffer>=0.8.1,<0.9.0',
 'jinja2>=2.11.2,<3.0.0',
 'pydantic>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['swagger = swagger.main:main']}

setup_kwargs = {
    'name': 'swagger-diff',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'jun',
    'author_email': 'wandy1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
