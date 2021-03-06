#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# 上证指数


import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from datetime import date
from rolling_window import *		# this module is built in script 'rolling_window' by Chen


# plot parameter setup
matplotlib.rcParams["axes.labelsize"]="large"
matplotlib.rcParams["axes.linewidth"]=2.0
matplotlib.rcParams["xtick.major.size"]=8
matplotlib.rcParams["ytick.major.size"]=8
matplotlib.rcParams["ytick.minor.size"]=5
matplotlib.rcParams["xtick.labelsize"]=16
matplotlib.rcParams["ytick.labelsize"]=16
matplotlib.rcParams['font.family']='Times New Roman'


ma = [50,150,250,500,750] 		# moving average window

fig = plt.figure(figsize=(18,8))
ax = fig.add_subplot(1,1,1)

fil = open('上证指数90_17.csv','r')
lines = fil.readlines()
L = len(lines)

TIME = list()
CLOSING = list()

for i in range(1,L):
	# read in time
	MO = int(lines[i].split(',')[0].split('/')[0])		# month
	DD = int(lines[i].split(',')[0].split('/')[1])		# day
	YY = int(lines[i].split(',')[0].split('/')[2])		# year
	# convert to full year expression
	if YY > 80:
		YYYY = 1900 + YY
	else:
		YYYY = 2000 + YY
	time = date(YYYY,MO,DD)					# time
	TIME.append(time)

	# deal with the data
	
	closing = float(lines[i].split(',')[3])
	CLOSING.append(closing)

# reverse the list because data was stored from the lastest one
TIME.reverse()
CLOSING.reverse()

# plot moving average
for ma_i in ma:
	MA_win = rolling_window(np.array(CLOSING), ma_i)
	MA = np.mean(MA_win,axis = 1)
	TIME_MA = TIME[ma_i-1:]
	#Color=ax._get_lines.color_cycle.next()			# get color cycle automatically
	Color=next(ax._get_lines.prop_cycler)['color']
	plt.plot(TIME_MA,MA,linewidth = 0.5,color = Color)
	plt.legend(ma, loc="upper left", shadow=True, title="Moving Average (Days)", fancybox=True)


# 大盘曲线
plt.plot(TIME, CLOSING, color = 'gray')
plt.xlabel('Year',fontsize = 20)
plt.ylabel('Index',fontsize = 20)
ax.yaxis.grid(color='gray', linestyle='dashed')

plt.show()

fil.close()