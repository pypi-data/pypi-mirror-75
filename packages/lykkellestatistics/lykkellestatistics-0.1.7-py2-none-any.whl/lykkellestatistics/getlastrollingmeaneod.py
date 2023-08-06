#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 11:56:35 2019

@author: debmishra
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:21:54 2019

@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd
import psycopg2 as psg
import numpy as np


class getlastrollingmean:
    def rollingmean50d(symbol, table, cursor):
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        selret = "select price, price_date,ma_50d from "+ table + " where symbol=%s and price_date > current_date - 31 order by price_date desc"
        delret = "delete from "+ table + " where symbol=%s and (price is null or price <= 0)"
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
            print(e)
        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['Price', 'Price_date','ma50d'])
        # print(sh['Price'])
        # print(len(sh),"before")
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        # print(len(sh),"after")
        if len(sh) > 1:
        # print(sh)
            rc = 0
            rl = 0
            for i in range(len(sh)):
                ma50d = sh['ma50d'].iloc[i]
                pdate = sh['Price_date'].iloc[i]
                #print(ma50d,pdate)
                if ma50d is None or np.isnan(ma50d):
                    rl = rl+1
                    selq = """select price,price_date from
                            stock_history where symbol=%s and price_date<=%s
                            order by price_date desc fetch first 50 rows only"""
                    cursor.execute(selq,(symbol,pdate))
                    list50d = cursor.fetchall()
                    if len(list50d)==50:
                        psum = 0
                        #counter = 0
                        for j in range(len(list50d)):
                            pprc = list50d[j][0]
                            psum = psum + pprc
                            #counter = counter + 1
                        p50 = psum/50
                        #print(counter)
                        #print("50day mean for ",symbol, "and date",pdate," is ",p50)
                    else:
                        p50 = None
                    updp50 = "update "+table+" set MA_50D=%s where symbol=%s and price_date=%s and MA_50D is null"
                    try:
                        cursor.execute(updp50, (p50, symbol, pdate))
                        rc = rc+1
                    except (Exception, psg.Error) as e:
                        print("Load unsuccessful for ", symbol, "& ", pdate)
                        print(e)
                else:
                    pass
                    #print("50day mean for ",symbol, "and date",pdate," is already present in DB-",ma50d,"so Skipping")
            print(rc, " out of ", rl , "valid 50D loaded for ticker", symbol,"having total ",len(sh),"entries to table ", table)
        else:
            print("Less than 2 entries for symbol ", symbol, "minmum non null entries needed is 2")
        print("postgres connection closed")
    def rollingmean200d(symbol, table, cursor):
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        selret = "select price, price_date,ma_200d from "+ table + " where symbol=%s and price_date > current_date - 31 order by price_date desc"
        delret = "delete from "+ table + " where symbol=%s and (price is null or price <= 0)"
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
            print(e)
        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['Price', 'Price_date','ma200d'])
        # print(sh['Price'])
        # print(len(sh),"before")
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        # print(len(sh),"after")
        if len(sh) > 1:
        # print(sh)
            rc = 0
            rl = 0
            for i in range(len(sh)):
                ma200d = sh['ma200d'].iloc[i]
                pdate = sh['Price_date'].iloc[i]
                #print(ma50d,pdate)
                if ma200d is None or np.isnan(ma200d):
                    rl = rl+1
                    selq = """select price,price_date from
                            stock_history where symbol=%s and price_date<=%s
                            order by price_date desc fetch first 200 rows only"""
                    cursor.execute(selq,(symbol,pdate))
                    list200d = cursor.fetchall()
                    if len(list200d)==200:
                        psum = 0
                        #counter = 0
                        for j in range(len(list200d)):
                            pprc = list200d[j][0]
                            psum = psum + pprc
                            #counter = counter + 1
                        p200 = psum/200
                        #print(counter)
                        #print("200day mean for ",symbol, "and date",pdate," is ",p200)
                    else:
                        p200 = None
                    updp200 = "update "+table+" set MA_200D=%s where symbol=%s and price_date=%s and MA_200D is null"
                    try:
                        cursor.execute(updp200, (p200, symbol, pdate))
                        rc = rc+1
                    except (Exception, psg.Error) as e:
                        print("Load unsuccessful for ", symbol, "& ", pdate)
                        print(e)
                else:
                    pass
                    #print("50day mean for ",symbol, "and date",pdate," is already present in DB-",ma50d,"so Skipping")
            print(rc, " out of ", rl , "valid 200D loaded for ticker", symbol,"having total ",len(sh),"entries to table ", table)
        else:
            print("Less than 2 entries for symbol ", symbol, "minmum non null entries needed is 2")
        print("postgres connection closed")