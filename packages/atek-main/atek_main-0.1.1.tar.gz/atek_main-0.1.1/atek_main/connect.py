"""Provides basic utilities to query a mysql database over an ssh tunnel"""
from sshtunnel import SSHTunnelForwarder, open_tunnel
import pymysql
import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np
import cytoolz.curried as tz
from typing import List, Optional, Union
from fnmatch import fnmatch
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
import os
from textwrap import fill
from tabulate import tabulate


__all__ = ["query", "root", "load_env"]


def root():
    #  return Path(__file__).parent
    return Path("/Users/rusty.hansen/py-analysis/atek_main")

DOT_ENV_PATH = Path(root() / ".env/connect.ini").resolve()
print(f"{DOT_ENV_PATH.exists()=}")

def load_env(path: Optional[Path]=None):
    """Loads contents of {path} to environment variables"""
    global DOT_ENV_PATH
    if path:
        DOT_ENV_PATH = path 

    if not DOT_ENV_PATH.exists():
        raise ValueError(f"DOT_ENV_PATH = '{DOT_ENV_PATH}' does not exist")

    result = load_dotenv(dotenv_path=DOT_ENV_PATH, override=True)

    if result:
        return f"load_env loaded '{DOT_ENV_PATH}'"
    else:
        return ValueError(f"load_env could not load '{DOT_ENV_PATH}'")

print(load_env())

@tz.curry
def query(sql: str) -> pd.DataFrame:
    """Returns a dataframe from provided {sql}"""
    ssh_host = os.getenv("SSH_HOST")
    ssh_port = int(os.getenv("SSH_PORT"))
    ssh_pass = os.getenv("SSH_PASS")
    ssh_user = os.getenv("SSH_USER")
    ssh_pkey = os.getenv("SSH_PKEY")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_password=ssh_pass,
        ssh_username=ssh_user,
        ssh_pkey=ssh_pkey,
        remote_bind_address=(db_host, 3306)) as tunnel:

        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            port=tunnel.local_bind_port,
            db=db_name,
        )

        df = pd.read_sql(sql, conn)
        conn.close()
        return df


if __name__ == "__main__":
    for k, v in os.environ.items():
        if "SSH_" in k or "DB_" in k:
            print(f"{k}:{v}")

    from atek_main.df_toolz import show
    show(query("select version() as version"))
