# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fooddata']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.24.0,<3.0.0', 'tqdm>=4.48.2,<5.0.0']

entry_points = \
{'console_scripts': ['fooddata = fooddata.cli:cli']}

setup_kwargs = {
    'name': 'fooddata',
    'version': '0.1.0',
    'description': 'Download, build, and query the USDA food database',
    'long_description': '# fooddata\n\nDownload, build, and query the USDA food database.\n\nDo you know what you are putting in your body?\n\n## Installation\n\n```shell script\n$ pip install fooddata --upgrade\n```\n\n## Usage\n\n```shell script\n$ fooddata build\n```\n\n```shell script\n$ fooddata query "SELECT * from foods WHERE category_id IS NOT NULL LIMIT 100;" --json | jq .\n```\n\n```shell script\n$ fooddata query "SELECT * from foods WHERE category_id IS NOT NULL LIMIT 100;" --json > output2.json\n```\n\n```shell script\n$ fooddata query "SELECT * from food_nutrients_v WHERE food_type IS NOT NULL AND food_category IS NOT NULL LIMIT 1000;" --json | jq .\n```\n\n## Update Database\n\nTo update the database, just run the first command again:\n\n```shell script\n$ fooddata build\n```\n\n## Note\n\nThe data comes from the USDA website:\n[https://fdc.nal.usda.gov/download-datasets.html](https://fdc.nal.usda.gov/download-datasets.html)\n',
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfdeux/fooddata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
