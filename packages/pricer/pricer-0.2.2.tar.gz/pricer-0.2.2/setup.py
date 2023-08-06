# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pricer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.2',
 'SLPP==1.2',
 'click==6.7',
 'fastparquet==0.3.3',
 'importlib_metadata>=1.7.0,<2.0.0',
 'pandas==1.0.1',
 'seaborn==0.9.0']

entry_points = \
{'console_scripts': ['pricer = pricer.run:main']}

setup_kwargs = {
    'name': 'pricer',
    'version': '0.2.2',
    'description': 'Use WoW addon data to optimize auction buying and selling policies',
    'long_description': '# WoW Auction engine\n[![Tests](https://github.com/bluemania/wow_auctions/workflows/Tests/badge.svg)](https://github.com/bluemania/wow_auctions/actions?workflow=Tests)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Codecov](https://codecov.io/gh/bluemania/wow_auctions/branch/master/graph/badge.svg)](https://codecov.io/gh/bluemania/wow_auctions)\n[![PyPI](https://img.shields.io/pypi/v/pricer.svg)](https://pypi.org/project/pricer/)\n[![Documentation Status](https://readthedocs.org/projects/pricer/badge/?version=latest)](https://pricer.readthedocs.io/en/latest/?badge=latest)\n\nThis project helps automate some aspects of trading on the World of Warcraft (WoW) auction house.\n\nRelated article here: https://www.nickjenkins.com.au/articles/personal/2020/07/07/programming-and-analytics-in-games\n\nThe program is currently under development and is not currently designed for third party use.\n\n### Requirements\n\nYou will need Python 3.7 and World of Warcraft: Classic installed locally on your machine.\n\nThis project uses [poetry](https://python-poetry.org/) to manage dependencies and versioning.\n\n```bash\npoetry install\n```\n\nYou will also need the following WoW Classic Addons installed to interface with the program:\n\n* ArkInventory\n* Auctioneer\n* Beancounter (comes with Auctioneer)\n\n### Running the script\n\nAfter the above setup, to run the script enter the following on command line.\n\n```bash\npoetry shell\npoetry run python run.py -a\n```\n\nThere are many command line options; -a will run primary analysis (except for sell policies). Please refer to the scripts for further information.\n\n### License\nAll assets and code are under the MIT LICENSE and in the public domain unless specified otherwise.\n\n#### TODO\n\n* Create additional selling profile for min-bid max-buy high-volume. May require splitting the function more carefully\n* More visibility on current inventory\n',
    'author': 'bluemania',
    'author_email': 'damnthatswack@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bluemania/wow_auctions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
