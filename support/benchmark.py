import random
import datetime
import csv

def testRand(i) :
	'''function adding random numbers
	and it returns time needed to do
	given number of iterations'''
	start = datetime.datetime.now()
	x = 0
	while i > 0 :
		x += random.random()
		i -= 1
	end = datetime.datetime.now()
	return ((end - start).total_seconds())

def testRead(filename, i) :
	'''function reads given number
	of lines in specifiecsv file and
	it returns time needed to do the job'''
	start = datetime.datetime.now()
	#open csv file
	csvfile = open(filename, 'r')
	csvread = csv.reader(csvfile, delimiter=',')
	csvlist = list(csvread)
	x = 0
	while x < i :
		r = csvlist[x][5]
		x += 1
	end = datetime.datetime.now()
	return ((end - start).total_seconds())
	
def testCustom(filename, i) :
	'''function reads given csv file
	with maximum 7 fields, splits it
	to the list and returns time needed
	to the given iterations'''
	start = datetime.datetime.now()
	file = open(filename, 'r')
	x = 0
	while x < i :
		line = file.readline()
		word = line.split(",") 
		x +=1
	end = datetime.datetime.now()
	return ((end - start).total_seconds())

        

#Random numbers
i = 1000000
tajm = testRand(i)
print ("TEST Random numbers")
print ("test " + str(int(i/1000000)) + "mio iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/i)) + " s")
print ("============================================")

#CSV reading 
i = 1000
filename = 'medium_dataset.csv'
tajm = testRead(filename, i)
print ()
print ("TEST CSV Read Line")
print ("test " + str(int(i/1000)) + "k iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/(i*60))) + " min")
print ("============================================")

#Custom reader
i = 100000
filename = 'medium_dataset.csv'
tajm = testCustom(filename, i)
print ()
print ("TEST Custom reader")
print ("test " + str(int(i/1000)) + "k iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/(i*60))) + " min")
print ("============================================")
