import datetime
import time
import math
from operator import itemgetter
import pandas as pd

def delayDistribution(filename):
	''' function reads csv file and
	returns distribution of delays'''
	start = datetime.datetime.now()
	#delays hash inicialized for zero delay
	delays = {0:0}
	#processing the file
	df = pd.read_csv(filename, iterator=True, chunksize=100000) 
	count = 0
	for chunk in df :
		n=0
		while n < len(chunk) :
			if str(chunk["actual_departure"][n]) != 'nan'  :
				schDep = datetime.datetime.strptime(str(chunk["scheduled_departure"][n]), "%Y-%m-%d %H:%M:%S")
				actDep = datetime.datetime.strptime(str(chunk["actual_departure"][n]), "%Y-%m-%d %H:%M:%S")
				delay = int(((actDep - schDep).total_seconds())/60)
				if  delay in delays :
					delays[delay] += 1
				else :
					delays[delay] = 1
			else :
				delays[0] += 1	
			n += 1
			count += 1
			#print info about progress
			if (count % 1000000) == 0 :
				end = datetime.datetime.now()
				time = (end - start).total_seconds()
				time = time / count
				time = (53000000 - count) * time
				print ("remain: " + str(int(time / 60)) + " min")
	#sorting the result
	delayList = delays.items()	
	delayList = sorted(delayList, key=itemgetter(0))
	end = datetime.datetime.now()
	time = (end - start).total_seconds()
	#print performance
	print ("time: " + str(time) + " s")
	print ("lines: " + str(count))
	print ("est 50mio: " + str(int((60000000 * time / count)/60)) + " min")
	#if everything is ok return delays hash
	return (delayList)

#CAREFULL YOU MUST BE

#filename = '../data/delays_dataset.csv'
filename = '../data/1mio_dataset.csv'
#filename = '../data/100k_dataset.csv'
#filename = '../data/10k_dataset.csv'
#filename = '../data/10_dataset.csv'

result = delayDistribution(filename)

#write result to a file
filename = "../output/" + str(time.strftime("%y%m%d")) + "_" + str(time.strftime("%H%M%S")) + "_distribution.txt"
file = open(filename, 'w')
i = 0
while i < len(result) :
	file.write (str(result[i][0]) + "," + str(result[i][1]) + "\n")
	i += 1
file.close()
