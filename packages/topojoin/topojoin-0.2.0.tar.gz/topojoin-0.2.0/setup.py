# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'topojoin']

package_data = \
{'': ['*'], 'tests': ['fixtures/*']}

install_requires = \
['click', 'importlib_metadata>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['topojoin = topojoin.cli:main']}

setup_kwargs = {
    'name': 'topojoin',
    'version': '0.2.0',
    'description': 'Top-level package for TopoJoin.',
    'long_description': '========\nTopoJoin\n========\n\n\n.. image:: https://img.shields.io/pypi/v/topojoin.svg\n        :target: https://pypi.python.org/pypi/topojoin\n\n.. image:: https://img.shields.io/travis/SimmonsRitchie/topojoin.svg\n        :target: https://travis-ci.com/SimmonsRitchie/topojoin\n\n.. image:: https://readthedocs.org/projects/topojoin/badge/?version=latest\n        :target: https://topojoin.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\nA lightweight utility to left join topojson data with CSV data.\n\n* Free software: MIT\n* Documentation: https://topojoin.readthedocs.io.\n\nInstall\n----------\n\n::\n\n    pip install topojoin\n\n\nBasic usage\n-----------\n\nCommand line\n============\n\nIn the command line, enter the topojoin command followed by the path to your topojson file and your CSV file.\n\nBy default topojoin will assume both files have a common field called \'id\' that can be joined.\n\n::\n\n    topojoin example.json example.csv\n\n    >> Joining example.csv to example.json...\n    >> CSV key \'id\' will be joined with topojson key \'id\'\n    >> Joined data saved to: joined.json\n\nTo define the join keys, use the \'-tk\' option for the key in your topojson file and the \'-ck\' option for the key in\nyour CSV file:\n\n::\n\n    topojoin -tk GEOID -ck fips example.json example.csv\n\n    >> Joining example.csv to example.json...\n    >> CSV key \'fips\' will be joined with topojson key \'GEOID\'\n    >> Joined data saved to: joined.json\n\n\nProgrammatic\n============\n\nIf you prefer, you can also import and call topojson from a python script:\n\n\n::\n\n    from topojoin.topojoin import TopoJoin\n\n    topojoin_obj = TopoJoin("./example.json", "./example.", topo_key="GEOID", csv_key="fips")\n    result = topojoin_obj.join()\n\n',
    'author': 'DSR',
    'author_email': 'info@simmonsritchie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SimmonsRitchie/topojoin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
