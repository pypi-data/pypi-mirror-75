# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 17:29:35 2019
You need a dataframe with the following fields to get the result:
    st.symbol,st.mean_annualized_return,st.std_annualized,st.beta, st.dividend_yield, st.mkt_cap_stocks_bill_eur,
    sh.cnt as scnt, bh.cnt as bcnt,const.exch, st.mkt_mean_annualized_return

#st - stock_statistics, sh - stock_history, bh - benchmark_history, const - index_acutulus_const
@author: debaj
"""

from lykkelleconf.connecteod import connect
import pandas as pd
import numpy as np
import psycopg2 as pgs

keympor = ['ACTWRLDSCAP', 'ACTWRLDMCAP', 'ACTWRLDLCAP', 'ACTUMLMSCAP',
               'ACTUMLMMCAP', 'ACTUMLMLCAP', 'ACTSASCAP', 'ACTSAMCAP',
               'ACTOCSCAP', 'ACTOCMCAP', 'ACTNASCAP', 'ACTNAMCAP',
               'ACTNALCAP', 'ACTNAEUSCAP', 'ACTNAEUMCAP',
               'ACTNAEULCAP', 'ACTHYSCAP', 'ACTHYMCAP',
               'ACTHGPRMSCAP', 'ACTHGPRMMCAP', 'ACTHGPRMLCAP',
               'ACTASIASCAP', 'ACTASIAMCAP', 'ACTASIALCAP', 'ACTSALCAP', 'ACTOCLCAP', 'ACTHYLCAP']
valmpor = [25, 25, 25, 10, 10 , 10, 10, 10, 10, 10, 10, 10 , 10, 15, 15, 15, 10, 10, 15, 15, 15, 10, 10, 10, 10, 10, 10]
dictpor = dict(zip(keympor, valmpor))
# 'symbol','mean','beta','divy','Mcapeur','scnt','mcnt', 'exch', 'porid'
class LoadOptPortfolio:
    def __init__(self, Pordf, Por):
        # LCAP world - Find out whats the return if this is used as an index
        self.Pordf = Pordf
        self.Por = Por
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            lstins = []
            # the data frame is passed
            symwdf = self.Pordf
            print("length of original portfolio:", len(symwdf))
            total = symwdf['Mcapeur'].sum()
            symwdf['wt'] = symwdf['Mcapeur']/total
            symwdf['wtmean'] = symwdf['mean'] * symwdf['wt']
            symwdf['wtmmean'] = symwdf['mmean'] * symwdf['wt']
            symwdf['wtbeta'] = symwdf['beta'] * symwdf['wt']
            # using variance - covariance matrix finding out variance of benchmark
            # print("order of stocks for verification:", symwdf['symbol'].values)
            minh = symwdf['scnt'].min()
            # print("minimum observation used for covariance calculation:",minh)
            nsymc = np.array([])
            for i in range(len(symwdf)):
                sym = symwdf['symbol'].iloc[i]
                selq = "select price_return from stock_history where symbol=%s and (price_return is not null and price_return <> 0) order by price_date desc"
                try:
                    cursor.execute(selq, (sym, ))
                    symres = cursor.fetchall()
                except pgs.Error as e:
                    print ("connection error for ", sym)
                    print(e.pgerror)
                nsym = np. array(symres)
                nsym = nsym[:minh]
                if i == 0:
                    nsymc = nsym
                else:
                    nsymc = np.append(nsymc, nsym, axis =1)
    #calculation for market - those that are in the current portfolio
            minb = symwdf['mcnt'].min()
            # print("minimum observation used for mkt covariance calculation:",minb)
            nbsymc = np.array([])
            for i in range(len(symwdf)):
                    msym = symwdf['exch'].iloc[i]
                    if minb !=0:
                        selmq = "select price_return from benchmark_history where symbol=%s and (price_return is not null or price_return <> 0) order by price_date desc"
                        try:
                            cursor.execute(selmq, (msym, ))
                            symbres = cursor.fetchall()
                        except pgs.Error as e:
                            print ("connection error for ", msym)
                            print(e.pgerror)
                        nbsym = np. array(symbres)
                        nbsym = nbsym[:minb]
                        if i == 0:
                            nbsymc = nbsym
                        else:
                            nbsymc = np.append(nbsymc, nbsym, axis =1)
                    else:
                        mm = symwdf['mcnt'] == 0
                        mmsym = symwdf[mm]
                        print("list of stocks where mkt count returned zero is:\n")
                        print(mmsym[['symbol','exch','mcnt']])
    # final covariance matrix creation for both stock portfolio
            nsymr = np.reshape(nsymc,(nsymc.shape[1], nsymc.shape[0]))
            nsymr = nsymr.astype('float64')
            # print("shape of input array for calculating stock cov. matrix:", nsymr.shape)
            covmat = np.cov(nsymr)
            # print("shape of stock covariance matrix:",covmat.shape)
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
            var95 = -(1.65 * stdpa) #removed mean
            var99 = -(2.33 * stdpa) # removed mean
            # using variance - covariance matrix find out ideal std for market index of this portfolio
            nbsymr = np.reshape(nbsymc,(nbsymc.shape[1], nbsymc.shape[0]))
            nbsymr = nbsymr.astype('float64')
            # print("shape of input array for calculating stock cov. matrix:", nbsymr.shape)
            covmatm = np.cov(nbsymr)
            # print("shape of covariance matrix:",covmatm.shape)
            varmp = np.dot(np.dot(wtc, covmatm),wtr)
            mstdp = np.sqrt(varmp[0][0])
            mstdpa = np.sqrt(252) * mstdp
            mvar95 = -(1.65 * mstdpa) #removed mkt_mean
            mvar99 = -(2.33 * mstdpa) #removed mkt_mean
            totalmc = symwdf['Mcapeur'].sum()
        self.finaldf = symwdf[['symbol','wt','SD','exch','price','currency']]
        # sprint(symwdf[['symbol','wt']])
    # uploading to the tables
        PorID = self.Por
        lstins = [PorID, mean,mkt_mean,stdpa, mstdpa,beta, var95, var99, mvar95, mvar99,totalmc]
        self.lstins = lstins

class calcOptPortfolio:
    def __init__(self, myseldf, mytop, mybottom, lenkpor, kpor):
       # print(myseldf['symbol'])
        # print("size of bottom selection:", len(mybottom))
        # print(mybottom)
        mybottom = list(mybottom)
        myos = myseldf['symbol'].isin(mytop)
        osdf = myseldf[myos]
        print("original")
        print(len(osdf))
        myopt = LoadOptPortfolio(osdf, kpor)
        myoptreturn = myopt.lstins
        osdf = None
        osdf = myseldf[myos]
        # PorID, mean,mkt_mean,stdpa, mstdpa,beta, var95, var99, mvar95, mvar99
        mean = myoptreturn[1]
        std = myoptreturn[3]
        print("original return mean, std:",mean, std)
        itr = 0
        ilst = []
        dlst = []
        while len(mybottom)>0:
            #print(mybottom)
            osdf = None
            osdf = myseldf[myos]
            #print("iteration-",itr+1)
            maxsd = osdf.sort_values(['SD'], ascending = 0).iloc[0]
            maxsd = maxsd['symbol']
            osm = osdf['symbol']==maxsd
            myros = osdf[osm]
            myros = myros['symbol'].values
            myros = myros[0]
            #print("replacing ",myros, "with ", mybottom[0])
            ns = myseldf['symbol']==mybottom[0]
            myaos = myseldf[ns]
            mynos = osdf
            mynos = mynos.append(myaos, ignore_index = True)
            rmv = mynos['symbol']!=myros
            mynos = mynos[rmv]
            print("intermediate")
            print(len(mynos))
            myir = LoadOptPortfolio(mynos, kpor)
            myireturn = myir.lstins
            imean = myireturn[1]
            istd = myireturn[3]
            print("intermediate return mean, std:",imean, istd)
            # checking if this iteration is better or worse than first one
            if istd < std:
                mdelta = (imean/mean)-1
                sdelta = (istd/std) - 1
                print("new combination better:isd-std",istd,"-",std)
                if mdelta > 0 and sdelta < 0:
                    #print("change in mean:",mdelta, "change in std:",sdelta, "difference in change:",mdelta - sdelta)
                    d = mdelta - sdelta
                    ilst.append([mybottom[0],d])
                    # print("successful upgrade with:",mybottom[0])
                    mybottom.pop(0)
                elif mdelta < 0 and sdelta < 0 and (abs(sdelta)-abs(mdelta))>0:
                    #print("change in mean:",mdelta, "change in std:",sdelta, "difference in change:",abs(sdelta) - abs(mdelta))
                    d = abs(sdelta) - abs(mdelta)
                    ilst.append([mybottom[0],d])
                    # print("successful upgrade with:",mybottom[0])
                    mybottom.pop(0)
                else:
                    print("std change less than mean change ignoring iteration:",itr+1," with stock ", mybottom[0])
                    dlst.append(mybottom[0])
                    mybottom.pop(0)
            else:
                print("the new std is greater than old one. ignoring iteration:", itr+1, " with stock ",mybottom[0])
                dlst.append(mybottom[0])
                mybottom.pop(0)
            itr = itr+1
        if len(ilst)> 0:
            ilst = pd.DataFrame(ilst, columns = ['symbol','delta'])
            osdf = None
            osdf = myseldf[myos]
            md = ilst.sort_values(['delta'], ascending = 0).iloc[0]
            md = md['symbol']
            maxsd = osdf.sort_values(['SD'], ascending = 0).iloc[0]
            maxsd = maxsd['symbol']
            osm = osdf['symbol']==maxsd
            myros = osdf[osm]
            myfros = myros['symbol'].values[0]
            print("replacing ",myfros, "with ", md, "for optimal portfolio")
            ns = myseldf['symbol']==md
            myaos = myseldf[ns]
            fosdf = pd.concat([myaos,osdf], ignore_index=True)
            rmv = fosdf['symbol']!=myfros
            fosdf = fosdf[rmv]
            print("final")
            print(len(fosdf))
            myf = LoadOptPortfolio(fosdf, kpor)
            myfreturn = myf.lstins
            print("the statistics for final and original are below:\n")
            print(myfreturn)
            print(myoptreturn)
            bestdf = myf.finaldf
            # print(myf.finaldf.head(30))
        else:
            print("No better combination than the original")
            myfreturn = myoptreturn
            bestdf = myopt.finaldf
            myfros = dlst
        self.bestdf = bestdf
        self.bret = myfreturn
        self.oret = myoptreturn
        self.myros = myfros
            # print(myopt.finaldf.head(30))


class bestpor:
    def __init__(self, myseldf, kpor, mytop, mybottom, lenkpor):
        print("selecting ", len(mytop), " stocks out of", lenkpor, "for portfoloo:", kpor)
        maxsdf = myseldf.loc[myseldf['symbol'].isin(mytop)]
        maxsd = maxsdf.sort_values(['SD'], ascending = 0).iloc[0]
        print("highest SD of the selection:",maxsd['SD'])
        sdlist = myseldf.loc[myseldf['symbol'].isin(mybottom)]
        sdlist = sdlist.loc[sdlist['SD']<maxsd['SD']]
        # print("list of symbols that have a Std < initial portfolios's max std\n", sdlist[['symbol','SD']])
        mybottom = sdlist['symbol'].values
        if len(mybottom)>0:
            mydf = calcOptPortfolio(myseldf, mytop, mybottom, lenkpor, kpor)
            self.bestdf = mydf.bestdf
            self. bret = mydf.bret
            self.oret = mydf.oret
            self.mdel = mydf.myros
            self.close = 0
        else:
            myfdf = LoadOptPortfolio(maxsdf, kpor)
            self.bestdf = myfdf.finaldf
            self. bret = myfdf.lstins
            print("No remaining symbols have std < max std of current portfolio. So this will be the only optimization")
            self.close = 1