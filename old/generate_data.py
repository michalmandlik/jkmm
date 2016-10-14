import random

#generate testing data
filename = '../data/delays_dataset.csv'
readF = open(filename, 'r')
count = [10, 100, 1000, 10000, 100000, 1000000]

for i in count :
	filename = '../data/delays_dataset.csv'
	readF = open(filename, 'r')
	
	name =""
	if i > 999 :
		name = str(int(i/1000)) + "k"
	else :
		name = str(int(i))
	if i > 999999 :
		name = str(int(i/1000000)) + "mio"
	
	filename = "../data/" + str(name) + "_dataset.csv"
	writeF = open(filename, 'w')

	#always write first line
	line = readF.readline()
	writeF.write (str(line))
	x = 1
	while x < i :
		line = readF.readline()
		#random writes i lines to the writeF
		if int(random.random() * 10) == 0 :
			writeF.write (str(line))
			x +=1
	writeF.close()

readF.close()
