#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from cytoolz.curried import pipe, curry, map
import cytoolz.curried as tz
import pandas as pd
import numpy as np
from typing import List
import openpyxl as xl
from atek_main import show, vert
import re
from datetime import date


def dir_root():
    return Path(__file__).parent.absolute()


def dir_mercury():
    return dir_root() / "acad_recon/mercury"


def dir_workday():
    return dir_root() / "acad_recon/workday"


def dir_reports():
    return dir_root() / "acad_recon/reports"


def sheets(path: Path) -> List[str]:
    wb = xl.load_workbook(str(path))
    return [sht.title for sht in wb.worksheets]


@curry
def resub(pat, repl, string):
    return re.sub(pat, repl, string)


def admin_fee(product: str) -> List[str]:
    apprs = {"1004", "1004C", "1025", "1073", "1075", "2055"}
    add_ons = {"216", "1007", "90251", "CIR", "CDAIR"}

    # 2020-07-30 Sarah J noted that Product = 'FHA Inspection (CIR)' is like a final inspection
    # and should be = $50. Did not make the change as 'CIR' is specifically listed as 
    # an add on. FHA Final Inspection (1004D) is $50.

    m = re.search("(\(.*\))", product)
    return pipe(
        m[0] if m else product
        ,resub("[(),]|and |FNMA", "")
        ,lambda s: set(s.split())
        ,lambda forms: (
            100 if forms & apprs and not forms & add_ons else
            125 if forms & apprs and forms & add_ons else
            25 if forms & add_ons else
            50 if "1004D" in forms else
            0 if "Conversion" in product else
            25 if "Disaster" in product else
            100 if product == "General Purpose Appraisal Report" else
            None
        ),
    )


def mercury_data():
    return pipe(
        dir_mercury().glob("*.xlsx")
        ,tz.map(lambda path: pd.read_excel(path).assign(**{"File_Name": path.name}))
        ,lambda dfs: pd.concat(list(dfs))
        .assign(**{
            "ATEK_Invoice_Date": lambda df: df.File_Name.str.extract("(\d{4}_\d{2}_\d{2})")
        })
        .astype({
            "Create Date": "datetime64",
            "Uploaded Date": "datetime64",
        })
        .assign(**{
            "ATEK Invoice Date": lambda df: df.ATEK_Invoice_Date.str.replace("_", "-").astype("datetime64"),
            "Diff": lambda df: df["Borrower Amount"] - df["Total Payable"],
            "Has Admin Fee": lambda df: df.eval("Diff > 0"),
            "Admin Fee": lambda df: df.Diff * df["Has Admin Fee"],
            "Loss": lambda df: df.eval("Diff < 0"),
            "Lost Money": lambda df: df.Diff * df.Loss,
            "After 07/01": lambda df: df.eval("`Create Date` >= '2020-07-01'"),
            # Status starts at 02 to preserver 01 for Workday recon
            "Admin Fee Status": lambda df: 
                np.where(df.eval("not `After 07/01`"), "02 Order Date Before 07/01",
                np.where(df.eval("`Property State` == 'AZ' and `Create Date` < '2020-07-13'"),
                    "03 AZ 07/13",
                np.where(df.eval("`Property State` == 'TX' and `Create Date` < '2020-07-13'"),
                    "04 TX before 07/13",
                np.where(df.eval("`Create Date` < '2020-07-10'"), "05 Mercury Script Incorrect Before 07/10",
                "06 Systems Correct"
             )))),
            "Correct Admin Fee": lambda df: df.Product.apply(admin_fee) * df["After 07/01"],
            "Admin Fee Loss": lambda df: df["Admin Fee"] - df["Correct Admin Fee"],
            "Has Dups": lambda df: np.where(
                df.groupby("Order ID")["Order ID"].transform("size") > 1, 1, 0),
            "Order Row": lambda df: 1, 
        })
        .sort_values(by=["Order ID", "Create Date", "ATEK Invoice Date"], ascending=[True, True, True])
        .assign(**{
            "Order Row": lambda df: df.groupby("Order ID")["Order Row"].cumsum(),
        })
        .filter(["Order ID", "Borrower", "Property Street Address", "Property State", 
            "Loan Number", "Create Date", "Uploaded Date", "Borrower Amount", "Total Payable", 
            "Product", "File_Name", "ATEK Invoice Date", "Diff", "Has Admin Fee", "Admin Fee", "Loss", 
            "Lost Money", "After 07/01", "Admin Fee Status", "Correct Admin Fee", "Admin Fee Loss", "Has Dups",
            "Order Row",
        ])
    )


def mercury_summary():
    return pipe(
        mercury_data()
        .groupby(["File Date", "Status"])
        .agg(**{
            "Orders": ("Order ID", "size"),
            "Borrower Amount": ("Borrower Amount", "sum"),
            "Total Payable": ("Total Payable", "sum"),
            "Admin Fee": ("Admin Fee", "sum"),
            "Lost Money": ("Lost Money", "sum"),
            "Correct Admin Fee": ("Correct Admin Fee", "sum"),
            "Admin Fee Loss": ("Admin Fee Loss", "sum"),
            "Has Admin Fee": ("Has Admin Fee", np.mean),
            "Loss": ("Loss", np.mean),
            "After 07/01": ("After 07/01", np.mean),
        })
        .reset_index()
        .assign(**{
            "% Orders by File Date": lambda df: df.Orders / df.groupby("File Date")["Orders"].transform("sum"),
        })
        .sort_values(by=["File Date", "Status"], ascending=[True, True])
        #  ,show(col_width=60)
    )


def workday_data():
    return pipe(
        Path.cwd() / "acad_recon/workday/ATEK Invoices 2020-07-31.xlsx"
        ,pd.read_excel
        ,lambda data: data
        .astype({"Invoice Date": "datetime64"})
        .assign(**{
            "IsEmployeeBillBack": lambda df: pd.notna(df["Supplier's Invoice Number"].str.extract("(0[67]\d\d2020)")),
            "IsAppraiserPayment": lambda df: pd.notna(df["Supplier's Invoice Number"].str.extract("(MERC-)")),
            "Invoice Type": lambda df: 
                np.where(df.IsEmployeeBillBack, "Employee Billback", 
                np.where(df.IsAppraiserPayment, "Appraiser Payment", 
                "Other")),
            "Order ID": lambda df: df["Supplier's Invoice Number"],
            "Has Dups": lambda df:
                np.where(df.IsAppraiserPayment == False, 0,
                np.where(df.groupby("Order ID")["Order ID"].transform("size") > 1, 1, 
                0)),
        })
    )

def make_report():
    path = dir_reports() / f"Admin Fee Analysis {date.today().strftime('%y-%m-%d')}.xlsx"
    with pd.ExcelWriter(path) as file:
        mercury_data().to_excel(file, sheet_name="Data", index=False)
        mercury_summary().to_excel(file, sheet_name="Summary", index=False)
    print(f"Saved {path}")

pipe(
    mercury_data()
    .query("`Order Row` == 1")
    .merge(
        workday_data().filter(["Order ID", "Invoice Type", "Invoice Date", "Invoice Amount", "Has Dups"]),
        on="Order ID",
        how="outer",
        suffixes=[" Mercury", " Workday"],
        indicator=True,
    )
    .assign(**{
        "Records": 1,
        "Mercury Invoice Status": lambda df: 
            np.where(df._merge == "right_only", "07 Not Included in Mercury Files",
            np.where(df._merge == "left_only", "01 Missing in Workday",
            df["Admin Fee Status"],
        )),
        "Academy Accounting Status": lambda df: 
            np.where(df._merge == "left_only", "Not Paid", 
            df["Invoice Type"]
        ),
        "Academy Invoice Date": lambda df: df["Invoice Date"],
        "Academy Paid Amount": lambda df: df["Invoice Amount"],
        "Mercury Invoice Amount": lambda df: df["Borrower Amount"],
        "Mercury Payable Amount": lambda df: -df["Total Payable"],
    })
    .to_excel(
        dir_reports() / f"Admin Fee Analysis {date.today().strftime('%y-%m-%d')}.xlsx",
        sheet_name="Recon",
        index=False
    )
)

#  if __name__ == "__main__":
    #  make_report()
    
