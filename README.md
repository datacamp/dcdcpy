# dcdcpy

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)

dcdcpy contains utilities to work with DataCamp Data Connector.

This package is designed to be used by administrators and managers of
DataCamp groups. Some prior experience of writing reports with Python is
recommended.

## Installation

You can install the development version with:

```
pip install git+https://github.com/datacamp/dcdcpy.git#egg=dcdcpy
```

## Importing data

Importing data requires two commands. First you set up the connector to
S3, then you get the datasets. By default, all the data is returned for
the most recent date.

```py
import dcdcpy

# Setup Amazon S3 session
s3_sess = dcdcpy.create_s3_session()

# Retrieve all data on the latest date available
dc = dcdcpy.get_dc_datasets(s3_sess)
```


You can specify which datasets are returned, on which date.

```py
dc_team = get_dc_datasets(s3_sess, ["team_dim"], datetime.date.today() - datetime.timedelta(days=7))
```
