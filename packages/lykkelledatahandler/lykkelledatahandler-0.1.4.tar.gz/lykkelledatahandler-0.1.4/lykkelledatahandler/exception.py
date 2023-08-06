#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:23:25 2019
program closes the exception and based on override values
close the exceptions and move closed exceptions to store table
@author: debmishra"""

import datetime as dt
from lykkelleconf.connecteod import connect
import psycopg2 as pgs


class exceptions:
    insexp = """insert into dbo.exception_master
                        (exception_date,symbol,exception_type,status,exception_field,
                        exception_table)
                        values (%s, %s, %s, %s, %s, %s)"""
    insexps = """insert into dbo.exception_master
                        (exception_date,symbol,exception_type,status,exception_field,
                        exception_table, exception_value_num, stale_days)
                        values (%s, %s, %s, %s, %s, %s, %s, %s)"""
    insexpv = """insert into dbo.exception_master
                        (exception_date,symbol,exception_type,status,exception_field,
                        exception_table, exception_value_num, exception_value_yst,exception_value_date)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    delexp = """delete from exception_master where symbol=%s
                        and exception_type=%s and exception_field=%s and exception_table=%s"""

    def __init__(self, ticker, cursor, type):
        edate = dt.datetime.today().date()
        missingdata = exceptions.missingdata(edate, ticker, cursor, type)
        vertical = exceptions.verticalexp(ticker, cursor, type)
        stale = exceptions.staleprice(ticker, cursor, type)
        # insert missing data to exception table
        if len(missingdata) > 0:
            for i in range(len(missingdata)):
                missingvalue = missingdata[i]
                if len(missingvalue) == 0:
                    pass
                else:
                    mvdate = missingvalue[0]
                    mvsymbol = missingvalue[1]
                    mvtyp = missingvalue[2]
                    mvstatus = missingvalue[3]
                    mvfield = missingvalue[4]
                    mvtable = missingvalue[5]
                    try:
                        cursor.execute(self.delexp, (mvsymbol, mvtyp, mvfield, mvtable))
                        # print("delete successful from exception master for ", ticker)
                    except pgs.Error as e:
                        print("delete unsuccessful for ", ticker)
                        print(e.pgerror)
                    try:
                        cursor.execute(self.insexp, (mvdate, mvsymbol, mvtyp, mvstatus, mvfield, mvtable))
                        print("successful insert into exception table for ticker ", ticker, "-", mvtable, "-", mvfield,
                              "-", mvtyp)
                    except pgs.Error as e:
                        print("insert unsuccessful for ", ticker)
                        print(e.pgerror)
        else:
            print("No entry found is missing list for ticker ", ticker)
        # inserting data into exception table for vertical exceptions
        if len(vertical) > 0:
            vdiff = vertical[0]
            vtype = vertical[1]
            evdte = vertical[4]
            evnum = vertical[2]
            evyst = vertical[3]
            if vdiff <= 0.10:
                pass
            else:
                mvdate = edate
                mvtyp = "vertical>10%"
                mvfield = "price"
                if vtype == 'S':
                    mvtable = "stock_history"
                else:
                    mvtable = "benchmark_history"
                mvstatus = "new"
                mvsymbol = ticker
                try:
                    cursor.execute(self.delexp, (mvsymbol, mvtyp, mvfield, mvtable))
                    # print("delete successful from exception master for ", ticker)
                except pgs.Error as e:
                    print("delete unsuccessful for ", ticker)
                    print(e.pgerror)
                try:
                    cursor.execute(self.insexpv, (mvdate, mvsymbol, mvtyp, mvstatus, mvfield, mvtable, evnum, evyst,
                                                  evdte))
                    print("successful insert into exception table for ticker ", ticker, "-", mvtable, "-", mvfield, "-",
                          mvtyp)
                except pgs.Error as e:
                    print("insert unsuccessful for ", ticker)
                    print(e.pgerror)
        else:
            print("no entry found for vertical list for ticker ", ticker)
        # insert data into exception table for stale exceptions
        if len(stale) > 0:
            sdiff = stale[0]
            stype = stale[1]
            snum = stale[2]
            if sdiff < 5:
                pass
            else:
                mvdate = edate
                mvtyp = "stale >=5 days"
                mvfield = "price"
                if vtype == 'S':
                    mvtable = "stock_history"
                else:
                    mvtable = "benchmark_history"
                mvstatus = "new"
                mvsymbol = ticker
                try:
                    cursor.execute(self.delexp, (mvsymbol, mvtyp, mvfield, mvtable))
                    # print("delete successful from exception master for ", ticker)
                except pgs.Error as e:
                    print("delete unsuccessful for ", ticker)
                    print(e.pgerror)
                try:
                    cursor.execute(self.insexps, (mvdate, mvsymbol, mvtyp, mvstatus, mvfield, mvtable, snum, sdiff))
                    print("successful insert into exception table for ticker ", ticker, "-", mvtable, "-", mvfield, "-",
                          mvtyp)
                except pgs.Error as e:
                    print("insert unsuccessful for ", ticker)
                    print(e.pgerror)
        else:
            print("no vertical exceptions for ticker ", ticker)

    def missingdata(edate, ticker, cursor, type):
        mdatalist = []
        pqry = """select price, currency, volume, name from stock_master where symbol=%s"""
        pbqry = """select price, name from benchmark_master where symbol=%s"""
        rqry = """select mean_annualized_return, std_annualized,mkt_mean_annualized_return,mkt_annualized_std,
                beta,bmk_symbol from stock_statistics where symbol=%s"""
        if type == 'S':
            # Finding stock master exceptions. Only from price table
            try:
                cursor.execute(pqry, (ticker,))
                results = cursor.fetchone()
                sprice = results[0]
                scurrency = results[1]
                svolume = results[2]
                if sprice is not None and scurrency is not None and svolume is not None:
                    sprclst = []
                    scurlst = []
                    svlmlst = []
                else:
                    if sprice is None:
                        sprclst = [edate, ticker, 'missing value', 'New', 'price', 'stock_master']
                    else:
                        sprclst = []
                    if scurrency is None:
                        scurlst = [edate, ticker, 'missing value', 'New', 'currency', 'stock_master']
                    else:
                        scurlst = []
                    if svolume is None:
                        svlmlst = [edate, ticker, 'missing value', 'New', 'volume', 'stock_master']
                    else:
                        svlmlst = []
                # statistics query output
                cursor.execute(rqry, (ticker,))
                results = cursor.fetchone()
                mret = results[0]
                std = results[1]
                mmret = results[2]
                mstd = results[3]
                beta = results[4]
                bsym = results[5]
                if mret is not None and std is not None and mmret is not None and mstd is not None and beta is not None and bsym is not None:
                    mretlst = []
                    stdlst = []
                    mmretlst = []
                    mstdlst = []
                    betalst = []
                    bsymlst = []
                else:
                    if mret is None:
                        mretlst = [edate, ticker, 'missing value', 'New', 'mean_annualized_return', 'stock_statistics']
                    else:
                        mretlst = []
                    if std is not None:
                        stdlst = [edate, ticker, 'missing value', 'New', 'std_annualized', 'stock_statistics']
                    else:
                        stdlst = []
                    if mmret is None:
                        mmretlst = [edate, ticker, 'missing value', 'New', 'mkt_mean_annualized_return',
                                    'stock_statistics']
                    else:
                        mmretlst = []
                    if mstd is not None:
                        mstdlst = [edate, ticker, 'missing value', 'New', 'mkt_annualized_std', 'stock_statistics']
                    else:
                        mstdlst = []
                    if beta is not None:
                        betalst = [edate, ticker, 'missing value', 'New', 'beta', 'stock_statistics']
                    else:
                        betalst = []
                    if bsym is not None:
                        bsymlst = [edate, ticker, 'missing value', 'New', 'bmk_symbol', 'stock_statistics']
                    else:
                        bsymlst = []
                misslist = [sprclst, scurlst, svlmlst, mretlst, stdlst, mmretlst, mstdlst, betalst, bsymlst]
            except pgs.Error as e:
                # print(e.pgerror)
                misslist = -899
        else:
            # Finding benchmark exceptions. Only from price table
            try:
                cursor.execute(pbqry, (ticker,))
                results = cursor.fetchone()
                bprice = results[0]
                bname = results[1]
                if bprice is not None and bname is not None:
                    bprclst = []
                    bnmelst = []
                else:
                    if bprice is None:
                        bprclst = [edate, ticker, 'missing value', 'New', 'price', 'benchmark_master']
                    else:
                        bprclst = []
                    if bname is None:
                        bnmelst = [edate, ticker, 'missing value', 'New', 'name', 'benchmark_master']
                    else:
                        bnmelst = []
                misslist = [bprclst, bnmelst]
            except pgs.Error as e:
                # print(e.pgerror)
                misslist = -899
        return misslist

    def staleprice(ticker, cursor, type):
        pqry = """select price from stock_history where symbol=%s 
                order by price_Date desc"""
        pbqry = """select price from benchmark_history where symbol=%s 
                order by price_Date desc"""
        if type == 'S':
            evnum = None
            try:
                cursor.execute(pqry, (ticker,))
                results = cursor.fetchall()
                sc = 0
                # print(results)
                for i in range(len(results)):
                    # print(results[i][0])
                    if i == 0:
                        new = results[i][0]
                        evnum = new
                    else:
                        if new == results[i][0]:
                            sc = sc + 1
                        else:
                            break
            except pgs.Error:
                sc = -899
        else:
            evnum = None
            try:
                cursor.execute(pbqry, (ticker,))
                results = cursor.fetchall()
                sc = 0
                for i in range(len(results)):
                    if i == 0:
                        new = results[i][0]
                        evnum = new
                    else:
                        if new == results[i][0]:
                            sc = sc + 1
                            new = results[i]
                        else:
                            break
            except pgs.Error:
                sc = -899
        stalelist = [sc, type, evnum]
        return stalelist

    def verticalexp(ticker, cursor, type):
        pqry = """select price, price_Date from stock_history where symbol=%s 
                order by price_Date desc fetch first 2 rows only"""
        pbqry = """select price, price_Date from benchmark_history where symbol=%s 
                order by price_Date desc fetch first 2 rows only"""
        if type == 'S':
            try:
                cursor.execute(pqry, (ticker,))
                results = cursor.fetchall()
                # results = results[0]
                if len(results) == 2:
                    restday = results[0][0]
                    resyday = results[1][0]
                    resydate = results[1][1]
                    # print(restday,resyday)
                    if resyday is not None and resyday > 0 and restday is not None and restday > 0:
                        diff = abs((restday / resyday) - 1)
                    else:
                        print("One of the prices have null value for ticker ", ticker)
                        diff = -999
                else:
                    print("Two records are needed to calculate vertical exception. Less than two records found for ",
                          ticker)
                    diff = -999
            except pgs.Error:
                diff = -899
        else:
            try:
                cursor.execute(pbqry, (ticker,))
                results = cursor.fetchall()
                if len(results) == 2:
                    restday = results[0][0]
                    resyday = results[1][0]
                    resydate = results[1][1]
                    # print(restday,resyday)
                    if resyday is not None and resyday > 0 and restday is not None and restday > 0:
                        diff = abs((restday / resyday) - 1)
                    else:
                        print("One of the prices have null value for ticker ", ticker)
                        diff = -999
                else:
                    print("Two records are needed to calculate vertical exception. Less than two records found for ",
                          ticker)
                    diff = -999
            except pgs.Error:
                diff = -899
        difflist = [diff, type, restday, resyday, resydate]
        return difflist