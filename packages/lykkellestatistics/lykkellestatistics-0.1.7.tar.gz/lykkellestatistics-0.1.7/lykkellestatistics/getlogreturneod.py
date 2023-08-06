#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#successfully tested. ready for Prod
"""
Created on Wed Jul 17 12:23:51 2019
calculate log returns for any series.
Input parameters are symbol and history table
send totest
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd
import psycopg2 as psg
import numpy as np


class getlogreturn:
    def __init__(self, symbol, table, cursor):
        # symbol = 'RDSA.AS'
        # table = 'stock_history'
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        selret = "select price, price_date from "+ table + " where symbol=%s and price_date > current_date - 31 order by price_date"
        delret = "delete from "+ table + " where symbol=%s and (price is null or price <= 0)"
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
            print(e)
        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['Price', 'Price_date'])
        # print(sh['Price'])
        # print(len(sh),"before")
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        # print(len(sh),"after")
        if len(sh) > 1:
        # print(sh)
            try:
                print("Getting log return for:", symbol)
                sh['return'] = np.log(sh['Price'])-np.log(sh['Price'].shift(1))
            except AttributeError:
                print(symbol, " couldn't fetch return. See value sample below")
                print(sh.head())
            # print(sh.head(20))
            # load the returns into table
            updret = "update "+table+" set price_return=%s where symbol=%s and price_date=%s"
            fl = len(sh)
            c = 0
            for i in range(fl):
                pdate = sh.iloc[i, 1]
                pret = sh.iloc[i, 2]
                if np.isnan(pret):
                    pret = None
                else:
                    pass
                try:
                    cursor.execute(updret, (pret, symbol, pdate))
                    c = c+1
                except (Exception, psg.Error) as e:
                    print("Load unsuccessful for ", symbol, "& ", pdate)
                    print(e)
            print(c, " out of ", fl, " loaded for ticker", symbol, "to table ", table)
        else:
            print("Less than 2 entries for symbol ", symbol, "minmum non null entries needed is 2")
        print("postgres connection closed")

