#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# retrieve transaction data from web
#
# BeautifulSoup documentation from https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import urllib
import datetime as dt
from bs4 import BeautifulSoup
from datetime import datetime
from rolling_window import *		# this module is built in script 'rolling_window' by Chen
from matplotlib.finance import candlestick_ohlc
from mpldatacursor import datacursor

import matplotlib.dates as mdates
import matplotlib.ticker as mticker

# plot parameter setup
matplotlib.rcParams["axes.labelsize"]="large"
matplotlib.rcParams["axes.linewidth"]=2.0
matplotlib.rcParams["xtick.major.size"]=8
matplotlib.rcParams["ytick.major.size"]=8
matplotlib.rcParams["ytick.minor.size"]=5
matplotlib.rcParams["xtick.labelsize"]=16
matplotlib.rcParams["ytick.labelsize"]=16
matplotlib.rcParams['font.family']='Times New Roman'
matplotlib.rcParams['font.sans-serif'] = ['FangSong'] 	# 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False 		# 解决保存图像是负号'-'显示为方块的问题

# ========================================================================================
# retrieve data from URL
stock_id = 600600
url = "http://www.aigaogao.com/tools/history.html?s=%s"%(stock_id)

html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
#print soup

# retrieve headers
stock_name = soup.head.title.string.split('(')[0]

rows = soup.findAll('td', {'class' : 'altertd'})
N = len(rows)

# create lists to store data
TIME    = list()
OPENP   = list()
HIGHEST = list()
LOWEST  = list() 
CLOSEP  = list()
VOLUME  = list()
AMOUNT  = list()
CHANGE  = list()
C_RATE  = list()
SUO     = list()	# 缩？
HL_DIFF = list()	# 高低差
SZ		= list()	# 深证
SZ_RATE = list()	# 深证%

OHLC    = list()

i = 0
while True:
	# read in time
	MO = int(rows[i].a.string.split('/')[0])		# month
	DD = int(rows[i].a.string.split('/')[1])		# day
	YY = int(rows[i].a.string.split('/')[2])		# year
	time = mdates.date2num(datetime(YY,MO,DD)) ; 	#print time
	TIME.append(time)

	# read in opening price
	i += 1
	openp = float(rows[i].string)	; #print opening
	OPENP.append(openp)

	# read in highest price
	i += 1
	highest = float(rows[i].string) ; #print highest
	HIGHEST.append(highest)
	
	# read in lowest price
	i += 1
	lowest  = float(rows[i].string) ; #print lowest
	LOWEST.append(lowest)
	
	# read in closing price
	i += 1
	closep = float(rows[i].string) ; #print closing
	CLOSEP.append(closep)	

	# read in transaction amount
	i += 1
	volume = int(rows[i].string.replace(',', ''))/10000. ; #print amount 	# 万手
	VOLUME.append(volume)

	# for candlestick
	OHLC.append((time,openp,highest,lowest,closep,volume))

	# read in transaction money
	i += 1
	amount = int(rows[i].string.replace(',', '')) ; #print money, 
	AMOUNT.append(amount)

	# read in change
	i += 1
	change = float(rows[i].string) ; #print change
	CHANGE.append(change)

	# read in change rate
	i += 1
	c_rate = float(rows[i].string.split()[0])/100.
	C_RATE.append(c_rate)

	# read in suo
	i += 1
	suo = rows[i].string
	SUO.append(suo)

	# read in high low difference
	i += 1
	hl_diff = float(rows[i].string.split()[0])/100.
	HL_DIFF.append(hl_diff)

	# read in shenzheng
	i += 1
	#sz = float(rows[i].string)
	#SZ.append(sz)

	# read in shenzheng rate
	i += 1
	#sz_rate = float(rows[i].string.split()[0])/100.
	#SZ_RATE.append(sz_rate)

	i += 1


	if i == N - 1 -12:
		break

# reverse the list because data was stored from the lastest one
TIME.reverse()
OPENP.reverse()
HIGHEST.reverse()
LOWEST.reverse()
CLOSEP.reverse()
VOLUME.reverse()
AMOUNT.reverse()
CHANGE.reverse()
C_RATE.reverse()
SUO.reverse()
HL_DIFF.reverse()
SZ.reverse()
SZ_RATE.reverse()
OHLC.reverse()

# =============================================================================================
# plot K and moving average
fig = plt.figure(figsize=(18,10))
ax1 = plt.subplot(2,1,1)

ma = [5,15,25] 		# moving average window

# moving average
for ma_i in ma:
	MA_win = rolling_window(np.array(CLOSEP), ma_i)
	MA = np.mean(MA_win,axis = 1)
	TIME_MA = TIME[ma_i-1:]
	Color=ax1._get_lines.color_cycle.next()			# get color cycle automatically
	plt.plot(TIME_MA,MA,linewidth = .5,color = Color)
	plt.legend(ma, loc="upper left", shadow=True, title="Moving Average (Days)", fancybox=True)

#plt.plot(TIME,CLOSEP,'gray')

# K candlesticks
candlestick_ohlc(ax1, OHLC, width=0.8, colorup='#77d879', colordown='#db3f3f')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax1.yaxis.grid(color='gray', linestyle='dashed')

plt.ylim(0.1, plt.ylim()[-1])			# awesome to fix only one limit of the axis!!!
plt.ylabel(u'价格（元）')
plt.title(stock_name+"(%06d)"%(stock_id))



# plot barplot of the transaction volume
# get data from candlesticks for a bar plot

ax2 = plt.subplot(2,1,2,sharex = ax1)		# sharex = ax1 to zoom figures together

dates_vol = [x[0] for x in OHLC]
dates_vol = np.asarray(dates_vol)
vol = [x[5] for x in OHLC]
vol = np.asarray(vol)

# make bar plots and color differently depending on up/down for the day
pos = np.array(OPENP)-np.array(CLOSEP)<0  	# return True or False
neg = np.array(OPENP)-np.array(CLOSEP)>0 	# return True or False
ax2.bar(dates_vol[pos],vol[pos],color='#db3f3f',width=1,align='center')
ax2.bar(dates_vol[neg],vol[neg],color='#77d879',width=1,align='center')
plt.ylabel(u'成交量（万手）')

datacursor()

plt.tight_layout()
plt.show()

		