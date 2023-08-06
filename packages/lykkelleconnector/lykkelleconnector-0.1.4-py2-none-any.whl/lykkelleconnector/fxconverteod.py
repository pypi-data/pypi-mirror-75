#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#tested successfully. ready to be deployed in prod
"""
Created on Wed Jul 10 23:35:00 2019

@author: debmishra
"""
import requests as req
import json as js
from lykkelleconf.connecteod import connect as c
import psycopg2 as pgs
import datetime as dt
from lykkelleconf.time2epoch2time import epochtime as tet
from lykkelleconf.workday import workday


class fxconvert:
    def __init__(self, cursor):
        pdate = dt.datetime.today()
        hr = dt.datetime.strftime(pdate,'%H')
        hr = int(hr)
        if hr < 11:
            pdate = dt.datetime.today().date()-dt.timedelta(days=1)
        else:
            pdate = dt.datetime.today().date()
        pdate = dt.datetime.strftime(pdate,'%Y-%m-%d')
        pdate = workday(pdate).sdate()
        #conn = c.create()
        #cursor = conn.cursor()
        #with conn:
        basecurr='EUR'
        currqry = """select distinct currency from
        ((select distinct currency from dbo.benchmark_All where currency is not null and currency<>'GLBL'
        union
        select distinct currency from ref_currency where is_active is true)
        except
        select currency from currency where currency_date>=%s) a
        """
        cur_rate = {}
        cnt = 0
        latestcurr = []
        stalecurr = []
        lcur = 1
        while lcur >0 and cnt < 3:
            try:
                cursor.execute(currqry,(pdate,))
                currlist = cursor.fetchall()
                lcur = len(currlist)
            except pgs.Error as e:
                print("the query to get currency list from system failed")
                print(e.pgerror)
                lcur = 0
            for i in range(lcur): #
                tgtcurr = currlist[i][0]
                currsym = basecurr + tgtcurr + '.FOREX'
            #print(mycurr)
                url="https://eodhistoricaldata.com/api/real-time/"+currsym
                params ={"api_token":"5d80cd89e4b201.98976318",
                         "fmt":"json"
                        }
                #print("Following are currency pairs being loaded with latest work date\n",tgtlist)
                response = req.request("GET", url, params=params)
                    #print(response.status_code)
                if response.status_code==200:
                    cnt = 4
                    quotedata = response.json()
                    print(type(quotedata))
                    if type(quotedata)==dict:
                        currpair = quotedata
                        curr = currpair.get('code')
                        tgtcurr = curr[3:6]
                        cd = currpair.get('timestamp')
                        currdate = tet.epoch2dateeod(cd)
                        curclose = currpair.get('close')
                        print(tgtcurr,currdate, curclose)
                        if currdate is None:
                            if curr=='EUREUR.FOREX':
                                tgtcurr= 'EUR'
                                curclose = 1
                                currdate = pdate
                                try:
                                    cq = """insert into dbo.currency (currency,rate,currency_date)
                                    values (%s,%s,%s) ON CONFLICT (currency, currency_date)
                                    DO UPDATE SET rate = EXCLUDED.rate"""
                                    cursor.execute(cq, (tgtcurr,curclose, currdate))
                                    print("successfully inserted ",tgtcurr,"to table on ", currdate)
                                    latestcurr.append(curr+":"+str(currdate)+":"+str(curclose))
                                except pgs.Error as e:
                                    print(e.pgerror)
                                    print("failed to load ",tgtcurr)
                                except ValueError:
                                    print(curr, " is not in list-",tgtlist)
                        elif currdate is not None and currdate >= pdate:
                            try:
                                cq = """insert into dbo.currency (currency,rate,currency_date)
                                values (%s,%s,%s) ON CONFLICT (currency, currency_date)
                                DO UPDATE SET rate = EXCLUDED.rate"""
                                cursor.execute(cq, (tgtcurr,curclose, currdate))
                                print("successfully inserted ",tgtcurr,"to table on ", currdate)
                                latestcurr.append(curr+":"+str(currdate)+":"+str(curclose))
                            except pgs.Error as e:
                                print(e.pgerror)
                                print("failed to load ",tgtcurr)
                        else:
                            print("Curr date turned out to be NULL for:",curr)
                    else:
                        print("Non-loadable output came as json\n",quotedata)
                        curr = tgtcurr
                        currdate = None
                        curclose = None
                else:
                    print("Error code not 200 for the batch")
                    cnt = cnt + 1
                if cnt==3:
                    print("No valid load after 5 attempts. Updating with yesterday's data")
                    lcq = """select rate from dbo.currency
                    where currency=%s
                    order by currency_date desc fetch first 1 rows only"""
                    try:
                        print("searching last known currency rate for ",tgtcurr)
                        cursor.execute(lcq, (tgtcurr,))
                        fxrate = cursor.fetchone()
                        if fxrate is not None:
                            fxrate = fxrate[0]
                        else:
                            print("cant find last currency value for ",tgtcurr," so defaulting to 1")
                            fxrate = 1
                    except pgs.Error as e:
                        print("cant find last currency value for ",tgtcurr," so defaulting to -99")
                        fxrate = -99
                    try:
                        cq = """insert into dbo.currency (currency,rate,currency_date)
                        values (%s,%s,%s) ON CONFLICT (currency, currency_date)
                        DO UPDATE SET rate = EXCLUDED.rate"""
                        cursor.execute(cq, (tgtcurr,fxrate, pdate))
                        print("successfully inserted ",tgtcurr,"to table on ", pdate)
                        stalecurr.append(tgtcurr+":"+str(pdate)+":"+str(fxrate))
                    except pgs.Error as e:
                        print(e.pgerror)
                        print("failed to load ",tgtcurr)
                else:
                    print("all currencies are updated with values >=",pdate)
            print("list of newly updated currencies\n",latestcurr)
            print("currencies whose current rate is overriden with last available rate\n",stalecurr)
            #creating a dictionary to store all currencies
            lc = """select currency, rate from (
                select currency,rate,currency_date,row_number()
                over (partition by currency order by currency_date desc) as rc
                from dbo.currency where currency_date>=%s
                order by currency_date desc) as lc
                where lc.rc=1"""
            try:
                cursor.execute(lc,(pdate,))
                cres = cursor.fetchall()
            except pgs.Error as e:
                print(e.pgerror)
                print("failure to fetch currencies for ",pdate)
            if cres is None:
                cres =[]
            else:
                pass
            if len(cres)>0:
                for i in range(len(cres)):
                    tcurr = cres[i][0]
                    trate = cres[i][1]
                    cur_rate.update({tcurr:trate})
            else:
                print("no currencies present in currency table for ",pdate)
            self.cur_rate = cur_rate
        print("postgresconnection closed")