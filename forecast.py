import os
import time
import random

def loadElement(element, filename):
	''' function loads dictionary of delays
	for specific id and returns list of delays'''
	delays = []
	dictionary = {}
	nodeFile = open(filename, "r")

	line = nodeFile.readline()
	while (line != ""):
		node = line.split(",")
		#search the line with right element id
		if node[0] != element:
			line = nodeFile.readline()
			continue

		#id, delay, count, delay, count, ...
		#predelat na generatorovou notaci
		i = 1
		while i < len(node):
			for n in range(int(node[i+1])):
				delays.append(node[i])
			i += 2
		line = nodeFile.readline()
	nodeFile.close()
	return(delays)

def adjElements(elements):
	'''function changes element string
	to have unique identificator'''
	t = time.strptime(str(elements[5])[:-1], "%Y-%m-%d %H:%M:%S" )
	elements[0] = "!" + str(elements[0]) #carrier
	elements[1] = "#" + str(elements[1]) #fltno
	elements[2] = "$" + str(elements[2]) #dep_apt
	elements[3] = "&" + str(elements[3]) #arr_apt	
	elements[4] = "+" + str(t[6]) #weekday
	elements[5] = ":" + str(int(t[3]/6)) #hour groups 0:0-6 1:6-12 2:12-18 3:18-24 
	elements.append(">" + str(t[1])) #month
	return (elements)

def prepareGame(elements, nodeName):
	'''function returns list of ids with
	associated list of delays'''
	game = [[],[]]
	elements = adjElements(elements)
	for i in range(len(elements)):
		delays = loadElement(elements[i], nodeName)
		if delays != []:
			game[0].append(elements[i])
			game[1].append(delays)
	return(game)

def printGame(game):
	'''function prints game plan
	in human readable form'''
	for i in range(len(game[0])):
		print(str(game[0][i]) + "=>" + str(game[1][i][:6]))
	print("xxxxxxxxxxxxxxxxxxx")
	return(0)

def playGame(game):
	'''function collects delays from game plan
	and returns expected delay'''
	delays = []
	for i in range(1000):
		select = int(random.random() * len(game[0]))
		field = int(random.random() * len(game[1][select]))
		delays.append(int(game[1][select][field]))
	#calculates average of the delay list
	result = int(sum(delays)/len(delays))
	return(result)

################################################################################

nodeName = ("data/small/100_nodeList.csv")
testName = ("data/small/100_test.csv")
testFile = open(testName, "r")
forecastName = ("data/small/100_forecast.csv")
#forecastFile = open(forecastName, "w")
game = [[],[]]
line = testFile.readline()
while (line != ""):
	elements = line.split(",")
	#write first line of the file
	if elements[0] == "carrier":
		line = testFile.readline()
		#forecastFile.write(line)
		continue
	#prepare gameplan
	game = prepareGame(elements, nodeName)
	result = playGame(game)
	print(result)
	#next line
	line = testFile.readline()

#close all files

testFile.close()
#forecastFile.close()


