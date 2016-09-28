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
	while(line != ''):		
		if str(elem[6])[:-1] :
			
		#DO SOMETHING USEFUL
			
		line = file.readline()
		elem = line.split(",")
	file.close()
	
	#if everything is ok return 0
	return 0

#carefull you must be
#filename = 'delays_dataset.csv'
#filename = 'medium_dataset.csv'
filename = 'small_dataset.csv'
delayDistribution(filename)
