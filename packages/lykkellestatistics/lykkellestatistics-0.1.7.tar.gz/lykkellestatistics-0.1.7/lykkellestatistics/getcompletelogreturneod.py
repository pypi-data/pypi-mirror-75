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
import os
from lykkelleconf.connecteod import connect
import pandas as pd
import psycopg2 as psg
import numpy as np

home = os.path.expanduser("~")
cwd = os.path.abspath(os.getcwd())
# print(cwd)

class getcompletelogreturn:
    def __init__(self, symbol, table, cursor, tmp):
        # symbol = 'RDSA.AS'
        # table = 'stock_history'
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        selret = "select symbol, price, price_date, source_table, volume  from "+ table + " where symbol=%s order by price_date"
        delret = "delete from "+ table + " where symbol=%s and (price is null or price <= 0)"
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
            print(e)
        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['symbol','Price', 'Price_date','source_table','volume'])
        # print(sh['Price'])
        # print(len(sh),"before")
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        # print(len(sh),"after")
        #print(sh['Price'])
        if len(sh) > 1:
        # print(sh)
            try:
                print("Getting log return for:", symbol)
                sh['return'] = np.log(sh['Price'])-np.log(sh['Price'].shift(1))
            except AttributeError:
                print(symbol, " couldn't fetch return. See value sample below")
                print(sh.head())
            sh['return'].fillna(-999, inplace=True)#df[1].fillna(0, inplace=True)
            #print(sh.head(5))
            firstdate = sh['Price_date'].head(1).iloc[0]
            lastdate = sh['Price_date'].tail(1).iloc[0]
            # load the returns into table
            delret = "delete from "+table+" where symbol=%s and price_date between %s and %s"
            copq = table
            fl = len(sh)
            c = 0
            myfile = cwd +'/'+tmp+'/logrt.csv'
            print(sh.head())
            try:
                sh.to_csv(myfile,index=None, header=False)
            except FileNotFoundError:
                myfile = cwd + '/logrt.csv'
                sh.to_csv(myfile, index=None, header=False)
            try:
                cursor.execute(delret, (symbol, firstdate, lastdate))
                print('delete successful and now loading')
#                with open(myfile, 'r') as fin:
#                    data = fin.read().splitlines(True)
#                with open(myfile, 'w') as fout:
#                    fout.writelines(data[1:])
                f = open(myfile, 'r')
                cursor.copy_from(f, copq, columns = ('symbol','price','price_date', 'source_table','volume', 'price_return'), sep=",")
                #updna = "update "+copq+" set price_return=NULL where symbol=%s and price_return=-999"
                #cursor.execute(updna, (symbol, ))
                f.close()
                c = fl
                os.remove(myfile)
            except (Exception, psg.Error) as e:
               print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
               print(e.pgerror)
            print(c, " out of ", fl, " loaded for ticker", symbol, "to table ", table)
        else:
            print("Less than 2 entries for symbol ", symbol, "minmum non null entries needed is 2")
        print("postgres connection closed")
