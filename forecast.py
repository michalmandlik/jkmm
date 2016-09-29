import datetime
import time
import os

def calcDelay(sch_dep, act_dep):
	'''function returs dealy in minutes
	calculated from two input strings
	formated YYYY-MM-DD HH-MM-SS'''
	delay = 0
	if act_dep :
		sch_dep = datetime.datetime.strptime(sch_dep, "%Y-%m-%d %H:%M:%S")
		act_dep = datetime.datetime.strptime(act_dep, "%Y-%m-%d %H:%M:%S")
		delay = int(((act_dep - sch_dep).total_seconds())/60)
		return (delay)
	#TODO osetrit dalsi mozne vstupy
	else :
		return (delay)

def printProgress(start, count):
	'''function prints info about the
	remaining time to finish the job'''
	end = datetime.datetime.now()
	time = (end - start).total_seconds()
	time = time / count
	time = (53E6 - count) * time
	print ("remain: " + str(int(time / 60)) + " min | " + str(int(count/1E6)) + " mio lines done")
	return 0
	
def infoMsg(message):
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return 0

def writeResult(vertList):
	'''function writes resulting
	vertList to the file'''
	filename = "output/" + str(time.strftime("%y%m%d")) + "_" + str(time.strftime("%H%M%S")) + "_vertList.csv"
	file = open(filename, 'w')
	infoMsg("WRITING vertList to file: " + filename)
	#write first line
	file.write ("type,id,vert_list\n")
	i = 0
	while i < len(vertList):
		file.write (str(vertList[i][0]) + "," + str(vertList[i][1]))
		n = 0
		sublist = vertList[i][2]
		while n < len(sublist):
			file.write ("," + str(sublist[n]))
			n += 1
		file.write ("\n")
		i += 1
	file.close()
	statinfo = os.stat(filename)
	infoMsg("SIZE of vertList is: " + str(statinfo.st_size/1000000) + " MB")
	return 0
	
def learn(filename):
	'''function creates structure
	made of verticies and nodes
	each vertice and nodes has a list
	which contains delays'''	
	#open file, initialize time counter
	start = datetime.datetime.now()
	file = open(filename, 'r')
	infoMsg("LEARNING from file: " + filename)
	#inicialize the structure
	vertList = [] #vert["type", "id", [delay_list]]
	nodeList = [] #node[{"id","id"}, [delay_list]]
	#step for distribution in minutes
	count = 0
	line = ""
	elem = []
	elements = ["car", "flt", "dep", "arr", "sch"]
	test = "carrier"
	#skipping first line of the file
	while test == "carrier":	
		line = file.readline()
		elem = line.split(",")
		test = elem[0]
	#processing the file
	while(line != ''):
		#calculate delay in minutes
		delay = calcDelay(str(elem[5])[:-1], str(elem[6])[:-1])
		#filling the structure
		n = 0
		while n < 5:
			search = str(elem[n])
			result = -1
			for sublist in vertList:
				if sublist[1] == search:
					result = (vertList.index(sublist))
					vertList[result][2].append(delay)
					break
			if result == -1:
				vertList.append([str(elements[n]), str(elem[n]), [delay]])
			n += 1
		#next line
		line = file.readline()
		elem = line.split(",")
		count += 1
		#print info about progress
		if (count % 1E6) == 0:
			printProgress(start, count)
	file.close()
	#sort vertList
	infoMsg("SORTING vertList")
	vertList.sort(key = lambda row: row[0])

	#print performance
	#end = datetime.datetime.now()
	#time = (end - start).total_seconds()
	#print ("time: " + str(time) + " s")
	#print ("lines: " + str(count))
	#print ("est 50mio: " + str(int((60000000 * time / count)/60)) + " min")
	#if everything is ok return list of verticies and nodes
	return (vertList)

########################################################################

#CAREFULL YOU MUST BE

#filename = 'data/delays_dataset.csv'
#filename = 'data/1mio_dataset.csv'
#filename = 'data/100k_dataset.csv'
#filename = 'data/10k_dataset.csv'
#filename = 'data/100_dataset.csv'
filename = 'data/10_dataset.csv'

#MAIN function
vertList = learn(filename)
#save the result
writeResult(vertList)
#write info, that job has been finished
infoMsg("DONE")

