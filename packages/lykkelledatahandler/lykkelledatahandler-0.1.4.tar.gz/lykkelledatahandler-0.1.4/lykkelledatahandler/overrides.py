#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:23:25 2019
program closes the exception and based on override values
close the exceptions and move closed exceptions to store table
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import psycopg2 as pgs
import lykkelleconf.workday
import datetime as dt


etyp = """select distinct exception_type from
        dbo.exception_master where status!='closed'"""# and symbol='7733.T'
etble = """select distinct exception_Table from dbo.exception_master where
        exception_type=%s and status!='closed'"""
efield = """select distinct exception_field from dbo.exception_master where
        exception_type=%s and status!='closed'
        and exception_Table=%s"""
esymbol = """select symbol,override_value_text,override_value_num,
        overide_comment,override_value_date
        from dbo.exception_master where
        exception_type=%s and status!='closed'
        and exception_Table=%s and exception_field=%s
        and overide_comment is not null
        """
dft = " order by price_date desc fetch first 1 rows only"
updval = " (symbol,price_date,price,source_table) values ("
updvalt = " (symbol,price_date,currency,source_table) values ("
cnflct =""" ON CONFLICT (symbol,price_date)
        DO UPDATE SET price=EXCLUDED.price,source_table=EXCLUDED.source_table"""


class overrides:
    def __init__(self):
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            try:
                cursor.execute(etyp)
                typlist = cursor.fetchall()
            except pgs.Error as e:
                print("couldn't fetch exception types")
                print(e.pgerror)
            if typlist is None:
                typlist =[]
            else:
                pass
            if len(typlist)>0:
                for i in range(len(typlist)):
                    etype = typlist[i][0]
                    try:
                        cursor.execute(etble,(etype,))
                        tblist = cursor.fetchall()
                    except pgs.Error as e:
                        print("couldn't fetch exception tables for ",etype)
                        print(e.pgerror)
                    if tblist is None:
                        tblist =[]
                    else:
                        pass
                    if len(tblist)>0:
                        for j in range(len(tblist)):
                            etbl = tblist[j][0]
                            try:
                                cursor.execute(efield,(etype, etbl))
                                fldlist = cursor.fetchall()
                            except pgs.Error as e:
                                print("couldn't fetch exception fields for ", etype, " and ", etbl)
                                print(e.pgerror)
                            if fldlist is None:
                                fldlist =[]
                            else:
                                pass
                            if len(fldlist)>0:
                                for k in range(len(fldlist)):
                                    efld = fldlist[k][0]
                                    try:
                                        cursor.execute(esymbol,(etype, etbl, efld))
                                        symlist = cursor.fetchall()
                                    except pgs.Error as e:
                                        print("couldn't fetch exception symbols for ", etype, " and ", etbl, " and ", efld)
                                        print(e.pgerror)
                                    if symlist is None:
                                        symlist =[]
                                    else:
                                        pass
                                    if len(symlist)>0:
                                        for l in range(len(symlist)):
                                            symbol = symlist[l][0]
                                            ovtext = symlist[l][1]
                                            ovnum = symlist[l][2]
                                            ovdate = symlist[l][4]
                                            # comment = symlist[l][3]
                                            if (efld == 'price' or efld == 'mkt_cap_stocks_bill_eur') and ovnum is not None:
                                                if 'history' in etbl:
                                                    dtqry = "select price_date,source_table from dbo.stock_statistics_history where symbol="+"'"+symbol+"'"+dft
                                                    try:
                                                        cursor.execute(dtqry)
                                                        hlst = cursor.fetchone()
                                                    except pgs.Error as e:
                                                        print("for some reason date is not fetched from statistics history table ",etbl," for symbol",symbol)
                                                        print(e.pgerror)
                                                    print(hlst,symbol,"for ovnum")
                                                    dbqry = "select count(*) from dbo.bond_master where symbol="+"'"+symbol+"'"
                                                    try:
                                                        cursor.execute(dbqry)
                                                        hbnd = cursor.fetchone()
                                                        bcnt = hbnd[0]
                                                    except pgs.Error as e:
                                                        print("for some reason count is not fetched from bond_master table ",etbl," for symbol",symbol)
                                                        print(e.pgerror)
                                                        bcnt = 0
                                                    print(hbnd,symbol,"for ovnum")
                                                    if hlst is not None:
                                                        hdate = hlst[0]
                                                        htbl = hlst[1]
                                                        hsdate = hdate
                                                        if ovdate is not None and str(hdate)==str(ovdate):
                                                            pass
                                                        elif ovdate is not None:
                                                            hdate = ovdate
                                                        else:
                                                            pass
                                                    elif bcnt >0:
                                                        hdate = dt.datetime.today().date() - dt.timedelta(days=1)
                                                        hdate = str(hdate)
                                                        if ovdate is not None and str(hdate)==str(ovdate):
                                                            pass
                                                        elif ovdate is not None:
                                                            hdate = ovdate
                                                        else:
                                                            pass
                                                        #hdate = workday.workday(hdate).sdate()
                                                        htbl = "bond_all"
                                                    else:
                                                        hdate = dt.datetime.today().date() - dt.timedelta(days=1)
                                                        hdate = str(hdate)
                                                        hdate = workday.workday(hdate).sdate()
                                                        if ovdate is not None and str(hdate)==str(ovdate):
                                                            pass
                                                        elif ovdate is not None:
                                                            hdate = ovdate
                                                        else:
                                                            pass
                                                        htbl = "benchmark_all"
                                                    updq1 = "update "+etbl
                                                    if 'statistics' in etbl:
                                                        updq = updq1+" set "+efld+"="+str(ovnum)+" where symbol="+"'"+symbol+"'"+" and price_date="+"'"+str(hsdate)+"'"
                                                    else:
                                                        try:
                                                            updq = "insert into "+etbl+updval+"'"+symbol+"',"+"'"+str(hdate)+"',"+str(ovnum)+","+"'"+htbl+"')"+cnflct
                                                        except TypeError:
                                                            print(updq)
                                                            updq = None
                                                    upde = """update dbo.exception_master set status='closed'
                                                            where symbol=%s and exception_field=%s and exception_table=%s
                                                            and exception_type=%s"""
                                                    if updq is not None:
                                                        try:
                                                            cursor.execute(updq)
                                                            print("successful insert for",symbol,etype,etbl,efld)
                                                            try:
                                                                cursor.execute(upde,(symbol,efld,etbl,etype))
                                                                print("successful status update in exception master for",symbol,etype,etbl,efld)
                                                            except pgs.Error as e:
                                                                print("failed status update in exception master for",symbol,etype,etbl,efld)
                                                                print(e.pgerror)
                                                        except pgs.Error as e:
                                                            print("attempt to insert price/mkt_cap to history table failed",symbol,etype,etbl,efld)
                                                            print(e.pgerror)
                                                    else:
                                                        print("updq resulted None output-ovnum")
                                                        print(etbl,symbol,hdate,ovnum,htbl)
                                                else:
                                                    updq1 = "update "+etbl
                                                    updq = updq1+" set "+efld+"="+str(ovnum)+" where symbol="+"'"+symbol+"'"
                                                    upde = """update dbo.exception_master set status='closed'
                                                            where symbol=%s and exception_field=%s and exception_table=%s
                                                            and exception_type=%s"""
                                                    try:
                                                        cursor.execute(updq)
                                                        print("successful insert for",symbol,etype,etbl,efld)
                                                        try:
                                                            cursor.execute(upde,(symbol,efld,etbl,etype))
                                                            print("successful status update in exception master for",symbol,etype,etbl,efld)
                                                        except pgs.Error as e:
                                                            print("failed status update in exception master for",symbol,etype,etbl,efld)
                                                            print(e.pgerror)
                                                    except pgs.Error as e:
                                                        print("attempt to insert price/mkt_cap to history table failed",symbol,etype,etbl,efld)
                                                        print(e.pgerror)
                                            elif ovtext is not None:
                                                if 'history' in etbl:
                                                    dtqry = "select price_date,source_table from dbo.stock_statistics_history where symbol="+"'"+symbol+"'"+dft
                                                    try:
                                                        cursor.execute(dtqry)
                                                        hlst = cursor.fetchone()
                                                    except pgs.Error as e:
                                                        print("for some reason date is not fetched from history table ",etbl," for symbol",symbol)
                                                        print(e.pgerror)
                                                    print(symbol,hlst,"for ovtext")
                                                    dbqry = "select count(*) from dbo.bond_master where symbol="+"'"+symbol+"'"
                                                    try:
                                                        cursor.execute(dbqry)
                                                        hbnd = cursor.fetchone()
                                                        bcnt = hbnd[0]
                                                    except pgs.Error as e:
                                                        print("for some reason count is not fetched from bond_master table ",etbl," for symbol",symbol)
                                                        print(e.pgerror)
                                                        bcnt = 0
                                                    print(hbnd,symbol,"for ovnum")
                                                    if hlst is not None:
                                                        hdate = hlst[0]
                                                        htbl = hlst[1]
                                                        hsdate = hdate
                                                        if ovdate is not None and str(hdate)==str(ovdate):
                                                            pass
                                                        elif ovdate is not None:
                                                            hdate = ovdate
                                                        else:
                                                            pass
                                                    elif bcnt > 0:
                                                        hdate = dt.datetime.today().date() - dt.timedelta(days=1)
                                                        hdate = str(hdate)
                                                        if ovdate is not None and str(hdate)==str(ovdate):
                                                            pass
                                                        elif ovdate is not None:
                                                            hdate = ovdate
                                                        else:
                                                            pass
                                                        #hdate = workday.workday(hdate).sdate()
                                                        htbl = "bond_all"
                                                    else:
                                                        hdate = dt.datetime.today().date() - dt.timedelta(days=1)
                                                        hdate = str(hdate)
                                                        hdate = workday.workday(hdate).sdate()
                                                        if ovdate is not None and str(hdate)==str(ovdate):
                                                            pass
                                                        elif ovdate is not None:
                                                            hdate = ovdate
                                                        else:
                                                            pass
                                                        htbl = "benchmark_all"
                                                    updq1 = "update "+etbl
                                                    if 'statistics' in etbl:
                                                        print(symbol,hdate,ovtext)
                                                        updq = updq1+" set "+efld+"="+"'"+ovtext+"'"+" where symbol="+"'"+symbol+"'"+" and price_date="+"'"+str(hsdate)+"'"
                                                    else:
                                                        print(symbol,hdate,ovtext)
                                                        updq = "insert into "+etbl+updvalt+"'"+symbol+"',"+"'"+str(hdate)+"',"+"'"+str(ovtext)+"',"+"'"+htbl+"')"+cnflct
                                                    upde = """update dbo.exception_master set status='closed'
                                                            where symbol=%s and exception_field=%s and exception_table=%s
                                                            and exception_type=%s"""
                                                    try:
                                                        cursor.execute(updq)
                                                        print("successful insert for",symbol,etype,etbl,efld)
                                                        try:
                                                            cursor.execute(upde,(symbol,efld,etbl,etype))
                                                            print("successful status update in exception master for",symbol,etype,etbl,efld)
                                                        except pgs.Error as e:
                                                            print("failed status update in exception master for",symbol,etype,etbl,efld)
                                                            print(e.pgerror)
                                                    except pgs.Error as e:
                                                        print("attempt to insert price/mkt_cap to history table failed",symbol,etype,etbl,efld)
                                                        print(e.pgerror)
                                                else:
                                                    updq1 = "update "+etbl
                                                    updq = updq1+" set "+efld+"="+"'"+ovtext+"'"+" where symbol="+"'"+symbol+"'"
                                                    upde = """update dbo.exception_master set status='closed'
                                                            where symbol=%s and exception_field=%s and exception_table=%s
                                                            and exception_type=%s"""
                                                    try:
                                                        cursor.execute(updq)
                                                        print("successful insert for",symbol,etype,etbl,efld)
                                                        try:
                                                            cursor.execute(upde,(symbol,efld,etbl,etype))
                                                            print("successful status update in exception master for",symbol,etype,etbl,efld)
                                                        except pgs.Error as e:
                                                            print("failed status update in exception master for",symbol,etype,etbl,efld)
                                                            print(e.pgerror)
                                                    except pgs.Error as e:
                                                        print("attempt to insert price/mkt_cap to history table failed",symbol,etype,etbl,efld)
                                                        print(e.pgerror)
                                            else:
                                                print("ovnum and ovtext were null for",symbol,"-",efld,"-",etbl,"-",etype)
                                                upde = """update dbo.exception_master set status='closed'
                                                    where symbol=%s and exception_field=%s and exception_table=%s
                                                    and exception_type=%s"""
                                                try:
                                                    cursor.execute(upde,(symbol,efld,etbl,etype))
                                                    print("successful status update in exception master for",symbol,etype,etbl,efld)
                                                except pgs.Error as e:
                                                    print("failed status update in exception master for",symbol,etype,etbl,efld)
                                                    print(e.pgerror)
                                    else:
                                        print("""the distinct open exception symbols from exceptionlist turned out to be 0 for type and table""",etype,"-",etbl,"-",efld)
                            else:
                                print("""the distinct open exception fields from exceptionlist turned out to be 0 for type and table""",etype,"-",etbl)
                    else:
                        print("""the distinct open exception tables from exceptionlist turned out to be 0 for type""",etype)
            else:
                print("""the distinct open exception types from exceptionlist turned out to be 0""")