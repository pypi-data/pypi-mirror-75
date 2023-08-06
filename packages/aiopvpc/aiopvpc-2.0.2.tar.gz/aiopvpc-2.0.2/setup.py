# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopvpc']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2', 'async_timeout>=3.0.1', 'pytz>=2020.1']

setup_kwargs = {
    'name': 'aiopvpc',
    'version': '2.0.2',
    'description': 'Retrieval of Spanish Electricity hourly prices (PVPC)',
    'long_description': '[![PyPi](https://pypip.in/v/aiopvpc/badge.svg)](https://pypi.org/project/aiopvpc/)\n[![Wheel](https://pypip.in/wheel/aiopvpc/badge.svg)](https://pypi.org/project/aiopvpc/)\n[![Travis Status](https://travis-ci.org/azogue/aiopvpc.svg?branch=master)](https://travis-ci.org/azogue/aiopvpc)\n[![codecov](https://codecov.io/gh/azogue/aiopvpc/branch/master/graph/badge.svg)](https://codecov.io/gh/azogue/aiopvpc)\n\n# aiopvpc\n\nSimple aio library to download Spanish electricity hourly prices.\n\nMade to support the [**`pvpc_hourly_pricing`** HomeAssistant integration](https://www.home-assistant.io/integrations/pvpc_hourly_pricing/).\n\n<span class="badge-buymeacoffee"><a href="https://www.buymeacoffee.com/azogue" title="Donate to this project using Buy Me A Coffee"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg" alt="Buy Me A Coffee donate button" /></a></span>\n\n\n## Install\n\nInstall with `pip install aiopvpc` or clone it to run tests or anything else.\n\n## Usage\n\n```\nfrom aiopvpc import PVPCData\n\npvpc_handler = PVPCData(tariff="discrimination")\n\nstart = datetime(2020, 3, 20, 22)\nend = datetime(2020, 4, 30, 16)\nprices_range: dict = await pvpc_handler.async_download_prices_for_range(start, end)\n```\n\nCheck [this example on a jupyter notebook](https://github.com/azogue/aiopvpc/blob/master/Notebooks/Download%20PVPC%20prices.ipynb), where the downloader is combined with pandas and matplotlib to plot the electricity prices:\n\n![sample_pvpc_plot.png](https://github.com/azogue/aiopvpc/blob/master/Notebooks/sample_pvpc_plot.png)\n',
    'author': 'Eugenio Panadero',
    'author_email': 'eugenio.panadero@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azogue/aiopvpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
