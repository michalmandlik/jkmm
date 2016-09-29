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
	'''function writes formated message'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return 0
	
def printVert(vertList):
	'''supportingfunction write
	structured vertList'''
	if len(vertList[0]) == 0:
		return 0
	i = 0
	while i < len(vertList[0]):
		print(str(vertList[0][i]) + ", " + str(vertList[1][i]), end="")
		sublist = vertList[2][i]
		max = 10
		if len(sublist) < 10:
			max = len(sublist)
		n = 0
		while n < max:
			print(", " + str(sublist[n]), end="")
			n += 1
		print("")
		i += 1
	print("=============================")
	return 0
		
def writeVert(vertList):
	'''function writes resulting
	vertList to the file'''
	filename = "output/" + str(time.strftime("%y%m%d")) + "_" + str(time.strftime("%H%M%S")) + "_vertList.csv"
	file = open(filename, 'w')
	infoMsg("WRITING vertList to file: " + filename)
	#write first line
	file.write ("type,id,vert_list\n")
	i = 0
	while i < len(vertList[0]):
		file.write (str(vertList[0][i]) + "," + str(vertList[1][i]))
		n = 0
		sublist = vertList[2][i]
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
	file = open(filename, "r")
	infoMsg("LEARNING from file: " + filename)
	#inicialize the structure
	vertList = [[], [], []] #[[type_list], [id_list], [[delay_list]]]
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
	#filling the structure
	#
	while(line != ""):
		delay = calcDelay(str(elem[5])[:-1], str(elem[6])[:-1])
		n = 0
		#TODO skip 5 and take 6
		#TODO v ID musi byt jeden znak navic, jako jednoznacny identifikator
		while n < 5:
			search = str(elem[n])
			try:
				#add only delay to existing line
				result = (vertList[1].index(search))
				vertList[2][result].append(delay)
			except:
				#add ne line to structure
				vertList[0].append(str(elements[n]))
				vertList[1].append(str(elem[n]))
				vertList[2].append([delay])
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
	#infoMsg("SORTING vertList")
	#vertList.sort(key = lambda row: row[0])

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
writeVert(vertList)
#write info, that job has been finished
infoMsg("DONE")

