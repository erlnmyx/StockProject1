#!/usr/bin/env python
#
# this script is looking for two-consecutive-day price rising

import numpy as np
from glob import glob


# parameter
rising_rate = 9.6
c1 = 8		# condition 1, 
c2 = 45		# 流通市值小于c2（亿）
# data directory
#db_localpath = '/Users/chenchen/Desktop/Stock/database'
db_localpath = '/Users/erln/Desktop/Stock/database'
dayK_yes_files = '/dayK_yes/*'

# glob all the files
files = glob(db_localpath+dayK_yes_files)
L = len(files)

# extract stock code from the file name
namelist = list()
for i in range(L):
	namelist.append(files[i].split('/')[-1].split('.')[0])

# search price rising for two days
for k,fil in enumerate(files):
	fh = open(fil,'r')
	data = np.loadtxt(fil,ndmin=2)
	#lines = fh.readlines(); print lines
	Ndays = len(data) 	# the no. of the days
	#print 'number of days in %s: %d\n'%(namelist[k], Ndays)
	if Ndays > 2:	# skip over empty files
		date = data[:,0]	# transaction date
		op = data[:,1]		# opening price
		hp = data[:,2]		# highest price
		lp = data[:,3]		# lowest price
		cp = data[:,4]		# closing price

		flag = 0
		if Ndays > 252: # only calculate the most recent year
			for j in range(Ndays-250,Ndays):
				if cp[j]>= (1+rising_rate/100.)*cp[j-1] and cp[j-1]>= (1+rising_rate/100.)*cp[j-2] \
				and cp[j-1] != op[j-1] and cp[j-2] != op[j-2] and op[j] <= (1+c1/100.)*cp[j-1]:
					flag += 1
					print 'ID:',namelist[k], 'date:',str(int(date[j])), '\n' #data[j-1], data[j]
		else:
			for j in range(2,Ndays):
				if cp[j]>= (1+rising_rate/100.)*cp[j-1] and cp[j-1]>= (1+rising_rate/100.)*cp[j-2] \
				and cp[j-1] != op[j-1] and cp[j-2] != op[j-2] and op[j] <= (1+c1/100.)*cp[j-1]:
					flag += 1
				print 'ID:',namelist[k], 'date:',str(int(date[j])), '\n' #data[j-1], data[j]


fh.close()