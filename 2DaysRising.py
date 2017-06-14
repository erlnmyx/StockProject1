#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# this script is looking for two-consecutive-day price rising


import numpy as np
from glob import glob

# parameters
c1 = 8		   # 前一天涨幅小于c1% 
c2 = 250       # 计算范围在c2天交易日内
c3 = 9.6       # 涨幅大于c3%视为涨停
c4 = 45        # 流通市值小于c4（亿）
c5 = 120       # 总市值小于c5（亿）
c6 = 1.2       # 成交量比前一日放大c6倍
c7 = 20170613  # 数据最新一天
c8 = 0.33      # 仓位

# data directory
#db_localpath = '/Users/chenchen/Desktop/Stock/database'
db_localpath = '/Users/erln/Desktop/Stock/database'	# 2球
dayK_yes_files = '/dayK_yes/*'

# 导入其他类数据文件（总股本，流通股本）
Equityinfo = list()
#Equityinfo = np.loadtxt('/Users/chenchen/Desktop/Stock/database/Equityinfo.txt') # 导入股本数据
Equityinfo = np.loadtxt('/Users/erln/Desktop/Stock/database/Equityinfo.txt') # 导入股本数据

StockID = Equityinfo[:,0]  # 股票代码

StockID = list(StockID)

for i in range(len(StockID)):
	StockID[i] = "%06d" % (int(StockID[i]))

FoE = Equityinfo[:,1]      # 流通股本(亿) Flow of Equity
E = Equityinfo[:,2]        # 总股本(亿) Equity

# glob all the files
files = glob(db_localpath+dayK_yes_files)
L = len(files)

# parameters
namelist = list()   # namelist for all stocks
Yield = 1           # 收益率
count1 = 0          # 计数因子，用来储存select stocks的数量
count2 = 0          # 计数因子，用来储存失败（利润小于0）的次数
count3 = 0          # 计数因子，
count4 = 0          # 计数因子，
count5 = 0          # 计数因子，
count6 = 0          # 计数因子，
count7 = 0          # 计数因子，
count8 = 0          # 计数因子，
count9 = 0          # 计数因子，
count10 = 0         # 计数因子，
count11 = 0         # 计数因子，
count12 = 0         # 计数因子，

# 均线定义
MA1 = 5   # 5日均线
MA2 = 10  # 10日均线
MA3 = 20  # 20日均线
MA4 = 30  # 30日均线
MA5 = 60  # 60日均线
MA6 = 120 # 120日均线
MA7 = 250 # 250日均线

# output lists
output1 = list()
output2 = list()
output3 = list()
output4 = list()
output5 = list()
output6 = list()
output7 = list()
output8 = list()

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

		if Ndays > c2+2: # only calculate the most recent year
			for j in range(Ndays-c2,Ndays):
				if cp[j]>= (1+c3/100.)*cp[j-1] and cp[j-1] >= (1+c3/100.)*cp[j-2] \
				and cp[j-1] != op[j-1] and cp[j-2] != op[j-2] and op[j] <= (1+c1/100.)*cp[j-1] \
				and cp[j-2] < cp[j-3]*(1+(c3/100.-0.03)) and cp[j]*FoE[kID] <= c4 and cp[j]*E[kID] <= c5 \
				and E[kID]>0.01 and int(date[j])> c7 - 10000:
				# 1.当天收盘涨幅大于c3%；2.前一天收盘涨幅大于c3%； # 去掉由于停牌原因造成的一年前的交易

					#and cp[j-1] > np.mean(cp[j-1-len(cp)-MA1:j-1-len(cp)])

					if int(date[j]) < c7:
						if op[j+1] > cp[j] and cp[j+1] > cp[j] * (1+c3/100):
							SP = cp[j+1] # SP=selling price, 如果高开且涨停，则在涨停价卖出
							count5 = count5 + 1
						elif op[j+1] > cp[j] and cp[j+1] < cp[j] * (1+c3/100):
							SP = (op[j+1] + hp[j+1])/2 # 如果高开但没涨停，假设卖出价位（开盘价+最高价）/2
							count6 = count6 + 1
						elif op[j+1] < cp[j]:
							SP = op[j+1] # 如果低开，直接卖出
							count7 = count7 + 1
						Profit = (SP-cp[j])/cp[j]*c8 # 利润
						#print 'ID:',namelist[k], 'Date:',str(int(date[j])), 'BuyPrice', cp[j], \
						#'SellPrice', SP, 'MA5','Profit', Profit, 'Yield', Yield, '\n' #data[j-1], data[j]

						#print round(np.mean(cp[j-len(cp)-MA1:j-len(cp)]),2)
					else:
						Profit = 0
						count8 = count8 + 1
						#print 'ID:',namelist[k], 'Date:',str(int(date[j])), 'BuyPrice', cp[j], \
						#'MA5', 'Yield', Yield,'\n' #data[j-1], data[j]
					output1.append(int(date[j]))   # 买入日期
					output2.append(namelist[k])    # 买入股票代码
					output3.append(cp[j])          # 买入价
					output4.append(SP)             # 卖出价
					output5.append(Profit)         # 利润率
					count2 = count2 + 1 
		else:
			for j in range(2,Ndays):
				if cp[j]>= (1+c3/100.)*cp[j-1] and cp[j-1]>= (1+c3/100.)*cp[j-2] \
				and cp[j-1] != op[j-1] and cp[j-2] != op[j-2] and op[j] <= (1+c1/100.)*cp[j-1] \
				and cp[j-2] < cp[j-3]*(1+(c3/100.-0.03)) and cp[j]*FoE[kID] <= c4 and cp[j]*E[kID] \
				<= c5 and E[kID]>0.01 and int(date[j])> c7 - 10000:
					if int(date[j]) < c7:
						if op[j+1] > cp[j] and cp[j+1] > cp[j] * (1+c3/100):
							SP = cp[j+1] # SP=selling price, 如果高开且涨停，则在涨停价卖出
							count9 = count9 + 1
						elif op[j+1] > cp[j] and cp[j+1] < cp[j] * (1+c3/100):
							SP = (op[j+1] + hp[j+1])/2 # 如果高开但没涨停，假设卖出价位（开盘价+最高价）/2
							count10 = count10 + 1
						elif op[j+1] < cp[j]:
							SP = op[j+1] # 如果低开，直接卖出
							count11 = count11 + 1
						Profit = (SP-cp[j])/cp[j]*c8 # 利润
						#print 'ID:',namelist[k], 'Date:',str(int(date[j])), 'BuyPrice', cp[j], \
						#'SellPrice', SP, 'Profit', Profit, 'Yield', Yield, 'MA5','\n' #data[j-1], data[j]
					else:
						Profit = 0
						count12 = count12 + 1
						#print 'ID:',namelist[k], 'Date:',str(int(date[j])), 'BuyPrice', cp[j], \
						#'Yield', Yield,'MA5','\n' #data[j-1], data[j]
					output1.append(int(date[j]))   # 买入日期
					output2.append(namelist[k])    # 买入股票代码
					output3.append(cp[j])          # 买入价
					output4.append(SP)             # 卖出价
					output5.append(Profit)         # 利润率
					count2 = count2 + 1

outputarray = np.zeros((count2,5))


for i in range(count2):
	outputarray[i,0] = output1[i]
	outputarray[i,1] = output2[i]
	outputarray[i,2] = output3[i]
	outputarray[i,3] = output4[i]
	outputarray[i,4] = output5[i]

outputlist = outputarray.tolist()
outputlist.sort()

for i in range(count2):
	#if int(outputlist[i][0]) > c7 - 10000: # 去掉由于停牌原因造成的一年前的交易
	Yield = Yield * (1+outputlist[i][4])   # 收益率计算
	print 'Date:',str(int(outputlist[i][0])), 'ID:', int(outputlist[i][1]),'Profit', \
	'BuyPrice', round(outputlist[i][2],2), 'SellPrice', round(outputlist[i][3],2), \
	'Profit', round(outputlist[i][4],3), 'Yield', round(Yield,3) ,'\n' 
	count3 = count3 + 1
	if round(outputlist[i][4],3) < 0:
		count4 = count4 + 1

print 'fail times', count4, 'total times', count3, 'total times', count2

print '老股，高开且涨停', count5
print '老股，高开没涨停',count6
print '老股，低开',count7
print '老股，当天买入',count8
print '新股，高开且涨停',count9
print '新股，高开没涨停',count10
print '新股，低开',count11
print '新股，当天买入',count12






