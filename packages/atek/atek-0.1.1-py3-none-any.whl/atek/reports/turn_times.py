#!/usr/bin/env python
# -*- coding: utf-8 -*-

from atek_main import *
from pathlib import Path
from cytoolz.curried import pipe, curry
import pandas as pd
import numpy as np
import cytoolz.curried as tz


def root():
    return Path(__file__).parent.resolve()


#  load_env(root() / ".env/connect.ini")
load_env()

def pretty(df):
    return pipe(
        df
        .sort_values(by=["Property_State", "Property_County"])
        .rename(columns={col: col.replace("_", " ") for col in df.columns})
    )


sql = """
select *
from (
select 
    *
    ,case
        when Form_1004         = 1 then 1
        when Form_1004C        = 1 then 1
        when Form_1004_Modular = 1 then 1
        when Form_1073         = 1 then 1
        when Form_1075         = 1 then 1
        when Form_2055I        = 1 then 1
        when Form_2055E        = 1 then 1
        else 0 
        end as Form_1004_1004C_1073_1075_2055
    ,case
        when Appraiser_Assigned_Date is not null 
            and Appraiser_Uploaded_Date is not null 
            then datediff(Appraiser_Uploaded_Date, Appraiser_Assigned_Date) +1
        when Appraiser_Assigned_Date is not null 
            and Appraiser_Uploaded_Date is null 
            and Appraiser_Due_Date is not null
            then datediff(Appraiser_Due_Date, Appraiser_Assigned_Date) +1
        else null
        end as Appraiser_Turn_Time
from (
    select
        orders.orderNo as Order_Number
        ,upper(left(orders.prop_state, 2)) as Property_State
        ,upper(us_zip_codes.county) as Property_County
        ,case 
            when orders.apprtype = 1 then 'Purchase'
            when orders.apprtype = 2 then 'Refinance'
            when orders.apprtype = 3 then 'Private'
            else 'Unknown'
            end as Appraisal_Type
        ,orders.delivery_method as Delivery_Method
        ,orders.status as Order_Status
        ,date(orders.order_date) as Order_Date
        ,nullif(orders.hold_date                                                    , 0000-00-00) as Hold_Date
        ,nullif(cast(orders.release_date as date)                                   , 0000-00-00) as Release_Date
        ,nullif(assign.assigned_date                                                , 0000-00-00) as Appraiser_Assigned_Date
        ,cast(orders.ex_delivery_date as date) as Appraiser_Estimated_Delivery_Date
        ,nullif(orders.first_client_delivery                                        , 0000-00-00) as Appraiser_Uploaded_Date
        ,nullif(orders.delivery_date                                                , 0000-00-00) as Client_Delivery_Date
        ,nullif(orders.req_complete_date                                            , 0000-00-00) as Appraiser_Due_Date
        ,case when sticky.orderno is not null then 1 else 0 end as Test_Order
        ,coalesce(orders.form1004                                                   , 0) as Form_1004
        ,coalesce(orders.form1073                                                   , 0) as Form_1073
        ,coalesce(orders.form1075                                                   , 0) as Form_1075
        ,coalesce(orders.form2055I                                                  , 0) as Form_2055I
        ,coalesce(orders.form2055E                                                  , 0) as Form_2055E
        ,coalesce(orders.form2075                                                   , 0) as Form_2075
        ,coalesce(orders.form1007                                                   , 0) as Form_1007
        ,coalesce(orders.form216                                                    , 0) as Form_216
        ,coalesce(orders.form_desk                                                  , 0) as Form_Desk
        ,coalesce(orders.form_field                                                 , 0) as Form_Field
        ,coalesce(orders.form_rewrite                                               , 0) as Form_Rewrite
        ,coalesce(orders.form_rewrite_info                                          , 0) as Form_Rewrite_Info
        ,coalesce(orders.form442                                                    , 0) as Form_442
        ,coalesce(orders.form_cir                                                   , 0) as Form_Cir
        ,coalesce(orders.form2000A                                                  , 0) as Form_2000A
        ,coalesce(orders.form_texasrev                                              , 0) as Form_Texasrev
        ,coalesce(orders.form_vacant                                                , 0) as Form_Vacant
        ,coalesce(orders.form2070                                                   , 0) as Form_2070
        ,coalesce(orders.form1025                                                   , 0) as Form_1025
        ,coalesce(orders.form1004C                                                  , 0) as Form_1004C
        ,coalesce(orders.form_nonlender                                             , 0) as Form_Nonlender
        ,coalesce(orders.form_disaster                                              , 0) as Form_Disaster
        ,coalesce(orders.form_hudfha                                                , 0) as Form_Hudfha
        ,coalesce(orders.form_1004cfha                                              , 0) as Form_1004Cfha
        ,coalesce(orders.form_1004usda                                              , 0) as Form_1004Usda
        ,coalesce(orders.form_AI_res_green                                          , 0) as Form_AI_Res_Green
        ,coalesce(orders.form203K                                                   , 0) as Form_203K
        ,coalesce(orders.form1004_modular                                           , 0) as Form_1004_Modular
        ,coalesce(orders.form_truewest_desk                                         , 0) as Form_Truewest_Desk
        ,coalesce(orders.form_other                                                 , 0) as Form_Other
        ,coalesce(orders.form_custom1                                               , 0) as Form_Custom1
        ,coalesce(orders.form_custom2                                               , 0) as Form_Custom2
        ,coalesce(orders.form_custom3                                               , 0) as Form_Custom3
        ,coalesce(orders.form_custom4                                               , 0) as Form_Custom4
        ,coalesce(orders.form_custom5                                               , 0) as Form_Custom5
        ,coalesce(orders.AVM                                                        , 0) as AVM
    from orders
        left join order_assignment assign on orders.orderNo = assign.orderno
        left join us_zip_codes on orders.prop_zip = us_zip_codes.zip 
        left join order_sticky sticky on orders.orderNo = sticky.orderno
            and (
                orders.clientID in(5691, 7114)
                or upper(coalesce(sticky.msg, '')) like '%TEST ORDER%'  
            )
    where
        orders.order_date >= '2020-03-01'
    ) as data
) as data2
where
    Form_1004_1004C_1073_1075_2055 = 1
    and Test_Order = 0
    and Appraiser_Turn_Time > 0
order by
    Property_State
    ,Property_County
"""


@curry
def turn_times(sql: str):
    return pipe(
        sql
        ,query
        ,lambda df: df
        .assign(**{
            "Median_Turn_Time_by_County": lambda df: 
                df.groupby(["Property_State", "Property_County"])["Appraiser_Turn_Time"]
                .transform("quantile", 0.50),
            "Pct_25_Turn_Time_by_County": lambda df: 
                df.groupby(["Property_State", "Property_County"])["Appraiser_Turn_Time"]
                .transform("quantile", 0.25),
            "Pct_75_Turn_Time_by_County": lambda df: 
                df.groupby(["Property_State", "Property_County"])["Appraiser_Turn_Time"]
                .transform("quantile", 0.75),
            "Median_Turn_Time_by_State": lambda df: 
                df.groupby(["Property_State"])["Appraiser_Turn_Time"]
                .transform("quantile", 0.50),
            "Pct_25_Turn_Time_by_State": lambda df: 
                df.groupby(["Property_State"])["Appraiser_Turn_Time"]
                .transform("quantile", 0.25),
            "Pct_75_Turn_Time_by_State": lambda df: 
                df.groupby(["Property_State"])["Appraiser_Turn_Time"]
                .transform("quantile", 0.75),
            "Total_Orders_in_State": lambda df: 
                df.groupby(["Property_State"])["Order_Number"].transform("size"),
            "Total_Orders_in_County": lambda df: 
                df.groupby(["Property_State", "Property_County"])["Order_Number"]
                .transform("size"),
            "Pct_Orders_in_State": lambda df: df.Total_Orders_in_County / df.Total_Orders_in_State,
        })
        .sort_values(by=["Property_State", "Property_County"])
    )


@curry
def summary(sql: str):
    return pipe(
        sql
        ,turn_times
        ,lambda df: df
        .filter(["Property_State", "Property_County", "Median_Turn_Time_by_State", "Pct_25_Turn_Time_by_County",
            "Pct_75_Turn_Time_by_County", "Total_Orders_in_State", "Total_Orders_in_County",
            "Due_Date_Suggestion", "Default_Due_Date"])
        .drop_duplicates()
    )


def make_report(sql):
    with pd.ExcelWriter(Path.cwd() / "Turn Time.xlsx") as file:
        pipe(
            sql
            ,turn_times
            ,pretty
            ,lambda df: df
            .to_excel(file, sheet_name="Orders", index=False)
        )
        
        pipe(
            sql
            ,summary
            ,pretty
            ,lambda df: df
            .to_excel(file, sheet_name="Summary", index=False)
        )


if __name__ == "__main__":
    make_report(sql)
    #  show(query(sql))
