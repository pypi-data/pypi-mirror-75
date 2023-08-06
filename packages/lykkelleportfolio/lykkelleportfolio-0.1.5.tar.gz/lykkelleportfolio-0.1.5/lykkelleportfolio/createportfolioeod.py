# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 13:38:33 2019
create a program that identifies the
bet combination of portfolio based on the following:
    best mean return +div_yield
    for:
        beta < 1.1
        SD < .15
        weighted capm > weighted mkt return
    for the the following:

@author: debaj
"""
from lykkelleconf.connecteod import connect
import pandas as pd
import numpy as np
import psycopg2 as pgs
import datetime as dt
import math as m

pd.options.mode.chained_assignment = None

class createportfolio:
    def createportfoliopd(porid, lind, qry, hqry, mas_q, fxr, cursor):
        if lind != 'ZZZ':
            Port = porid + lind
            cursor.execute(qry, (lind,))
        else:
            Port = porid
            cursor.execute(qry)
        v = cursor.fetchall()
        ACTWRLDPD_stat = pd.DataFrame(v, columns=['symbol', 'industry', 'mean', 'mkt_mean',
                                                  'capm', 'SD', 'mkt_SD', 'div_y', 'price', 'currency',
                                                  'Mcapeur', 'per', 'beta', 'src', 'abbr'])
        symlist = ACTWRLDPD_stat['symbol'].values
        symlist = tuple(symlist)
        if len(symlist)>0:
            cursor.execute(hqry, (symlist,))
            v = cursor.fetchall()
            ACTWRLDPD_hst = pd.DataFrame(v, columns=['symbol', 'count'])
            cursor.execute(mas_q, (symlist,))
            v = cursor.fetchall()
            ACTWRLDPD_mas = pd.DataFrame(v, columns=['symbol', 'exchange'])
            ACTWRLDPD = pd.merge(left=ACTWRLDPD_stat, right=ACTWRLDPD_hst, left_on='symbol', right_on='symbol')
            ACTWRLDPD = pd.merge(left=ACTWRLDPD, right=ACTWRLDPD_mas, left_on='symbol', right_on='symbol')
            if len(ACTWRLDPD) > 0:
                createportfolio(Port, ACTWRLDPD, fxr, cursor)
            else:
                print(Port, "resulted in zero output in the dataframe. Check the tables")
        else:
            print(Port, "had zero stocks part of it's initial statistics query output")

    def __init__(self, Port, symwdf, fxr, cursor):
        # LCAP world - Find out whats the return if this is used as an index
        print("Passing PorID:", Port)
        if len(symwdf)!=0:
            total = symwdf['Mcapeur'].sum()
            symwdf['wt'] = symwdf['Mcapeur']/total
            symwdf['wtmean'] = symwdf['mean'] * symwdf['wt']
            symwdf['wtmmean'] = symwdf['mkt_mean'] * symwdf['wt']
            symwdf['wtbeta'] = symwdf['beta'] * symwdf['wt']
            symwdf['wtcapm'] = symwdf['capm'] * symwdf['wt']
            # symwdf['wtprice'] = symwdf['price']* symwdf['wt']
            cc = fxr
            maxprice = []
            maxsymbol =[]
            prwt = []
            # using variance - covariance matrix finding out variance of benchmark
            length = len(symwdf)
            print("Number of stocks:", length)
            print("order of stocks for verification:", symwdf['symbol'].values)
            minh = symwdf['count'].min()
            print("minimum observation used for covariance calculation:",minh)
            nsymc = np.array([])
            symwdf['msymbol'] = ""
            symwdf['mcnt'] = 0
            for i in range(length):
                sym = symwdf['symbol'].iloc[i]
                curr = symwdf['currency'].iloc[i]
                abbr = symwdf['abbr'].iloc[i]
                src = symwdf['src'].iloc[i]
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
                mprice = symwdf['price'].iloc[i]
                if mprice is not None and ccr is not None:
                    eurprice = symwdf['price'].iloc[i]/ccr
                else:
                    print("ccr was null and therefore marking price in eur same as mprice for",sym)
                    eurprice = mprice
                #print("price of stock ", symwdf['symbol'].iloc[i], " was ", symwdf['price'].iloc[i], "in local currency and ",eurprice, "in euros" )
                maxprice.append(eurprice)
                maxsymbol.append(sym)
                prwt.append(symwdf['wt'].iloc[i])
                try:
                    msymbol = abbr
                    symwdf['msymbol'].iloc[i] = msymbol
                    selc = "select count(*) from benchmark_history where symbol=%s and (price_return is not null and price_return <> 0)"
                    cursor.execute(selc, (msymbol, ))
                    mc = cursor.fetchone()
                    symwdf['mcnt'].iloc[i] = mc[0]
                except TypeError:
                    print(abbr, " was the response from stock exchanges for ", sym)
                    msymbol = None
                selq = "select price_return from stock_history where symbol=%s and (price_return is not null and price_return <> 0) order by price_date desc"
                cursor.execute(selq, (sym, ))
                symres = cursor.fetchall()
                nsym = np. array(symres)
                nsym = nsym[:minh]
                if i == 0:
                    nsymc = nsym
                else:
                    nsymc = np.append(nsymc, nsym, axis =1)
            #calculation for market - those that are in the current portfolio
            minb = symwdf['mcnt'].min()
            print("minimum observation used for mkt covariance calculation:",minb)
            mm = symwdf['mcnt'] == 0
            mmdf = symwdf[mm]
            nbsymc = np.array([])
            mlength = len(symwdf['msymbol'])
            for i in range(mlength):
                    msym = symwdf['msymbol'].iloc[i]
                    MktC = 'T'
                    if msymbol is not None and minb !=0:
                        selmq = "select price_return from benchmark_history where symbol=%s and (price_return is not null or price_return <> 0) order by price_date desc"
                        cursor.execute(selmq, (msym, ))
                        symbres = cursor.fetchall()
                        nbsym = np. array(symbres)
                        nbsym = nbsym[:minb]
                        if i == 0:
                            nbsymc = nbsym
                        else:
                            nbsymc = np.append(nbsymc, nbsym, axis =1)
                    else:
                        MktC = 'F'
            # final covariance matrix creation for both stock portfolio
            nsymr = np.reshape(nsymc,(nsymc.shape[1], nsymc.shape[0]))
            nsymr = nsymr.astype('float64')
            print("shape of input array for calculating cov. matrix:", nsymr.shape)
            covmat = np.cov(nsymr)
            print("shape of covariance matrix:",covmat.shape)
             # the weight product matrix to get portfolio SD
            wtr = symwdf['wt'].values
            wtr = np.reshape(wtr, (wtr.shape[0], -1))
            wtc = np.reshape(wtr, (-1, wtr.shape[0]))
            varp = np.dot(np.dot(wtc, covmat),wtr)
            stdp = np.sqrt(varp[0][0])
            stdpa = np.sqrt(252) * stdp
            mean = symwdf['wtmean'].sum()
            mkt_mean = symwdf['wtmmean'].sum()
            beta = symwdf['wtbeta'].sum()
            capm = symwdf['wtcapm'].sum()
            var95 = -(1.65 * stdpa) #removed mean
            var99 = -(2.33 * stdpa) #removed mean
            totalmc = symwdf['Mcapeur'].sum()
            # using variance - covariance matrix find out ideal std for market index of this portfolio
            if MktC == 'T':
                nbsymr = np.reshape(nbsymc,(nbsymc.shape[1], nbsymc.shape[0]))
                nbsymr = nbsymr.astype('float64')
                covmatm = np.cov(nbsymr)
                print("shape of covariance matrix:",covmatm.shape)
                varmp = np.dot(np.dot(wtc, covmatm),wtr)
                mstdp = np.sqrt(varmp[0][0])
                mstdpa = np.sqrt(252) * mstdp
                mvar95 = -(1.65 * mstdpa) #removed mkt_mean
                mvar99 = -(2.33 * mstdpa) #removed mkt_mean
            else:
                mstdpa = None
                mvar95 = None
                mvar99 = None
                print("For Portfolio ",Port,", the market statistics are None as the covariance matrix couldn't be formed")
                print("missing index:\n",mmdf.values)
            # uploading to the tables
            print("maximum price in portfolio:",Port, " is",max(maxprice))
            pos = maxprice.index(max(maxprice))
            prwt = prwt[pos]
            porsymbol = maxsymbol[pos]
            porprice = m.ceil(maxprice[pos]/prwt)
            print("the max price of an individual symbol is",porprice, "for symbol ",porsymbol,"having weight",prwt)
            PorID = Port
            lstins = [PorID, mean,mkt_mean,stdpa, mstdpa,beta, var95, var99, mvar95, mvar99,capm,porprice,'EUR', totalmc]
            print("Purchase price of ",PorID," is ",porprice," per unit in EURO")
            delpor = "delete from index_acutulus where Portfolio_Id=%s"
            inspor = """insert into index_acutulus
            (Portfolio_Id, mean, mkt_mean, stdp, mkt_stdp,
             beta, var95, var99, mkt_var95, mkt_var99, capm,price,currency,mkt_cap)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"""
            statusM = 'F'
            try:
                cursor.execute(delpor, (PorID, ))
                cursor.execute(inspor, lstins)
                statusM = 'S'
            except pgs.Error as e:
                print ("Unable to connect!")
                print (e.pgerror)
            c= 0
            delconst = "delete from index_acutulus_const where Portfolio_Id=%s"
            try:
                cursor.execute(delconst, (PorID, ))
            except pgs.Error as e:
                print ("Unable to connect!")
                print (e.pgerror)
            pdate = dt.datetime.today().date() - dt.timedelta(days = 1)
            for i in range (len(symwdf)):
                symbol = symwdf['symbol'].iloc[i]
                price = symwdf['price'].iloc[i]
                currency = symwdf['currency'].iloc[i]
                wt = symwdf['wt'].iloc[i]
                src = symwdf['src'].iloc[i]
                msym = symwdf['msymbol'].iloc[i]
                lstconst = [PorID, symbol, price, wt, currency, src, msym]
                lstconsth = [PorID, symbol, price, wt, currency, src, msym, pdate]
                insconst = """insert into index_acutulus_const
                (Portfolio_Id, symbol, price, weight, currency, source_table, exch)
                 values (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""
                insconsth = """insert into index_acutulus_const_history
                (Portfolio_Id, symbol, price, weight, currency, source_table, exch, price_Date)
                 values (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""
                statusC = 'F'
                 # print(lstconst)
                try:
                    cursor.execute(insconst, lstconst)
                    cursor.execute(insconsth, lstconsth)
                    statusC = 'S'
                    c = c+1
                except pgs.Error as e:
                    print ("Unable to connect!")
                    print (e.pgerror)
            print("missing index:\n",mmdf.values)
            lstins.append(pdate)
            print(lstins)
            # print(symwdf[['symbol','msymbol']])
            insporh = """insert into index_acutulus_history
                    (portfolio_id, mean, mkt_mean, stdp, mkt_stdp,
                     beta, var95, var99, mkt_var95, mkt_var99, capm,price,currency,mkt_cap, price_date)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s, %s)
                    ON CONFLICT (portfolio_id, price_date) DO UPDATE SET
                        mean = EXCLUDED.mean, mkt_mean=EXCLUDED.mkt_mean,
                        stdp=EXCLUDED.stdp, mkt_stdp = EXCLUDED.mkt_stdp,
                        beta=EXCLUDED.beta, var95 = EXCLUDED.var95,
                        var99=EXCLUDED.var99, mkt_var95 = EXCLUDED.mkt_var95,
                        capm=EXCLUDED.capm, mkt_var99 = EXCLUDED.mkt_var99,
                        price=EXCLUDED.price,currency=EXCLUDED.currency,
                        mkt_cap=EXCLUDED.mkt_cap"""
            statusH = 'F'
            try:
                cursor.execute(insporh, lstins)
                statusH = 'S'
            except pgs.Error as e:
                print ("Unable to connect!")
                print (e.pgerror)
            if statusM == 'S' and statusC =='S' and statusH =='S':
                print(PorID, " was successfully added to the index. check index_acutulus for details")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            elif statusM == 'S' and statusC != 'S' and statusH != 'S':
                print(PorID, " was successfully inserted in master but failed in history and constituents")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            elif statusM != 'S' and statusC == 'S' and statusH !='S':
                print(PorID, " was successfully inserted in conmstituents but failed in history and master")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            elif statusM != 'S' and statusC != 'S' and statusH =='S':
                print(PorID, " was successfully inserted in history but failed in master and constituents")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            elif statusM == 'S' and statusC == 'S' and statusH !='S':
                print(PorID, " was successfully inserted in master n constituents but failed in history")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            elif statusM == 'S' and statusC != 'S' and statusH =='S':
                print(PorID, " was successfully inserted in master and history but failed in constituents")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            elif statusM != 'S' and statusC == 'S' and statusH =='S':
                print(PorID, " was successfully inserted in constituent and history but failed in master")
                print(c, " out of ",len(symwdf), " constituents were loaded")
            else:
                print(PorID, " couldnt be loaded anywhere")
            # pd.set_option("display.max_rows", len(symwdf))
            # print(symwdf[['symbol','msymbol']])
        else:
            print("This particular Portfolio group", Port, "currently has no constituents")


