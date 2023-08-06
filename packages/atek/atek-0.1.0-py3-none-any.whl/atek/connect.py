"""Provides basic utilities to query a mysql database over an ssh tunnel"""
from sshtunnel import SSHTunnelForwarder, open_tunnel
import pandas as pd
import pymysql
from pathlib import Path
from typing import Optional, List, Dict, Any, Iterable, Union
from enum import Enum
from configparser import ConfigParser
from contextlib import contextmanager


__all__ = ["query", "connect", "query_df", "query_dicts", "query_gen"]


def config():
    """Returns the connection parameters to connect to atek02_main database on public_html server."""
    path = Path("~/.atek/read_only").expanduser()
    config = ConfigParser()
    config.read(path)

    server = {
        "ssh_address_or_host": (
            config["db"]["ssh_address"],
            int(config["db"]["ssh_port"])
        ),
        "ssh_username": config["db"]["ssh_username"],
        "ssh_password": config["db"]["ssh_password"],
        "ssh_pkey": config["db"]["ssh_pkey"],
        "remote_bind_address": (config["db"]["db_host"], int(config["db"]["db_port"])),
    }

    db = {
        "host": config["db"]["db_host"],
        "db": config["db"]["db_name"],
        "user": config["db"]["db_user"], 
        "password": config["db"]["db_password"],
    }

    return {"server": server, "db": db}


class Returns(Enum):
    """Used to determine the return type of query and the cusrosclass of connect."""
    dataframe          = 1
    list_of_dicts      = 2
    generator_of_dicts = 3


@contextmanager
def connect(returns: Returns=Returns.dataframe) -> pymysql.connections.Connection:
    """Creates a ssh tunnel and returns a connection options to atek02_main."""
    cursorclass = (
        pymysql.cursors.DictCursor if returns is Returns.list_of_dicts else 
        pymysql.cursors.SSDictCursor if returns is Returns.generator_of_dicts else 
        pymysql.cursors.Cursor
    )


    with SSHTunnelForwarder(**config()["server"]) as server:

        conn = pymysql.connect(
            **config()["db"],
            port=server.local_bind_port,
            cursorclass=cursorclass
        )

        yield conn

        conn.close()

Record = Dict[str,Any]
ListTable = List[Record]
GenTable = Iterable[Record]
Table = Union[pd.DataFrame, ListTable, GenTable]

def query_df(sql: str) -> pd.DataFrame:
    """Returns a dataframe."""
    with connect(Returns.dataframe) as conn:
        return pd.read_sql(sql, conn)


def query_dicts(sql: str) -> ListTable:
    """Returns a list of dict objects as records."""
    with connect(Returns.list_of_dicts) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows


def query_gen(sql: str) -> GenTable:
    """Yiels a generator of dict objects as records."""
    with connect(Returns.generator_of_dicts) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall_unbuffered()
        for row in rows:
            yield row
        

def query(sql: str, returns: Returns=Returns.dataframe) -> Table:
    """Utility function with combines connect, query_df, query_dicts, and 
    query_gen."""
    funcs = {
        Returns.dataframe: query_df,
        Returns.list_of_dicts: query_dicts,
        Returns.generator_of_dicts: query_gen,
    }
    return funcs[returns](sql)


if __name__ == "__main__":
    # Import test libraries
    from tabulate import tabulate
    from cytoolz.curried import pipe

    # Info query to execute on atek02_main
    sql =  """
    select
    database() as current_database
    ,current_user() as login_user
    ,version() as version
    ,now() as connected
    """

    #  For each return type
    for member in Returns:
        print(member)

        print("Raw")
        print(f"{query(sql, member)}")

        print("\nFormatted")
        if member is Returns.dataframe:
            pipe(
                query_df(sql)
                .to_markdown(tablefmt="fancy_grid")
                ,print
            )
        elif member is Returns.list_of_dicts:
            pipe(
                query_dicts(sql)
                ,lambda data: tabulate(data, headers="keys", tablefmt="fancy_grid")
                ,print
            )
        elif member is Returns.generator_of_dicts:
            pipe(
                query_gen(sql)
                ,list
                ,lambda data: tabulate(data, headers="keys", tablefmt="fancy_grid")
                ,print
            )

