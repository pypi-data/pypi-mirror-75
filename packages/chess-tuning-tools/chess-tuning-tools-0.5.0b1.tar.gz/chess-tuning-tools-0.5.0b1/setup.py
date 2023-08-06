# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tune', 'tune.db_workers', 'tune.db_workers.dbmodels']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.2,<8.0.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'bask>=0.7.2,<0.8.0',
 'emcee>=3.0.2,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'scikit-optimize>=0.7.4,<0.8.0',
 'scipy>=1.5.2,<2.0.0']

extras_require = \
{'dist': ['joblib>=0.16.0,<0.17.0',
          'psycopg2>=2.8.5,<3.0.0',
          'sqlalchemy>=1.3.18,<2.0.0',
          'pandas>=1.1.0,<2.0.0']}

entry_points = \
{'console_scripts': ['tune = tune.cli:cli']}

setup_kwargs = {
    'name': 'chess-tuning-tools',
    'version': '0.5.0b1',
    'description': 'A collection of tools for local and distributed tuning of chess engines.',
    'long_description': '==================\nChess Tuning Tools\n==================\n\n\n.. image:: https://img.shields.io/pypi/v/chess-tuning-tools.svg\n        :target: https://pypi.python.org/pypi/chess-tuning-tools\n\n.. image:: https://img.shields.io/travis/kiudee/chess-tuning-tools.svg\n        :target: https://travis-ci.org/kiudee/chess-tuning-tools\n\n.. image:: https://readthedocs.org/projects/chess-tuning-tools/badge/?version=latest\n        :target: https://chess-tuning-tools.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nA collection of tools for local and distributed tuning of chess engines.\n\n\n* Free software: Apache Software License 2.0\n* Documentation: https://chess-tuning-tools.readthedocs.io.\n\n\nFeatures\n--------\n\n* Optimization of chess engines using state-of-the-art Bayesian optimization.\n* Support for automatic visualization of the optimization landscape.\n* Scoring matches using the pentanomial model for paired openings.\n\nQuick Start\n-----------\n\nIn order to be able to start the tuning, first create a python\nenvironment and install chess-tuning-tools by typing::\n\n   pip install chess-tuning-tools\n\nFurthermore, you need to have `cutechess-cli <https://github.com/cutechess/cutechess>`_\nin the path. The tuner will use it to run matches.\n\nTo execute the local tuner, simply run::\n\n   tune local -c tuning_config.json\n\nTake a look at the `usage instructions`_ and the `example configurations`_ to\nlearn how to set up the ``tuning_config.json`` file.\n\n\nDistributed tuning\n------------------\n\nThe distributed tuning framework is currently not actively supported.\nTo be able to run the tuning client, you need the following directory structure::\n\n   folder/\n   |---- networks/\n   |     |---- networkid\n   |---- openings/\n   |     |---- ...\n   |     |---- openings.pgn\n   |     |---- ...\n   |---- dbconfig.json\n   |---- engine1[.exe]\n   |---- engine2[.exe]\n\nFinally, the tuning client can be started as follows::\n\n   cd path/to/folder\n   tune run-client dbconfig.json\n\nThe client can be terminated gracefully by inputting ctrl-c once or terminated\nimmediately by sending it twice.\n\nYou will also need to run a PostgreSQL database, which the server will use to\npost jobs for the clients to fetch and the clients to report their results to.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n.. _example configurations: https://github.com/kiudee/chess-tuning-tools/tree/master/examples\n.. _usage instructions: https://chess-tuning-tools.readthedocs.io/en/latest/usage.html\n',
    'author': 'Karlson Pfannschmidt',
    'author_email': 'kiudee@mail.upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiudee/chess-tuning-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
