# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:38:33 2019
create a program that identifies the
bet combination of portfolio based on the following:
    best mean return +div_yield
    for:
        beta < 1.1
        SD < .20
        weighted capm > weighted mkt return
    for the the following:

@author: debaj
"""
from lykkelleconnector.fxconverteod import fxconvert
from lykkelleportfolio.createOptportfolioeod import bestpor
from lykkelleconf.connecteod import connect
import pandas as pd
import psycopg2 as pgs
import datetime as dt
from os.path import expanduser
import math as mt

home = expanduser("~")
pd.options.mode.chained_assignment = None

keympor = ['ACTWRLDSCAP', 'ACTWRLDMCAP', 'ACTWRLDLCAP', 'ACTUMLMSCAP',
               'ACTUMLMMCAP', 'ACTUMLMLCAP', 'ACTSASCAP', 'ACTSAMCAP',
               'ACTOCSCAP', 'ACTOCMCAP', 'ACTNASCAP', 'ACTNAMCAP',
               'ACTNALCAP', 'ACTNAEUSCAP', 'ACTNAEUMCAP',
               'ACTNAEULCAP', 'ACTHYSCAP', 'ACTHYMCAP',
               'ACTHGPRMSCAP', 'ACTHGPRMMCAP', 'ACTHGPRMLCAP',
               'ACTASIASCAP', 'ACTASIAMCAP', 'ACTASIALCAP', 'ACTSALCAP',
               'ACTOCLCAP', 'ACTHYLCAP','ACTEULCAP','ACTEUMCAP','ACTEUSCAP',
               'ACTUVWRLD','ACTUVWRLDLM','ACTDIVWRLD','ACTWRLDALL','ACTWRLDLRALL','ACTWRLDIND']
valmpor = [25, 25, 25, 10, 10 , 10, 10, 10, 10, 10, 10, 10 ,
           10, 15, 15, 15, 10, 10, 15, 15, 15, 10, 10, 10, 10,
           10, 10, 10, 10, 10, 25, 15, 20, 25,15,20]
dictpor = dict(zip(keympor, valmpor))
# 'symbol','mean','beta','divy','Mcapeur','scnt','mcnt', 'exch', 'porid'

def FinalOptPortfolio():
    conn = connect.create()
    cursor = conn.cursor()
    with conn:
        cc = fxconvert(cursor)
        myporq ="""select distinct portfolio_id from index_acutulus
        order by portfolio_id desc"""
        myselq ="""select distinct st.symbol,st.mean_annualized_return,st.std_annualized,st.beta,
                    st.dividend_yield, st.mkt_cap_stocks_bill_eur,0 as scnt,0 as bcnt,
                const.exch, st.mkt_mean_annualized_return,st.price,st.currency,0 as isdel
                from dbo.index_acutulus act
                join
                dbo.index_acutulus_const const
                on act.portfolio_id=const.portfolio_id
                join dbo.stock_statistics st
                on st.symbol=const.symbol
                where act.portfolio_id=%s and st.currency is not null
                and st.mean_annualized_return >= st.mkt_mean_annualized_return
                and const.exch in (select symbol from benchmark_all where is_active=True)
                order by st.mean_annualized_return desc"""
        scntq = """select count(*) as cnt from dbo.stock_history
        where price_return <>0 and price_return is not null and symbol=%s"""
        bcntq = """select count(*) as cnt from dbo.benchmark_history
        where price_return <>0 and price_return is not null and symbol=%s"""
        cursor.execute (myporq)
        mypor = cursor.fetchall()
        kpord = []
        for i in range(len(mypor)):
            v = dictpor.get(mypor[i][0])
            if v is not None:
                kpord.append(mypor[i][0])
            else:
                print(mypor[i][0], "is not in list of portfolio dictionary")
    # calculate the list of stocks under each category.
        for i in range(len(kpord)): #len(kpord)
            print("starting portfolio:",kpord[i])
            cursor.execute(myselq, (kpord[i], ))
            mysel = cursor.fetchall()
            # lenmysel = len(mysel)
            lenkpor = dictpor.get(kpord[i])
            kpor = kpord[i]
            myseldf = pd.DataFrame(mysel, columns = ['symbol','mean','SD','beta','divy','Mcapeur','scnt' ,'mcnt','exch','mmean','price','currency','isdel'])
            print("clearing entries from portfolio with data < 1000")
            if len(myseldf)>0:
                print("size of portfolio before clearning entries:",len(myseldf))
                for i in range(len(myseldf)):
                    chksym = myseldf['symbol'].iloc[i]
                    cursor.execute(scntq, (chksym,))
                    scnt = cursor.fetchone()
                    #print(scnt)
                    scnt = scnt[0]
                    chkbym = myseldf['exch'].iloc[i]
                    cursor.execute(bcntq, (chkbym,))
                    bcnt = cursor.fetchone()
                    bcnt = bcnt[0]
                    #print(scnt,':',chksym,' & ',bcnt,':',chkbym)
                    if scnt>0 and bcnt >0:
                        myseldf['scnt'].iloc[i] = scnt
                        myseldf['mcnt'].iloc[i] = bcnt
                        #print(myseldf['scnt'].iloc[i])
                        #print(myseldf['mcnt'].iloc[i])
                    else:
                        myseldf['isdel'].iloc[i] = 1
                        #indexNames = mypordf[(mypordf['symbol']== chksym)].index
                        print("deleted ",chksym, " from portfolio entry as scnt:",scnt, " &bcnt:",bcnt)
                indexnames = myseldf[(myseldf['isdel']==1)].index
                myseldf.drop(indexnames, inplace=True)
                print("size of portfolio after clearning entries:",len(myseldf))
            else:
                print("zero records in selected portfolio. No operation needed", kpor)
            print("portfolio being evaluated:",kpor)
            print("length of portfolio:",len(myseldf))
            if len(mysel)!= 0:
                mytop = myseldf['symbol'].iloc[0:lenkpor].values
                print("length of first top:", len(mytop))
                mybottom = myseldf['symbol'].iloc[lenkpor:len(myseldf)].values
                top = mytop
                bottom = mybottom
                mydel = []
                close = 0
                closeFlag = 0
                mycomp = None
                myret = None
                seldf = myseldf
                mycheck = 1
                while (closeFlag ==0):#
                    print("entering main loop:",mycheck)
                    fo = bestpor(seldf, kpor, top, bottom, lenkpor)
                    close = fo.close
                    if close ==0:
                        bestdf = fo.bestdf
                        bret = fo.bret
                        tmp = fo.mdel
                        print("value passed:",tmp, type(tmp))
                        if tmp is not None and type(tmp)==str:
                            mydel.append(tmp)
                        elif tmp is not None and type(tmp)==list:
                            mydel.extend(tmp)
                        else:
                            pass
                        print(mydel)
                        # oret = fo.oret
                        top = bestdf['symbol'].values
                        print("top calculation in loop:",len(top))
                        SD = bestdf.sort_values(['SD'], ascending =0).iloc[0]
                        SD = SD['SD']
                        print(SD)
                        bottom = myseldf.loc[~myseldf['symbol'].isin(top)]
                        bottom = bottom.loc[~bottom['symbol'].isin(mydel)]
                        #print(bottom)
                        bottom = bottom.loc[bottom['SD']<SD]
                        bottom = bottom['symbol'].values
                        print(bottom)
                        mycomp = fo.bestdf
                        myret = bret
                        if len(bottom)>0:
                            closeFlag = 0
                        else:
                            closeFlag = 1
                    else:
                        print("No iteration needed. Skipping to next")
                        mycomp = fo.bestdf
                        myret = fo.bret
                        closeFlag = 1
                    mycheck = mycheck +1
                print("optimal combinations found after ",mycheck, "trials for portfolio:", kpor)
                print(len(mycomp))
                #mycomp['wtprice'] = mycomp['price']*mycomp['wt']
                maxprice = []
                maxsymbol = []
                prwt = []
                for mc in range (len(mycomp)):
                    mprice = mycomp['price'].iloc[mc]
                    curr = mycomp['currency'].iloc[mc]
                    if curr == 'GBX':
                        ccr = cc.cur_rate.get('GBP', None)
                        ccr=ccr * 100
                        #print("conversion rate of ",curr, " to EUR was ", ccr)
                    elif curr == 'ZAc':
                        ccr = cc.cur_rate.get('ZAR', None)
                        ccr = ccr * 100
                        #print("conversion rate of ",curr, " to EUR was ", ccr)
                    else:
                        ccr = cc.cur_rate.get(curr, None)
                        #print("conversion rate of ",curr, " to EUR was ", ccr)
                    if ccr is not None and mprice is not None:
                        eurprice = mprice/ccr
                    else:
                        print("ccr was null and therefore marking price in eur same as mprice for",mycomp['symbol'].iloc[mc])
                        eurprice = mprice
                    #print("price of stock ", mycomp['symbol'].iloc[mc], " was ", mprice, "in local currency and ",eurprice, "in euros" )
                    maxprice.append(eurprice)
                    maxsymbol.append(mycomp['symbol'].iloc[mc])
                    prwt.append(mycomp['wt'].iloc[mc])
                OPorid = 'O'+myret[0]
                insv = []
                insv.append(OPorid)
                insv.extend(myret)
                pos = maxprice.index(max(maxprice))
                prwt = prwt[pos]
                porsymbol = maxsymbol[pos]
                porprice = mt.ceil(maxprice[pos]/prwt)
                print("the max price of an individual symbol is",porprice, "for symbol ",porsymbol,"having weight",prwt)
                insv.append(porprice)
                insv.append('EUR')
                pdate = dt.datetime.today().date()
                pdate = pdate - dt.timedelta(days = 1)
                print("Loading Portfolio details for ",OPorid," as of ", pdate)
                print(insv)
                insvh = []
                insvh.extend(insv)
                insvh.append(pdate)
                # print(insvh)
                delp ="""delete from por_acutulus where portfolio_id=%s"""
                print("Purchase price of ", OPorid, "in euro per unit is:", porprice)
                try:
                    cursor.execute(delp,(OPorid,))
                    print("successful delete")
                except pgs.Error as e:
                    e.pgerror
                insp = """insert into por_acutulus
                (portfolio_id,idx_portfolio_id,mean,mkt_mean,stdp, mkt_stdp,beta, var95, var99, mkt_var95, mkt_var99,mkt_cap,price,currency)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
                insph = """insert into por_acutulus_history
                (portfolio_id,idx_portfolio_id,mean,mkt_mean,stdp, mkt_stdp,beta, var95, var99, mkt_var95, mkt_var99,mkt_cap,price,currency,price_date)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s) ON CONFLICT DO NOTHING"""
                try:
                    cursor.execute(insp,(insv))
                    cursor.execute(insph, (insvh))
                    print("successul addition of por_acutulus for:", OPorid)
                except pgs.Error as e:
                    print(e.pgerror)
                    print("Rejected entry of por_acutulus for:", OPorid)
                delcon = """delete from por_acutulus_const where portfolio_id=%s"""
                try:
                    cursor.execute(delcon,(OPorid,))
                    print("successful delete")
                except pgs.Error as e:
                    print(e.pgerror)
                if len(mycomp)>0:
                    for m in range (len(mycomp)):
                        symbol = mycomp['symbol'].iloc[m]
                        weight = mycomp['wt'].iloc[m]
                        exchange = mycomp['exch'].iloc[m]
                        inscon = """insert into dbo.por_acutulus_const
                        (portfolio_id, symbol,weight, exchange) values (%s, %s, %s, %s)"""
                        insconh = """insert into dbo.por_acutulus_const_history
                        (portfolio_id, symbol,weight, exchange, price_date) values (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING"""
                        try:
                            cursor.execute(inscon, (OPorid, symbol, weight, exchange))
                            cursor.execute(insconh, (OPorid, symbol, weight, exchange, pdate))
                        except pgs.Error as e:
                            print("couldn't insert index constituents for: ", OPorid)
                            e.pgerror
                    print("successul addition of", len(mycomp),"constituents for:", OPorid)
                else:
                    print("No constituents inserted for entry: ", OPorid)
            else:
                print("for the portfolio id ", kpor, " no combinations were found")


#FinalOptPortfolio()



