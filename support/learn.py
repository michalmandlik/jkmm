import datetime
import time
import os
import sys
from pprint import pprint

def calcDelay (sch_dep, act_dep):
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

#TODO common routines to separate file	
def infoMsg (message):
	'''function writes formated message'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return 0
	
def printList (nodeList):
	'''supportingfunction write
	structured nodeList'''
	if len(nodeList) == 0:
		return 0
	for i in range(len(nodeList[0])):
		#only first 20 delays is printed out
		print(str(nodeList[0][i]) + ", " + str(nodeList[1][i]))
	print("=============================")
	return 0
		
def writeNode (nodeList, outDir, prefix):
	'''function writes resulting
	nodeList to the file'''
	filename = (str(outDir) + str(prefix) + "_nodeList.csv")
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
	
def writeVert (vertList, outDir, prefix):
	'''function writes resulting
	nodeList to the file'''
	filename = (str(outDir) + str(prefix) + "_vertList.csv")
	file = open(filename, 'w')
	infoMsg("LEARNING vertList written to file: " + filename)
	#write first line
	file.write("id,id,delay,count,delay,count,delay,count,...\n")
	for i in range(len(vertList[0])):
		file.write(str(vertList[0][i][0]) + "," + str(vertList[0][i][1]))
		for key in vertList[1][i]:
			file.write("," + str(key) + "," + str(vertList[1][i][key]))
		file.write("\n")
	file.close()
	statinfo = os.stat(filename)
	infoMsg("LEARNING size of vertList is: " + str(statinfo.st_size/1000000) + " MB")
	return 0
	
def adjElements (elements):
	'''adjust elements, remove redundant
	sch_date, split sch_dep to days and hours
	add unique identificator
	original
	["CX", "615", "LAX", "PRG", "2016-05-04", "2016-05...", "2016-05..."]
	example result
	[carrier, fltno, dep_apt, arr_apt, delay]
	["!CX", "#615", "$LAX", "&PRG", "+7", ":0", ">5"]'''
	t = time.strptime(str(elements[5]), "%Y-%m-%d %H:%M:%S" )
	elements.append(calcDelay(str(elements[5]), str(elements[6])[:-1])) #delay
	elements[0] = "!" + str(elements[0]) #carrier
	elements[1] = "#" + str(elements[1]) #fltno
	elements[2] = "$" + str(elements[2]) #dep_apt
	elements[3] = "&" + str(elements[3]) #arr_apt	
	elements[4] = "+" + str(t[6]) #weekday
	elements[5] = ":" + str(int(t[3]/6)) #hour groups 0:0-6 1:6-12 2:12-18 3:18-24 
	elements[6] = ">" + str(t[1]) #month
	return (elements)

def transformRaw(rawList):
	''' function reduces the size
	of nodeRaw and returns nodeList
	consisting of list of unique ids
	and coresponding list of dicts of delays'''
	list = [[], []]
	rawList.sort(key = lambda row: row[0])
	index = rawList[0][0]
	delays = []
	for i in range(len(rawList)):
		#collect delays
		if index == rawList[i][0]:
			delays.append(rawList[i][1])
		#append to list and continue with next id
		else:
			list[0].append(index)
			list[1].append(listToDict(delays))
			index = rawList[i][0]
			delays = [rawList[i][1]]		
		#append last data
		if i == (len(rawList) - 1):
			list[0].append(index)
			list[1].append(listToDict(delays))
	return (list)
	
def listToDict (listx):
	'''convert node list to dictionary,
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
	
def mergeList (listA, listB):
	'''function merges two sorted
	nodelists, it returns merged
	and sorted nodelist'''
	if len(listA) == 0:
		return (listB)
	a = 0
	for b in range(len(listB[0])):
		while 1:
			#end of listA
			if listB[0][b] > listA[0][-1]:
				listA[0].append(listB[0][b])
				listA[1].append(listB[1][b])
				a += 1
				break
			#merge elements
			if listB[0][b] == listA[0][a]:
				mergeDict(listA[1][a], listB[1][b])
				a += 1
				break
			#insert new element
			if listB[0][b] < listA[0][a]:
				listA[0].insert(a, listB[0][b])
				listA[1].insert(a, listB[1][b])
				a += 1
				break
			a +=1
	return (listA)
	
def learnData(filename, genVert):
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
	nodeRaw = [] #[[id, delay]]
	nodeList = []	
	vertRaw = [] #[[(idA, idB), delay] 
	vertList = []
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
		l = len(elements)
		#nodeRaw
		for n in range(l-1):
			nodeRaw.append([elements[n], elements[-1]])
		#vertRaw
		if genVert == True:
			for n in range(l-2):
				for m in range(l-2-n):
					vertRaw.append([(elements[n], elements[l-2-m]),elements[-1]])
		#next line
		line = file.readline()
		elements = line.split(",")
		count += 1
		#clean nodeRaw every 2E5 cycles
		if (count % int(1E6)) == 0:
			nodeX = transformRaw(nodeRaw)
			nodeList = mergeList(nodeList, nodeX)
			nodeRaw = []
		#clean vertRaw every 1E5 cycles
		if (count % int(1E5)) == 0 and genVert == True :
			vertX = transformRaw(vertRaw)
			vertList = mergeList(vertList, vertX)
			vertRaw = []
		#print info about progress every ~1 minute TODO count
		if (count % int(1E6)) == 0:
			prog = 100 * float(count) / float(total) #% lines done
			end = datetime.datetime.now()
			time = (end - start).total_seconds()
			#MEM nodeList
			sizeN = sys.getsizeof(nodeList[0])
			for i in range(len(nodeList[0])):
				sizeN += sys.getsizeof(nodeList[1][i])
			#MEM vertList
			sizeV = 0
			if genVert == True:
				for i in range(len(vertList[0])):
					sizeV += sys.getsizeof(vertList[0][i])
					sizeV += sys.getsizeof(vertList[1][i])
			infoMsg("LEARNING " + str(int(prog)) + "% done, " +
					str(int(100 * (time / 60) / prog)) +
					" min remains, MEM nodeList " + str(int(sizeN/1E6)) +
					" MB, MEM vertRaw " + str(int(sizeV/1E6)) + " MB")
	file.close()
	#final clean of nodeRaw
	if (count % int(2E5)) != 0:
		nodeX = transformRaw(nodeRaw)
		nodeList = mergeList(nodeList, nodeX)
		nodeRaw=[]
	#final clean of vertRaw
	if (count % int(1E5)) != 0 and genVert == True:
		vertX = transformRaw(vertRaw)
		vertList = mergeList(vertList, vertX)
		vertRaw = []
	end = datetime.datetime.now()
	time = (end - start).total_seconds()
	#MEM nodeList
	sizeN = sys.getsizeof(nodeList[0])
	for i in range(len(nodeList[0])):
		sizeN += sys.getsizeof(nodeList[1][i])
	#MEM vertList
	sizeV = 0
	if genVert == True:
		for i in range(len(vertList[0])):
			sizeV += sys.getsizeof(vertList[0][i])
			sizeV += sys.getsizeof(vertList[1][i])
	infoMsg("LEARNING " + str(count) + " lines in " +
			str(int(time / 60)) + " min, MEM nodeList " +
			str(int(sizeN / 1E6)) + " MB, MEM vertList " +
			str(int(sizeV / 1E6)) + " MB")
	return(nodeList, vertList)
