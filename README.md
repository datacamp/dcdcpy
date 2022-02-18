# dcdcpy

<!-- badges: start -->
[![Lifecycle: experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
<!-- badges: end -->

DataCamp Data Connector utilities in Python.

This package contains utilities to work with DataCamp Data Connector. It is designed to be used by administrators and managers of DataCamp groups. Some prior experience of writing reports with Python is recommended.

## Installation

You can install the development version with:

```bash
$ pip install git+https://github.com/datacamp/dcdcpy.git#egg=dcdcpy
```

## Getting Started

Before you begin, you need to enable Data Connector in your DataCamp group, and 
set S3 credentials as environment variables, as described in this [this Support article](https://enterprise-docs.datacamp.com/data-connector/getting-started/storing-your-credentials).
If in doubt, speak to your Customer Success Manager.

## Accessing Data

You can access any of the tables in the data connector by initializing the `DataConnector` class and accessing the tables as methods using autocomplete.

By default the connector is set up to access data for the latest date. However, you can also pass a `date` argument to `DataConnector` to initialize it to access data for a specific date. This is useful when you want to create reports and want to pin your analysis to data as on a specific date.
## Usage

```python
from dcdcpy.dcdcpy import DataConnector
dc = DataConnector()
dc.assessment_dim()
```

You can also print the documentation for each table by printing the method without invoking it. 

```python
dc.assessment_dim
```

---
### Assessment Dim

#### Description

The assessment dimension provides descriptive data about a specific  assessment.


#### Columns

assessment_id

> The unique id of the assessment id.

title

> The title of the assessment.

slug

> The slug of The assessment.

technology

> The assessment technology (e.g., Python, R, SQL)


id

> [DEPRECATED] Use assessment_id instead.

---


All the data accessors are memoized and will cache the results in memory when they are run for the first time. This should speed up analysis considerably since the data is already cached in memory.
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`dcdcpy` was created by Richard Cotton and Ramnath Vaidyanathan. It is licensed under the terms of the MIT license.

## Credits

`dcdcpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
