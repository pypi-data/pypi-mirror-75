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
                fetch first 5 rows only"""
        else:
            sqlafrica = """select distinct m.symbol,b.prio from stock_master m join stock_all a 
                        on m.symbol = a.symbol join benchmark_all b on a.index_code=b.symbol
                        """
        if param == 'T':
            sqlafricab = """select distinct b.symbol,ba.prio from benchmark_master b join
                benchmark_all ba on b.symbol=ba.symbol fetch first 5 rows only"""
        else:
            sqlafricab = """select distinct b.symbol,ba.prio from benchmark_master b join
                        benchmark_all ba on b.symbol=ba.symbol"""
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            cursor.execute(sqlafrica)
            results = cursor.fetchall()
            # print(results)
            if len(results)>0:
                for i in range(len(results)):
                    symbol = results[i][0]
                    exceptions(symbol, cursor, 'S')
            else:
                print("For all run, no stocks were found between prio 1 to 6")
            cursor.execute(sqlafricab)
            resultsb = cursor.fetchall()
            # print(resultsb)
            if len(resultsb)>0:
                for i in range(len(resultsb)):
                    symbol = resultsb[i][0]
                    exceptions(symbol, cursor, 'B')
            else:
                print("For all run, no benchmarks were found with between prio 1 to 6")

#exceptionlog()


