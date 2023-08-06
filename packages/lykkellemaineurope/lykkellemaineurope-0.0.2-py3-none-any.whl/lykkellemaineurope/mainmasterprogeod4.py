#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 05 2019
Program to load all master data into the system.
This is the 2nd program to run in the sequence on weekend and 1st on weekdays
This program runs every weekday automatically
@author: debmishra
"""
from lykkelleconf.connecteod import connect
from lykkelleloader.loadstockeod import loadstockprice
from lykkelleloader.loadstockeod import loadstockfundamentals
import lykkelleconf.workday
import psycopg2 as pgs
import datetime as dt
from lykkelleconnector.fxconverteod import fxconvert
from os.path import expanduser

home = expanduser("~")


def mainmasterprogfundamental(param):
    jday = dt.datetime.today().date() #change it later to yesterday
    print("The date for jobload=",jday)
    conn4 = connect.create()
    cursor4 = conn4.cursor()
    with conn4:
        cc = fxconvert(cursor4)
        fxr = cc.cur_rate
        insjob = """insert into jobrunlist
                (symbol, runsource, rundate,runstatus,jobtable)
                values(%s,%s,%s,%s,%s)ON CONFLICT DO NOTHING"""
        seljobload = """select symbol from jobrunlist where
                    rundate=%s and runsource='mfundamental'
                    and runstatus='complete'"""
        jobloadlist =[]
        cursor4.execute(seljobload,(jday,))
        jobtbl = cursor4.fetchall()
        if jobtbl is None:
            jobtbl = []
        else:
            pass
        jlt = len(jobtbl)
        if jlt>0:
            for i in range(jlt):
                jsym = jobtbl[i][0]
                jobloadlist.append(jsym)
        else:
            print("job run list is empty for date:",jday,"with status=complete and runsource=mfundamental")
        if param == 'T':
            stktblq = """select distinct sa.symbol,ba.prio from stock_all sa join benchmark_all ba
                        on sa.index_code=ba.symbol join stock_master mas
                        on sa.symbol=mas.symbol
                        where ba.prio=4 order by ba.prio fetch first 5 rows only"""
        else:
            stktblq = """select distinct sa.symbol,ba.prio from stock_all sa join benchmark_all ba
                        on sa.index_code=ba.symbol join stock_master mas
                        on sa.symbol=mas.symbol
                        where ba.prio=4 order by ba.prio"""
        cursor4.execute(stktblq)
        tbl = cursor4.fetchall()
        if tbl is None:
            tbl = []
        else:
            pass
        lt = len(tbl)
        if lt>0:
            for i in range(lt):
                symbol = tbl[i][0]
                prio = tbl[i][1]
                stocktable='stock_all'
                if symbol in jobloadlist:
                    print(symbol,"is part of completed jobs loaded today with source=mfundamental")
                else:
                    print("Loading:",symbol, stocktable, prio)
                    cursor4.execute(insjob,(symbol,'mfundamental',jday,'WIP','stock_all'))
                    loadstockfundamentals(symbol, stocktable, fxr, prio, jday, cursor4)
        else:
            print("no stocks in stock_All with prio=4. check if someone deleted the stock_All entries")
        if param == 'T':
            bmktblq = """select distinct ba.symbol,ba.prio from benchmark_all ba
                        join benchmark_master bm on
                        bm.symbol=ba.symbol
                        where ba.prio=4 order by ba.prio fetch first 5 rows only"""
        else:
            bmktblq = """select distinct ba.symbol,ba.prio from benchmark_all ba
                        join benchmark_master bm on
                        bm.symbol=ba.symbol
                        where ba.prio=4 order by ba.prio"""
        cursor4.execute(bmktblq)
        btbl = cursor4.fetchall()
        if btbl is None:
            btbl = []
        else:
            pass
        blt = len(btbl)
        if blt>0:
            for i in range(blt):
                bsymbol = btbl[i][0]
                bprio = btbl[i][1]
                bstocktable='benchmark_all'
                if bsymbol in jobloadlist:
                    print(bsymbol,"is part of completed jobs loaded today with source=mfundamental")
                else:
                    print("Loading:",bsymbol, bstocktable, bprio)
                    cursor4.execute(insjob,(bsymbol,'mfundamental',jday,'WIP','benchmark_all'))
                    loadstockfundamentals(bsymbol, bstocktable, fxr, bprio, jday, cursor4)
        else:
            print("no stocks in stock_All with prio=4. check if someone deleted the stock_All entries")

def mainmasterprog(param):
    # create a connection to postgres
    jday = dt.datetime.today().date()
    print("The date for jobload=",jday)
    conn4 = connect.create()
    cursor4 = conn4.cursor()
    with conn4:
        insjob = """insert into jobrunlist
                (symbol, runsource, rundate,runstatus,jobtable)
                values(%s,%s,%s,%s,%s)ON CONFLICT DO NOTHING"""
        seljobload = """select symbol from jobrunlist where
                    rundate=%s and runsource='mprice'
                    and runstatus='complete'"""
        jobloadlist =[]
        cursor4.execute(seljobload,(jday,))
        jobtbl = cursor4.fetchall()
        if jobtbl is None:
            jobtbl = []
        else:
            pass
        jlt = len(jobtbl)
        if jlt>0:
            for i in range(jlt):
                jsym = jobtbl[i][0]
                jobloadlist.append(jsym)
        else:
            print("job run list is empty for date:",jday,"with status=complete and runsource=mprice")
        if param == 'T':
            stktblq = """select distinct substring(sa.symbol,position('.' in sa.symbol)+1) as exch,
                        ba.prio from stock_all sa join benchmark_all ba
                        on sa.index_code=ba.symbol where ba.prio=4
                        order by ba.prio fetch first 5 rows only"""
        else:
            stktblq = """select distinct substring(sa.symbol,position('.' in sa.symbol)+1) as exch,
                                    ba.prio from stock_all sa join benchmark_all ba
                                    on sa.index_code=ba.symbol where ba.prio=4
                                    order by ba.prio"""
        cursor4.execute(stktblq)
        tbl = cursor4.fetchall()
        if tbl is None:
            tbl = []
        else:
            pass
        lt = len(tbl)
        if lt>0:
            for i in range(lt):
                symbol = tbl[i][0]
                prio = tbl[i][1]
                if prio is None:
                    prio = 6
                else:
                    pass
                stocktable='stock_all'
                if symbol in jobloadlist:
                    print(symbol,"is part of completed jobs loaded today with source=mprice")
                else:
                    print("Loading:",symbol, stocktable, prio)
                    cursor4.execute(insjob,((symbol+'-'+str(prio)),'mprice',jday,'WIP','stock_all'))
                    loadstockprice(symbol, stocktable, jday, prio, cursor4)
        else:
            print("no stocks in stock_All with prio=4. check if someone deleted the stock_All entries")
        if param == 'T':
            bmrk = """select distinct symbol,prio from benchmark_all
            where is_active=True and prio=4 order by prio fetch first 5 rows only"""
        else:
            bmrk = """select distinct symbol,prio from benchmark_all
            where is_active=True and prio=4 order by prio"""
        cursor4.execute(bmrk)
        btbl = cursor4.fetchall()
        if btbl is None:
            btbl = []
        else:
            pass
        blt = len(btbl)
        if blt>0:
            for i in range(blt):
                bsymbol = btbl[i][0]
                bprio = btbl[i][1]
                if bprio is None:
                    bprio = 6
                else:
                    pass
                bstocktable='benchmark_all'
                if bsymbol in jobloadlist:
                    print(bsymbol,"is part of completed jobs loaded today with source=mprice")
                else:
                    print("Loading:",bsymbol, bstocktable, bprio)
                    cursor4.execute(insjob,(bsymbol,'mprice',jday,'WIP','benchmark_all'))
                    loadstockprice(bsymbol, bstocktable, jday, bprio, cursor4)
        else:
            print("no benchmark in benchmark_All with prio=4. check if someone deleted the benchmark_All entries")
    print("postgres connection closed")
def stocksplits(param):
    if param == 'T':
        stk = """select distinct symbol,prio from
            (select h.symbol,b.prio, row_number() over(partition by h.symbol) mr from stock_history h
            join stock_all a on h.symbol=a.symbol
            join benchmark_all b
            on a.index_code=b.symbol
            where b.prio=4) a
            where a.mr>1 fetch first 5 rows only"""
    else:
        stk = """select distinct symbol,prio from
                (select h.symbol,b.prio, row_number() over(partition by h.symbol) mr from stock_history h
                join stock_all a on h.symbol=a.symbol
                join benchmark_all b
                on a.index_code=b.symbol
                where b.prio=4) a
                where a.mr>1"""
    spltq ="""select split_factor, split_date from dbo.stock_master
            where symbol=%s"""
    upd_h="""update dbo.stock_history set price=%s * price
            where symbol=%s and price_date <>%s"""
    upd_sh="""update dbo.stock_statistics_history set price=%s * price
            where symbol=%s and price_date <>%s"""
    split_list="""select symbol,split_date from dbo.split_load where symbol
                =%s"""
    split_ins="""insert into dbo.split_load (symbol,split_date)
                values (%s,%s) ON CONFLICT (symbol) DO UPDATE SET
                split_date=EXCLUDED.split_date"""
    #pdate = str(pdate)
    #pdate = workday.workday(pdate).sdate()
    conn = connect.create()
    cursor = conn.cursor()
    with conn:
        try:
            cursor.execute(stk)
            stklist = cursor.fetchall()
        except pgs.Error as e:
            print(e.pgerror)
            stklist = []
        if len(stklist)>0:
            for i in range(len(stklist)):
                symbol = stklist[i][0]
                prio = stklist[i][1]
                if prio >= 3:
                    pdate = dt.datetime.today().date() - dt.timedelta(days=1)
                    pdate = lykkelleconf.workday.workday(str(pdate)).sdate()
                    print(pdate, "is the date used to find for available splits")
                    try:
                        cursor.execute(split_list, (symbol,))
                        sl = cursor.fetchone()
                        if sl is None:
                            lsym = None
                            ldate = None
                        else:
                            lsym = sl[0]
                            ldate = sl[1]
                    except pgs.Error as e:
                        print(e.pgerror)
                        lsym = None
                        ldate = None
                    if symbol == lsym and str(pdate) == str(ldate):
                        print("stock split calculation is already factored for ", symbol, "on ",pdate)
                    else:
                        try:
                            cursor.execute(spltq, (symbol,))
                            splt = cursor.fetchone()
                            if splt is not None:
                                spltf = splt[0]
                                spltdt = splt[1]
                            else:
                                splt = []
                                spltf = None
                                spltdt = None
                        except pgs.Error as e:
                            print(e.pgerror)
                            splt = []
                            spltf = None
                            spltdt = None
                        #print(type(spltdt),type(pdate))
                        if len(splt)>0 and spltf is not None and spltdt is not None and str(spltdt)==str(pdate):
                            print("split details found for ", symbol, " and ",pdate," having split considerations:",spltf,":",spltdt)
                            try:
                                cursor.execute(upd_h, (spltf,symbol, pdate))
                                print("successful update to stock history for ", symbol," with split factor:",spltf)
                                try:
                                    cursor.execute(upd_sh, (spltf,symbol, pdate))
                                    print("successful update to stock statistics history for ", symbol," with split factor:",spltf)
                                    try:
                                        cursor.execute(split_ins, (symbol,pdate))
                                        print("successful entry to split_load for",symbol, "on ", pdate)
                                    except pgs.Error as e:
                                        print(e.pgerror)
                                except pgs.Error as e:
                                    print(e.pgerror)
                            except pgs.Error as e:
                                print(e.pgerror)
                        else:
                            print("Split details for:",symbol,":",spltf,":",spltdt,"<> today's consideration date:",pdate)
                else:
                    pdate = dt.datetime.today().date()
                    print(pdate,"-",symbol, "is Asia-Oceania so skipping")
        else:
            print("Stock_all and stock_history ahve no common symbols. Weird!!")
# calling main program
#mainmasterprog()
#mainmasterprogfundamental()
#maincalculationprog.stocksplits()

