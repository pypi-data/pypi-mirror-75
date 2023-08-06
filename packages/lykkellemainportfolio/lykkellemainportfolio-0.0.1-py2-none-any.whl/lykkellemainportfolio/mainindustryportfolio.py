#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 23:29:07 2019
create statistics for personalized accounts
@author: debmishra
"""
from lykkelleconf.connecteod import connect
import pandas as pd
from lykkelleportfolio.createOptportfolioeod import LoadOptPortfolio
import psycopg2 as pgs
import datetime as dt
from os.path import expanduser

home = expanduser("~")
pd.options.mode.chained_assignment = None


selind = """select distinct industry,currency from stock_statistics where currency is not Null and industry is not null
            union
            select distinct industry,'GLBL' from stock_statistics where industry is not null"""
calcquery = """select distinct st.symbol,st.mean_annualized_return,
                st.std_annualized,st.beta, st.dividend_yield,st.mkt_cap_stocks_bill_eur,
                0 as scnt, 0 as bcnt, st.bmk_symbol,
                st.mkt_mean_annualized_return,st.price,st.currency,0 as isdel
                from stock_statistics st
                where st.industry=%s and st.currency=%s
                and st.std_annualized<>'NaN'"""
scntq = """select count(*) as cnt from dbo.stock_history
    where price_return <>0 and price_return is not null and symbol=%s"""
bcntq = """select count(*) as cnt from dbo.benchmark_history
    where price_return <>0 and price_return is not null and symbol=%s"""
calcqueryg = """select distinct st.symbol,st.mean_annualized_return,
                st.std_annualized,st.beta, st.dividend_yield,st.mkt_cap_stocks_bill_eur,
                0 as scnt, 0 as bcnt,
                st.bmk_symbol, st.mkt_mean_annualized_return,st.price,st.currency,0 as isdel
                from stock_statistics st
                where st.industry=%s
                and st.std_annualized<>'NaN'"""

def personalportfolio():
    conn = connect.create()
    cursor = conn.cursor()
    try:
        cursor.execute(selind)
        myact = cursor.fetchall()
    except pgs.Error as e:
        print(e.pgerror)
    if len(myact)!=0:
        for i in range(len(myact)):
            actid = myact[i][0]
            actcurr = myact[i][1]
            indid=actid.replace(' ','') + '_'+ actcurr
            if actcurr == 'GLBL':
                try:
                    cursor.execute(calcqueryg, (actid,))
                    mycalc = cursor.fetchall()
                except pgs.Error as e:
                    print(e.pgerror)
                    mycalc = None
            else:
                try:
                    cursor.execute(calcquery, (actid, actcurr ))
                    mycalc = cursor.fetchall()
                except pgs.Error as e:
                    print(e.pgerror)
                    mycalc = None
            if mycalc is not None and len(mycalc)>0:
                mypordf = pd.DataFrame(mycalc, columns = ['symbol','mean','SD','beta','divy','Mcapeur','scnt','mcnt', 'exch','mmean','price','currency','isdel'])
                #print(mypordf.head())
                print("size of portfolio before clearning entries:",len(mypordf))
                for i in range(len(mypordf)):
                    chksym = mypordf['symbol'].iloc[i]
                    cursor.execute(scntq, (chksym,))
                    scnt = cursor.fetchone()
                    #print(scnt)
                    scnt = scnt[0]
                    chkbym = mypordf['exch'].iloc[i]
                    cursor.execute(bcntq, (chkbym,))
                    bcnt = cursor.fetchone()
                    bcnt = bcnt[0]
                    #print(scnt,':',chksym,' & ',bcnt,':',chkbym)
                    if scnt>0 and bcnt >0:
                        mypordf['scnt'].iloc[i] = scnt
                        mypordf['mcnt'].iloc[i] = bcnt
                        #print(myseldf['scnt'].iloc[i])
                        #print(myseldf['mcnt'].iloc[i])
                        #print(mypordf.iloc[i])
                        #print("good",mypordf[['symbol','scnt','mcnt']])
                    else:
                        mypordf['isdel'].iloc[i] = 1
                        #indexNames = mypordf[(mypordf['symbol']== chksym)].index
                        print("deleted ",chksym, " from portfolio entry as scnt:",scnt, " &bcnt:",bcnt)
                        #mypordf.drop(indexNames , inplace=True)
                        #print("bad2",mypordf[['symbol','scnt','mcnt']])
                indexnames = mypordf[(mypordf['isdel']==1)].index
                mypordf.drop(indexnames, inplace=True)
                #print(mypordf.head())
                print("size of portfolio after clearning entries:",len(mypordf))
                myoutput = LoadOptPortfolio(mypordf, indid)
                myfdf = myoutput.finaldf
                myflst = myoutput.lstins
                #print(myfdf.head(10))
                # PorID, mean,mkt_mean,stdpa, mstdpa,beta, var95, var99, mvar95, mvar99,totalmc
                act = myflst[0]
                mean = myflst[1]
                mkt_mean = myflst[2]
                stdpa = myflst[3]
                mstdpa = myflst[4]
                beta = myflst[5]
                var95 = myflst[6]
                var99 = myflst[7]
                mvar95 = myflst[8]
                mvar99 = myflst[9]
                pdate = dt.datetime.today().date()
                print("trying to insert the following statistics for the currnt industry:", indid)
                print(act,mean,mkt_mean,stdpa,mstdpa,beta,var95,var99,mvar95,mvar99)
                myentry = [act,mean,mkt_mean,stdpa,mstdpa,beta,var95,var99,mvar95,mvar99]
                strq ="""insert into ind_acutulus_store
                    (store_date,industry_id,mean,mkt_mean,stdp,mkt_stdp,beta,
                    var95,var99,mkt_var95,mkt_var99)
                    select %s,industry_id,mean,mkt_mean,stdp,
                    mkt_stdp,beta,var95,var99,mkt_var95,mkt_var99
                    from ind_acutulus where industry_id=%s ON CONFLICT
                    DO NOTHING"""
                delq = """delete from ind_acutulus where industry_id=%s"""
                try:
                    cursor.execute(strq,(pdate, indid))
                    print("successful entry of old entry ind_Acutulus_store for ", indid)
                    cursor.execute(delq, (indid,))
                    print("successful delete of old entry from ind_Acutulus for ", indid)
                except pgs.Error as e:
                    print(e.pgerror)
                    print("delete unsuccessful for ", act)
                insq = """insert into ind_acutulus
                (industry_id,mean,mkt_mean,stdp,mkt_stdp,beta,var95,var99,mkt_var95,mkt_var99)
                 values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                try:
                     cursor.execute(insq, myentry)
                     print("successful insert for ", act)
                except pgs.Error as e:
                     print(e.pgerror)
                     print("insert unsuccessful for ", act)
            else:
                print("No entry found in Db for the selcted stocks in industry id:", indid)
                print("list of selected stocks mentioned below")
                print(mycalc)
    else:
        print("industry empty")

#personalportfolio()

