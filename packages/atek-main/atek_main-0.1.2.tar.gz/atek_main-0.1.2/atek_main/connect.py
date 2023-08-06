"""Provides basic utilities to query a mysql database over an ssh tunnel"""
from sshtunnel import SSHTunnelForwarder, open_tunnel
import pandas as pd
import pymysql
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
import os


__all__ = ["query", "load_env"]


def load_env(path: Optional[Path]=None):
    """Loads contents of {path} to environment variables"""

    if not path.exists():
        raise ValueError(f"path = '{path}' does not exist")

    result = load_dotenv(dotenv_path=path, override=True)

    if result:
        return f"load_env loaded '{path}'"
    else:
        return ValueError(f"load_env could not load '{path}'")


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
    load_env(Path(__file__).parent.resolve() / ".env/connect.ini")
    for k, v in os.environ.items():
        if "SSH_" in k or "DB_" in k:
            print(f"{k}:{v}")

    from tabulate import tabulate
    from cytoolz.curried import pipe
    pipe(
        query("select version() as version")
        ,lambda df: df
        .to_dict("records")
        ,lambda table: tabulate(table, headers="keys", tablefmt="fancy_grid")
        ,print
    )
