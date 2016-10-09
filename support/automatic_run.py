import os
import datetime
import learn
import forecast
import generator

#TODO common routines to separate file
def infoMsg (message):
	'''function writes formated message'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return 0

### SETTING ###

# FILES #

#where is your source file located?
source = "data/delays_dataset.csv"
#where do you want to store output data?
folder = "output/test/"
#do you want a prefix for output data?
prefix = "X_"

# GENERATOR #

#do you want to generate tes data?
generate = False
#how many learn files do you want?
genNum = 52
#how many lines for each learn file do you want
genLines = 1E6
#how many lines for each test file do you want?
genTest = 1E3


# LEARNING #

#do you wat to generate nodeList from test data?
learning = False
#do you want to load multiple files?
iterative = True
#do you want to generate vertList as well?
genVert = False

# FORECAST #

#do you want to generate forecast file?
prediction = True

# RESULT #

#do you want to calculate result and generte report?
result = True

################################################################################
### MULTIPLE file prediction ###

#generate testing files
if generate == True:
	if not os.path.isdir(folder):
		os.mkdir(folder)
	generator.generate(source, folder, prefix, genNum, genLines, genTest)
	infoMsg("GENERATING Completed")
#generate learn data
if learning == True and iterative == True:
	#learn.learn(folder, prefix, numGen, vertGen)
	for i in range(genNum):
		filename = folder + prefix + str(i) + "_learn.csv"
		#MAIN function
		nodeList, vertList = learn.learnData(filename, genVert)
		#save the result
		learn.writeNode(nodeList, folder, prefix + str(i))
		if genVert == True:
			learn.writeVert(vertList, folder, prefix + str(i))
	#write info, that job has been finished
	infoMsg("LEARNING Completed")
#predict delay anf fill the test file
if prediction == True:
	for i in range(genNum):
		nodeName = (folder + prefix + str(i) + "_nodeList.csv")
		testName = (folder + prefix + str(i) + "_test.csv")
		forecastName = (folder + prefix + str(i) + "_forecast.csv")
		forecast.forecast(nodeName, testName, forecastName)

################################################################################
### SINGLE file prediction ###

#CAREFULL YOU MUST BE

#Select the file
	#filename = 'data/delays_dataset.csv'
	#filename = 'data/1mio_dataset.csv'
	#filename = 'data/100k_dataset.csv'
	#filename = 'data/10k_dataset.csv'
	#filename = 'data/100_dataset.csv'
	#filename = 'data/10_dataset.csv'

