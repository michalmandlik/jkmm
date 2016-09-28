import datetime
import time

def learn(filename):
	'''function creates structure
	made of verticies and nodes
	each vertice and nodes has a list
	which contains delays'''
	
	#open file, initialize time counter
	#start = datetime.datetime.now()
	file = open(filename, 'r')
	#inicialize the structure
	vertList = [] #vert[id, "x", [1,2,3]]
	nodeList = [] #node[("x","y"), [1,2,3]]
	#step for distribution in minutes
	count = 0
	line = ""
	elem = []
	elements = ["car", "flt", "dep", "arr", "sch"]
	test = "carrier"
	#skipping first line of the file
	while test == "carrier" :	
		line = file.readline()
		elem = line.split(",")
		test = elem[0]
	#processing the file
	while(line != ''):
		#calculate delay in minutes
		delay = 0	
		if str(elem[6])[:-1] :
			schDep = datetime.datetime.strptime(str(elem[5])[:-1], "%Y-%m-%d %H:%M:%S")
			actDep = datetime.datetime.strptime(str(elem[6])[:-1], "%Y-%m-%d %H:%M:%S")
			delay = int(((actDep - schDep).total_seconds())/60)
		#filling the structure
		n = 0
		while n < 5 :
			search = str(elem[n])
			result = -1
			for sublist in vertList :
				if sublist[1] == search :
					result = (vertList.index(sublist))
					vertList[result][2].append(delay)
					break
			if result == -1 :
				vertList.append([str(elements[n]), str(elem[n]), [delay]])
			n += 1
		#next line
		line = file.readline()
		elem = line.split(",")
		count += 1
		#print info about progress
		if (count % 1000000) == 0 :
			end = datetime.datetime.now()
			time = (end - start).total_seconds()
			time = time / count
			time = (53000000 - count) * time
			print ("remain: " + str(time / 60) + " min")
	file.close()
	#sort and print vertList
	vertList.sort(key = lambda row: row[0])
	for item in vertList:
		print (item[0], ', '.join(map(str, item[1:])))
	
	#print performance
	#end = datetime.datetime.now()
	#time = (end - start).total_seconds()
	#print ("time: " + str(time) + " s")
	#print ("lines: " + str(count))
	#print ("est 50mio: " + str(int((60000000 * time / count)/60)) + " min")
	#if everything is ok return list of verticies and nodes
	return (0)

#carefull you must be
#filename = 'data/delays_dataset.csv'
#filename = 'data/100k_dataset.csv'
filename = 'data/10_dataset.csv'

learn(filename)
