#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import the stock's technical details from eodhistorical data
import lykkelleconf.connecteod as c
from lykkelleconnector.geteodstock import geteodfundamental
from lykkelleconnector.geteodstock import geteodprice
from lykkelleconnector.geteodstock import geteodbprice
import psycopg2 as pgs
import datetime as dt
from lykkelleconf.workday import workday
import time
# class to hold the function that will call the ticker and load data to psql


class loadstockprice:
    def loadpricedetails(ticker, price,volume ,sourcetable, prio, jday, cursor):
        SHI = 0
        SMI = 0
        SSI = 0
        #conn = c.connect.create()
        #cursor = conn.cursor()
        #with conn:
        if 'benchmark' in sourcetable:
            tscr = """delete from benchmark_master where symbol=%s"""
            try:
                cursor.execute(tscr, (ticker,))
                # print('successful delete')
            except pgs.Error as e:
                print(e.pgerror)
            iscr = """insert into benchmark_master
                (symbol, price,volume,source_table)
                values (%s, %s,%s, %s)"""
            ilst = [ticker, price,volume,sourcetable]
            SMI = 1
        else:
            tscr = """delete from stock_master where symbol=%s"""
            try:
                cursor.execute(tscr, (ticker,))
                # print('successful delete')
            except pgs.Error as e:
                print(e.pgerror)
            iscr = """insert into stock_master
                (symbol, price, volume ,source_table)
                values (%s, %s, %s, %s)"""
            ilst = [ticker, price, volume,sourcetable]
            SMI = 1
        try:
            cursor.execute(iscr, ilst)
            #print('successful insert')
        except pgs.Error as e:
            print(e.pgerror)
        # loading the data into history table. two checks are done here:
        # - check if today is a workday and if it's not a holiday
        if 'benchmark' in sourcetable:
            iscrh = """insert into benchmark_history (symbol, price_date,
                        price,volume, source_table) values
                    (%s, %s, %s,%s, %s) ON CONFLICT DO NOTHING"""
        else:
            iscrh = """insert into stock_history (symbol, price_date,
                        price,volume, source_table) values
                    (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""
        if prio >2:
            pdate = dt.date.today() - dt.timedelta(days =1)
            print("This is not an Asia/Oceania symbol-",ticker,"-",pdate)
        else:
            pdate = dt.date.today()
            print("This is an Asia/Oceania symbol-",ticker,"-",pdate)
        pdate = workday(str(pdate)).sdate()
        try:
            cursor.execute(iscrh, (ticker, pdate, price,volume, sourcetable))
            SHI = 1
            # print('successful history insert')
        except pgs.Error as e:
            print(e.pgerror)
        if 'benchmark' in sourcetable:
            if SMI == 1 and SHI ==1:
                pass
        else:
            tscr = """delete from stock_statistics where symbol=%s"""
            indscr = 'select sector from '+ sourcetable+ ' where symbol=%s'
            try:
                cursor.execute(tscr, (ticker,))
            except pgs.Error as e:
                print(e.pgerror)
            try:
                cursor.execute(indscr, (ticker,))
            except pgs.Error as e:
                print(e.pgerror)
            try:
                ind = cursor.fetchone()
                try:
                    ind = ind[0]
                    if ind is None or ind=='':
                        ind ='Unknown'
                    else:
                        pass
                except TypeError:
                    print('query to find industry didnot give any result for',ticker,' in table ',sourcetable)
                    ind = 'Unknown'
            except pgs.Error:
                print('No results to fetch')
                ind = None
            istr = """insert into stock_statistics
                (symbol, industry, source_table, price)
                 values (%s, %s, %s, %s)"""
            istrv = [ticker, ind, sourcetable, price]
            try:
                cursor.execute(istr,istrv)
                SSI = 1
            except pgs.Error as e:
                print(e.pgerror)
            if SMI == 1 and SHI ==1 and SSI==1:
                pass
            else:
                pass
        print('postgres connection closed for ', ticker)
    def __init__(self, ticker,sourcetable, jday, prio, cursor):
        stkall = """select distinct sa.symbol from stock_all sa join
        benchmark_all ba on ba.symbol=sa.index_code where ba.prio=%s"""
#        bmkall = """select distinct ba.symbol from benchmark_all ba
#        where ba.prio=%s and is_active=True"""
        self.ticker = ticker
        self.sourcetable = sourcetable
        #conn = c.connect.create()
        #cursor = conn.cursor()
        stkalst = []
        #with conn:
        if 'benchmark' in sourcetable:
            pass
        else:
            cursor.execute(stkall, (prio,))
            stkal = cursor.fetchall()
            if stkal is None:
                stkalst = []
            else:
                for i in range(len(stkal)):
                    bmkchk = stkal[i][0]+'-'+str(prio)
                    stkalst.append(bmkchk)
        #print(stkalst)
        if 'benchmark' in self.sourcetable:
            if prio >2:
                pdate = dt.date.today() - dt.timedelta(days =1)
            else:
                pdate = dt.date.today()
            if self.ticker=='TA100.INDX':
                pass
            else:
                pdate = workday(str(pdate)).sdate()
            #print(pdate," is the last day for stock price load")
            gystock = geteodbprice(self.ticker, pdate)
        elif 'manual' in self.sourcetable:
            if prio >2:
                pdate = dt.date.today() - dt.timedelta(days =1)
            else:
                pdate = dt.date.today()
            if self.ticker=='TA100.INDX' or self.ticker[-3:]=='.TA':
                pass
            else:
                pdate = workday(str(pdate)).sdate()
            #print(pdate," is the last day for stock price load")
            gystock = geteodbprice(self.ticker, pdate)
        else:
            gystock = geteodprice(self.ticker)
        status = gystock.status
        header = gystock.header
        att = 0
        while att<4:
            if status == 200:
                att = 6
                break
            elif att < 4:
                # print("begins wait of 10 sec. att-", att)
                time.sleep(15)
                if 'benchmark' in self.sourcetable:
                    if prio >2:
                        pdate = dt.date.today() - dt.timedelta(days =1)
                    else:
                        pdate = dt.date.today()
                    if self.ticker=='TA100.INDX':
                        pass
                    else:
                        pdate = workday(str(pdate)).sdate()
                    #print(pdate," is the last day for stock price load")
                    gystock = geteodbprice(self.ticker, pdate)
                elif 'manual' in self.sourcetable:
                    if prio >2:
                        pdate = dt.date.today() - dt.timedelta(days =1)
                    else:
                        pdate = dt.date.today()
                    if self.ticker=='TA100.INDX' or self.ticker[-3:]=='.TA':
                        pass
                    else:
                        pdate = workday(str(pdate)).sdate()
                    #print(pdate," is the last day for stock price load")
                    gystock = geteodbprice(self.ticker, pdate)
                else:
                    gystock = geteodprice(self.ticker)
                status = gystock.status
                header = gystock.header
                att = att +1
            else:
                rdate = dt.datetime.today().date()
                print("date for no response:",rdate)
                print("even after 5 reattempts not getting status code 200 for\n",self.ticker)
                break
        if status == 999:
            print(gystock.bad_ticker, "couldnt get an output from eodhistorical data")
            if header is not None:
                ldate = dt.date.today()
                ldate = workday(str(ldate)).sdate()
                myheader = header.get('X-RateLimit-Remaining')
            else:
                myheader = None
            #conn = c.connect.create()
            #cursor = conn.cursor()
            #with conn:
            desc = ticker+":"+str(jday)+":"+str(prio)+":=",status
            nrtbl = """insert into ticker_no_response_list
            (symbol, load_date,src, "description",tablename,errorcode,headeroutput)
            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            cursor.execute(nrtbl, (ticker,ldate,'mprice',desc,sourcetable,status,myheader))
        elif status == 400:
            print(gystock.no_response_ticker, "couldnt get an output from eodhistorical data")
            if header is not None:
                ldate = dt.date.today()
                ldate = workday(str(ldate)).sdate()
                myheader = header.get('X-RateLimit-Remaining')
            else:
                myheader = None
            #conn = c.connect.create()
            #cursor = conn.cursor()
            #with conn:
            desc = ticker+":"+str(jday)+":"+str(prio)+":=",status
            nrtbl = """insert into ticker_no_response_list
            (symbol, load_date,src, "description",tablename,errorcode,headeroutput)
            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            cursor.execute(nrtbl, (ticker,ldate,'mprice',desc,sourcetable,status,myheader))
        else:
            yr = gystock.stock_Response
            #print(header,status)
            #print(yr,type(yr),len(yr))
            if yr is None:
                print("no response came from vendor for the dataset:\n",self.ticker)
            else:
                print(type(yr),":is the type of data returned")
                if type(yr) is list and len(yr)>0:
                    res = 1
                    for i in range(len(yr)):
                        iyr =yr[i]
                        if 'benchmark' in sourcetable:
                            isymbol = self.ticker
                        elif 'manual' in sourcetable:
                            isymbol = self.ticker
                        else:
                            isymbol = iyr.get('code')+'.'+iyr.get('exchange_short_name')
                        try:
                            ivol = iyr.get('volume')
                        except AttributeError:
                            ivol = None
                        try:
                            iprice = iyr.get('adjusted_close')
                            if iprice == 'NA':
                                try:
                                    iprice = iyr.get('close')
                                    if iprice=='NA':
                                        try:
                                            print("entering previous day's price for",isymbol)
                                            iprice = iyr.get('previousClose')
                                        except AttributeError:
                                            iprice = None
                                    else:
                                        pass
                                except AttributeError:
                                    iprice = None
                            else:
                                pass
                        except AttributeError:
                            iprice = None
                        if iprice =='NA':
                            iprice = None
                        else:
                            pass
                        #print(isymbol,iprice,ivol,sourcetable,prio,jday)
                        if 'benchmark' in sourcetable:
                            print("loading the following stock details to system")
                            print(isymbol,iprice,ivol,sourcetable,prio,jday)
                            try:
                                loadstockprice.loadpricedetails(isymbol, iprice,ivol, sourcetable, prio, jday, cursor)
                            except Exception:
                                print("prices couldn't be loaded for exchange:",isymbol)
                                res = 0
                        else:
                            valchk = isymbol+'-'+str(prio)
                            if valchk in stkalst:
                                if 'manual' in sourcetable:
                                    sourcetable='stock_all'
                                else:
                                    pass
                                print("loading the following stock details to system")
                                print(isymbol,iprice,ivol,sourcetable,prio,jday)
                                try:
                                    loadstockprice.loadpricedetails(isymbol, iprice,ivol, sourcetable, prio, jday, cursor)
                                except Exception:
                                    print("prices couldn't be loaded for exchange:",isymbol)
                                    res = 0
                            else:
                                #print(valchk, stkalst)
                                pass
                    if res ==1:
                        jobload = """update jobrunlist
                            set runstatus = 'complete' where symbol=%s and
                            runsource='mprice' and rundate=%s and jobtable=%s """
                        if 'benchmark' in sourcetable:
                            myticker = self.ticker
                        else:
                            myticker = ticker+'-'+str(prio)
                        try:
                             cursor.execute(jobload, (myticker, jday, sourcetable))
                             print(ticker, " job executed successfully")
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        pass
                elif yr is not None and type(yr) is not list:
                    res = 1
                    iyr =yr
                    if 'benchmark' in sourcetable:
                        isymbol = self.ticker
                    elif 'manual' in sourcetable:
                        isymbol = self.ticker
                    else:
                        isymbol = iyr.get('code')+'.'+iyr.get('exchange_short_name')
                    try:
                        ivol = iyr.get('volume')
                    except AttributeError:
                        ivol = None
                    try:
                        iprice = iyr.get('adjusted_close')
                        if iprice == 'NA':
                            try:
                                iprice = iyr.get('close')
                                if iprice=='NA':
                                    try:
                                        print("entering previous day's price for",isymbol)
                                        iprice = iyr.get('previousClose')
                                    except AttributeError:
                                        iprice = None
                                else:
                                    pass
                            except AttributeError:
                                iprice = None
                        else:
                            pass
                    except AttributeError:
                        iprice = None
                    if iprice =='NA':
                        iprice = None
                    else:
                        pass
                    if 'benchmark' in sourcetable:
                        try:
                            print("loading the following stock details to system")
                            print(isymbol,iprice,ivol,sourcetable,prio,jday)
                            loadstockprice.loadpricedetails(isymbol, iprice,ivol, sourcetable, prio, jday, cursor)
                        except Exception:
                            print("prices couldn't be loaded for exchange:",isymbol)
                            res = 0
                    else:
                        valchk = isymbol+'-'+str(prio)
                        if valchk in stkalst:
                            if 'manual' in sourcetable:
                                sourcetable='stock_all'
                            else:
                                pass
                            try:
                                print("loading the following stock details to system")
                                print(isymbol,iprice,ivol,sourcetable,prio,jday)
                                loadstockprice.loadpricedetails(isymbol, iprice,ivol, sourcetable, prio, jday, cursor)
                            except Exception:
                                print("prices couldn't be loaded for exchange:",isymbol)
                                res = 0
                        else:
                            pass
                    if res ==1:
                        jobload = """update jobrunlist
                            set runstatus = 'complete' where symbol=%s and
                            runsource='mprice' and rundate=%s and jobtable=%s """
                        if 'benchmark' in sourcetable:
                            myticker = self.ticker
                        else:
                            myticker = ticker+'-'+str(prio)
                        try:
                             cursor.execute(jobload, (myticker, jday, sourcetable))
                             print(ticker, " job executed successfully")
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        pass
                else:
                    print("for ticker:",self.ticker," & jday:",jday,"empty response came")
                    if header is not None:
                        ldate = dt.date.today()
                        ldate = workday(str(ldate)).sdate()
                        myheader = header.get('X-RateLimit-Remaining')
                    else:
                        myheader = None
                    #conn = c.connect.create()
                    #cursor = conn.cursor()
                    #with conn:
                    desc = ticker+":"+str(jday)+":"+str(prio)+":=",status
                    nrtbl = """insert into ticker_no_response_list
                    (symbol, load_date,src, "description",tablename,errorcode,headeroutput)
                    values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
                    cursor.execute(nrtbl, (ticker,ldate,'mprice',desc,sourcetable,status,myheader))
            #loading all pricedetails


class loadstockfundamentals:
    def loadstockfinancial(ticker, res, cursor):
        #conn = c.connect.create()
        #cursor = conn.cursor()
        #with conn:
        delbalq = """delete from balancesheet where symbol=%s and fields=%s"""
        insbalq = """insert into balancesheet
                (symbol,fields,"Value_YrT")
                values (%s,%s,%s)"""
        updbalqT1 = """update balancesheet set "Value_YrT-1"=%s
                    where symbol=%s and fields=%s"""
        updbalqT2 = """update balancesheet set "Value_YrT-2"=%s
                    where symbol=%s and fields=%s"""
        updbalqT3 = """update balancesheet set "Value_YrT-3"=%s
                    where symbol=%s and fields=%s"""
        delincq = """delete from incomestatement where symbol=%s and fields=%s"""
        insincq = """insert into incomestatement
                (symbol,fields,"Value_YrT")
                values (%s,%s,%s)"""
        updincqT1 = """update incomestatement set "Value_YrT-1"=%s
                    where symbol=%s and fields=%s"""
        updincqT2 = """update incomestatement set "Value_YrT-2"=%s
                    where symbol=%s and fields=%s"""
        updincqT3 = """update incomestatement set "Value_YrT-3"=%s
                    where symbol=%s and fields=%s"""
        delcasq = """delete from cashflow where symbol=%s and fields=%s"""
        inscasq = """insert into cashflow
                (symbol,fields,"Value_YrT")
                values (%s,%s,%s)"""
        updcasqT1 = """update cashflow set "Value_YrT-1"=%s
                    where symbol=%s and fields=%s"""
        updcasqT2 = """update cashflow set "Value_YrT-2"=%s
                    where symbol=%s and fields=%s"""
        updcasqT3 = """update cashflow set "Value_YrT-3"=%s
                    where symbol=%s and fields=%s"""
        balq = {0:insbalq,1:updbalqT1,2:updbalqT2,3:updbalqT3}
        incq = {0:insincq,1:updincqT1,2:updincqT2,3:updincqT3}
        casq = {0:inscasq,1:updcasqT1,2:updcasqT2,3:updcasqT3}
        try:
            balres = res.get('Financials').get('Balance_Sheet').get('yearly')
        except AttributeError:
            print("No balancesheet info was found for ticker",ticker)
            balres = None
        try:
            incres = res.get('Financials').get('Income_Statement').get('yearly')
        except AttributeError:
            print("No incomestatment info was found for ticker",ticker)
            incres = None
        try:
            casres = res.get('Financials').get('Cash_Flow').get('yearly')
        except AttributeError:
            print("No cashflow info was found for ticker",ticker)
            casres = None
        #print(type(balres))
        if balres is not None and incres is not None and casres is not None:
        # balancesheet data
                byr_list = list(balres.keys())
                iyr_list = list(incres.keys())
                cyr_list = list(casres.keys())
                yr_list = []
                for i in range(len(byr_list)):
                    if len(yr_list)<4:
                        yr = byr_list[i]
                        #print(yr)
                        if yr in iyr_list and yr in cyr_list:
                            yr_list.append(yr)
                        else:
                            pass
                    else:
                        print("the latest 4 years for consideration of financials of stock:",ticker)
                        print(yr_list)
                        break
                minl = len(yr_list)
                if minl>0:
                    #print(ticker,"-balancesheet: totaliablity and total assets")
                    for i in range(minl):# len(yr_list)
                        #print(balres.get(yr_list[i]).keys())
                        try:
                            totalLiability = balres.get(yr_list[i]).get('totalLiab')
                        except AttributeError:
                            totalLiability = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'totalLiability'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'totalLiability', totalLiability))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(totalLiability, ticker, 'totalLiability'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            totalassets = balres.get(yr_list[i]).get('totalAssets')
                        except AttributeError:
                            totalassets = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'totalAssets'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'totalAssets', totalassets))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(totalassets, ticker, 'totalAssets'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            totalcurrentasset = balres.get(yr_list[i]).get('totalCurrentAssets')
                        except AttributeError:
                            totalcurrentasset = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'totalCurrentAssets'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'totalCurrentAssets', totalcurrentasset))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(totalcurrentasset, ticker, 'totalCurrentAssets'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            totalcurrentliability = balres.get(yr_list[i]).get('totalCurrentLiabilities')
                        except AttributeError:
                            totalcurrentliability = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'totalCurrentLiabilities'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'totalCurrentLiabilities', totalcurrentliability))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(totalcurrentliability, ticker, 'totalCurrentLiabilities'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            inventory = balres.get(yr_list[i]).get('inventory')
                        except AttributeError:
                            inventory = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'inventory'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'inventory', inventory))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(inventory, ticker, 'inventory'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            totalequity = balres.get(yr_list[i]).get('totalStockholderEquity')
                        except AttributeError:
                            totalequity = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'totalStockholderEquity'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'totalStockholderEquity', totalequity))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(totalequity, ticker, 'totalStockholderEquity'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            totalLTDebt = balres.get(yr_list[i]).get('longTermDebtTotal')
                        except AttributeError:
                            totalLTDebt = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'longTermDebtTotal'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'longTermDebtTotal', totalLTDebt))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(totalLTDebt, ticker, 'longTermDebtTotal'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            accountpayable = balres.get(yr_list[i]).get('accountsPayable')
                        except AttributeError:
                            accountpayable = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'accountsPayable'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'accountsPayable', accountpayable))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(accountpayable, ticker, 'accountsPayable'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            commonstock = balres.get(yr_list[i]).get('commonStock')
                        except AttributeError:
                            commonstock = None
                        if i == 0:
                            try:
                                cursor.execute(delbalq,(ticker, 'commonStock'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(balq.get(i),(ticker, 'commonStock', commonstock))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(balq.get(i),(commonstock, ticker, 'commonStock'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        #print(totalLiability," and ", totalassets)
                        # incomestatment data
                    #print(ticker,"-incomestatement: totalrevenue and netincome")
                    for i in range(minl):# len(yr_list)
                        #print(incres.get(yr_list[i]).keys())
                        try:
                            totalrevenue = incres.get(yr_list[i]).get('totalRevenue')
                        except AttributeError:
                            totalrevenue = None
                        if i == 0:
                            try:
                                cursor.execute(delincq,(ticker, 'totalRevenue'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(incq.get(i),(ticker, 'totalRevenue', totalrevenue))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(incq.get(i),(totalrevenue, ticker, 'totalRevenue'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            netincome = incres.get(yr_list[i]).get('netIncome')
                        except AttributeError:
                            netincome = None
                        if i == 0:
                            try:
                                cursor.execute(delincq,(ticker, 'netIncome'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(incq.get(i),(ticker, 'netIncome', netincome))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(incq.get(i),(netincome, ticker, 'netIncome'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        #print(totalrevenue," and ", netincome)
                        # cashflow data
                    #print(ticker,"-cashflow: totalrevenue and netincome")
                    for i in range(minl):# len(yr_list)
                        #print(casres.get(yr_list[i]).keys())
                        try:
                            Operatingcashflow = casres.get(yr_list[i]).get('totalCashFromOperatingActivities')
                        except AttributeError:
                            Operatingcashflow = None
                        if i == 0:
                            try:
                                cursor.execute(delcasq,(ticker, 'totalCashFromOperatingActivities'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(casq.get(i),(ticker, 'totalCashFromOperatingActivities', Operatingcashflow))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(casq.get(i),(Operatingcashflow, ticker, 'totalCashFromOperatingActivities'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            capitalexpense = casres.get(yr_list[i]).get('capitalExpenditures')
                        except AttributeError:
                            capitalexpense = None
                        if i == 0:
                            try:
                                cursor.execute(delcasq,(ticker, 'capitalExpenditures'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(casq.get(i),(ticker, 'capitalExpenditures', capitalexpense))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(casq.get(i),(capitalexpense, ticker, 'capitalExpenditures'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        try:
                            changetocash = casres.get(yr_list[i]).get('cashAndCashEquivalentsChanges')
                        except AttributeError:
                            changetocash = None
                        if i == 0:
                            try:
                                cursor.execute(delcasq,(ticker, 'cashAndCashEquivalentsChanges'))
                            except pgs.Error as e:
                                print(e.pgerror)
                            try:
                                cursor.execute(casq.get(i),(ticker, 'cashAndCashEquivalentsChanges', changetocash))
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            try:
                                cursor.execute(casq.get(i),(changetocash, ticker, 'cashAndCashEquivalentsChanges'))
                            except pgs.Error as e:
                                print(e.pgerror)
                        #print(Operatingcashflow," and ", capitalexpense, "and", changetocash)
                else:
                    print("No common financials years were found between BS,IS and CF for ticker:",ticker)
        else:
            print("financial were not found for symbol:", ticker)
    def __init__(self, ticker, sourcetable, fxr, prio, jday, cursor):
        self.ticker = ticker
        self.sourcetable = sourcetable
        SMI = 0
        SSI = 0
        if prio >2:
            pdate = dt.date.today() - dt.timedelta(days =1)
            print("This is not an Asia/Oceania symbol-",ticker,"-",pdate)
        else:
            pdate = dt.date.today()
            print("This is an Asia/Oceania symbol-",ticker,"-",pdate)
        pdate = dt.datetime.strftime(pdate,'%Y-%m-%d')
        pdate=workday(pdate).date
        pdate = dt.datetime.strptime(pdate,'%Y-%m-%d').date()
        #conn = c.connect.create()
        #cursor = conn.cursor()
        #with conn:
        gystock = geteodfundamental(self.ticker)
        status = gystock.sts
        header = gystock.header
        att = 0
        while status!=200:
            if att < 5:
                # print("begins wait of 10 sec. att-", att)
                time.sleep(15)
                gystock = geteodfundamental(self.ticker)
                status = gystock.sts
                header = gystock.header
                att = att +1
            else:
                rdate = dt.datetime.today().date()
                print("date for no response:",rdate)
                print("even after 5 reattempts not getting status code 200 for ",self.ticker)
                break
        if status != 200:
            print(gystock.no_response_ticker, "couldnt get an output from eodhistorical data")
            if header is not None:
                ldate = dt.date.today()
                ldate = workday(str(ldate)).sdate()
                myheader = header.get('X-RateLimit-Remaining')
            else:
                myheader = None
            #conn = c.connect.create()
            #cursor = conn.cursor()
            #with conn:
            desc = ticker+":"+str(jday)+":"+str(prio)+":=",status
            nrtbl = """insert into ticker_no_response_list
            (symbol, load_date,src, "description",tablename,errorcode,headeroutput)
            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            cursor.execute(nrtbl, (ticker,ldate,'mfundamental',desc,sourcetable,status,myheader))
        else:
            yr = gystock.stock_Response
            #loading all the details for the stock financials
            loadstockfundamentals.loadstockfinancial(ticker,yr, cursor)
            #loading all other stock static details
            try:
                yr_sname = yr.get('General').get('Name')
            except AttributeError:
                yr_sname = None
            try:
                yr_currency = yr.get('General').get('CurrencyCode')
            except AttributeError:
                yr_currency = None
            try:
                yr_exch = yr.get('General').get('Exchange')
            except AttributeError:
                yr_exch = None
            try:
                yr_mkt_cap = yr.get('Highlights').get('MarketCapitalization')
                # print(yr_mkt_cap)
            except AttributeError:
                yr_mkt_cap = None
            try:
                yr_split = yr.get('SplitsDividends').get('LastSplitFactor')
                try:
                    print(yr_split,":are split details")
                    num=yr_split[:yr_split.find(":")]
                    den = yr_split[yr_split.find(":")+1:]
                    inum = int(num)
                    dnum = int(den)
                    if inum is not None and inum!=0 and dnum is not None and dnum!=0:
                        yr_split = inum/dnum
                    else:
                        print("weird value encountered for ",self.ticker," value:", yr_split)
                        yr_split = -999
                except ValueError:
                    num = yr_split
                    try:
                        print(yr_split, ":are split details")
                        num = yr_split[:yr_split.find("/")]
                        den = yr_split[yr_split.find("/") + 1:]
                        inum = int(num)
                        dnum = int(den)
                        if inum is not None and inum != 0 and dnum is not None and dnum != 0:
                            yr_split = inum / dnum
                        else:
                            print("weird value encountered for ", self.ticker, " value:", yr_split)
                            yr_split = -999
                    except ValueError:
                        if num is not None and num!='' and ':' not in num:
                            num = int(num)
                        else:
                            num = None
                        yr_split = num
            except AttributeError:
                print("split factor is Null for",self.ticker)
                yr_split = None
            try:
                yr_split_date = yr.get('SplitsDividends').get('LastSplitDate')
            except AttributeError:
                print("split date is null for ",self.ticker)
                yr_split_date = None
            try:
                yr_52_wk_l = yr.get('Technicals').get('52WeekLow')
            except AttributeError:
                yr_52_wk_l = None
            try:
                yr_52_wk_h = yr.get('Technicals').get('52WeekHigh')
            except AttributeError:
                yr_52_wk_h = None
            try:
                yr_dy = yr.get('SplitsDividends').get('ForwardAnnualDividendYield')
            except AttributeError:
                yr_dy = None
            try:
                yr_eps = yr.get('Highlights').get('EarningsShare')
            except AttributeError:
                yr_eps = None
            try:
                yr_ldiv = yr.get('SplitsDividends').get('ForwardAnnualDividendRate')
                #print("dividend:",yr_ldiv)
            except AttributeError:
                yr_ldiv = None
            # getting the statistics stock data from yahoo
            try:
                yr_tot_rev = yr.get('Highlights').get('RevenueTTM')
            except AttributeError:
                yr_tot_rev = None
            try:
                yr_pro_mar = yr.get('Highlights').get('ProfitMargin')
            except AttributeError:
                yr_pro_mar = None
            try:
                yr_shr_out = yr.get('SharesStats').get('SharesOutstanding')
            except AttributeError:
                yr_shr_out = None
            try:
                yr_ROE = yr.get('Highlights').get('ReturnOnEquityTTM')
            except AttributeError:
                yr_ROE = None
            try:
                yr_ROA = yr.get('Highlights').get('ReturnOnAssetsTTM')
            except AttributeError:
                yr_ROA = None
            try:
                yr_rev_gr = yr.get('Highlights').get('QuarterlyRevenueGrowthYOY')
            except AttributeError:
                yr_rev_gr = None
            try:
                yr_pro_gr = yr.get('Highlights').get('QuarterlyEarningsGrowthYOY')
            except AttributeError:
                yr_pro_gr = None
            try:
                yr_peg = yr.get('Highlights').get('PEGRatio')
            except AttributeError:
                yr_peg = None
            try:
                yr_div_po = yr.get('SplitsDividends').get('PayoutRatio')
            except AttributeError:
                yr_div_po = None
            try:
                yr_xdivdt = yr.get('SplitsDividends').get('ExDividendDate')
            except AttributeError:
                yr_xdivdt = None
            try:
                yr_divdt = yr.get('SplitsDividends').get('DividendDate')
            except AttributeError:
                yr_divdt = None
            try:
                tgt_mean_prc = yr.get('Highlights').get('WallStreetTargetPrice')
            except AttributeError:
                tgt_mean_prc = None
            # now allocating values to these fields obtained from eoddata
            try:
                ls = list(yr.get('Earnings').get('History').keys())
            except AttributeError:
                ls = []
            mpdate = dt.datetime.strftime(pdate,'%Y-%m-%d')
            mpdate = dt.datetime.strptime(mpdate,'%Y-%m-%d')
            edate = None
            if len(ls)>0:
                for i in range(len(ls)):
                    csl = dt.datetime.strptime(ls[i],'%Y-%m-%d')
                    if mpdate > csl:
                        pass
                    else:
                        if edate is None:
                            edate = csl
                        else:
                            if edate <= csl:
                                pass;
                            else:
                                edate = csl
                if edate is None:
                    print("No earning dates found that are >= ",pdate,"for ticker:",self.ticker)
                else:
                    print(edate.date())
            else:
                print("No earnings information found for ticker",self.ticker)
            if yr_sname is not None:
                name = yr_sname
            else:
                name = None
            currency = yr_currency
            exchange = yr_exch
            if yr_mkt_cap is not None:
                mkt_Cap = yr_mkt_cap/10**9
                # print(mkt_Cap)
            else:
                mkt_Cap = None
            wk_52_l = yr_52_wk_l
            wk_52_h = yr_52_wk_h
            dy = yr_dy
            eps = yr_eps
            try:
                per = yr.get('Highlights').get('PERatio')
            except AttributeError:
                per = None
            # start rebuilding from here
            if edate is not None:
                earningsDate = edate.date()
            else:
                earningsDate = None
            div_payout = yr_div_po
            shr_out = yr_shr_out
            TR = yr_tot_rev
            if TR is None or float(TR)==0:
                trq = """select "Value_YrT"
                from incomestatement where symbol=%s
                and fields='totalRevenue'"""
                try:
                    cursor.execute(trq,(self.ticker,))
                    trqr = cursor.fetchone()
                    if trqr is None:
                        print("No entry for totalliability present in DB for ticker",self.ticker)
                    else:
                        trcalc = 0
                        cnt  = 0
                        for i in range(len(trqr)):
                            if trqr[i] is not None:
                                trcalc = trcalc+trqr[i]
                                cnt = cnt + 1
                            else:
                                pass
                        if trcalc !=0:
                            TR = trcalc/cnt
                            print("TR is:",TR)
                        else:
                            TR = None
                except pgs.Error as e:
                    print(e.pgerror)
            else:
                pass
            if yr_divdt =='NA' or yr_divdt=='0000-00-00':
                yr_divdt = None
            else:
                pass
            if yr_xdivdt =='NA' or yr_xdivdt=='0000-00-00':
                yr_xdivdt = None
            else:
                pass
            if yr_split_date =='NA' or yr_split_date=='0000-00-00':
                yr_split_date = None
            else:
                pass
            # find the details for total debt
            TD = None
            tdq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
            from balancesheet where symbol=%s
            and fields='totalLiability' """
            try:
                cursor.execute(tdq,(self.ticker,))
                tdqr = cursor.fetchone()
                if tdqr is None:
                    print("No entry for totalliability present in DB for ticker",self.ticker)
                else:
                    tdcalc = 0
                    cnt  = 0
                    for i in range(len(tdqr)):
                        if tdqr[i] is not None:
                            tdcalc = tdcalc+tdqr[i]
                            cnt = cnt + 1
                        else:
                            pass
                    if tdcalc !=0:
                        TD = tdcalc/cnt
                        print("Avg TD is:",TD)
                    else:
                        TD = None
            except pgs.Error as e:
                print(e.pgerror)
            FCF = None
            fcfq = """select a."Value_YrT"-b."Value_YrT" as yrT,
                    a."Value_YrT-1"-b."Value_YrT-1" as yrT1,
                    a."Value_YrT-2"-b."Value_YrT-2" as yrT2
                    ,a."Value_YrT-3"-b."Value_YrT-3" as yrT3
                    from
                    (select symbol,"Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                    from cashflow where symbol=%s
                    and fields='totalCashFromOperatingActivities') as a
                    join
                    (select symbol,"Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                    from cashflow where symbol=%s
                    and fields='capitalExpenditures') as b
                    on a.symbol=b.symbol"""
            try:
                cursor.execute(fcfq,(self.ticker,self.ticker))
                fcfqr = cursor.fetchone()
                if fcfqr is None:
                    print("No entry for totalassets present in DB for ticker",self.ticker)
                else:
                    fcfcalc = 0
                    cnt  = 0
                    for i in range(len(fcfqr)):
                        if fcfqr[i] is not None:
                            fcfcalc = fcfcalc+fcfqr[i]
                            cnt = cnt + 1
                        else:
                            pass
                    if fcfcalc !=0:
                        FCF = fcfcalc/cnt
                        print("Avg FCF is:",FCF)
                    else:
                        FCF = None
            except pgs.Error as e:
                print(e.pgerror)
            PM = yr_pro_mar
            ROE = yr_ROE
            ROA = yr_ROA
            rev_gr = yr_rev_gr
            pro_gr = yr_pro_gr
            PEG = yr_peg
            TA = None
            taq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
            from balancesheet where symbol=%s
            and fields='totalAssets'"""
            try:
                cursor.execute(taq,(self.ticker,))
                taqr = cursor.fetchone()
                if taqr is None:
                    print("No entry for totalassets present in DB for ticker",self.ticker)
                else:
                    tacalc = 0
                    cnt  = 0
                    for i in range(len(taqr)):
                        if taqr[i] is not None:
                            tacalc = tacalc+taqr[i]
                            cnt = cnt + 1
                        else:
                            pass
                    if tacalc !=0:
                        TA = tacalc/cnt
                        print("Avg TA is:",TA)
                    else:
                        TA = None
            except pgs.Error as e:
                print(e.pgerror)
            if (TR is None or TR == 0) or (PM is None or PM == 0):
                NI = None
            else:
                TR = float(TR)
                PM = float(PM)
                NI = TR*PM
            if (FCF is None or FCF == 0) or (TD is None or TD ==0):
                FCF2D = None
            else:
                FCF = float(FCF)
                TD = float(TD)
                FCF2D = FCF/TD
            if (NI is None or NI == 0) or (TD is None or TD ==0):
                DSCR = None
            else:
                NI = float(NI)
                TD = float(TD)
                DSCR = NI/TD
            if (TR is None or TR == 0) or (TA is None or TA ==0):
                ATR = None
            else:
                TR = float(TR)
                ATR = TR/TA
            #cc = fxconvert()
            cc = fxr
            ccr = cc.get(currency, None)
            if mkt_Cap is not None:
                if currency == 'GBX':
                    ccr = cc.get('GBP', None)
                    mkt_Cap_eur = mkt_Cap/ccr
                    print('mkt_Cap_eur is',mkt_Cap_eur,'for GBP based on fx was',ccr)
                elif currency == 'ZAc':
                    ccr = cc.get('ZAR', None)
                    mkt_Cap_eur = mkt_Cap/ccr
                    print('mkt_Cap_eur is',mkt_Cap_eur,'for ZAR based on fx was',ccr)
                elif ccr is not None:
                    mkt_Cap_eur = mkt_Cap/ccr
                    print('mkt_Cap_eur is',mkt_Cap_eur,'for currency ',currency,'since fx was',ccr)
                else:
                    mkt_Cap_eur = None
                    print('mkt_cap_in_euro is null as ccr is Null')
            else:
                mkt_Cap_eur = None
                print('mkt_cap_in_euro is null')
            if PEG is None:
                if per is not None and pro_gr is not None and float(pro_gr)!=0:
                    print(per,pro_gr)
                    PEG = float(per)/(float(pro_gr)*100)
                elif pro_gr==0:
                    PEG = 0
                    print("for the ticker ",self.ticker," the PER=",per," and profit_growth=",pro_gr)
                else:
                    PEG = None
            elif float(PEG) == 0 or float(PEG) < 0:
                if per is not None and pro_gr is not None and float(pro_gr)!=0:
                    print(per,pro_gr)
                    PEG = float(per)/(float(pro_gr)*100)
                elif pro_gr==0:
                    PEG = 0
                    print("for the ticker ",self.ticker," the PER=",per," and profit_growth=",pro_gr)
                else:
                    PEG = None
            else:
                pass
            print(ticker, name, currency, exchange, mkt_Cap, wk_52_l, wk_52_h, dy, eps, per, sourcetable)
            print(ticker,ATR,DSCR,FCF2D,ROE,ROA,rev_gr,pro_gr,PEG)
            print(ticker,shr_out,div_payout,earningsDate,yr_divdt,yr_xdivdt,tgt_mean_prc,yr_split_date,yr_split)
                # loading the data into stock_master
            if 'benchmark' in self.sourcetable:
                iscr = """update benchmark_master set "name"=%s,exchange=%s
                        where symbol=%s"""
                ilst = [name, exchange,self.ticker]
            else:
                iscr = """update stock_master set "name"=%s, currency=%s,
                exchange=%s,mkt_cap_in_bill=%s,price_52wk_low=%s,
                price_52wk_high=%s,dividend=%s,eps=%s,per_mkt=%s,
                exdivdate=%s,divdate=%s,earningsdate=%s,tgt_price_1yr=%s,
                div_value=%s,split_date=%s,split_factor=%s,shr_outstanding=%s
                where symbol=%s"""
                if shr_out is not None and type(shr_out)!=int:
                    print(type(shr_out)," was the type for shares oustanding",shr_out,self.ticker)
                    shr_out = round(float(shr_out),0)
                    shr_out=int(shr_out)
                else:
                    pass
                ilst = [name, currency, exchange,
                        mkt_Cap, wk_52_l, wk_52_h, dy, eps, per,
                        yr_xdivdt, yr_divdt,earningsDate,
                        tgt_mean_prc, yr_ldiv, yr_split_date,
                        yr_split, shr_out,self.ticker]
            try:
                cursor.execute(iscr, ilst)
                SMI = 1
                # print('successful insert')
            except pgs.Error as e:
                print(e.pgerror)
            if 'benchmark' in self.sourcetable:
                jobload = """update jobrunlist
                set runstatus = 'complete' where symbol=%s and
                runsource='mfundamental' and rundate=%s and jobtable=%s """
                try:
                     cursor.execute(jobload, (ticker, jday, sourcetable))
                     print(ticker, " job executed successfully")
                except pgs.Error as e:
                    print(e.pgerror)
                else:
                    pass
            else:
                cursor.execute("select price from stock_statistics where symbol=%s",(self.ticker,))
                price = cursor.fetchone()
                if price is not None:
                    price = price[0]
                else:
                    price = None
                if (price is not None and float(price)!=0) and (TR is not None and float(TR)!=0) and (shr_out is not None and float(shr_out)!=0):
                    #print(TR,'-',shr_out)
                    P2S = price/(TR/shr_out)
                else:
                    P2S = None
                CA = None
                caq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                from balancesheet where symbol=%s
                and fields='totalCurrentAssets'"""
                try:
                    cursor.execute(caq,(self.ticker,))
                    caqr = cursor.fetchone()
                    if caqr is None:
                        print("No entry for totalCurrentAssets present in DB for ticker",self.ticker)
                    else:
                        cacalc = 0
                        cnt  = 0
                        for i in range(len(caqr)):
                            if caqr[i] is not None:
                                cacalc = cacalc+caqr[i]
                                cnt = cnt + 1
                            else:
                                pass
                        if cacalc !=0:
                            CA = cacalc/cnt
                            print("Avg CA is:",CA)
                        else:
                            CA = None
                except pgs.Error as e:
                    print(e.pgerror)
                CL = None
                clq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                from balancesheet where symbol=%s
                and fields='totalCurrentLiabilities'"""
                try:
                    cursor.execute(clq,(self.ticker,))
                    clqr = cursor.fetchone()
                    if clqr is None:
                        print("No entry for totalCurrentLiabilities present in DB for ticker",self.ticker)
                    else:
                        clcalc = 0
                        cnt  = 0
                        for i in range(len(clqr)):
                            if clqr[i] is not None:
                                clcalc = clcalc+clqr[i]
                                cnt = cnt + 1
                            else:
                                pass
                        if clcalc !=0:
                            CL = clcalc/cnt
                            print("Avg CL is:",CL)
                        else:
                            CL = None
                except pgs.Error as e:
                    print(e.pgerror)
                if CL is not None and CA is not None:
                    CR = CA/CL
                else:
                    CR = None
                INV = None
                invq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                from balancesheet where symbol=%s
                and fields='inventory'"""
                try:
                    cursor.execute(invq,(self.ticker,))
                    invqr = cursor.fetchone()
                    if invqr is None:
                        print("No entry for inventory present in DB for ticker",self.ticker)
                    else:
                        invcalc = 0
                        cnt  = 0
                        for i in range(len(invqr)):
                            if invqr[i] is not None:
                                invcalc = invcalc+invqr[i]
                                cnt = cnt + 1
                            else:
                                pass
                        if invcalc !=0:
                            INV = invcalc/cnt
                            print("Avg INV is:",INV)
                        else:
                            INV = None
                except pgs.Error as e:
                    print(e.pgerror)
                if CA is not None and CL is not None and INV is not None:
                    QR = (CA - INV)/CL
                else:
                    QR = None
                LD = None
                ldq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                from balancesheet where symbol=%s
                and fields='totalLiability'"""
                try:
                    cursor.execute(ldq,(self.ticker,))
                    ldqr = cursor.fetchone()
                    if ldqr is None:
                        print("No entry for totalLiability present in DB for ticker",self.ticker)
                    else:
                        ldcalc = 0
                        cnt  = 0
                        for i in range(len(ldqr)):
                            if ldqr[i] is not None:
                                ldcalc = ldcalc+ldqr[i]
                                cnt = cnt + 1
                            else:
                                pass
                        if ldcalc !=0:
                            LD = ldcalc/cnt
                            print("Avg LD is:",LD)
                        else:
                            LD = None
                except pgs.Error as e:
                    print(e.pgerror)
                TE = None
                teq = """select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"
                from balancesheet where symbol=%s
                and fields='totalStockholderEquity'"""
                try:
                    cursor.execute(teq,(self.ticker,))
                    teqr = cursor.fetchone()
                    if ldqr is None:
                        print("No entry for totalStockholderEquity present in DB for ticker",self.ticker)
                    else:
                        tecalc = 0
                        cnt  = 0
                        for i in range(len(teqr)):
                            if teqr[i] is not None:
                                tecalc = tecalc+teqr[i]
                                cnt = cnt + 1
                            else:
                                pass
                        if tecalc !=0:
                            TE = tecalc/cnt
                            print("Avg TE is:",TE)
                        else:
                            TE = None
                except pgs.Error as e:
                    print(e.pgerror)
                if LD is not None and TE is not None:
                    D2E = LD/TE
                else:
                    D2E = None
                istr = """update stock_statistics set "name"=%s,currency=%s,
                        mkt_cap_stock_in_bill=%s,mkt_cap_stocks_bill_eur=%s,
                        eps=%s,per=%s,dividend_yield=%s,exchange=%s,
                        div_payout=%s,price_2_sales=%s,roa=%s,roe=%s,
                        profit_margin=%s,current_ratio=%s,quick_Ratio=%s,
                        debt_2_equity=%s,asset_turnover_ratio=%s,
                        profitability_growth=%s,sales_growth=%s,fcf2debt=%s,
                        dscr=%s,peg=%s where symbol=%s"""
                istrv = [name, currency, mkt_Cap, mkt_Cap_eur,
                         eps, per, dy, exchange, div_payout, P2S, ROA, ROE,
                         PM, CR, QR, D2E, ATR, pro_gr, rev_gr,
                         FCF2D, DSCR, PEG,self.ticker]
                try:
                    cursor.execute(istr,istrv)
                    SSI = 1
                except pgs.Error as e:
                    print(e.pgerror)
                if SMI == 1 and SSI == 1:
                    jobload = """update jobrunlist
                    set runstatus = 'complete' where symbol=%s and
                    runsource='mfundamental' and rundate=%s and jobtable=%s """
                    try:
                         cursor.execute(jobload, (ticker, jday, sourcetable))
                         print(ticker, " job executed successfully")
                    except pgs.Error as e:
                        print(e.pgerror)
                else:
                    pass
        print('postgres connection closed for ', self.ticker)

