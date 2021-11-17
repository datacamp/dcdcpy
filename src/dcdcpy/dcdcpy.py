import boto3
import pandas as pd
import os
import awswrangler as wr
import pkg_resources
from functools import lru_cache
from jinja2 import Template
from pyathena import connect
from IPython.display import display, Markdown


def list_tables_s3():
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket(os.getenv("AWS_BUCKET"))
    return [
        obj.key.split("/")[1].split(".")[0]
        for obj in my_bucket.objects.filter(Delimiter="/", Prefix=f"latest/")
    ]


def read_table_s3(table_name, conn=None):
    @lru_cache(maxsize=None)
    def read_table(date="latest"):
        return wr.s3.read_csv(f"s3://{os.getenv('AWS_BUCKET')}/{date}/{table_name}.csv")

    return read_table


def read_table_athena(table_name, conn):
    @lru_cache(maxsize=None)
    def read_table(date="latest"):
        s3_bucket = os.getenv("AWS_BUCKET")
        return pd.read_sql_query(f'SELECT * FROM "{s3_bucket}"."{table_name}"', conn)

    return read_table


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
            "table_description": doc["table_description"].tolist()[0],
            "columns": doc[["column", "description"]].to_dict(orient="records"),
        }
    return data


HELP_DOCS = get_docs_bic()

TEMPLATE = """
### {{ table_name }}

#### Description

{{ table_description }}

#### Columns
{%- for column in columns %}

{{ column['column'] }}

> {{ column['description'] }}

{%- endfor -%}
"""


class ReadTable:
    def __init__(self, table_name, source="s3", conn=None):
        self.table_name = table_name
        self.conn = conn
        if source == "s3":
            self.table = read_table_s3(table_name, conn)
        else:
            self.table = read_table_athena(table_name, conn)

    def __call__(self, *args, **kwargs):
        return self.table(*args, **kwargs)

    def _repr_html_(self):
        tpl = Template(TEMPLATE)
        out = tpl.render(HELP_DOCS[self.table_name])
        return display(Markdown(out))


class DataConnector:
    def __init__(self, source="s3"):
        self.tables = list_tables_s3()
        if source == "s3":
            conn = None
        else:
            conn = connect(
                s3_staging_dir=os.getenv("AWS_ATHENA_S3_STAGING_DIR"),
                region_name=os.getenv("AWS_REGION"),
            )
        for table in self.tables:
            setattr(self, table, ReadTable(table, source=source, conn=conn))
