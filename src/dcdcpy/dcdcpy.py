import boto3
import pandas as pd
import os
import awswrangler as wr
import pkg_resources
from functools import lru_cache
from jinja2 import Template
from pyathena import connect
from IPython.display import display, Markdown
from warnings import warn


def get_env_var_s3_bucket():
    env_var = os.getenv("AWS_S3_BUCKET_NAME", os.getenv("AWS_BUCKET"))
    if env_var is None:
        raise EnvironmentError("The environment variable 'AWS_BUCKET' has not been set.")
    return env_var


def get_env_var_region():
    env_var = os.getenv("AWS_DEFAULT_REGION", os.getenv("AWS_REGION"))
    if env_var is None:
        raise EnvironmentError("The environment variable 'AWS_REGION' has not been set.")
    return env_var

def get_env_var_aws_access_key():
    env_var = os.getenv("AWS_ACCESS_KEY_ID")
    if env_var is None:
        raise EnvironmentError("The environment variable 'AWS_ACCESS_KEY_ID' has not been set.")
    return env_var

def get_env_var_aws_secret():
    env_var = os.getenv("AWS_SECRET_ACCESS_KEY")
    if env_var is None:
        raise EnvironmentError("The environment variable 'AWS_SECRET_ACCESS_KEY' has not been set.")
    return env_var

def get_env_var_athena_s3_staging_dir():
    env_var = os.getenv("AWS_ATHENA_S3_STAGING_DIR")
    if env_var is None:
        raise EnvironmentError("The environment variable 'AWS_ATHENA_S3_STAGING_DIR' has not been set.")
    return env_var



@lru_cache(maxsize=None)
def list_tables_s3():
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket(get_env_var_s3_bucket())
    return [
        obj.key.split("/")[1].split(".")[0]
        for obj in my_bucket.objects.filter(Delimiter="/", Prefix=f"latest/")
    ]


@lru_cache(maxsize=None)
def get_docs_bic():
    stream = pkg_resources.resource_stream(__name__, "data/docs_bic.csv")
    docs_bic = pd.read_csv(stream)
    tables = docs_bic.table_name.unique().tolist()
    data = {}

    for table in tables:
        doc = docs_bic.query("table_name == @table")
        data[table] = {
            "table_name": doc["table_name"].tolist()[0],
            "table_title": " ".join(
                [w.title() for w in doc["table_name"].tolist()[0].split("_")]
            ),
            "table_description": doc["table_description"].tolist()[0],
            "columns": doc[["column", "description"]].to_dict(orient="records"),
        }
    return data


@lru_cache(maxsize=None)
def read_table_s3(table_name, conn=None, date="latest"):
    return wr.s3.read_csv(f"s3://{get_env_var_s3_bucket()}/{date}/{table_name}.csv")


@lru_cache(maxsize=None)
def read_table_athena(table_name, conn, date="latest"):
    s3_bucket = get_env_var_s3_bucket()
    return pd.read_sql_query(f'SELECT * FROM "{s3_bucket}"."{table_name}"', conn)


HELP_DOCS = get_docs_bic()

TEMPLATE = """
### {{ table_title }}

#### Description

{{ table_description }}

#### Columns
{%- for column in columns %}

{{ column['column'] }}

> {{ column['description'] }}

{%- endfor -%}
"""


def display_help(table_name):
    tpl = Template(TEMPLATE)
    out = tpl.render(HELP_DOCS[table_name])
    return display(Markdown(out))


class ReadTable:
    def __init__(self, table_name, date="latest", source="s3", conn=None):
        self.table_name = table_name
        self.conn = conn
        self.date = date
        if source == "s3":
            self.table = read_table_s3
        else:
            self.table = read_table_athena

    def __call__(self, *args, **kwargs):
        return self.table(self.table_name, self.conn, self.date)

    # def __repr__(self):
    #     tpl = Template(TEMPLATE)
    #     out = tpl.render(HELP_DOCS[self.table_name])
    #     return out

    def _repr_html_(self):
        tpl = Template(TEMPLATE)
        out = tpl.render(HELP_DOCS[self.table_name])
        return display(Markdown(out))


class DataConnector:
    def __init__(self, date="latest", source="s3"):
        warn('This package is no longer actively maintained or supported by DataCamp, '
             'please see https://enterprise-docs.datacamp.com/data-connector/data-connector-faq/deprecating-dcdcpy-and-dcdcr '
             'for more information.')
        self.date = date
        self.source = source
        self.tables = list_tables_s3()
        if self.source == "s3":
            self.conn = None
        else:
            self.conn = connect(
                s3_staging_dir=get_env_var_athena_s3_staging_dir(),
                region_name=get_env_var_region(),
            )
        for table in self.tables:
            setattr(
                self,
                table.replace("learning_", ""),
                ReadTable(table, date=self.date, conn=self.conn, source=self.source),
            )
