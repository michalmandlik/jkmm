import os
import time
import random
import datetime

def loadIndex(nodeFile):
	#TODO implement loadin index of lines

def loadElement(element, nodeFile, nodeIndex):
	''' function loads dictionary of delays
	for specific id and returns list of delays'''
	delays = []
	dictionary = {}

	#TODO load specific line from nodeFile

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

def prepareGame(elements, nodeFile, nodeIndex):
	'''function returns list of ids with
	associated list of delays'''
	game = [[],[]]
	elements = adjElements(elements)
	for i in range(len(elements)):
		delays = loadElement(elements[i], nodeFile, nodeIndex)
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

#TODO Evaluate time consumption
def playGame(game):
	'''function collects delays from game plan
	and returns expected delay'''
	delays = []
	for i in range(10000):
		select = int(random.random() * len(game[0]))
		field = int(random.random() * len(game[1][select]))
		delays.append(int(game[1][select][field]))
	#calculates average of the delay list
	result = int(sum(delays)/len(delays))
	return(result)

#TODO common routines to separate file
def infoMsg (message):
	'''function writes formated message'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S.%f") + " " + message)
	return 0

################################################################################
def forecast(nodeName, testName, forecastName):
	infoMsg("PREDICTING started for \"" + testName + "\"")
	testFile = open(testName, "r")
	nodeFile = open(nodeName, "r")
	forecastFile = open(forecastName, "w")

	
	game = [[],[]]
	line = testFile.readline()
	#for each line append expected departure time
	i = 0
	while (line != ""):
		elements = line.split(",")
		#write first line of the file
		if elements[0] == "carrier":
			forecastFile.write(line[:-1] + ",actual_departure\n")
			line = testFile.readline()
			continue
		date = datetime.datetime.strptime(elements[-1][:-1], "%Y-%m-%d %H:%M:%S")
		#prepare gameplan
		infoMsg("start")
		game = prepareGame(elements, nodeFile)
		infoMsg("game done")
		result = playGame(game)
		infoMsg("result done")
		if result != 0:
			date += datetime.timedelta(minutes = result)
			forecastFile.write(line[:-1] + "," + str(date) + "\n")
			i += 1
			if (i % 10) == 0:
				infoMsg(str(i))
		#next line
		line = testFile.readline()
	#close all files
	testFile.close()
	forecastFile.close()
	infoMsg("PREDICTING done")


