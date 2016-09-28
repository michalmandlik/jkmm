import datetime

def delayDistribution(filename):
	''' function reads csv file and
	returns distribution of delays'''
	start = datetime.datetime.now()
	maxDelay = 0
	minDelay = 0
	file = open(filename, 'r')
	
	line = ""
	elem = []
	test = "carrier"
	#skipping first line of the file
	while test == "carrier" :	
		line = file.readline()
		elem = line.split(",")
		test = elem[0]
	#processing the file
	count = 0
	while(line != ''):		
		if str(elem[6])[:-1]:
			schDep = datetime.datetime.strptime(str(elem[5])[:-1], "%Y-%m-%d %H:%M:%S")
			actDep = datetime.datetime.strptime(str(elem[6])[:-1], "%Y-%m-%d %H:%M:%S")
			delay = int(((actDep - schDep).total_seconds())/60)
			if delay > maxDelay :
				maxDelay = delay
			if delay < minDelay :
				minDelay = delay
		line = file.readline()
		elem = line.split(",")
		count += 1
		if (count % 1000000) == 0 :
			end = datetime.datetime.now()
			rem = (end - start).total_seconds() / count
			rem = (50000000 - count) * rem
			print ("rem: " + str(int(rem/60)) + " min || proc: " + str(int(count/1000000)) + "mio lines")
	file.close()
	
	#print results
	print ("max: " + str(maxDelay))
	print ("min: " + str(minDelay))
	#print processing time
	end = datetime.datetime.now()
	print ("time: " + str((end - start).total_seconds()) + " s")
	print ("lines: " + str(count))
	print ("****************************************")	
	#if everything is ok return 0
	return 0

#carefull you must be
filename = 'delays_dataset.csv'
#filename = 'medium_dataset.csv'
#filename = 'small_dataset.csv'
delayDistribution(filename)
