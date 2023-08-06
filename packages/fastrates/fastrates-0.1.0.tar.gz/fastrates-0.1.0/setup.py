# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastrates']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'typer[all]>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['fastrates = fastrates_cli.main:app']}

setup_kwargs = {
    'name': 'fastrates',
    'version': '0.1.0',
    'description': '',
    'long_description': '<img src="https://github.com/ycd/fastrates/blob/master/fastrates/frontend/static/logo.png" width=500>\n\n## Command line interface for [Fast Rates](https://github.com/ycd/fastrates)\n\n\n# Installation :pushpin:\n\n```python\npip install fastrates-cli\n\n\nSuccessfully installed fastrates-cli-0.1.0\n\n```\n\n# How to use? :rocket:\n```python\nOptions:\n  --base TEXT             Base ticker for currency  [default: EUR]\n  --latest / --no-latest  Get the latest foreign exchange reference rates\n                          [default: False]\n\n  --start-at TEXT         Get historical rates for any day since start_at\n  --end-at TEXT           Get historical rates for any day till end_at\n  --symbols TEXT          Compare specific exchange rates\n  --date TEXT             Get historical date\n  --help                  Show this message and exit.\n```\n\n* ## Example \n```python\nfastrates-cli --latest\n```\n## Which will return\n```JSON\n{\n    "rates":{\n        "2020-07-31":{\n            "AUD":1.6488,\n            "BGN":1.9558,\n            "BRL":6.1219,\n            "CAD":1.5898,\n            "CZK":26.175,\n            "DKK":7.4442,\n            "GBP":0.90053,\n            "TRY":8.2595,\n            "USD":1.1848,\n        }\n    },\n    "base":"EUR"\n}\n```\n\n\n\n## Release Notes :mega:\n\n### Latest Changes\n\n### 0.1.0\n\n* Prototype of project\n',
    'author': 'yagizd',
    'author_email': 'yagizcanilbey1903@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
