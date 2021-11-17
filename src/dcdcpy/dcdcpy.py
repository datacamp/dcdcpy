import boto3
import pandas as pd
import os
import awswrangler as wr
import pkg_resources
from functools import lru_cache
from jinja2 import Template
from IPython.display import display, Markdown


def list_tables_s3():
    s3 = boto3.resource("s3")
    my_bucket = s3.Bucket(os.getenv("AWS_BUCKET"))
    return [
        obj.key.split("/")[1].split(".")[0]
        for obj in my_bucket.objects.filter(Delimiter="/", Prefix=f"latest/")
    ]


@lru_cache(maxsize=None)
def read_table_s3(table_name, conn=None):
    def read_table(date="latest"):
        return wr.s3.read_csv(f"s3://{os.getenv('AWS_BUCKET')}/{date}/{table_name}.csv")

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


def display_help(table_name):
    def help():
        docs = get_docs_bic()
        tpl = Template(TEMPLATE)
        out = tpl.render(docs[table_name])
        return display(Markdown(out))

    return help


class DataConnector:
    def __init__(self, source="s3"):
        self.tables = list_tables_s3()
        if source == "s3":
            read_table_bic = read_table_s3
        else:
            read_table_bic = read_table_s3

        for table in self.tables:
            setattr(self, table, read_table_bic(table, None))
            setattr(self, f"{table}_help", display_help(table))
