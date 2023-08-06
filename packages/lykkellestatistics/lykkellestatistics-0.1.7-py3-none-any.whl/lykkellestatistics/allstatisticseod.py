#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#successfully tested. ready for prod
"""
Created on Tue Jul 16 00:17:24 2019
Python program to calculate the following using parameters stock ticker, benchmark ticker, country code, currency code:
    1 = Geometric return (stock and benchmark)
    2 = standard deviation using Garch/EWMA (stock and benchmark)
    3 = VAR 95% (stock and benchmark)
    4 = VAR 99% (stock and benchmark)
    5 = beta (stock)
    6 = market weight (stock), weighted beta
    7 = risk free rate (stock)
    8 = capm (stock)
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd
import numpy as np
import math as m
import psycopg2 as pgs


class allstatistics:
    def __init__(self, sticker, bticker, ctry, sourcetable, cursor):
        #conn = connect.create()
        #cursor = conn.cursor()
        #with conn:
        shist = """select price_date, price_return,MA_50D,MA_200D from stock_history
        where symbol=%s and abs(price_return)<0.45 order by price_date"""
        bhist = """select price_date, price_return from benchmark_history
        where symbol=%s and abs(price_return)<0.45 order by price_date"""
        cursor.execute(shist, (sticker,))
        shistr = cursor.fetchall()
        cursor.execute(bhist, (bticker,))
        bhistr = cursor.fetchall()
        if shistr == [] or len(shistr)<=1:
            print("exiting code. check the history data for ",sticker)
        elif bhistr == [] or len(bhistr)<=1:
            print("exiting code. check the history data for ",bticker)
        else:
            shdf = pd.DataFrame(shistr, columns =['pricedate','return','MA_50D','MA_200D'])
            bhdf = pd.DataFrame(bhistr, columns = ['pricedate','return'])
            is_valid_sreturn = shdf['return'].notnull()
            mshdf = shdf[is_valid_sreturn]
            is_valid_breturn = bhdf['return'].notnull()
            mbhdf = bhdf[is_valid_breturn]
            nz_sret = mshdf['return'] != 0
            nz_bret = mbhdf['return'] != 0
            mshdfz = mshdf[nz_sret]
            mbhdfz = mbhdf[nz_bret]
            nz_sret = mshdf['return'] != -0
            nz_bret = mbhdf['return'] != -0
            mshdfz = mshdf[nz_sret]
            mbhdfz = mbhdf[nz_bret]
            # calculate geometric mean and EWMA std dev of stock and benchmark
            mshdfz = mshdfz.sort_values(['pricedate'], ascending=0)
            mbhdfz = mbhdfz.sort_values(['pricedate'], ascending=0)
            lstk = len(mshdfz['return'])
            lidx = len(mbhdfz['return'])
            if lstk is not None and lstk > 0 and not mshdfz['return'].empty:
                samean = mshdfz['return'].mean()
                if not mshdfz['MA_50D'].empty:
                    sa50dmean = mshdfz['MA_50D'].iloc[0]
                else:
                    sa50dmean = None
                if not mshdfz['MA_200D'].empty:
                    sa200dmean = mshdfz['MA_200D'].iloc[0]
                else:
                    sa200dmean = None
                stkmean = samean*252
                sstd = mshdfz['return'].std()
                stkstd = sstd * m.sqrt(252)
            else:
                print("No return found for ", sticker, "length of returns-", lstk)
                stkmean = None
                stkstd = None
                sa50dmean = None
                sa200dmean = None
            if lidx is not None and lidx > 0:
                iamean = mbhdfz['return'].mean()
                idxmean = iamean*252
                istd = mbhdfz['return'].std()
                idxstd = istd * m.sqrt(252)
            else:
                print("No return found for ", bticker, "length of returns-", lidx)
                idxmean = None
                idxstd = None
                # calculate 95% and 99% VAR for stock and benchmark
            if stkmean is not None and stkstd is not None:
                stkvar95 = -(1.65*stkstd) #removed stkmean
                stkvar99 = -(2.33*stkstd) #removed stkmean
            else:
                stkvar95 = None
                stkvar99 = None
            if idxmean is not None and idxstd is not None:
                idxvar95 = -(1.65*idxstd) #removed idxmean
                idxvar99 = -(2.33*idxstd) #removed idxmean
            else:
                idxvar95 = None
                idxvar99 = None
            # calculate covariance and variance of market and using that find out beta
            if len(mshdfz['pricedate']) > 1 and len(mbhdfz['pricedate']) > 1:
                smatch = mshdfz.loc[mshdfz['pricedate'].isin(mbhdfz['pricedate'].values),['pricedate','return']]
                imatch = mbhdfz.loc[mbhdfz['pricedate'].isin(mshdfz['pricedate'].values),['pricedate','return']]
                corr = np.corrcoef(smatch['return'].values,imatch['return'].values)
                corr = corr[0, 1]
            else:
                corr = None
            # beta = corr *(std of stk /std of market)
            if corr is not None and stkstd is not None and idxstd is not None:
                beta = corr * (stkstd/idxstd)
            else:
                beta = None
            # calculating the risk free rate for the stock
            selrf = "select risk_free_rate from benchmark_all where country=%s"
            cursor.execute(selrf, (ctry,))
            rf = cursor.fetchone()
            # calculating the capm return using r = rf +beta (rm-rf)
            try:
                rf = float(rf[0])
            except TypeError:
                rf = None
            if rf is not None and beta is not None and idxmean is not None:
                capm = rf+beta*(idxmean-rf)
                # capm = capm[0]
            else:
                capm = None
            # calculating the ind_category
            selind = """select mkt_cap_stocks_bill_eur
            from stock_statistics where symbol=%s"""
            cursor.execute(selind, (sticker,))
            mcap = cursor.fetchone()
            if mcap is None:
                mcap = None
            elif len(mcap)>0:
                mcap = mcap[0]
            else:
                mcap = None
            if mcap is not None and mcap > 90:
                ind = 'LCAP'
            elif mcap is not None and mcap >= 10 and mcap < 90:
                ind = 'MCAP'
            else:
                ind = 'SCAP'
            # updating the stock statistics with all new information
            statupd ="""update stock_statistics set capm_return = %s,
            mean_annualized_Return = %s, beta = %s, var95_annualized = %s,
            var99_annualized = %s, annual_rf_rate = %s,
            mkt_mean_annualized_return = %s, std_annualized = %s,
            mkt_annualized_std= %s, mkt_annualized_var95 = %s,
            mkt_annualized_var99 = %s, ind_category=%s,bmk_symbol=%s,mean_50D=%s, mean_200D=%s where symbol=%s"""
            statdata = [capm, stkmean, beta, stkvar95, stkvar99, rf, idxmean, stkstd, idxstd, idxvar95, idxvar99, ind,bticker, sa50dmean, sa200dmean, sticker]
            try:
                cursor.execute(statupd, statdata)
            except pgs.Error as e:
                print("unsuccessful update for ticker", sticker)
                print(e)
        print("postgres connection successfully closed")















