import os
import random
from pprint import pprint

#input parameter, input file and num of outputs
num = 52
output = "data/test/"
inputName = "data/delays_dataset.csv"
inputFile = open(inputName, "r")

#create list of output files
learnName = "_learn.csv"
learnCount = int(1E6)
learn = []
controlName = "_control.csv"
controlCount = int(1E3)
control = []
testName = "_test.csv"


for i in range(num):
	l = str(output) + str(i) + str(learnName)
	learn.append([open(l, 'w'), learnCount])
	c = str(output) + str(i) + str(controlName)
	control.append([open(c, 'w'), controlCount])

#writing first line to all files
line = inputFile.readline()
for i in range(num):
	learn[i][0].write(line)
	control[i][0].write(line)

count = 0
x = 0
while(line != ""):
	a = int(random.random()*num)
	b = int((random.random()*(learnCount + controlCount))/learnCount)
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
#close all files
for i in range(num):
	learn[i][0].close()
	control[i][0].close()
inputFile.close()

#open control data files and remove actual departure, write as test file
for i in range(num):
	inputFile = str(output) + str(i) + str(controlName)
	controlFile = open(inputFile, "r")
	outputFile = str(output) + str(i) + str(testName)
	testFile = open(outputFile, "w")
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
print("DONE")
