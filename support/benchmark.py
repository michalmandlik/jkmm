import random
import datetime
import csv
import pandas as pd

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

def testRead(filename) :
	'''function reads given number
	of lines in specifiecsv file and
	it returns time needed to do the job'''
	start = datetime.datetime.now()
	#open csv file
	csvfile = open(filename, 'r')
	csvread = csv.reader(csvfile, delimiter=',')
	#tohle bude kolabovat na pameti
	csvlist = list(csvread)
	x = 0
	while x < len(csvlist) :
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
	print(x)
	end = datetime.datetime.now()
	return ((end - start).total_seconds())

def testPandas(filename) :
	'''function test reading of the file
	using Pandas and it returns time 
	needed to do a job'''
	start = datetime.datetime.now()
	df = pd.read_csv(filename, iterator=True, chunksize=100000) 
	for chunk in df :
		n=0
		while n < len(chunk) :
			data = chunk["scheduled_departure"][n]
			n += 1
	end = datetime.datetime.now()
	return ((end - start).total_seconds())
        

#CAREFULL YOU MUST BE

#filename = '../data/delays_dataset.csv'
#i = 52000000
filename = '../data/1mio_dataset.csv'
i = 1000000
#filename = '../data/100k_dataset.csv'
#i = 100000
#filename = '../data/10k_dataset.csv'
#i = 10000
#filename = '../data/10_dataset.csv'
#i = 10

#Random numbers
tajm = testRand(i)
print ("TEST Random numbers")
print ("test " + str(int(i/1000000)) + "mio iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/i)) + " s")
print ("============================================")

#CSV reading 
tajm = testRead(filename)
print ()
print ("TEST CSV Read Line")
print ("test " + str(int(i/1000)) + "k iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/(i*60))) + " min")
print ("============================================")

#Custom reader
tajm = testCustom(filename, i)
print ()
print ("TEST Custom reader")
print ("test " + str(int(i/1000)) + "k iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/(i*60))) + " min")
print ("============================================")

#Custom reader
tajm = testPandas(filename)
print ()
print ("TEST PANDAS reader")
print ("test " + str(int(i/1000)) + "k iter: " + str(tajm) + " s")
print ("per iter: " + str(tajm/i) + " s")
print ("50mio iter: " + str(int(50000000*tajm/(i*60))) + " min")
print ("============================================")
