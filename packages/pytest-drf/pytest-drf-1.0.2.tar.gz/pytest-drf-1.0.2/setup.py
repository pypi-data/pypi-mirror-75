# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_drf',
 'pytest_drf.util',
 'tests',
 'tests.example_project',
 'tests.example_project.views',
 'tests.pytest_drf']

package_data = \
{'': ['*']}

modules = \
['pytest', 'LICENSE', 'CHANGELOG']
install_requires = \
['djangorestframework>3',
 'inflection>=0.3.1,<0.4.0',
 'pytest-assert-utils>=0,<1',
 'pytest-common-subject>=1.0,<2.0',
 'pytest-lambda>=1.1,<2.0',
 'pytest>=3.6']

entry_points = \
{'pytest11': ['drf = pytest_drf.plugin']}

setup_kwargs = {
    'name': 'pytest-drf',
    'version': '1.0.2',
    'description': 'A Django REST framework plugin for pytest.',
    'long_description': '# pytest-drf\n\npytest-drf allows you to test your Django REST framework APIs with the [pytest testing tool](http://pytest.org).\n',
    'author': 'Zach "theY4Kman" Kanzler',
    'author_email': 'they4kman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theY4Kman/pytest-drf',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
