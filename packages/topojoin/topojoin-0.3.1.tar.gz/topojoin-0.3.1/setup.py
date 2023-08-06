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
    'version': '0.3.1',
    'description': 'Top-level package for TopoJoin.',
    'long_description': '========\nTopoJoin\n========\n\n\n.. image:: https://img.shields.io/pypi/v/topojoin.svg\n        :target: https://pypi.python.org/pypi/topojoin\n\n.. image:: https://img.shields.io/travis/SimmonsRitchie/topojoin.svg\n        :target: https://travis-ci.com/SimmonsRitchie/topojoin\n\n.. image:: https://readthedocs.org/projects/topojoin/badge/?version=latest\n        :target: https://topojoin.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\nA lightweight utility to join CSV data to a topojson file. Produces a new topojson file with CSV properties added to\nthe properties of each feature.\n\n* Free software: MIT\n* Documentation: https://topojoin.readthedocs.io.\n\nInstall\n----------\n\n::\n\n    pip install topojoin\n\n\nBasic usage\n-----------\n\nCommand line\n============\n\nIn the command line, enter the topojoin command followed by the path to your topojson file and your CSV file.\n\nBy default TopoJoin will assume both files have a common field called \'id\' that can be joined.\n\n::\n\n    topojoin example.json example.csv\n\n    >> Joining example.csv to example.json...\n    >> CSV key \'id\' will be joined with topojson key \'id\'\n    >> Joined data saved to: joined.json\n\nTo define the join keys, use the \'-tk\' option for the key in your topojson file and the \'-ck\' option for the key in\nyour CSV file:\n\n::\n\n    topojoin -tk GEOID -ck fips example.json example.csv\n\n    >> Joining example.csv to example.json...\n    >> CSV key \'fips\' will be joined with topojson key \'GEOID\'\n    >> Joined data saved to: joined.json\n\n\nProgrammatic\n============\n\nIf you prefer, you can also import and call TopoJoin from a python script:\n\n\n::\n\n    from topojoin.topojoin import TopoJoin\n\n    tj = TopoJoin("./example.json", "./example.csv", topo_key="GEOID", csv_key="fips")\n    topojson_data = tj.join()\n\n\nOr, to write to a file:\n\n::\n\n    from topojoin.topojoin import TopoJoin\n\n    tj = TopoJoin("./example.json", "./example.csv", topo_key="GEOID", csv_key="fips")\n    tj.join("joined.json")\n\n\nAdvanced usage\n--------------\n\nCommand line\n================\n\nTopoJoin\'s actions can be modified in a number of ways by passing optional arguments. Here are its available options:\n\n  -tk, --topokey TEXT     Key in CSV file that will be used to join with CSV\n                          file  [default: id]\n\n  -ck, --csvkey TEXT      Key in CSV file that will be used to join with\n                          topojson file  [default: id]\n\n  -cp, --csv_props TEXT   Comma separated list of fields in CSV file to merge\n                          to each topojson feature (eg:\n                          name,population,net_income). Defaults to including\n                          all fields in CSV file.\n\n  -o, --output_path TEXT  Output path of joined topojson file. Defaults to\n                          current working directory.\n\n  -q, --quiet             Disables stdout during program run\n  --version               Show the version and exit.\n  --help                  Show this message and exit.\n\n\n\n\nFor example:\n\n::\n\n    topojoin -tk GEOID -ck fips -o "mydir/my-custom-filename.json" example.json example.csv\n\n\nTO DO\n-----\n- Prefix CSV keys if key name is already present in topojson props.\n- Raise exception or prompt if CSV file has duplicate values in column specified by csv_key.\n\nAlternatives\n------------\n\n- `py-geojoin <https://github.com/shawnbot/py-geojoin>`__\n',
    'author': 'DSR',
    'author_email': 'info@simmonsritchie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SimmonsRitchie/topojoin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
