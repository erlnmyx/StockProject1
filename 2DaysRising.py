# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# this script is looking for two-consecutive-day price rising


import numpy as np
from glob import glob

# parameters
c1 = 8		# 前一天涨幅小于c1% 
c2 = 250    # 计算范围在c2天交易日内
c3 = 9.6    # 涨幅大于c3%视为涨停
c4 = 45     # 流通市值小于c4（亿）
c5 = 120    # 总市值小于c5（亿）
c6 = 1.2    # 成交量比前一日放大c6倍

# data directory
#db_localpath = '/Users/chenchen/Desktop/Stock/database'
db_localpath = '/Users/erln/Desktop/Stock/database'	# 2球
dayK_yes_files = '/dayK_yes/*'

# 导入其他类数据文件（总股本，流通股本）
Equityinfo = list()
Equityinfo = np.loadtxt('/Users/erln/Desktop/Stock/database/Equityinfo.txt') # 导入股本数据
StockID = Equityinfo[:,0]  # 股票代码
StockID = list(StockID)

for i in range(len(StockID)):
	StockID[i] = "%06d"%(int(StockID[i])

FoE = Equityinfo[:,1]      # 流通股本(亿) Flow of Equity
E = Equityinfo[:,2]        # 总股本(亿) Equity

# glob all the files
files = glob(db_localpath+dayK_yes_files)
L = len(files)

# extract stock code from the file name
namelist = list()
for i in range(L):
	namelist.append(files[i].split('/')[-1].split('.')[0])

# search price rising for two days
for k,fil in enumerate(files):
	kID = StockID.index(namelist[k]) # 找到股本数据中某个股票所对应的index
	data = np.loadtxt(fil,ndmin=2)
	Ndays = len(data) 	# the no. of the days
	if Ndays > 2:	# skip over empty files
		date = data[:,0]	# transaction date
		op = data[:,1]		# opening price
		hp = data[:,2]		# highest price
		lp = data[:,3]		# lowest price
		cp = data[:,4]		# closing price

		flag = 0
		if Ndays > c2+2: # only calculate the most recent year
			for j in range(Ndays-c2,Ndays):
				if cp[j]>= (1+c3/100.)*cp[j-1] and cp[j-1]>= (1+c3/100.)*cp[j-2] \
				and cp[j-1] != op[j-1] and cp[j-2] != op[j-2] and op[j] <= (1+c1/100.)*cp[j-1] \
				and cp[j]*FoE[kID] <= c4 and cp[j]*E[kID] <= c5 and E[kID]>0.01:
					flag += 1
					print 'ID:',namelist[k], 'date:',str(int(date[j])), '\n' #data[j-1], data[j]
		else:
			for j in range(2,Ndays):
				if cp[j]>= (1+c3/100.)*cp[j-1] and cp[j-1]>= (1+c3/100.)*cp[j-2] \
				and cp[j-1] != op[j-1] and cp[j-2] != op[j-2] and op[j] <= (1+c1/100.)*cp[j-1] \
				and cp[j]*FoE[kID] <= c4 and cp[j]*E[kID] <= c5 and E[kID]>0.01:
					flag += 1
					print 'ID:',namelist[k], 'date:',str(int(date[j])), '\n' #data[j-1], data[j]


fh.close()