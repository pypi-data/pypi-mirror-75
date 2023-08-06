from atek_main.connect import *
import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np
import cytoolz.curried as tz
from typing import List, Optional, Union
from fnmatch import fnmatch
from pathlib import Path
from datetime import date


def orders_by_client(refresh: bool=False) -> pd.DataFrame:
    path = root() / "data/Orders by Client.csv"
    sql = """
    select
        curdate() as As_of_Date
        ,orders.orderNo as Order_Number
        ,orders.clientID as Client_ID
        ,clients.Client
        ,orders.order_date as Order_DateTime
        ,orders.status as Order_Status
        ,orders.prop_state as Property_State
        ,assignment.appr_fee as Appraiser_Fee
        ,invoices.total as Client_Fee
        ,case
            when orders.status = 'Complete' then invoices.total - assignment.appr_fee
            else null
            end as Admin_Fee
    from orders
        left join clients on orders.clientID = clients.ID
        left join order_assignment assignment on orders.orderNo = assignment.orderno
        left join invoices on orders.orderNo = invoices.order_num
    where
        orders.order_date >= '2017-01-01'
    """
    if path.exists() and refresh:
        path.unlink()

    def read():
        return tz.pipe(
            pd.read_csv(path, parse_dates=["As_of_Date", "Order_DateTime"])
            .assign(**{
                "Order_Date": lambda df: df.Order_DateTime.dt.strftime("%Y-%m-%d").astype("datetime64"),
                "Order_Month": lambda df: df.Order_Date.dt.strftime("%Y-%m"),
                "Order_Year": lambda df: df.Order_Date.dt.year,
            })
            .query("Order_Status != 'Cancelled'")
        )

    if path.exists():
        return read()

    return tz.pipe(
        query(sql)
        .to_csv(path, index=False)
        ,lambda _: read()
    )


def report_orders_by_client(refresh: bool=False, pretty: bool=False, export: bool=False) -> pd.DataFrame:
    data = orders_by_client(refresh)
    path = root() / f"reports/Orders by Client {data.As_of_Date.max().strftime('%Y-%m_%d')}.xlsx"

    return tz.pipe(
        orders_by_client(refresh)
        .assign(**{
            "Rel_Year": lambda df: df.Order_Year - df.As_of_Date.dt.year,
            "YTD_Date": lambda df: (df.As_of_Date + (df.Rel_Year * np.timedelta64(1, "Y"))).dt.normalize(),
            "YTD": lambda df: np.where(df.Order_Date <= df.YTD_Date, 1, 0),
        })
        ,lambda df: pd.concat([
            df.query("YTD == 1").assign(**{"Period": "YTD"}),
            df.assign(**{"Period": "All"}),
        ])
        .groupby(["As_of_Date", "Client_ID", "Client", "Order_Year", "Period"])
        .agg(**{
            "Orders": ("Order_Number", "size")
        })
        .reset_index()
        ,lambda df: df.merge(
            df
                .assign(**{
                    "Prior_Orders": df.Orders,
                    "Prior_Year": df.Order_Year + 1,
                })
                .filter(["Client_ID", "Period", "Prior_Year", "Prior_Orders"]),
            left_on=["Client_ID", "Period", "Order_Year"],
            right_on=["Client_ID", "Period", "Prior_Year"],
            how="left"
        )
        .drop(columns=["Prior_Year"])
        .assign(**{
            "Prior_Orders": lambda df: df.Prior_Orders.fillna(0),
            "Client_Status": lambda df:
                np.where(df.eval("Prior_Orders > 0 and Orders == 0"), "Lost",
                np.where(df.eval("Prior_Orders > 0"), "Existing",
                "New"
            )),
            "Change_YoY": lambda df: df.Orders - df.Prior_Orders,
            "Pct_Change_YoY": lambda df: np.where(df.Prior_Orders > 0, df.Change_YoY / df.Prior_Orders, pd.NA),
            "Pct_Orders_by_Year": lambda df: df.Orders / df.groupby(["Period", "Order_Year"])["Orders"].transform("sum"),
            "Pct_Orders_by_Year_Client_Status": lambda df: df.Orders
                / df.groupby(["As_of_Date", "Period", "Order_Year", "Client_Status"])["Orders"].transform("sum"),
            "Rank_by_Year": lambda df: df.groupby(["Period", "Order_Year"])["Orders"]
                .rank(ascending=False, method="min"),
            "Rank_by_Client_Status": lambda df: df.groupby(["As_of_Date", "Period", "Order_Year", "Client_Status"])["Orders"]
                .rank(ascending=False, method="min"),
        })
        ,lambda df: df.rename(columns={col: col.replace("_", " ") for col in df.columns}) if pretty else df
        ,lambda df: df.to_excel(path, sheet_name="Orders by Client", index=False) if export else df
    )

#  report_orders_by_client(False, True, True)
import os
for k, v in os.environ.items():
    if "SSH_" in k or "DB_" in k:
        print(f"{k}:{v}")

tz.pipe(
    query("select * from orders order by order_date desc limit 10")
    ,vert
    ,show
)
