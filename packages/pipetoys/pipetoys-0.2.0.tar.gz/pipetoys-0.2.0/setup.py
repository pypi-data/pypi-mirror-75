# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipetoys']
setup_kwargs = {
    'name': 'pipetoys',
    'version': '0.2.0',
    'description': 'Pythonic pipelines.',
    'long_description': '# pipestuff\n\nPythonic pipelines. Just higher-order functions.\n\nOnly used for personal projects and small scripts.\nI have no plans for documentation.\n',
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
