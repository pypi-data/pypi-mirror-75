# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pypart']
install_requires = \
['pipelinehelper>=0.7.6,<0.8.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'pypart',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Benjamin Murauer',
    'author_email': 'b.murauer@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
