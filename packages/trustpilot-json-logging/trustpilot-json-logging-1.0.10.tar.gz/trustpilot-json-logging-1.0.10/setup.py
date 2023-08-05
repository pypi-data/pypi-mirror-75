# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trustpilot_json_logging']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trustpilot-json-logging',
    'version': '1.0.10',
    'description': 'oppinionated json logger',
    'long_description': '# Trustpilot Logging\n\n[![Build Status](https://travis-ci.org/trustpilot/python-logging.svg?branch=master)](https://travis-ci.org/trustpilot/python-logging) [![Latest Version](https://img.shields.io/pypi/v/trustpilot-json-logging.svg)](https://pypi.python.org/pypi/trustpilot-json-logging) [![Python Support](https://img.shields.io/pypi/pyversions/trustpilot-json-logging.svg)](https://pypi.python.org/pypi/trustpilot-json-logging)\n\nOpinionated json logging module used by [Trustpilot](https://developers.trustpilot.com/), *( based on [python-json-logger](https://github.com/madzak/python-json-logger) by [madzak](https://github.com/madzak) )*\n\n## Installation\n\nInstall the package from [PyPI](http://pypi.python.org/pypi/) using [pip](https://pip.pypa.io/):\n\n```bash\npip install trustpilot-logging\n```\n\n## Usage\n\n```python\nimport trustpilot_json_logging\nlogging = trustpilot_json_logging.setup_logging()\n\nlogging.warning("i\'m alive")\n\n# outputs\n# {"message": "i\'m alive", "Module": "root", "Severity": "INFO"}\n```\n\n## Advanced Usage\n\n```python\nimport trustpilot_json_logging\nlogging = trustpilot_json_logging.setup_logging("INFO", sys.stderr, ignore={"elasticsearch":"WARNING"})\n\nlogging.info({\n    "message": "i just arrived",\n    "age": 32,\n    "location": "north pole"\n})\n\n# outputs\n# {"message": "i just arrived", "age": 32, "location": "north pole", "Module": "root", "Severity": "INFO"}\n```\n',
    'author': 'sloev',
    'author_email': 'johanned.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trustpilot/python-logging',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
