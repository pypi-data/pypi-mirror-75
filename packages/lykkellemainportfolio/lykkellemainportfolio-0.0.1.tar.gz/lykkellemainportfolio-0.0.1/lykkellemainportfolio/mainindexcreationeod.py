# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 01:25:13 2019
this program creates the custom benchmark portfolios of acutulus
this will be the starting point for optimal portfolio creation
@author: debaj
"""
from lykkelleportfolio.createportfolioeod import createportfolio
from lykkelleconf.connecteod import connect
from lykkelleconnector.fxconverteod import fxconvert
from os.path import expanduser

home = expanduser("~")
# pd.options.mode.chained_assignment = None


def acutulusbenchmarks():
    Lind = ['LCAP', 'MCAP', 'SCAP']
    stat_q = """select distinct st.symbol,st.industry,st.mean_annualized_return,st.mkt_mean_annualized_return,st.capm_return,
                        st.std_annualized,st.mkt_annualized_std,st.dividend_yield,st.price,st.currency,
                        st.mkt_cap_stocks_bill_eur,st.per,st.beta, st.source_table,
                        st.bmk_symbol as abbr
                    from dbo.stock_statistics st"""
    hst_q = """select symbol, count(*) as cnt from dbo.stock_history
                        where price_return is not null and price_return <>0 and symbol in %s"""
    hst_q2 = """ group by symbol"""
    mas_q = """select symbol, exchange from stock_master where symbol in %s"""
    conn = connect.create()
    cursor = conn.cursor()
    with conn:
        fxr = fxconvert(cursor)
        #all stocks - world
        porid = 'ACTWRLD'
        hst_cnt_ACTWRLD = " having count(*) > 252"
        stat_q_ACTWRLD = """ where st.ind_category=%s
                and (st.profit_margin>0 and st.profit_margin is not null
                and st.profitability_growth>0 and st.profitability_growth is not null)
                and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
                and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
                order by st.mkt_cap_stocks_bill_eur desc"""
        hqry = hst_q + hst_q2 + hst_cnt_ACTWRLD
        qry = stat_q + stat_q_ACTWRLD
        for i in range(len(Lind)):
            createportfolio.createportfoliopd(porid, Lind[i], qry, hqry, mas_q, fxr, cursor)
    # large cap AAA and AA
        porid2 = "ACTHGPRM"
        hst_cnt_ACTHGPRM = " having count(*) > 252"
        stat_q_ACTHGPRM =""" join benchmark_All exch on 
                        st.bmk_symbol = exch.symbol 
                        where st.ind_category=%s 
                        and left(exch.rating,2)='AA'
                        and (st.profit_margin>0 and st.profit_margin is not null
                        and st.profitability_growth>0 and st.profitability_growth is not null)
                        and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
                        and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
                        order by st.mkt_cap_stocks_bill_eur desc"""
        hqry2 = hst_q + hst_q2 + hst_cnt_ACTHGPRM
        qry2 = stat_q + stat_q_ACTHGPRM
        for i in range(len(Lind)):
            createportfolio.createportfoliopd(porid2, Lind[i], qry2, hqry2, mas_q, fxr, cursor)
    # large cap NA and Europe
    porid3 = "ACTNAEU"
    hst_cnt_ACTNAEU= " having count(*) > 252"
    stat_q_ACTNAEU = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and (exch.region='Europe' or exch.region='NAmerica')
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry3 = hst_q + hst_q2 + hst_cnt_ACTNAEU
    qry3 = stat_q + stat_q_ACTNAEU
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid3, Lind[i], qry3, hqry3, mas_q, fxr, cursor)
    # Portfolio with UM and LM rating
    porid4 = "ACTUMLM"
    hst_cnt_ACTUMLM = " having count(*) > 252"
    stat_q_ACTUMLM = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and (right(exch.mkt_type,8)='UM Grade' or left(exch.rating,3)='BBB')
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry4 = hst_q + hst_q2 + hst_cnt_ACTUMLM
    qry4 = stat_q + stat_q_ACTUMLM
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid4, Lind[i], qry4, hqry4, mas_q, fxr, cursor)
    # Portfolio for asian stocks
    porid5 = "ACTASIA"
    hst_cnt_ACTASIA = " having count(*) > 252"
    stat_q_ACTASIA = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and exch.region='Asia'
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry5 = hst_q + hst_q2 + hst_cnt_ACTASIA
    qry5 = stat_q + stat_q_ACTASIA
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid5, Lind[i], qry5, hqry5, mas_q, fxr, cursor)
    # portfolio for oceania stocks
    porid6 = "ACTOC"
    hst_cnt_ACTOC = " having count(*) > 252"
    stat_q_ACTOC = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and exch.region='Oceania'
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry6 = hst_q + hst_q2 + hst_cnt_ACTOC
    qry6 = stat_q + stat_q_ACTOC
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid6, Lind[i], qry6, hqry6, mas_q, fxr, cursor)
    #portfolio for north american stocks
    porid7 = "ACTNA"
    hst_cnt_ACTNA = " having count(*) > 252"
    stat_q_ACTNA = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and exch.region='NAmerica'
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry7 = hst_q + hst_q2 + hst_cnt_ACTNA
    qry7 = stat_q + stat_q_ACTNA
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid7, Lind[i], qry7, hqry7, mas_q, fxr, cursor)
    #portfolio of south american stocks
    porid8 = "ACTSA"
    hst_cnt_ACTSA = " having count(*) > 252"
    stat_q_ACTSA = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and exch.region='SAmerica'
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry8 = hst_q + hst_q2 + hst_cnt_ACTSA
    qry8 = stat_q + stat_q_ACTSA
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid8, Lind[i], qry8, hqry8, mas_q, fxr, cursor)
    #portfolio of HY stocks
    porid9 = "ACTHY"
    hst_cnt_ACTHY = " having count(*) > 252"
    stat_q_ACTHY = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and left(exch.rating,1)!='A' and left(exch.rating,3)!='BBB'
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry9 = hst_q + hst_q2 + hst_cnt_ACTHY
    qry9 = stat_q + stat_q_ACTHY
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid9, Lind[i], qry9, hqry9, mas_q, fxr, cursor)
    #portfolio of European stocks
    porid10='ACTEU'
    hst_cnt_ACTEU = " having count(*) > 252"
    stat_q_ACTEU = """ join benchmark_All exch on 
            st.bmk_symbol = exch.symbol
            where st.ind_category=%s
            and exch.region='Europe'
            and (st.profit_margin>0 and st.profit_margin is not null
            and st.profitability_growth>0 and st.profitability_growth is not null)
            and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
            and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
            order by st.mkt_cap_stocks_bill_eur desc"""
    hqry10 = hst_q + hst_q2 + hst_cnt_ACTEU
    qry10 = stat_q + stat_q_ACTEU
    for i in range(len(Lind)):
        createportfolio.createportfoliopd(porid10, Lind[i], qry10, hqry10, mas_q, fxr, cursor)
    #Portfolio of under valued stocks
    porid11 = 'ACTUVWRLD'
    hst_cnt_ACTUVWRLD = " having count(*) > 252"
    stat_q_ACTUVWRLD = """  join stock_master mas on 
                    st.symbol=mas.symbol
        where st.mean_annualized_return>st.mkt_mean_annualized_return
        and st.std_annualized < 0.30
        and st.dividend_yield>0.02
        and (st.profit_margin>0 and st.profit_margin is not null
        and st.profitability_growth>0 and st.profitability_growth is not null)
        and mas.exdivdate between current_date + 1 and current_date+91
        and st.debt_2_equity<100"""
    hqry11 = hst_q + hst_q2 + hst_cnt_ACTUVWRLD
    qry11 = stat_q + stat_q_ACTUVWRLD
    createportfolio.createportfoliopd(porid11, 'ZZZ', qry11, hqry11, mas_q, fxr, cursor)
    #portfolio selection of large medium cap under valued stocks
    porid12 = 'ACTUVWRLDLM'
    hst_cnt_ACTUVWRLDLM = " having count(*) > 252"
    stat_q_ACTUVWRLDLM = """ join stock_master mas on 
        st.symbol=mas.symbol
        where st.mean_annualized_return>st.mkt_mean_annualized_return
        and st.std_annualized < 0.30
        and st.dividend_yield>0.02
        and (st.profit_margin>0 and st.profit_margin is not null
        and st.profitability_growth>0 and st.profitability_growth is not null)
        and mas.exdivdate between current_date + 1 and current_date+91
        and st.debt_2_equity<100
        and st.ind_category<>'SCAP'"""
    hqry12 = hst_q + hst_q2 + hst_cnt_ACTUVWRLDLM
    qry12 = stat_q + stat_q_ACTUVWRLDLM
    createportfolio.createportfoliopd(porid12, 'ZZZ', qry12, hqry12, mas_q, fxr, cursor)
    # portfolio of dividend paying stocks
    porid13 = 'ACTDIVWRLD'
    hst_cnt_ACTDIVWRLD = " having count(*) > 252"
    stat_q_ACTDIVWRLD =""" join stock_master mas on 
                    st.symbol=mas.symbol
        where exdivdate between current_date+1 and current_date + 91
        and dividend>0.03 and st.debt_2_equity<100 and per_mkt>0
        and st.profitability_growth>0
        and st.mean_annualized_return>st.mkt_mean_annualized_return"""
    hqry13 = hst_q + hst_q2 + hst_cnt_ACTDIVWRLD
    qry13 = stat_q + stat_q_ACTDIVWRLD
    createportfolio.createportfoliopd(porid13, 'ZZZ', qry13, hqry13, mas_q, fxr, cursor)
    # portfolio of world's companies that pay >1% dividend
    porid14 = "ACTWRLDALL"
    hst_cnt_ACTWRLDALL = " having count(*) > 252"
    stat_q_ACTWRLDALL = """ join stock_master mas on 
                    st.symbol=mas.symbol
                    where st.debt_2_equity<100 and per_mkt>0 and
                    (st.profit_margin>0 and st.profit_margin is not null
                    and st.profitability_growth>0 and st.profitability_growth is not null)
                    and mas.dividend>0.01
                    and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
                    and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
                    order by st.mkt_cap_stocks_bill_eur desc"""
    hqry14 = hst_q + hst_q2 + hst_cnt_ACTWRLDALL
    qry14 = stat_q + stat_q_ACTWRLDALL
    createportfolio.createportfoliopd(porid14, 'ZZZ', qry14, hqry14, mas_q, fxr, cursor)
    #portfolio of all of world's low risk companies
    porid15 = "ACTWRLDLRALL"
    hst_cnt_ACTWRLDLRALL = " having count(*) > 252"
    stat_q_ACTWRLDLRALL = """ join stock_master mas on 
                    st.symbol=mas.symbol
                    where st.debt_2_equity<100 and per_mkt>0 and
                    (st.profit_margin>0 and st.profit_margin is not null
                    and st.profitability_growth>0 and st.profitability_growth is not null)
                    and st.mean_annualized_return > st.mkt_mean_annualized_return
                    and st.std_annualized<st.mkt_annualized_std
                    and st.price is not null and st.mkt_cap_stocks_bill_eur is not null and st.currency is not null
                    and st.mean_annualized_return is not null and st.mkt_mean_annualized_return is not null
                    order by st.mkt_cap_stocks_bill_eur desc"""
    hqry15 = hst_q + hst_q2 + hst_cnt_ACTWRLDLRALL
    qry15 = stat_q + stat_q_ACTWRLDLRALL
    createportfolio.createportfoliopd(porid15, 'ZZZ', qry15, hqry15, mas_q, fxr, cursor)
    #portfolio of companies that give a higher return than industry
    porid16 = "ACTWRLDIND"
    hst_cnt_ACTWRLDIND = " having count(*) > 252"
    stat_q_ACTWRLDIND = """   join stock_master mas
                    on st.symbol=mas.symbol
                    join ind_acutulus i on
                i.industry_id=concat(replace(st.industry,' ',''),'_',st.currency)
                and st.mean_annualized_return>i.mean and st.std_annualized<i.stdp
                order by st.mkt_cap_stocks_bill_eur desc"""
    hqry16 = hst_q + hst_q2 + hst_cnt_ACTWRLDIND
    qry16 = stat_q + stat_q_ACTWRLDIND
    createportfolio.createportfoliopd(porid16, 'ZZZ', qry16, hqry16, mas_q, fxr, cursor)

#acutulusbenchmarks()



