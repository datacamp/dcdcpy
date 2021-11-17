# dcdcpy

DataCamp Data Connector utilities in Python.

This package contains utilities to work with DataCamp Data Connector. It is designed to be used by administrators and managers of DataCamp groups. Some prior experience of writing reports with Python is recommended.

## Installation

You can install the development version with:

```bash
$ pip install git+https://github.com/datacamp/dcdcpy.git#egg=dcdcpy
```

## Getting Started

Before you begin, you need to enable Data Connector in your DataCamp group, and 
set S3 credentials as environment variables, as described in this [this Support article](https://support.datacamp.com/hc/en-us/articles/4405070893591-DataCamp-Data-Connector-A-Step-by-Step-Configuration-Guide-for-Automated-Data-Exports).
If in doubt, speak to your Customer Success Manager.

## Accessing Data

You can access any of the tables in the data connector by initializing it using the `DataConnector()` class.

## Usage

```python
from dcdcpy.dcdcpy import DataConnector
dc = DataConnector()
dc.assessment_dim()
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`dcdcpy` was created by Richard Cotton. It is licensed under the terms of the MIT license.

## Credits

`dcdcpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
