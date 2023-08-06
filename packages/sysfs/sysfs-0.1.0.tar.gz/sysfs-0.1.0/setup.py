# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sysfs']
setup_kwargs = {
    'name': 'sysfs',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gregory C. Oakes',
    'author_email': 'gregoryoakes@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
