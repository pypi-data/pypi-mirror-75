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
import os

home = os.path.expanduser("~")
cwd = os.path.abspath(os.getcwd())
# print(cwd)

class getrollingmean:
    def rollingmean50d(symbol, table, cursor,tmp):
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        selret = "select symbol, price, price_date,price_return, source_table, ma_50d, ma_200d,volume from "+ table + " where symbol=%s order by price_date"
        delret = "delete from "+ table + " where symbol=%s and (price is null or price <= 0)"
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
            print(e)
        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['symbol','Price', 'Price_date','return','source','ma50','ma200','volume'])
        # print(sh['Price'])
        # print(len(sh),"before")
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        # print(len(sh),"after")
        if len(sh) > 1:
        # print(sh)
            firstdate = sh['Price_date'].head(1).iloc[0]
            lastdate = sh['Price_date'].tail(1).iloc[0]
            print(firstdate)
            print(lastdate)
            sh['ma50'] = sh['Price'].rolling(window=50).mean()
            sh['ma50'].fillna(-999, inplace=True)
            sh['ma200'].fillna(-999, inplace=True)
            #sh['return'].fillna(-999, inplace=True)
            print(sh.head())
            rl = len(sh)
            myfile = cwd + '/'+tmp+'/m50.csv'
            try:
                sh.to_csv(myfile,index=None, header=False)
            except FileNotFoundError:
                myfile = cwd + '/m50.csv'
                sh.to_csv(myfile, index=None, header=False)
            delret = "delete from "+table+" where symbol=%s and price_date between %s and %s"
            copq = table
            try:
                cursor.execute(delret, (symbol, firstdate, lastdate))
                print('successful delete and now loading')
                f = open(myfile, 'r')
                cursor.copy_from(f, copq, columns = ('symbol','price','price_date', 'price_return','source_table','ma_50d','ma_200d','volume'), sep=",")
                f.close()
                rc = len(sh)
                os.remove(myfile)
            except (Exception, psg.Error) as e:
                print("Load unsuccessful for ", symbol)
                print(e)
                rc = 0
            print(rc, " out of ", rl , "valid 50D loaded for ticker", symbol,"having total ",len(sh),"entries to table ", table)
        else:
            print("Less than 2 entries for symbol ", symbol, "minmum non null entries needed is 2")
        print("postgres connection closed")
    def rollingmean200d(symbol, table, cursor, tmp):
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        selret = "select symbol, price, price_date,price_return, source_table, ma_50d, ma_200d,volume from "+ table + " where symbol=%s order by price_date"
        delret = "delete from "+ table + " where symbol=%s and (price is null or price <= 0)"
        print(table, symbol)
        try:
            cursor.execute(delret, (symbol,))
            cursor.execute(selret, (symbol,))
        except (Exception, psg.Error) as e:
            print("Error fetching data from PostgreSQL table for ", symbol, "& ", table)
            print(e)
        rsel = cursor.fetchall()
        sh = pd.DataFrame(rsel, columns=['symbol','Price', 'Price_date','return','source','ma50','ma200','volume'])
        # print(sh['Price'])
        # print(len(sh),"before")
        vp = sh['Price'].notnull()
        sh = sh[vp]
        vp = sh['Price'] != 0
        sh = sh[vp]
        # print(len(sh),"after")
        if len(sh) > 1:
            firstdate = sh['Price_date'].head(1).iloc[0]
            lastdate = sh['Price_date'].tail(1).iloc[0]
            print(firstdate)
            print(lastdate)
            sh['ma200'] = sh['Price'].rolling(window=200).mean()
            sh['ma200'].fillna(-999, inplace=True)
            print(sh.head())
            rl = len(sh)
            myfile =cwd + '/'+tmp+'/m200.csv'
            try:
                sh.to_csv(myfile,index=None, header=False)
            except FileNotFoundError:
                myfile = cwd + '/m200.csv'
                sh.to_csv(myfile, index=None, header=False)
            delret = "delete from "+table+" where symbol=%s and price_date between %s and %s"
            copq = table
            try:
                cursor.execute(delret, (symbol, firstdate, lastdate))
                print('successful delete and now loading')
                f = open(myfile, 'r')
                cursor.copy_from(f, copq, columns = ('symbol','price','price_date', 'price_return','source_table','ma_50d','ma_200d','volume'), sep=",")
                updna = "update "+copq+" set ma_200d=NULL where symbol=%s and ma_200d=-999"
                updrt = "update "+copq+" set price_return=NULL where symbol=%s and price_return=-999"
                updna5 = "update "+copq+" set ma_50d=NULL where symbol=%s and ma_50d=-999"
                cursor.execute(updna5, (symbol, ))
                cursor.execute(updna, (symbol, ))
                cursor.execute(updrt, (symbol, ))
                f.close()
                rc = len(sh)
                os.remove(myfile)
            except (Exception, psg.Error) as e:
                print("Load unsuccessful for ", symbol)
                print(e)
                rc = 0
            print(rc, " out of ", rl , "valid 200D loaded for ticker", symbol,"having total ",len(sh),"entries to table ", table)
        else:
            print("Less than 2 entries for symbol ", symbol, "minmum non null entries needed is 2")
        print("postgres connection closed")