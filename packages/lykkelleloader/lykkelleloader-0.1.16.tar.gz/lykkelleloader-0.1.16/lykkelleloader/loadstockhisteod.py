#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#tested successfully and now ready to be deployed in Prod
"""
Created on Sat Jul  6 11:25:21 2019

@author: debmishra
"""

# import the stock history to the database. This program runs only on weekends
# import lykkelleconf.connecteod as c
from lykkelleconnector.geteodstock import geteodhprice as ysh
import datetime as dt
import lykkelleconf.workday as wd
import sys
# from lykkelleconf.time2epoch2time import epochtime as et
import numpy as np
import psycopg2 as pgs
import time
import os
import pandas as pd
import math

home = os.path.expanduser("~")
cwd = os.path.abspath(os.getcwd())
# print(cwd)
class loadstockhist:
    def stockhist(ticker, todate, fromdate, sourcetable, cursor):
        loaddata = []
        fromdate = fromdate.strftime('%Y-%m-%d')
        todate = todate.strftime('%Y-%m-%d')
        if todate == fromdate:
            print("""the dates used for history calculation are same.
                  History requires delta of dates. Moving to next ticker""")
            status = -999
            header = None
        else:
            histr = ysh(ticker, fromdate, todate)
            status = histr.sts
            header = histr.header
        # print(status)
        att = 0
        while status!=200 and status!=-999:
            if att <= 5:
                print("begins wait of 30 sec. att-", att)
                time.sleep(30)
                histr = ysh(ticker, fromdate, todate)
                status = histr.sts
                header = histr.header
                att = att +1
            else:
                print("even after 6 reattempts not getting status code 200")
                status = -899
                break
        if status == 200:
            val = histr.stock_Response
            if val is not None:
                lt = len(val)
                if lt>0:
                    load = 0
                    badload = 0
                    ldate = []
                    lprice = []
                    lvolume = []
                    lticker = []
                    lsource = []
                    for i in range(lt):
                        try:
                            volume = val[i].get('volume')
                            if volume is not None and volume>0:
                                volume = math.floor(volume)
                                volume = int(volume)
                            else:
                                volume = 0
                        except AttributeError:
                            volume=None
                        try:
                            close =val[i].get('adjusted_close')
                        except AttributeError:
                            try:
                                close = val[i].get('close')
                            except AttributeError:
                                close = None
                        try:
                            pricedate = val[i].get('date')
                        except AttributeError:
                            pricedate = None
                        if pricedate is not None and close is not None:
                            #print(ticker,":",pricedate,"-",close)
                            if 'benchmark' in sourcetable:
                                delq = """delete from benchmark_history where symbol=%s
                                        and price_date between %s and %s"""
                                copq = "benchmark_history"
                            else:
                                delq = """delete from stock_history where symbol=%s
                                        and price_date between %s and %s"""
                                copq = "stock_history"
                            try:
                                ldate.append(pricedate)
                                lprice.append(close)
                                lvolume.append(volume)
                                lticker.append(ticker)
                                lsource.append(sourcetable)
                                load = load + 1
                            except Exception as e:
                                badload = badload + 1
                                print(e)
                        else:
                            print("Failed load for ",ticker," had a close price of ", close, "for date ", pricedate)
                    data = {'ticker':lticker,
                            'pricedate':ldate,
                            'price':lprice,
                            'volume':lvolume,
                            'sourcetable':lsource
                            }
                    myfile = cwd + '/tmp/ticker.csv'
                    df = pd.DataFrame(data,columns=['ticker','pricedate','price','volume','sourcetable'])
                    try:
                        df.to_csv(myfile,index=None, header=False)
                    except FileNotFoundError:
                        myfile = cwd + '/ticker.csv'
                        df.to_csv(myfile, index=None, header=False)
#                    iconn = c.connect.create()
#                    icursor = iconn.cursor()
#                    with iconn:
                    #print("deletion started at:",dt.datetime.today())
                    cursor.execute(delq,(ticker, fromdate, todate))
                    #print("deletion finished at:",dt.datetime.today())
                    #print("load started at:",dt.datetime.today())
#                    with open(myfile, 'r') as fin:
#                        data = fin.read().splitlines(True)
#                    with open(myfile, 'w') as fout:
#                        fout.writelines(data[1:])
                    f = open(myfile, 'r')
                    cursor.copy_from(f, copq, columns = ('symbol','price_date','price','volume', 'source_table'), sep=",")
                    f.close()
                    #cursor.execute(copq, (myfile,))
                    #print("load started at:",dt.datetime.today())
                    os.remove(myfile)
                    loaddata = [ticker, load, badload]
                    return loaddata
                else:
                    print("No history data found for ticker", ticker, "and dates ", fromdate,":",todate)
                    loaddata = [ticker, "fail"]
                    return loaddata
            else:
                print("No history data found for ticker", ticker, "and dates ", fromdate,":",todate)
                loaddata = [status, ticker]
                return loaddata
        elif status == -899:
            print("Error code 200 after 5 attempts for ticker", ticker, "and dates ", fromdate,":",todate)
            loaddata = [ticker, "fail"]
            if header is not None:
                ldate = dt.date.today()
                ldate = wd.workday(str(ldate)).sdate()
                myheader = header.get('X-RateLimit-Remaining')
            else:
                myheader = None
#            conn = c.connect.create()
#            cursor = conn.cursor()
#            with conn:
            desc = ticker+":"+str(fromdate)+":"+str(todate)+":=",status
            nrtbl = """insert into ticker_no_response_list
            (symbol, load_date,src,"description",tablename,errorcode,headeroutput)
            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            cursor.execute(nrtbl, (ticker,ldate,'mhistory',desc,sourcetable,status,myheader))
            return loaddata
        else:
            print("Ignored as data already present for ticker", ticker, "and dates ", fromdate,":",todate)
            loaddata = [ticker, "ignore"]
            return loaddata

    def __init__(self, ticker, sourcetable, mode, jday, cursor):
        self.ticker = ticker
        self.sourcetable = sourcetable
        td = dt.date.today()
        iwd = td.isoweekday()
        todate = wd.workday(str(td)).sdate()
        todate = dt.datetime.strptime(todate, '%Y-%m-%d').date()
        modevalue = ['A', 'M']
        if mode in modevalue:
            pass
        else:
            print('Possible entries in mode are A or M. System will exit now')
            sys.exit(1)
        # print(todate)
        if iwd in [6, 7, 1] or mode == 'M':
        # execute the code that identifies the to and fromdates and calls the history functions
#            conn = c.connect.create()
#            with conn:
#            cursor = conn.cursor()
            if 'benchmark' in self.sourcetable:
                maxdate = """select max(price_date) from benchmark_history
                        where symbol = %s"""
                mindate = """select min(price_date) from benchmark_history
                        where symbol = %s"""
                validrecords = """select price_date from benchmark_history
                            where symbol =%s and price is not Null"""
            else:
                maxdate = """select max(price_date) from stock_history
                        where symbol = %s"""
                mindate = """select min(price_date) from stock_history
                        where symbol = %s"""
                validrecords = """select price_date from stock_history
                            where symbol =%s and price is not Null"""
            cursor.execute(maxdate, (ticker,))
            md = cursor.fetchone()
            cursor.execute(mindate, (ticker,))
            mid = cursor.fetchone()
            if md is not None and len(md)>0:
                md = md[0]
            else:
                md = None
            if mid is not None and len(mid) > 0:
                mid = mid[0]
            else:
                mid = None
            # print(md)
            eparam = 1
            if ticker[-3:] == '.TA':
                lastworkingday = wd.workday(str(dt.datetime.today().date()))
                lastworkingday = lastworkingday.sdate()
                # print(type(lastworkingday))
                lastworkingday = dt.datetime.strptime(lastworkingday,'%Y-%m-%d') - dt.timedelta(days=1)
                lastworkingday = lastworkingday.date()
            else:
                lastworkingday = wd.workday(str(dt.datetime.today().date()))
                lastworkingday = lastworkingday.sdate()
                lastworkingday = dt.datetime.strptime(lastworkingday,'%Y-%m-%d').date()
            print('latest record in history table should be ', lastworkingday, ' or higher')
            # print(mid, md, ticker)
            if mid is not None and lastworkingday is not None:
                bdays = np.busday_count(mid, lastworkingday)
            else:
                bdays = -999
            print(bdays, '-max businessdaycount for ', ticker)
            cursor.execute(validrecords, (ticker,))
            valid = cursor.fetchall()
            validcnt = len(valid)
            print(len(valid),'-valid records for ',ticker)
            if bdays == -999:
                print("Maximum and minimum enetries in history table are ", md,'-',mid,' for ticker ',ticker)
            elif validcnt is not None and bdays is not None:
                diff = abs((bdays/validcnt) - 1)
                print('delta between actual and expected for symbol ',ticker, ' is ',diff)
            else:
                print("Either the numenator or denominator have null values")
                diff = 0
            if md is None or md == mid or mode == 'M':
                # ts = 'delete from '+t+' where symbol ='+"'"+self.ticker+"'"
                # cursor.execute(ts)
                wks = 52*15
                fromdate = lastworkingday - dt.timedelta(weeks=wks)
                # print(fromdate)
            elif md < lastworkingday:
                print("symbol ",ticker, " doesn't have all records updated so reloading from last date ", md)
                fromdate = md
                # print(fromdate)
            elif md >= lastworkingday and diff > 0.10:
                print("Reloading history as the expected vs actual account has a difference >10% i.e.",diff*100,'%',' for symbol ',ticker)
                wks = 52 * 15
                fromdate = todate - dt.timedelta(weeks=wks)
            else:
                 eparam = 0
            if eparam == 0:
                print("""No valid history since the max history date is equal or > to latest date for symbol:""", self.ticker)
                jobload = """update jobrunlist
                set runstatus = 'ignored' where symbol=%s and
                runsource='mhistory' and rundate=%s and jobtable=%s """
                try:
                     cursor.execute(jobload, (ticker, jday, sourcetable))
                     print(ticker, " job executed successfully")
                except pgs.Error as e:
                    print(e.pgerror)
            else:
                shload = loadstockhist.stockhist(self.ticker, todate, fromdate, self.sourcetable, cursor)
                ignr = 0
                if shload[1]=='fail':
                    print("the ticker ", shload[0], "didn't find a result from eodhd")
                    rdate = dt.datetime.today().date()
                    print("date for no response:",rdate)
                    print(shload[0], " was not able to fetch history data from EODHD even after 5 attempts")
                elif shload[1]=='ignore':
                    print("the ticker ", shload[0], " was ignored from run as data already present")
                    rdate = dt.datetime.today().date()
                    print("date for no response:",rdate)
                    print(shload[0], " was ignored as data already present")
                    ignr = 1
                elif isinstance(shload[0], int) is True and shload[0]!=-999:
                    rdate = dt.datetime.today().date()
                    print("date for no response:",rdate)
                    print(self.ticker, " was not able to fetch history data from EODHD even after 5 attempts")
                elif isinstance(shload[0], int) is True and shload[0]==-999:
                    print(self.ticker,"'s history is too recent. There should be at least>1 days delta")
                    ignr = 1
                else:
                    print('For the ticker:', shload[0], ', total of ', shload[1],
                      ' number of successful records were loaded and ',shload[2],
                      ' number of records could not be loaded')
                if ignr == 1:
                    jobload = """update jobrunlist
                    set runstatus = 'ignored' where symbol=%s and
                    runsource='mhistory' and rundate=%s and jobtable=%s """
                    try:
                         cursor.execute(jobload, (ticker, jday, sourcetable))
                         print(ticker, " job executed successfully")
                    except pgs.Error as e:
                        print(e.pgerror)
                else:
                    jobload = """update jobrunlist
                    set runstatus = 'complete' where symbol=%s and
                    runsource='mhistory' and rundate=%s and jobtable=%s """
                    try:
                         cursor.execute(jobload, (ticker, jday, sourcetable))
                         print(ticker, " job executed successfully")
                    except pgs.Error as e:
                        print(e.pgerror)
        else:
            print('not a weekend. scrapping history run')
            sys.exit(1)