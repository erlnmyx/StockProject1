#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import numpy as np
from glob import glob
from datetime import datetime

# data directory
db_localpath = '/Users/chenchen/Desktop/Stock/database'
#db_localpath = '/Users/erln/Desktop/Stock/database'    # 2球
dayK_yes_files = '/dayK_yes/*'
# glob all the files
files = glob(db_localpath+dayK_yes_files)
L = len(files)
# retrieve all stock id
IDlist = list()   # namelist for all stocks
for i in range(L):
        IDlist.append(files[i].split('/')[-1].split('.')[0])

# connect your account
conn = mysql.connector.Connect(host='localhost',user='root',password='xxxxxx')
c = conn.cursor()

# delete database if exists
c.execute("DROP DATABASE IF EXISTS dayK_yes")
conn.commit()

# create database
c.execute("CREATE DATABASE IF NOT EXISTS dayK_yes")
conn.commit()
c.execute("USE dayK_yes")

# create tables
for i in range(len(IDlist)):
        tb_name = IDlist[i]
        table  = "CREATE TABLE IF NOT EXISTS `%06d` (time datetime, primary key\
                openprice float, highestprice float, lowestprice float, closeprice float, \
                volume bigint unsigned, transactionamount bigint unsigned)" % (int(tb_name))
        c.execute(table)

        # 个股信息
        fil = open(files[i],'r')
        data = np.loadtxt(fil,ndmin=2)
        N = len(data)

        if not N:
                pass
        else:
                time = data[:,0]        # transaction date
                op = data[:,1]          # open price
                hp = data[:,2]          # highest price
                lp = data[:,3]          # lowest price
                cp = data[:,4]          # close price
                vol = data[:,5]         # volume (手)
                amt = data[:,6]         # amount (元)

                for j in range(N):
                        timesql = datetime.strptime(str(int(time[j])), '%Y%m%d').strftime('%Y-%m-%d') 
                        #print timesql
                        insert = "INSERT INTO `%06d` (time, openprice, highestprice, lowestprice, closeprice, \
                                volume, transactionamount) values ('%s', '%f', '%f', '%f', '%f', '%f', '%f')" %(int(tb_name), \
                                timesql, op[j], hp[j], lp[j], cp[j], vol[j], amt[j])
                        
                        print insert
                        c.execute(insert)

                conn.commit()

c.close()