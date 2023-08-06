#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:47:59 2019
daily checklist that runs a health check on the load details
@author: debaj
"""
from lykkelleconf.connecteod import connect
from os.path import expanduser
from lykkelledatahandler.exception import exceptions

home = expanduser("~")


class exceptionlog:
    def __init__(self, param):
        if param == 'T':
            sqlafrica = """select distinct m.symbol,b.prio from stock_master m join stock_all a 
                on m.symbol = a.symbol join benchmark_all b on a.index_code=b.symbol
                where b.prio=2 and b.symbol<>'TA100.INDX' fetch first 5 rows only"""
            sqlafricab = """select distinct b.symbol,ba.prio from benchmark_master b join
                benchmark_all ba on b.symbol=ba.symbol where ba.prio=2 and b.symbol<>'TA100.INDX'
                fetch first 5 rows only"""
        else:
            sqlafrica = """select distinct m.symbol,b.prio from stock_master m join stock_all a 
                on m.symbol = a.symbol join benchmark_all b on a.index_code=b.symbol
                where b.prio=2 and b.symbol<>'TA100.INDX'"""
            sqlafricab = """select distinct b.symbol,ba.prio from benchmark_master b join
                benchmark_all ba on b.symbol=ba.symbol where ba.prio=2 and b.symbol<>'TA100.INDX'"""
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            cursor.execute(sqlafrica)
            results = cursor.fetchall()
            #print(results)
            if len(results)>0:
                for i in range(len(results)):
                    symbol = results[i][0]
                    exceptions(symbol, cursor, 'S')
            else:
                print("For africa run, no stocks were found with prio=2")
            cursor.execute(sqlafricab)
            resultsb = cursor.fetchall()
            #print(resultsb)
            if len(resultsb)>0:
                for i in range(len(resultsb)):
                    symbol = resultsb[i][0]
                    exceptions(symbol, cursor, 'B')
            else:
                print("For africa run, no benchmarks were found with prio=2")

#exceptionlog()

