# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'topojoin']

package_data = \
{'': ['*'], 'tests': ['fixtures/*']}

install_requires = \
['click']

entry_points = \
{'console_scripts': ['topojoin = topojoin.cli:main']}

setup_kwargs = {
    'name': 'topojoin',
    'version': '0.1.0',
    'description': 'Top-level package for TopoJoin.',
    'long_description': '========\nTopoJoin\n========\n\n\n.. image:: https://img.shields.io/pypi/v/topojoin.svg\n        :target: https://pypi.python.org/pypi/topojoin\n\n.. image:: https://img.shields.io/travis/SimmonsRitchie/topojoin.svg\n        :target: https://travis-ci.com/SimmonsRitchie/topojoin\n\n.. image:: https://readthedocs.org/projects/topojoin/badge/?version=latest\n        :target: https://topojoin.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nTool to easily join CSV data to topojson.\n\n\n* Free software: MIT\n* Documentation: https://topojoin.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'DSR',
    'author_email': 'DSR',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SimmonsRitchie/topojoin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.8.1',
}


setup(**setup_kwargs)
