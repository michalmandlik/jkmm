import os
import random
import datetime

def infoMsg (message):
	'''function writes formated message'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return 0

def writeTest(testName, controlName):
	'''function loads control data file,
	removes actual_departure data and
	it writes test file'''
	controlFile = open(controlName, "r")
	testFile = open(testName, "w")
	#read control file
	line = controlFile.readline()
	elements = line.split(",")
	#write all elements, instead of the last one
	while(line != ""):
		line = ""
		for i in range(len(elements)-1):
			if i > 0:
				line += ","
			line += elements[i]
		line += "\n"	
		testFile.write(line)
		line = controlFile.readline()
		elements = line.split(",")
	#close files
	controlFile.close()
	testFile.close()

def generate(source, folder, prefix, genNum, genLine, genTest):
	'''function generates defined number of file groups, consist of
	learn, test and control file each'''
	infoMsg("GENERATING Test files to \"" + folder + "\"")
	testPost = "_test.csv"
	controlPost = "_control.csv"
	learnPost = "_learn.csv"
	output = folder + prefix
	#file structures
	inputFile = open(source, "r")
	learn = []
	control = []
	#generate files
	for i in range(genNum):
		l = output + str(i) + learnPost
		learn.append([open(l, 'w'), int(genLine)])
		c = output + str(i) + controlPost
		control.append([open(c, 'w'), int(genTest)])
	#writing identical first line to all files
	line = inputFile.readline()
	for i in range(genNum):
		learn[i][0].write(line)
		control[i][0].write(line)
	#main cycle
	count = 0
	i = 0
	while(line != ""):
		#randomly select output file
		a = int(random.random()*genNum)
		b = int((random.random()*(int(genLine) + int(genTest)))/int(genLine))
		line = inputFile.readline()
		#write control data
		if b == 1:
			count = 0
			while 1:
				if count == len(control[0]):
					break
				if control[a][1] > 0 :
					control[a][0].write(line)
					control[a][1] -= 1
					break
				else:
					a -= 1
					count += 1
		#write learn data		
		else:
			count = 0
			while 1:
				if count == len(learn[0]):
					break
				if learn[a][1] > 0 :
					learn[a][0].write(line)
					learn[a][1] -= 1
					break
				else:
					a -= 1
					count += 1
		#print info about progress
		i += 1
		if (i % 3E6) == 0:
			infoMsg("GENERATING " + str(int(100*i/float(53E6))) + "% done")
	#close all files
	for i in range(genNum):
		learn[i][0].close()
		control[i][0].close()
	inputFile.close()
	#generate testing files from control files
	for i in range(genNum):
		testName = folder + prefix + str(i) + testPost
		controlName = folder + prefix + str(i) + controlPost
		writeTest(testName, controlName)
	#if everything is ok return 0
	return(0)
