# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wetterdienst',
 'wetterdienst.additionals',
 'wetterdienst.constants',
 'wetterdienst.data_models',
 'wetterdienst.download',
 'wetterdienst.enumerations',
 'wetterdienst.exceptions',
 'wetterdienst.file_path_handling',
 'wetterdienst.indexing',
 'wetterdienst.parsing_data']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.4.0,<0.5.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'cachetools>=3.1.1,<4.0.0',
 'dateparser>=0.7.4,<0.8.0',
 'docopt>=0.6.2,<0.7.0',
 'fire>=0.3.1,<0.4.0',
 'h5py==2.10.0',
 'munch>=2.5.0,<3.0.0',
 'numpy==1.18.3',
 'pandas==1.0.4',
 'python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy==1.4.1',
 'tables==3.6.1']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata==1.6.1'],
 'ipython': ['ipython>=7.10.1,<8.0.0',
             'ipython-genutils>=0.2.0,<0.3.0',
             'matplotlib>=3.0.3,<4.0.0']}

entry_points = \
{'console_scripts': ['wetterdienst = wetterdienst.cli:run']}

setup_kwargs = {
    'name': 'wetterdienst',
    'version': '0.4.0',
    'description': 'Python library to ease access to open weather data',
    'long_description': "Introduction to wetterdienst\n############################\n\n.. image:: https://github.com/earthobservations/wetterdienst/workflows/Tests/badge.svg\n   :target: https://github.com/earthobservations/wetterdienst/actions?workflow=Tests\n.. image:: https://codecov.io/gh/earthobservations/wetterdienst/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/earthobservations/wetterdienst\n.. image:: https://readthedocs.org/projects/wetterdienst/badge/?version=latest\n    :target: https://wetterdienst.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\n\n.. image:: https://img.shields.io/pypi/pyversions/wetterdienst.svg\n   :target: https://pypi.python.org/pypi/wetterdienst/\n.. image:: https://img.shields.io/pypi/v/wetterdienst.svg\n   :target: https://pypi.org/project/wetterdienst/\n.. image:: https://img.shields.io/pypi/status/wetterdienst.svg\n   :target: https://pypi.python.org/pypi/wetterdienst/\n.. image:: https://pepy.tech/badge/wetterdienst/month\n   :target: https://pepy.tech/project/wetterdienst/month\n.. image:: https://img.shields.io/github/license/earthobservations/wetterdienst\n   :target: https://github.com/earthobservations/wetterdienst/blob/master/LICENSE.rst\n.. image:: https://zenodo.org/badge/160953150.svg\n   :target: https://zenodo.org/badge/latestdoi/160953150\n\n\nWelcome to wetterdienst, your friendly weather service library for Python from the\nneighbourhood! We are an group of people, who try to make access to weather data in\nPython feel like a warm summer breeze, similar to other projects like\n`rdwd <https://github.com/brry/rdwd>`_ ,\nwhich originally drew our interest in this project. As we reach to provide you with data\nfrom multiple weather services, we are still stuck with this one weather service from\nGermany, that has questioned our believe in humanity. But we think we are at good\ncondition to make further progress to soon fully cover the German weather service, right\nafter finishing this documentation. But now it's up to you to take a closer look at\nwhat we did here.\n\n**CAUTION**\nAlthough the data is specified as being open, the DWD asks you to reference them as\nCopyright owner. To check out further, take a look at\n`Open Data at the DWD <https://www.dwd.de/EN/ourservices/opendata/opendata.html>`_\nand the\n`Official Copyright <https://www.dwd.de/EN/service/copyright/copyright_artikel.html?nn=495490&lsbId=627548>`_\n\nThe full documentation of wetterdienst is available at:\nhttps://wetterdienst.readthedocs.io/en/latest/\n\nTo keep you updated about added features etc. we provide a\n`Changelog <https://wetterdienst.readthedocs.io/en/latest/pages/development.html#current>`_\n. Furthermore to get insight on which data we have made available the section\n`Data Coverage <https://wetterdienst.readthedocs.io/en/latest/pages/data_coverage.html>`_\nmay be of special interest for you.\n\nGetting started\n***************\n\nRun the following\n\n.. code-block:: Python\n\n    pip install wetterdienst\n\nto make wetterdienst available in your current environment. To get some historical\nobserved station data call\n\n.. code-block:: Python\n\n    from wetterdienst import collect_dwd_data\n    from wetterdienst import Parameter, PeriodType, TimeResolution\n\n    station_data = collect_dwd_data(\n        station_ids=[1048],\n        parameter=Parameter.CLIMATE_SUMMARY,\n        time_resolution=TimeResolution.DAILY,\n        period_type=PeriodType.HISTORICAL\n    )\n\nFor other examples and functionality such getting metadata, running the library in a\nDocker image and a client take a look at the\n`API <https://wetterdienst.readthedocs.io/en/latest/pages/api.html>`_\nsection, which will be constantly updated with new functions. Also don't miss out our\n`examples <https://github.com/earthobservations/wetterdienst/tree/master/example>`_\n.\n\n\n\n",
    'author': 'Benjamin Gutzmann',
    'author_email': 'gutzemann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wetterdienst.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
