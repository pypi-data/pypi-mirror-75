# Trustpilot Logging

[![Build Status](https://travis-ci.org/trustpilot/python-logging.svg?branch=master)](https://travis-ci.org/trustpilot/python-logging) [![Latest Version](https://img.shields.io/pypi/v/trustpilot-json-logging.svg)](https://pypi.python.org/pypi/trustpilot-json-logging) [![Python Support](https://img.shields.io/pypi/pyversions/trustpilot-json-logging.svg)](https://pypi.python.org/pypi/trustpilot-json-logging)

Opinionated json logging module used by [Trustpilot](https://developers.trustpilot.com/), *( based on [python-json-logger](https://github.com/madzak/python-json-logger) by [madzak](https://github.com/madzak) )*

## Installation

Install the package from [PyPI](http://pypi.python.org/pypi/) using [pip](https://pip.pypa.io/):

```bash
pip install trustpilot-logging
```

## Usage

```python
import trustpilot_json_logging
logging = trustpilot_json_logging.setup_logging()

logging.warning("i'm alive")

# outputs
# {"message": "i'm alive", "Module": "root", "Severity": "INFO"}
```

## Advanced Usage

```python
import trustpilot_json_logging
logging = trustpilot_json_logging.setup_logging("INFO", sys.stderr, ignore={"elasticsearch":"WARNING"})

logging.info({
    "message": "i just arrived",
    "age": 32,
    "location": "north pole"
})

# outputs
# {"message": "i just arrived", "age": 32, "location": "north pole", "Module": "root", "Severity": "INFO"}
```


## Publish new version

To publish a new version:

1. Make pr with
    1. your changes
    2. good linting: `black .` should be happy
    3. bump [semantic version](https://github.com/trustpilot/python-logging/blob/master/pyproject.toml#L3)
2. get pr reviewed
3. merge to master
4. pull master locally and run `poetry publish` with the TP pypi credentials
