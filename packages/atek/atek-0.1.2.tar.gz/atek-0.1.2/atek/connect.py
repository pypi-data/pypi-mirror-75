"""Provides basic utilities to query a mysql database over an ssh tunnel"""
from sshtunnel import SSHTunnelForwarder, open_tunnel
import pandas as pd
import pymysql
from pymysql.cursors import Cursor, SSDictCursor
from pymysql.connections import Connection
from pathlib import Path
from typing import *
from enum import Enum
from configparser import ConfigParser
from contextlib import contextmanager


__all__ = ["query", "connect", "Returns", "paths", "print_dict"]


def get_config(config_path: str):
    config = ConfigParser()
    path = Path(config_path).expanduser()
    config.read(path)
    settings = {
        section: {
            key: (
                tuple([
                    value.split()[0], 
                    int(value.split()[1])
                ]) if "address" in key else 
                value
            )
            for key, value in config[section].items()
        }
        for section in config.sections()
    }
    return settings


def server():
    return get_config("~/.atek/config")["public_html"]


def database():
    return get_config("~/.atek/config")["atek02_main"]


def paths():
    return get_config("~/.atek/config")["paths"]


def print_dict(name: str, d: dict, print_out: bool=True):
    text = name
    max_k = max(len(str(k)) for k in d)
    for k, v in d.items():
        text += f"\n\t{k: <{max_k}} = {v}"
    if print_out:
        print(text)
    return text


class Returns(Enum):
    """Used to determine the return type of query and the cusrosclass of connect."""
    dataframe = 1
    records   = 2


def cursor_type(returns: Returns) -> Union[Cursor, SSDictCursor]:
    cursors = {
        Returns.records   : SSDictCursor,
        Returns.dataframe : Cursor,
    }
    return cursors[returns]


@contextmanager
def connect(returns: Returns) -> Connection:
    """Creates a ssh tunnel and returns a connection options to atek02_main."""

    with SSHTunnelForwarder(**server()) as tunnel:

        conn = pymysql.connect(
            **database(),
            port=tunnel.local_bind_port,
            cursorclass=cursor_type(returns)
        )

        yield conn

        conn.close()


def query_dataframe(sql: str) -> pd.DataFrame:
    """Returns a dataframe."""
    with connect(Returns.dataframe) as conn:
        return pd.read_sql(sql, conn)


Record = Dict[str,Any]
Table = Iterable[Record]

def query_records(sql: str) -> Table:
    """Yiels a generator of dict objects as records."""
    with connect(Returns.records) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall_unbuffered()
        for row in rows:
            yield row


def query(sql: str, returns: Returns=Returns.dataframe) -> Union[pd.DataFrame, Table]:
    """Utility function with combines connect, query_df, query_dicts, and 
    query_gen."""
    funcs = {
        Returns.dataframe: query_dataframe,
        Returns.records: query_records,
    }
    return funcs[returns](sql)


if __name__ == "__main__":
    from pprint import pprint

    sql =  """
    select
    database() as current_database
    ,current_user() as login_user
    ,version() as version
    ,now() as connected
    """

    print(Returns.dataframe)
    print(query(sql, Returns.dataframe), "\n\n")

    print(Returns.records)
    pprint(list(query(sql, Returns.records)))
