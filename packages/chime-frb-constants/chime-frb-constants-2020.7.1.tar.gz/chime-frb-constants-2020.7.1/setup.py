# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chime_frb_constants']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chime-frb-constants',
    'version': '2020.7.1',
    'description': 'CHIME/FRB Constants',
    'long_description': '\n![chime-frb-constants](https://github.com/CHIMEFRB/frb-constants/workflows/chime-frb-constants/badge.svg) \n[![Coverage Status](https://coveralls.io/repos/github/CHIMEFRB/frb-constants/badge.svg?branch=master&t=2TpXqG)](https://coveralls.io/github/CHIMEFRB/frb-constants?branch=master)\n![pypi-version](https://img.shields.io/pypi/v/chime-frb-constants)\n![black-formatting](https://img.shields.io/badge/code%20style-black-000000.svg)\n# CHIME/FRB Constants \nA pure-python, lightweight and zero dependency package to access constants used in the CHIME/FRB software projects.\n\n## Installation\n```\npip install chime-frb-constants\n```\n\n### Optional\nIf `scipy` is installed in the python environment, `frb-constants` will also expose the physical constants, otherwise it is set to `None`\n```python\nimport chime_frb_constants as constants\nconstants.phy_const\n```\n\n## Usage\n```python\nimport chime_frb_constants as constants\n\n>>> constants.K_DM\n4149.377593360996\n\n>>> constants.phys_const.speed_of_light\n299792458.0\n```\n\n## Changelog\n\n### 2020.07\n  - Updated `CHANNEL_BANDWIDTH_MHZ`\n  - Fixed errors with `FREQ`\n  - Added optional physical constants from `scipy`\n\n### 2020.06.3\n  - Fixed error with `CHANNEL_BANDWIDTH_MHZ`\n  - Change to `SAMPLING_TIME_MS`\n  - New constant `SAMPLING_TIME_S`\n\n### 2020.06.2\n  - Added constants `FREQ` and `FREQ_FREQ`\n\n### 2020.06\n  - Release on [PYPI](https://pypi.org/project/chime-frb-constants/)\n  - All constants are now uppercase\n  - All physical constants from `scipy` are not availaible anymore under constants.\n\n\n',
    'author': 'Shiny Brar',
    'author_email': 'charanjotbrar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CHIMEFRB/frb-constants',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
