# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['build_sqli_url']
entry_points = \
{'console_scripts': ['build-sqli-url = build_sqli_url:main']}

setup_kwargs = {
    'name': 'build-sqli-url',
    'version': '0.1.0',
    'description': 'Build SQLi URL Helper.',
    'long_description': None,
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
