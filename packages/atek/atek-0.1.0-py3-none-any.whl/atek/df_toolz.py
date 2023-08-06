#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from fnmatch import fnmatch
from tabulate import tabulate
from cytoolz.curried import pipe, curry, take, identity
from textwrap import fill
from typing import Union, Optional, List, Any

__all__ = ["is_df", "filter_col", "vert", "show"]

def is_df(obj: Any, param_name: str="dataframe") -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj

    raise ValueError(f"arg '{param_name}' must be a pandas.DataFrame")


@curry
def filter_col(patterns: Union[str, List[str]],
    dataframe: pd.DataFrame) -> pd.DataFrame:
    """Filteres the columns of a dataframe using list
    of fnmatch patterns"""

    patterns = [patterns] if isinstance(patterns, str) else patterns
    columns = list(dataframe.columns)
    filtered = set(
        col
        for col in is_df(dataframe).columns
        for pat in patterns
        if fnmatch(col.lower(), pat.lower())
    )
    return dataframe.filter(list(filtered))


@curry
def vert(dataframe: pd.DataFrame, limit: Optional[int]=3) -> pd.DataFrame:
    """Transposes dataframe columns to rows"""

    return pipe(
        dataframe
        ,is_df
        ,lambda df: df.head(limit) if limit else df
        ,lambda df: df.transpose()
        .reset_index()
        ,lambda df: df.rename(columns={
            col:("column" if col == "index" else f"row {int(col)+1:02}")
            for col in df.columns
        })
    )


@curry
def show(dataframe: pd.DataFrame, limit: Optional[int]=100, 
    print_out: bool=True, col_width: int=20, **kwds) -> str:
    """Returns a DataFrame as an asci table using tabulate"""

    defaults = {
        "headers": "keys",
        "tablefmt": "fancy_grid",
    }

    args = {**defaults, **kwds}

    return pipe(
        dataframe
        ,is_df
        ,lambda df: df.head(limit) if limit else df
        ,lambda df: df.to_dict("records")
        ,lambda table: [
            {
                fill(str(k), col_width): fill(str(v), col_width)
                for k, v in row.items()
            }
            for row in table
        ]
        ,lambda x: tabulate(x, **args)
        ,lambda x: print(x) if print_out else x
    )


if __name__ == "__main__":
    from connect import query
    from pathlib import Path


    pipe(
        query("select * from orders limit 10")
        ,filter_col("*date*")
        ,vert
        ,show
    )
