import datetime
import time
import os
import sys

def calcDelay(sch_dep, act_dep):
	'''function returs dealy in minutes
	calculated from two input strings
	formated YYYY-MM-DD HH:MM:SS'''
	delay = 0
	if act_dep :
		sch_dep = datetime.datetime.strptime(sch_dep, "%Y-%m-%d %H:%M:%S")
		act_dep = datetime.datetime.strptime(act_dep, "%Y-%m-%d %H:%M:%S")
		delay = int(((act_dep - sch_dep).total_seconds())/60)
		return (delay)
	else :
		return (delay)
	
def infoMsg(message):
	'''function writes formated message'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return 0
	
def printNode(nodeList):
	'''supportingfunction write
	structured nodeList'''
	if len(nodeList) == 0:
		return 0
	for i in range(len(nodeList[0])):
		#only first 20 delays is printed out
		print(str(nodeList[0][i]) + ", " + str(nodeList[1][i]))
	print("=============================")
	return 0
		
def writeNode(nodeList):
	'''function writes resulting
	nodeList to the file'''
	filename = "output/" + str(time.strftime("%y%m%d")) + "_" + str(time.strftime("%H%M%S")) + "_nodeList.csv"
	file = open(filename, 'w')
	infoMsg("WRITING nodeList to file: " + filename)
	#write first line
	file.write ("id,delay,count,delay,count,delay,count,...\n")
	for i in range(len(nodeList[0])):
		file.write (str(nodeList[0][i]))
		for key in nodeList[1][i]:
			file.write ("," + str(key) + "," + str(nodeList[1][i][key]))
		file.write ("\n")
	file.close()
	statinfo = os.stat(filename)
	infoMsg("SIZE of nodeList is: " + str(statinfo.st_size/1000000) + " MB")
	return 0
	
def adjElements(elements):
	'''adjust elements, remove redundant
	sch_date, split sch_dep to days and hours
	add unique identificator
	original
	["CX", "615", "LAX", "PRG", "2016-05-04", "2016-05...", "2016-05..."]
	example result
	[carrier, fltno, dep_apt, arr_apt, delay]
	["~CX", "!615", "@LAX", "#PRG", "$7", "+14", "5"]'''
	t = time.strptime(str(elements[5]), "%Y-%m-%d %H:%M:%S" )
	elements[6] = calcDelay(str(elements[5])[:-1], str(elements[6])[:-1]) #delay
	elements[0] = "!" + str(elements[0]) #carrier
	elements[1] = "#" + str(elements[1]) #fltno
	elements[2] = "$" + str(elements[2]) #dep_apt
	elements[3] = "&" + str(elements[3]) #arr_apt	
	elements[4] = "+" + str(t[6]) #weekday
	elements[5] = ":" + str(t[3]) #hour
	return (elements)

def transformNode(nodeRaw):
	''' function reduces the size
	of nodeRaw and returns nodeList
	consisting of list of unique ids
	and coresponding list of lists of delays'''
	nodeList = [[], []]
	nodeRaw.sort(key = lambda row: row[0])
	index = nodeRaw[0][0]
	delays = []
	for i in range(len(nodeRaw)):
		#collect delays
		if index == nodeRaw[i][0]:
			delays.append(nodeRaw[i][1])
		#append to nodeList and continue with next id
		else:
			nodeList[0].append(index)
			nodeList[1].append(listToDict(delays))
			index = nodeRaw[i][0]
			delays = [nodeRaw[i][1]]		
		#append last data
		if i == (len(nodeRaw) - 1):
			nodeList[0].append(index)
			nodeList[1].append(listToDict(delays))
	return (nodeList)
	
def listToDict (listx):
	'''connode list to dictionary,
	where the key is unique item
	from the list and value is
	count of the item in the list'''
	dictx = {}
	listx.sort()
	count = 0
	elem = listx[0]
	for i in range(len(listx)):
		if elem == listx[i]:
			count += 1
		else:
			dictx[elem] = count
			elem = listx[i]
			count = 1
		if i == (len(listx) - 1):
			dictx[elem] = count
	return (dictx)

def mergeDict (dictA, dictB):
	'''merges two dictionaries,
	where values are ints, if there is
	the same key in both dict it unites
	values as result'''
	for key in dictB:
		if key in dictA:
			dictA[key] = dictA[key] + dictB[key]
		else:
			dictA[key] = dictB[key]
	return (dictA)
	
def mergeNode (nodeA, nodeB):
	'''function merges two sorted
	nodelists, it returns merged
	and sorted nodelist'''
	if len(nodeA) == 0:
		return (nodeB)
	a = 0
	for b in range(len(nodeB[0])):
		while 1:
			#end of nodeA
			if nodeB[0][b] > nodeA[0][-1]:
				nodeA[0].append(nodeB[0][b])
				nodeA[1].append(nodeB[1][b])
				a += 1
				break
			#merge elements
			if nodeB[0][b] == nodeA[0][a]:
				mergeDict(nodeA[1][a], nodeB[1][b])
				a += 1
				break
			#insert new element
			if nodeB[0][b] < nodeA[0][a]:
				nodeA[0].insert(a, nodeB[0][b])
				nodeA[1].insert(a, nodeB[1][b])
				a += 1
				break
			a +=1
	return (nodeA)
	
def learn(filename):
	'''function creates structure
	made of nodeicies and nodes
	each nodeice and nodes has a list
	which contains delays'''	
	#open file, initialize time counter
	start = datetime.datetime.now()
	#estimation of total lines in dataset
	total = int(os.stat(filename).st_size / 56)
	file = open(filename, "r")
	infoMsg("LEARNING from file: " + filename)
	#inicialize the structure
	nodeRaw = [] #[[id, delay], ...]
	nodeList = []
	elements = []
	count = 0
	line = ""
	test = "carrier"
	#skipping first line of the file
	while test == "carrier":	
		line = file.readline()
		elements = line.split(",")
		test = elements[0]
	#filling the structure
	while(line != ""):
		elements = adjElements(elements)
		for n in range(6):
			nodeRaw.append([elements[n], elements[6]])
		#next line
		line = file.readline()
		elements = line.split(",")
		count += 1
		#clean nodeRaw every 2E% cycles
		if (count % 2E5) == 0:
			nodeX = transformNode(nodeRaw)
			nodeList = mergeNode(nodeList, nodeX)
			nodeRaw = []
		#print info about progress every ~1 minute
		if (count % 2E5) == 0:
			prog = 100 * count / total
			end = datetime.datetime.now()
			time = (end - start).total_seconds()
			#MEM nodeList
			size = sys.getsizeof(nodeList[0])
			for i in range(len(nodeList[0])):
				size += sys.getsizeof(nodeList[1][i])
			infoMsg(str(int(prog)) + "% done, " + str(int(time / 60 * 100 / prog)) + " min remains, MEM nodeList " + str(int(size/1E6)) + " MB")
	file.close()
	#final clean of nodeRaw
	nodeX = transformNode(nodeRaw)
	nodeList = mergeNode(nodeList, nodeX)
	end = datetime.datetime.now()
	time = (end - start).total_seconds()
	#MEM nodeList
	size = sys.getsizeof(nodeList[0])
	for i in range(len(nodeList[0])):
		size += sys.getsizeof(nodeList[1][i])
	infoMsg("PROCESSED " + str(count) + " lines in " + str(int(time / 60)) + " min, MEM nodeList " + str(int(size / 1E6)) + " MB")
	return(nodeList)

########################################################################

#CAREFULL YOU MUST BE

#Select the file
#filename = 'data/delays_dataset.csv'
filename = 'data/1mio_dataset.csv'
#filename = 'data/100k_dataset.csv'
#filename = 'data/10k_dataset.csv'
#filename = 'data/100_dataset.csv'
#filename = 'data/10_dataset.csv'

#MAIN function
nodeList = learn(filename)

#save the result
writeNode(nodeList)

#write info, that job has been finished
infoMsg("DONE Be happy :-)")

