# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_handy_utils',
 'django_handy_utils.filters',
 'django_handy_utils.models',
 'django_handy_utils.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2', 'djangorestframework>=3']

setup_kwargs = {
    'name': 'django-handy-utils',
    'version': '1.1.0',
    'description': 'Handy utilities for working on Django projects',
    'long_description': '# django-handy-utils\n\n`django-handy-utils` contains various model, view, filter, and other miscellaneous utilities that are standardized across projects.\n\n## Installation\n\n```shell\npip install django-handy-utils --upgrade\n```\n\n## Usage in Django\n\nTO COME\n\n\n## Contributors\n\nAll contributors are welcome.',
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfdeux/django-handy-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
