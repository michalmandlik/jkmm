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
for i in range(num):
	l = str(output) + str(i) + str(learnName)
	learn.append((open(l, 'w'), learnCount))
	c = str(output) + str(i) + str(controlName)
	control.append((open(c, 'w'), controlCount))

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
	
	if b ==
	line = inputFile.readline()

#close all files
for i in range(num):
	learn[i][0].close()
	control[i][0].close()
inputFile.close()
print("DONE")
