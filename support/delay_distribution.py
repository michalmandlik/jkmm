import datetime
import time
from operator import itemgetter

def delayDistribution(filename):
	''' function reads csv file and
	returns distribution of delays'''
	start = datetime.datetime.now()
	maxDelay = 0
	minDelay = 0
	file = open(filename, 'r')
	
	#delays hash inicialized for zero delay
	delays = {0:0}
	#step for distribution in minutes
	count = 0
	line = ""
	elem = []
	test = "carrier"
	#skipping first line of the file
	while test == "carrier" :	
		line = file.readline()
		elem = line.split(",")
		test = elem[0]
	#processing the file
	while(line != ''):		
		if str(elem[6])[:-1] :
			schDep = datetime.datetime.strptime(str(elem[5])[:-1], "%Y-%m-%d %H:%M:%S")
			actDep = datetime.datetime.strptime(str(elem[6])[:-1], "%Y-%m-%d %H:%M:%S")
			delay = int(((actDep - schDep).total_seconds())/60)
			if  delay in delays :
				delays[delay] += 1
			else :
				delays[delay] = 1
		else :
			delays[0] += 1	
		line = file.readline()
		elem = line.split(",")
		count += 1
		#print info about progress
		if (count % 1000000) == 0 :
			end = datetime.datetime.now()
			time = (end - start).total_seconds()
			time = time / count
			time = (53000000 - count) * time
			print ("remain: " + str(int(time / 60)) + " min")
	file.close()
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

#carefull you must be
#filename = '../data/delays_dataset.csv'
filename = '../data/1mio_dataset.csv'
#filename = '../data/100k_dataset.csv'
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
