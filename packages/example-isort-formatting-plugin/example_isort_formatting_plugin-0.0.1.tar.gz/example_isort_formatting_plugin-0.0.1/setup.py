# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['example_isort_formatting_plugin']
install_requires = \
['black>=19.10b0,<20.0', 'isort>=5.1.4,<6.0.0']

entry_points = \
{'isort.formatters': ['example = '
                      'example_isort_formatting_plugin:black_format_import_section']}

setup_kwargs = {
    'name': 'example-isort-formatting-plugin',
    'version': '0.0.1',
    'description': 'An example plugin that modifies isort formatting using black.',
    'long_description': None,
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
