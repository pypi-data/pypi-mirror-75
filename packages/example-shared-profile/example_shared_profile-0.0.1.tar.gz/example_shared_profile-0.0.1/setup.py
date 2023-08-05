# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['example_shared_profile']
entry_points = \
{'isort.profiles': ['example = example_shared_profile:PROFILE']}

setup_kwargs = {
    'name': 'example-shared-profile',
    'version': '0.0.1',
    'description': 'An example shared isort profile',
    'long_description': None,
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
