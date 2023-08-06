#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 15:58:16 2019

@author: debmishra
"""
#get stock data from EODhistoricaldata. can take upto 20 stocks at the same time
import requests as req
from requests.exceptions import HTTPError
import json


class geteodprice:
    bad_ticker=None
    no_response_ticker=None
    stock_Response = None
    status = None
    header = None
    def __init__(self, exch):
        mexch=exch+'?'
        url="http://eodhistoricaldata.com/api/eod-bulk-last-day/"+mexch
        params ={"api_token":"5d80cd89e4b201.98976318",
                 "fmt":"json",
             }
        try:
            response=req.get(url,params=params)
            status=response.status_code
            header = response.headers
        except ConnectionError:
            print("An HTTPError occured for the symbol:",exch,"Putting the ticker into bad ticker list")
            bad_ticker=exch
            status = 999
            self.bad_ticker = bad_ticker
            self.status = status
            self.header= header
        except Exception:
            print("An Connection occured for the symbol:",exch,"Putting the ticker into bad ticker list")
            bad_ticker=exch
            status = 999
            self.bad_ticker = bad_ticker
            self.status = status
            self.header= header
        if status==200:
            stock_Response=response.json()
            self.stock_Response = stock_Response
            self.status = 200
            self.header = header
            #print(type(stock_Response))
        else:
            print("Recieved response code was not 200 for ticker ",exch,"Putting the ticker to no_response_ticker list")
            no_response_ticker=exch
            status = 400
            self.no_response_ticker = no_response_ticker
            self.status= status
            self.header= header


class geteodbprice:
    bad_ticker=None
    no_response_ticker=None
    stock_Response = None
    status = None
    header = None
    def __init__(self, exch, jday):
        mexch=exch+'?'
        url="https://eodhistoricaldata.com/api/eod/"+mexch
        params ={"api_token":"5d80cd89e4b201.98976318",
                 "fmt":"json","period":"d",
                 "from":jday,"to":jday

             }
        try:
            response=req.get(url,params=params)
            status=response.status_code
            header = response.headers
        except ConnectionError:
            print("An HTTPError occured for the symbol:",exch,"Putting the ticker into bad ticker list")
            bad_ticker=exch
            status = 999
            self.bad_ticker = bad_ticker
            self.status = status
            self.header= header
        except Exception:
            print("An Connection occured for the symbol:",exch,"Putting the ticker into bad ticker list")
            bad_ticker=exch
            status = 999
            self.bad_ticker = bad_ticker
            self.status = status
            self.header= header
        if status==200:
            stock_Response=response.json()
            self.stock_Response = stock_Response
            self.status = 200
            self.header = header
            #print(type(stock_Response))
        else:
            print("Recieved response code was not 200 for ticker ",exch, '& date:',jday,"Putting the ticker to no_response_ticker list")
            no_response_ticker=exch
            status = 400
            self.no_response_ticker = no_response_ticker
            self.status= status
            self.header= header

class geteodhprice:
    stock_Response=None
    bad_ticker=None
    no_response_ticker=None
    sts = None
    header = None
    def __init__(self,mticker, fromdate, todate):
        ticker=mticker
        bad_ticker=None
        no_response_ticker=None
        url="https://eodhistoricaldata.com/api/eod/"+ticker
        params ={"api_token":"5d80cd89e4b201.98976318",
                 "fmt":"json","period":"d","from":fromdate,"to":todate
                }
        try:
            response=req.get(url,params=params)
            status=response.status_code
            header = response.headers
        except ConnectionError:
            print("An HTTPError occured for the symbol:",ticker,"Putting the ticker into bad ticker list")
            bad_ticker=ticker
            self.bad_ticker=bad_ticker
            status = 999
            self.header= header
        except Exception:
            print("An Connection occured for the symbol:",ticker,"Putting the ticker into bad ticker list")
            bad_ticker=ticker
            self.bad_ticker=bad_ticker
            status = 999
            self.header= header
        if status==200:
            stock_Response=response.json()
            self.stock_Response=stock_Response
            self.sts = 200
            self.header = header
            #print(type(stock_Response))
        else:
            print("Recieved response code was not 200 for ticker ",ticker,"Putting the ticker to no_response_ticker list")
            no_response_ticker=ticker
            self.no_response_ticker=no_response_ticker
            self.sts = 400
            self.header= header


class geteodfundamental:
    stock_Response=None
    bad_ticker=None
    no_response_ticker=None
    sts = None
    header = None
    def __init__(self,mticker):
        ticker=mticker
        bad_ticker=None
        no_response_ticker=None
        url="https://eodhistoricaldata.com/api/fundamentals/"+ticker
        params ={"api_token":"5d80cd89e4b201.98976318"
                }
        try:
            response=req.get(url,params=params)
            status=response.status_code
            header = response.headers
        except ConnectionError:
            print("An HTTPError occured for the symbol:",ticker,"Putting the ticker into bad ticker list")
            bad_ticker=ticker
            self.bad_ticker=bad_ticker
            status = 999
            self.header= header
        except Exception:
            print("An Connection occured for the symbol:",ticker,"Putting the ticker into bad ticker list")
            bad_ticker=ticker
            self.bad_ticker=bad_ticker
            status = 999
            self.header= header
        if status==200:
            stock_Response=response.json()
            self.stock_Response=stock_Response
            self.sts = 200
            self.header = header
            #print(type(stock_Response))
        else:
            print("Recieved response code was not 200 for ticker ",ticker,"Putting the ticker to no_response_ticker list")
            no_response_ticker=ticker
            self.no_response_ticker=no_response_ticker
            self.sts = 400
            self.header= header


class geteodidxconstituent:
    stock_Response=None
    bad_ticker=None
    no_response_ticker=None
    sts = None
    def __init__(self,mticker):
        ticker=mticker
        bad_ticker=None
        no_response_ticker=None
        url="https://eodhistoricaldata.com/api/fundamentals/"+ticker
        params ={"api_token":"5d80cd89e4b201.98976318"
                }
        try:
            response=req.get(url,params=params)
            status=response.status_code
        except ConnectionError:
            print("An HTTPError occured for the symbol:",ticker,"Putting the ticker into bad ticker list")
            bad_ticker=ticker
            self.bad_ticker=bad_ticker
            status = 999
        except Exception:
            print("An Connection occured for the symbol:",ticker,"Putting the ticker into bad ticker list")
            bad_ticker=ticker
            self.bad_ticker=bad_ticker
            status = 999
        if status==200:
            stock_Response=response.json()
            self.stock_Response=stock_Response
            self.sts = 200
            #print(type(stock_Response))
        else:
            print("Recieved response code was not 200 for ticker ",ticker,"Putting the ticker to no_response_ticker list")
            no_response_ticker=ticker
            self.no_response_ticker=no_response_ticker
            self.sts = 400
