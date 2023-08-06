#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 20:33:29 2019
Take all the records from stock master and benchmark master
and compute returns
Program should run daily
@author: debmishra
"""
from lykkelleconf.connecteod import connect
from lykkellestatistics.getlogreturneod import getlogreturn
from lykkellestatistics.getcompletelogreturneod import getcompletelogreturn
import psycopg2 as pgs
from lykkellestatistics.allstatisticseod import allstatistics
import datetime as dt
from os.path import expanduser
from lykkellestatistics.getrollingmeaneod import getrollingmean
from lykkellestatistics.getlastrollingmeaneod import getlastrollingmean
from lykkelleconf.workday import workday
import pandas as pd

home = expanduser("~")


class maincalculationprog:
    def logreturns(param):
        # loading the tickers from stock history and BMhistory and calculates return
        conn0 = connect.create()
        cursor0 = conn0.cursor()
        with conn0:
            #startdate = dt.datetime.today()
            if param == 'T':
                q = """select distinct a.symbol from stock_all a join benchmark_all b 
                        on a.index_code=b.symbol
                        where b.is_active=true and b.prio=2 and b.symbol='TA100.INDX' fetch first 5 rows only"""
            else:
                q = """select distinct a.symbol from stock_all a join benchmark_all b 
                        on a.index_code=b.symbol
                        where b.is_active=true and b.prio=2 and b.symbol='TA100.INDX'"""
            cursor0.execute(q)
            val = cursor0.fetchall()
            val = tuple(val)
            # print(val)
            hq = """select symbol, count(*) as cnt from stock_history
                    where symbol in %s
                    group by symbol"""
            if len(val)>0:
                cursor0.execute(hq, (val,))
                hval = cursor0.fetchall()
                # print(hval)
                mypd = pd.DataFrame(hval, columns=['symbol', 'cnt'])
                # print(mypd.head())
                mypdvalid = mypd[mypd['cnt'] > 1]
                mypdinvalid = mypd[mypd['cnt'] <= 1]
                # print(mypdvalid.head())
                deltastk = mypdinvalid['symbol'].values
                stklst = mypdvalid['symbol'].values
                #print(mylist)
                #enddate = dt.datetime.today()
                #print(enddate - startdate)
                print("list of stocks that are in master but don't have 2 or more valid prices in history:\n", deltastk)
            else:
                print("No stocks present ins stock_all for prio-0")
                stklst = []
            #startdate = dt.datetime.today()
            if param == 'T':
                q = """select distinct b.symbol from benchmark_all b 
                        where b.is_active=true and b.prio=2 and b.symbol='TA100.INDX' fetch first 5 rows only"""
            else:
                q = """select distinct b.symbol from benchmark_all b 
                        where b.is_active=true and b.prio=2 and b.symbol='TA100.INDX'"""
            cursor0.execute(q)
            val = cursor0.fetchall()
            val = tuple(val)
            # print(val)
            hq = """select symbol, count(*) as cnt from benchmark_history
                    where symbol in %s
                    group by symbol"""
            if len(val)>0:
                cursor0.execute(hq, (val,))
                hval = cursor0.fetchall()
                # print(hval)
                mybpd = pd.DataFrame(hval, columns=['symbol', 'cnt'])
                # print(mypd.head())
                mybpdvalid = mybpd[mybpd['cnt'] > 1]
                mybpdinvalid = mybpd[mybpd['cnt'] <= 1]
                # print(mypdvalid.head())
                deltabmk = mybpdinvalid['symbol'].values
                bmklst = mybpdvalid['symbol'].values
                #print(mylist)
                #enddate = dt.datetime.today()
                #print(enddate - startdate)
                print("list of bmark that are in master but don't have 2 or more valid prices in history:\n", deltabmk)
            else:
                print("No benchmarks present in benchmark all for prio-0")
                bmklst = []
                #getting log returns for the stock table
            for i in range(len(stklst)):
                stk = stklst[i]
                #stk = stk[0]
                chk = """select count(*) from stock_history
                    where symbol=%s and price_return is not null
                    and price_date > current_date - 31"""
                cursor0.execute(chk,(stk,))
                chkc = cursor0.fetchone()
                chkc = chkc[0]
                if chkc != 0:
                    getlogreturn(stk, 'stock_history', cursor0)
                else:
                    getcompletelogreturn(stk, 'stock_history', cursor0,'tmp0')
                    print("Ran the complete log return solution for stock ", stk)
                chk50 = """select count(*) from stock_history
                    where symbol=%s and ma_50d is not null
                    and price_date > current_date - 31"""
                cursor0.execute(chk50,(stk,))
                chk50c = cursor0.fetchone()
                chk50c = chk50c[0]
                if chk50c != 0:
                    getlastrollingmean.rollingmean50d(stk,'stock_history', cursor0)
                else:
                    getrollingmean.rollingmean50d(stk,'stock_history', cursor0,'tmp0')
                    print("Ran the complete 50d rolling mean solution for stock ", stk)
                chk200 = """select count(*) from stock_history
                    where symbol=%s and ma_200d is not null
                    and price_date > current_date - 31"""
                cursor0.execute(chk200,(stk,))
                chk200c = cursor0.fetchone()
                chk200c = chk200c[0]
                if chk200c != 0:
                    getlastrollingmean.rollingmean200d(stk,'stock_history', cursor0)
                else:
                    getrollingmean.rollingmean200d(stk,'stock_history', cursor0,'tmp0')
                    print("Ran the complete 200d rolling mean solution for stock ", stk)
            #getting log returns for the benchmark return
            for i in range(len(bmklst)):
                bmk = bmklst[i]
                #bmk = bmk[0]
                chkb = """select count(*) from benchmark_history
                    where symbol=%s and price_return is not null
                    and price_date > current_date - 31"""
                cursor0.execute(chkb,(bmk,))
                chkbc = cursor0.fetchone()
                chkbc = chkbc[0]
                if chkbc != 0:
                    getlogreturn(bmk, 'benchmark_history', cursor0)
                else:
                    getcompletelogreturn(bmk, 'benchmark_history', cursor0,'tmp0')
                    print("Ran the complete log return solution for stock ", bmk)
            stklst = tuple(stklst)
            bmklst = tuple(bmklst)
            chkrets = """select symbol from dbo.stock_history where price_return is null and symbol in %s
                       group by symbol having count(*)>1"""
            chkretb = """select symbol from dbo.benchmark_history where price_return is null and symbol in %s
                       group by symbol having count(*)>1"""
            if len(stklst)>0:
                cursor0.execute(chkrets, (stklst,))
                failstk = cursor0.fetchall()
                #print(failstk)
                print(failstk, "\n are the list of ", len(failstk), " records from ", len(stklst),
                      " stock history that have no calculated return")
            else:
                print("No need to check empty returns as stock list for prio-0 is empty")
            if len(bmklst)>0:
                cursor0.execute(chkretb, (bmklst,))
                failbmk = cursor0.fetchall()
                print(failbmk, "\n are the list of ",len(failbmk)," records from ",len(bmklst)," benchmark history that have no calculated return")
            else:
                print("No need to calculate empty returns as benchmark list is empty fo prio-0")
        print("postgres connection closed for logreturns")

    def statistics(param):
        # loading the tickers from stock history and BMhistory and calculates return
        conn0 = connect.create()
        cursor0 = conn0.cursor()
        with conn0:
            if param == 'T':
                statqry = """select mas.symbol, mas.exchange, mas.currency,
                rf.abbr as abbr,
                rf.country as country, mas.source_table,rf.symbol as bmk_ticker
                from stock_master mas
                join stock_all as sall on mas.symbol=sall.symbol
                join benchmark_all rf on sall.index_code=rf.symbol
                where rf.prio=2 and rf.symbol='TA100.INDX' fetch first 5 rows only"""
            else:
                statqry = """select mas.symbol, mas.exchange, mas.currency,
                rf.abbr as abbr,
                rf.country as country, mas.source_table,rf.symbol as bmk_ticker
                from stock_master mas
                join stock_all as sall on mas.symbol=sall.symbol
                join benchmark_all rf on sall.index_code=rf.symbol
                where rf.prio=2 and rf.symbol='TA100.INDX'"""
            try:
                cursor0.execute(statqry)
                statres = cursor0.fetchall()
            except pgs.Error as e:
                print(e.pgerror)
                statres = []
            if statres is None:
                statres = []
            else:
                pass
            if len(statres)>0:
                for i in range(len(statres)):
                    symbol = statres[i][0]
                    exchange = statres[i][1]
                    currency = statres[i][2]
                    abbr = statres[i][3]
                    country = statres[i][4]
                    sourcetable = statres[i][5]
                    bsymbol = statres[i][6]
                    print(symbol, bsymbol, country, sourcetable,'asia stock')
                    if symbol is not None and bsymbol is not None and country is not None:
                        allstatistics(symbol, bsymbol, country, sourcetable, cursor0)
                        #loading all statistics to stat history table
                        pdate = dt.datetime.today().date()
                        pdate = str(pdate)
                        pdate = workday(pdate).sdate()
                        print('asia stock date-',pdate)
                        delq = """delete from stock_statistics_history
                        where symbol=%s and price_date=%s"""
                        cursor0.execute(delq, (symbol, pdate))
                        selq = """select * from stock_statistics where symbol=%s"""
                        cursor0.execute(selq, (symbol, ))
                        statdata = cursor0.fetchone()
                        statdata = list(statdata)
                        statdata.append(pdate)
                        insq = """insert into stock_statistics_history
                            (symbol,name,industry,source_table,price,
                            currency,capm_return,mean_annualized_return,
                            beta,var95_annualized,var99_annualized,
                            annual_rf_rate,mkt_mean_annualized_return,
                            mkt_cap_stock_in_bill,std_annualized,eps,per,
                            mkt_cap_stocks_bill_eur,dividend_yield,
                            exchange,mkt_annualized_std,mkt_annualized_var95,
                            mkt_annualized_var99,ind_category,div_payout,
                            price_2_sales,roa,roe,profit_margin,current_ratio,
                            quick_ratio,debt_2_equity,asset_turnover_ratio,
                            profitability_growth,sales_growth,fcf2debt,dscr,peg,bmk_symbol,mean_50D,mean_200D,price_date)
                            values (%s, %s , %s, %s, %s, %s,
                            %s, %s , %s, %s, %s, %s,
                            %s, %s , %s, %s, %s, %s,
                            %s, %s , %s, %s, %s, %s,
                            %s, %s , %s, %s, %s, %s,
                            %s, %s , %s, %s, %s, %s,
                            %s, %s, %s, %s,%s,%s)"""
                        try:
                            cursor0.execute(insq, (statdata))
                        except pgs.Error as e:
                            print("For the ", symbol, "&", pdate, " insert was unsuccessful")
                            print(e.pgerror)
                    else:
                        print("No paramater for statistics found for following combination")
                        print(symbol,bsymbol,country,sourcetable)
            else:
                print("The query to get statistics returned zero results")

# calling main program
#maincalculationprog.logreturns()
#maincalculationprog.statistics()
