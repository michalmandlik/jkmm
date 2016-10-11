#!/usr/bin/python3

import sqlite3 as lite
import sys
import os
import time
import datetime
import random
import marshal

#TODO verticies ...
#TODO easy parameter selection
#TODO prepare test data for single test
#TODO separate game loading function
#TODO return delay 0 if there are no data in nodes ???

#NOTE it is expected 200k lines in testing dataset delays.csv

def loadDB(dbName, dataName, table):
	'''
	Function creates SQLite database and loads data from csv file.
	
	Example csv file with header and just one line:
	carrier,fltno,dep_apt,arr_apt,sched_departure_date,scheduled_departure,\
	actual_departure
	AZ,611,JFK,FCO,2016-04-29,2016-04-29 22:05:00,2016-04-29 21:55:00

	If the actual_departure is missing, the line is not loaded
	into the database.

	nameDB: string, path to database file
	dataFile: string, path to csv dataset
	'''
	dataFile = open(dataName)
	totalLines = int(os.stat("data/delays_dataset_clean.csv").st_size / 66)
	con = lite.connect(dbName)
	infoMsg("LOAD started", True)
	#writing the database
	i = 0
	fault = 0
	with con:
		cur = con.cursor()
		#prepare database table
		cur.execute("DROP TABLE IF EXISTS " + table)
		cur.execute("CREATE TABLE " + table + "(carrier TEXT, fltno TEXT, " +
										"dep_apt TEXT, arr_apt TEXT, " +
										"month TEXT, day TEXT, hour TEXT, " +
										"sch_dep TEXT, delay INT)")
		#skip first line
		line = dataFile.readline()
		ele = line.split(",")
		if ele[0] == "carrier":
			line = dataFile.readline()
			ele = line.split(",")
		else:
			print("ERR")
			return(1)		
		#read line by line and save elements to a list of tuples
		data = []
		while (line != ""):
			#skip lines with missing actual_departure
			if ele[-1][:-1] == "":
				fault += 1
			else:
				#if loading prediction dataset, set delay really high
				delay = 0
				if len(ele) == 6:
					delay = 99999
					ele[5] = ele[5][:-1]					
				else:
					delay = calcDelay(ele[5], ele[6][:-1])
				#split time to more relevant chunks
				t = time.strptime(str(ele[5]), "%Y-%m-%d %H:%M:%S" )
				month = t[1]
				day = t[6] #weekday
				hour = int(t[3]/6) #hour range 0-6, 6-12, 12-18, 18-24
				#apend all data to the list
				data.append((ele[0], ele[1], ele[2], ele[3],
							str(month), str(day), str(hour), 
							ele[5], delay))
			#next line
			line = dataFile.readline()
			ele = line.split(",")
			#every 1E6 lines, write to database
			i += 1
			if (i % 1E6) == 0 or len(line) == 0:
				infoMsg("LOAD " + str(int(i/1e6)) +
						"M lines written to DB, " +
						str(int(100*((i+fault)/1e6)/(totalLines / 1e6))) +
						"% processed", False)
				cur.executemany("INSERT INTO " + table + " VALUES" +
								"(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
				data = []
	con.close()
	infoMsg("LOAD done, " + str(i) + " lines written, " 
						+ str(fault) + " faulty lines", True)
	return(0)

def printDB(dbName, table):
	'''
	Supporting function. It prints the database to the standart output.

	dbName: string, path to database file
	'''
	con = lite.connect(dbName)
	with con:	
		cur = con.cursor()
		cur.execute("SELECT * FROM " + table)
		for row in cur:
			print(str(row)[:100])
	con.close()
	return(0)

def exportDB(dbName, exportName):
	'''
	Function reads through rows in the database and it writes each
	line to the CVS dataset file.

	Example format of the CSV dataset:
	carrier,fltno,dep_apt,arr_apt,sched_departure_date,scheduled_departure,\
	actual_departure
	AZ,611,JFK,FCO,2016-04-29,2016-04-29 22:05:00,2016-04-29 21:55:00

	dbName: string, path to database file
	exportName: string, path to the exported file
	'''
	infoMsg("EXPO started", True)
	#prepare file and write first line
	exportFile = open(exportName, "w")
	firstLine = ("carrier,fltno,dep_apt,arr_apt," + 
				"sched_departure_date,scheduled_departure,actual_departure\n")
	exportFile.write(firstLine)
	con = lite.connect(dbName)
	cur = con.cursor()
	cur.execute('SELECT * FROM Data')
	#read database line by line and write it to the file
	i = 0
	for row in cur:
		sch_dep = row[-2][:9]
		act_dep = reverseDelay(row[-2], int(row[-1]))
		line = (row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," +
				sch_dep + "," + row[-2] + "," + act_dep + "\n")
		exportFile.write(line)
		i += 1
		if (i % 5E4) == 0:
			infoMsg("EXPO " + str(int(i/1E3)) + "k lines exported", False)
	exportFile.close()
	con.close()
	infoMsg("EXPO done", True)
	return(0)

def removeDuplicity(dbName):
	'''
	Function search database and removes duplicit lines.
	If there are two or more lines with same data and just different
	actual_departure item, then only the line with lowes difference of
	scheduled departure - actual_departure will be loaded into the database.

	dbName: string, path to database file
	'''
	infoMsg("DUPL started", True)
	con = lite.connect(dbName)
	count = 0
	with con:	
		cur = con.cursor()
		cur.execute("SELECT Count() FROM Data")
		count = cur.fetchone()[0]
		#create backup table
		cur.execute("DROP TABLE IF EXISTS Backup")
		cur.execute("CREATE TABLE  Backup(carrier TEXT, fltno TEXT, " +
										"dep_apt TEXT, arr_apt TEXT, " +
										"month INT, day INT, hour INT, " +
										"sch_dep TEXT, delay INT)")
		infoMsg("DUPL backup created", False)
		#write all lines from data to backup
		#if there is duplicity, take the one with max delay		
		cur.execute("INSERT INTO Backup " +
					"SELECT carrier,fltno,dep_apt,arr_apt," +
							"month,day,hour,sch_dep, " + 
							"Max(delay) delay " +
		 			"FROM Data " +
		 			"GROUP BY carrier,fltno,dep_apt,arr_apt,sch_dep")
		infoMsg("DUPL removing finished", True)	
		#delete Data and rename Backup to Data
		cur.execute("DROP TABLE Data")
		cur.execute("ALTER TABLE Backup RENAME TO Data")
		cur.execute("SELECT Count() FROM Data")
		count = count - cur.fetchone()[0]
	con.close()
	infoMsg("DUPL done, " + str(count) + " duplicities removed", True)
	return(0)

def calcDelay (sch_dep, act_dep):
	'''
	Function returns dealy in minutes calculated from scheduled_departure
	and actual departure, both formated YYYY-MM-DD HH:MM:SS

	sch_dep: string scheduled departure
	act_dep: string, actual departure

	delay: int, number of minutes between sch_dep and act_dep
	'''
	sch = sch_dep.split(" ")
	act = act_dep.split(" ")
	delay = 0
	#if both times are within one day, use simple and fast method
	if sch[0] == act[0]:
		sch = sch[1].split(":")
		act = act[1].split(":")
		delay += (int(act[0]) - int(sch[0])) * 60 #hours
		delay += (int(act[1]) - int(sch[1])) #minutes
	#else use inbuilt robust and slow function
	else:
		sch_dep = datetime.datetime.strptime(sch_dep, "%Y-%m-%d %H:%M:%S")
		act_dep = datetime.datetime.strptime(act_dep, "%Y-%m-%d %H:%M:%S")
		delay = int(((act_dep - sch_dep).total_seconds())/60)
	return (delay)

def reverseDelay (sch_dep, delay):
	'''
	Function returns dealy in minutes calculated from scheduled_departure
	and actual departure, both formated YYYY-MM-DD HH:MM:SS

	sch_dep: string scheduled departure
	delay: int, number of minutes between sch_dep and act_dep

	act_dep: string, actual departure
	'''
	sch = sch_dep.split(" ")
	sch = sch[1].split(":")
	sch = int(sch[0]) * 60 + int(sch[1])
	#if both times are within one day, use simple and fast method
	if int(sch) + delay > 0 and int(sch) + delay < 24 * 60 :
		act = sch + delay
		hours = int(act / 60)
		minutes = int(act % 60)
		time = (format(str(hours).zfill(2)) + ":" + 
				format(str(minutes).zfill(2)) + ":" + "00")
		date = sch_dep.split(" ")
		act_dep = str(date[0] + " " + time)
	else:
		act_dep = datetime.datetime.strptime(sch_dep, "%Y-%m-%d %H:%M:%S")
		act_dep += datetime.timedelta(minutes = delay)
		act_dep = act_dep.strftime("%Y-%m-%d %H:%M:%S")
	return (act_dep)

def infoMsg(message, log):
	'''
	Supporting function prints actual time and defined message.

	message: string, message printed to the stdout
	log: bool, if true write message to log file
	'''
	logName = "output/prediction.log"
	#create blank log if it is not existing
	if not os.path.isfile(logName):
		logFile = open(logName, "w")
		logFile.close()
	t = datetime.datetime.now()
	msg = t.strftime("%H:%M:%S") + " " + message
	print(msg)
	#write to log
	if log == True:
		logFile = open(logName, "a")
		logFile.write(msg + "\n")
		logFile.close()
	return(0)

def playGame(game):
	'''
	Function goes through delays each relevant element. It calculates
	final delay and returns it.
	It choose next element randomly and also randomly chose the delay from its
	list of delays. Probability of choosing the element is weighted by its
	size od delay list.
	Resulting delay is calculated as average of choosen delays
	
	game: list of lists, element name with coresponding list of delays

	result: int, final delay
	'''
	delays = []
	steps = 1000
	#weigth for carrier,fltno, dep_apt, arr_apt, month, day, hour
	weigth = [100, 100, 100, 100, 100, 100, 100]
	prob = []
	#calculate preference of the elements
	for i in range(len(game[1])):
		#prob.append(len(game[1][i]) * weigth[i])
		prob.append(weigth[i])
	#gather delays according weights
	for i in range(steps):
		#select which game element will be used next
		a = int(random.random() * (sum(prob) - 1))
		for n in range(len(prob)):
			#empty element
			if prob[n] == 0:
				continue
			if int(a / prob[n]) == 0:
				a = n
				break
			else:
				a = a - prob[n]
		#check if game element contains some data
		if (len(game[1][a]) == 0):
			continue
		#select which delay from element will be gathered
		b = int(random.random() * (len(game[1][a]) - 1))
		delays.append(game[1][a][b])
	#calculate average from delays list
	result = int(sum(delays) / len(delays))
	return (result)

def predictDelays(dbName, predictName):
	'''
	Function opens file with data for prediction. It loads the file to the
	databes. Then it runs "game" for each line of the file and writes
	predicted delay to the database. At the end it exports the file.

	dbName: string, path to database file
	predictName: string, pat to file with data for prediction
	'''
	#open DB, create table Pred and load data from prediction file
	infoMsg("PRED prediction started", True)
	loadDB(dbName, predictName, "Pred")
	con = lite.connect(dbName)	
	with con:		
		cur = con.cursor()
		ele = cur.execute("SELECT * FROM Pred")
		ele = ele.fetchall()
		#setup which nodes will be used
		#NODES
		ids = ["carrier","fltno","dep_apt","arr_apt","month","day","hour"]
		#Load time data in front of the algoritm - month, days, hours
		timeDelays = [[], [], []]
		timeLen = (12, 7, 4)
		for i in range(len(timeDelays)):
			for n in range(timeLen[i]):
				cur.execute("SELECT delay FROM Nodes" +
							" WHERE id = \'" + str(i) + "@" + 
											ids[i-3] + "\'" +
							" LIMIT 1")
				delays = cur.fetchall()
				if len(delays) != 0:
					timeDelays[i].append(marshal.loads(delays[0][0]))
				else:
					timeDelays[i].append([])
		count = 0
		for row in ele:
			#load all element names to the first list
			game = [[],[]]
			#prepare list for game
			for i in range(len(ids)):
				game[0].append(row[i])
			#TIME 2000 us / cycle (4 param)
			#TIME 30 000 us / cycle (7 param)
			for i in range(len(ids)):
				#if loading time delays, use preloaded data
				if i >= ids.index("month"):
					x = game[0][i].split("@")
					t = int(x[0])
					game[1].append(timeDelays[i-4][t])
					continue
				element = (game[0][i], ids[i])
				#load data from node list
				cur.execute("SELECT delay FROM Nodes" +
							" WHERE id = \'" + game[0][i] + "@" +
												ids[i] + "\'" +
							" LIMIT 1")
				delays = cur.fetchall()
				#check if the result is empty
				if len(delays) != 0:
					delays = marshal.loads(delays[0][0])
					game[1].append(delays)
				else:
					game[1].append([])
			#check if game is not empty
			#TIME < 5000 us / cycle
			gameSum = 0
			for i in range(len(game[1])):
				gameSum += len(game[1][i])
			if gameSum == 0:
				delay = 0
			else:
				#predict delay
				delay = playGame(game)
			#write delay to the database
			#TIME < 3000 us / cycle
			#NODES
			cur.execute("UPDATE Pred " +
						"SET delay = " + str(delay) +
						" WHERE carrier = \'" + game[0][0] + "\'" +
							" AND fltno = \'" + game[0][1] + "\'" +
							" AND dep_apt = \'" + game[0][2] + "\'" +
							" AND arr_apt = \'" + game[0][3] + "\'" +
							#" AND month = \'" + game[0][4] + "\'" +
							#" AND day = \'" + game[0][5] + "\'" +
							#" AND hour = \'" + game[0][6] + "\'" +
							" AND sch_dep = \'" + row[-2] + "\'" +
							" AND delay = 99999")
			con.commit()
			#progress info
			count += 1
			if (count % 1e3) == 0:
				infoMsg("PRED " + str(count) + " lines processed, " + 
						str(int(count/len(ele))) + "% done", False)
	con.commit()
	con.close()
	infoMsg("PRED prediction done", True)
	return(0)

def evaluatePrediction(dbName, controlName):
	'''
	Funtion reads the database and calculates difference between
	predicted and real delays. It writes the report with results.

	dbName: string, path to database file
	controlName: string, path to the file with control values

	diff: int, total difference of delays
	count: int, number of predicted values
	'''
	infoMsg("EVAL evaluating the prediction", True)
	loadDB(dbName, controlName, "Control")
	con = lite.connect(dbName)
	diff = 0
	count = 0
	tables = ["Pred", "Control", "Data"]
	delays = [[], [], []]
	with con:		
		cur = con.cursor()
		#delays from prediction
		for i in range(len(tables)):
			values = cur.execute("SELECT delay FROM " + tables[i])
			values = values.fetchall()
			for n in range(len(values)):
				delays[i].append(values[n][0])
		#calculate results
		count = len(delays[0])
		predErr = (sum(delays[0]) - sum(delays[1])) / count
		zeroErr = sum(delays[1]) / count
		avgErr = ((count * sum(delays[2]) / len(delays[2])) - sum(delays[1])) / count
	con.close()
	infoMsg("EVAL evaluating done", True)
	return((predErr, zeroErr, avgErr))

def evaluationReport(evaluation, predictName, multi):
	'''
	Function prints the report with prediction precision.
	The report is also written to the log file.
	
	evaluation: tuple or list of tuples, data with prediction precision
	predictName: string, file name, which wil be in report
	multi: bool, if true than report for multiple files will be printed out
	'''
	if multi:
		result = [0.0, 0.0, 0.0]
		for i in range(len(evaluation)):
			result[0] += float(evaluation[0])
			result[1] += float(evaluation[1])
			result[2] += float(evaluation[2])
		result[0] = result[0] / float(len(evaluation))
		result[1] = result[1] / float(len(evaluation))
		result[2] = result[2] / float(len(evaluation))
		evaluation = result
	#print the message	
	infoMsg("=====================================",True)
	infoMsg("File: " + predictName,True)
	infoMsg("Method: nodeList + average",True)
	infoMsg("Prediction error: " + format(evaluation[0], '.2f') + " min",True)
	x = 100 * (abs(evaluation[0]) - abs(evaluation[1])) / abs(evaluation[1])
	infoMsg("Zero error: " + format(evaluation[1], '.2f') +
			" min, delta: " + format(x, '.2f') + "%", True)
	x = 100 * (abs(evaluation[0]) - abs(evaluation[2])) / abs(evaluation[2])
	infoMsg("Average error: " + format(evaluation[2], '.2f') +
			" min, delta:" + format(x, '.2f') + "%", True)
	infoMsg("=====================================",True)
	return(0)

def prepareTestSet(dbName, output, num):
	'''
	Function splits original data to the smaller sets. It creates
	files for learning, files for testing and also control file
	for evaluating of prediction results.

	dbName: string, path to database file
	output: string, path to the output folder, to store the test set
	num: int, count of test files generated from test set
	'''
	infoMsg("SET preparation of test set started", True)
	#rate between lear lines count and test lines count
	countLearn = 1e6
	countPredict = 1e4
	#initialize "num" files for learn, predict and control 
	files = [[],[],[]]
	names = ["learn", "predict", "control"]
	firstLine = ("carrier,fltno,dep_apt,arr_apt," + 
				"sched_departure_date,scheduled_departure,actual_departure\n")
	for i in range(num):
		for n in range(len(names)):
			name = output + str(i) + "_" + names[n] + ".csv"
			files[n].append(open(name, "w"))
			files[n][i].write(firstLine)
	#randomly select file and write the line into it
	con = lite.connect(dbName)
	with con:	
		cur = con.cursor()
		cur.execute("SELECT * FROM Data ORDER BY sch_dep")
		i = 0
		n = 0
		x = 0
		for row in cur:
			sch_dep = row[-2][:9]
			act_dep = reverseDelay(row[-2], int(row[-1]))
			line = (row[0] + "," + row[1] + "," + row[2] + "," + row[3] + 
					"," + sch_dep + "," + row[-2] + "," + act_dep + "\n")
			if n > countLearn:
				#predict and control file
				c = line[:-21] + "\n"
				files[1][x].write(c)
				files[2][x].write(line)
				n += 1
			else:
				#learn file
				files[0][x].write(line)
				n += 1
			if n == (countLearn + countPredict):
				n = 0
				x += 1
				if x >= num:
					break
			i += 1
			if (i % 1E6) == 0:
				infoMsg("SET " + str(int(i/1E6)) + "M lines exported", False)
	#close all open files
	for i in range(num):
		for n in range(len(names)):
			files[n][i].close()
	con.close()
	infoMsg("SET test set generated in \"" + output + "\"", True)
	return(0)

def createNode(dbName):
	'''
	Function creates table of nodes wit corresponding delays.
	These are later used for faster search to prepare the game

	dbName: string, path to database file	
	'''
	con = lite.connect(dbName)
	infoMsg("CNOD started", True)
	#writing the database
	with con:
		cur = con.cursor()
		#prepare database table
		cur.execute("DROP TABLE IF EXISTS Nodes")
		cur.execute("CREATE TABLE Nodes (id TEXT, delay BLOB)")
		ids = ["carrier","fltno","arr_apt","dep_apt","month","hour","day"]
		#search all names for each id
		nodeRaw = [] #(id, type, delays)
		cur.execute("SELECT * FROM Data")
		count = 0
		#load raw delays to the list
		n = 0
		#for row in cur:
		for i in range(len(ids)):
			cur.execute("SELECT " + ids[i] +
						",delay FROM Data ORDER BY " + ids[i])
			last = ""
			nodeList = []
			for row in cur:
				name = str(row[0]) + "@" + str(ids[i])
				#next id			
				if last == "" or name != last:					
					nodeList.append([name,row[1]])
					last = name
				#collect delays
				else:
					nodeList[-1].append(row[1])
			#serialize delays
			for n in range(len(nodeList)):
				nodeList[n] = (nodeList[n][0], marshal.dumps(nodeList[n][1:]))
			#export to DB
			cur.executemany("INSERT INTO Nodes VALUES (?, ?)", nodeList)
			nodeList = []
	cur.execute("CREATE UNIQUE INDEX Prim_Id ON Nodes(id)")
	con.close()	
	infoMsg("CNOD done", True)
	return(0)

def exportNodes (dbName, exportName):
	'''
	Function exports nodes from database to the csv list.
	'''
	infoMsg("ENOD started", True)
	#prepare file and write first line
	exportFile = open(exportName, "w")
	firstLine = ("id,delay,count,delay,count\n")
	exportFile.write(firstLine)
	#connect to database
	con = lite.connect(dbName)
	cur = con.cursor()
	cur.execute('SELECT * FROM Nodes')
	#read database line by line and write it to the file
	i = 0
	for row in cur:
		x = row[0].split("@")
		name = x[0]
		if x[1] == "carrier":
			c = "!"
		if x[1] == "fltno":
			c = "#"
		if x[1] == "dep_apt":
			c = "$"
		if x[1] == "arr_apt":
			c = "&"
		if x[1] == "month":
			c = ">"
		if x[1] == "day":
			c = "+"
		if x[1] == "hour":	
			c = ":"
		delays = marshal.loads(row[1])
		exportFile.write(c + name + "," + str(delays)[1:-1] + "\n")
		i += 1
		if (i % 1e6) == 0:
			infoMsg("EXPO " + str(int(i/1e6)) + "M lines exported", False)
	exportFile.close()
	con.close()
	infoMsg("EXPO done", True)
	return(0)
	return(0)

def test():
	'''
	Supporting function for testing of crazy ideas.
	'''
	dbName = "output/small/1M_data.db"

	# #DB count lines
	# con = lite.connect(dbName)
	# with con:	
	# 	cur = con.cursor()
	# 	cur.execute("SELECT Count() FROM Data")
	# 	total = cur.fetchone()[0]
	# 	print(total)

	# #DB search min and max
	# con = lite.connect(dbName)
	# with con:	
	# 	cur = con.cursor()
	# 	x = cur.execute("SELECT MIN(sch_dep), MAX(sch_dep) FROM Data")
	# 	print(cur.fetchall())

	#serialize object
	# listicek = [0,1,-3,19]
	# print(listicek)
	# listicek = marshal.dumps(listicek)
	# print(listicek)
	# listicek = marshal.loads(listicek)
	# print(listicek)

	#get unique values from db
	# con = lite.connect(dbName)
	# with con:	
	# 	cur = con.cursor()
	# 	cur.execute("SELECT DISTINCT carrier FROM Data ORDER BY carrier")
	# 	x = cur.fetchall()
	# 	print(x=)

	#indexing the DB
	# con = lite.connect(dbName)
	# with con:	
	#  	cur = con.cursor()
	#  	cur.execute("CREATE INDEX Prim_Id ON Nodes(id)")
	#  	con.commit()
	#  	printDB(dbName, "Nodes")

	return(0)

##############################################################################

### THE PROGRAM ###
def main():

	#RUN SETUP
	#If you want to start testrun with multiple files, set True
	multi = False
	#If you want test run
	testing = True
	#If yo want very small dataset
	fast = False
	#If you want to run prediction for real
	real = False

	#Single fast test
	#multi, testing, fast, real = (False, True, True, False)
	#Single long test
	#multi, testing, fast, real = (False, True, False, False)
	#Multiple load test
	multi, testing, fast, real = (True, True, False, False)
	#Real run
	#multi, testing, fast, real = (False, False, False, True)

	#Run conditions check
	if multi:
		if not testing or fast or real:
			infoMsg("Run conditions are not right!", True)
			return(1)
	if real:
		if multi or testing or fast:
			infoMsg("Run conditions are not right!", True)
			return(1)
	if fast:
		if multi or not testing or real:
			infoMsg("Run conditions are not right!", True)
			return(1)

	#DEFINITIONS
	#path to dataset file	
	if testing:
		dataName = "output/small/1M_learn.csv"
	if fast:
		dataName = "output/small/100_learn.csv"
		#dataName = "data/delays_dataset_clean.csv"
	if multi or real:
		dataName = "data/delays_dataset_clean.csv"
	#path to file, which shoud be predicted
	if testing:	
		predictName = "output/small/1M_predict.csv"
	if fast:
		predictName = "output/small/100_predict.csv"
	if real:
		predictName = "delays.csv"
	#path to file with control data
	if testing:
		controlName = "output/small/1M_control.csv"
	if fast:
		controlName = "output/small/100_control.csv"
	#path, where te result data will be stored
	if testing:
		exportName = "output/small/1M_export.csv"
	if fast:
		exportName = "output/small/100_export.csv"
	if real:
		exportName = "delays.csv"
	#path, where the database will be stored
	if testing:
		dbName = "output/small/1M_data.db"
	if fast:
		dbName = "output/small/100_data.db"	
	if real:
		dbName = "database.db"
	if multi:
		dbName = "output/set/multi.db"
	#export cleaned dataset file
	nodeName = "output//small/nodeList.csv"
	#path to log file
	if testing:
		logName = "output/predict.log"
	if real:
		logName = "predict.log"
	#output dir for testing set and test file count
	outputSet = "output/set/"
	num = 2 #19

	#PROGRAM
	#check if DB already exists
	dbWrite = True
	if os.path.isfile(dbName) and not real:
		print("File \"" + dbName + " already exists.")
		q = input("Do you want to owerwrite it (y/[n]): ")
		if q == "y":
			os.remove(dbName)		
		else:
			dbWrite = False
	#check output directory
	if not os.path.exists("output"):
			os.makedirs("output")

	#multiple file load - testing purposes
	if multi:
		#check directory for test set
		if not os.path.exists(outputSet):
			os.makedirs(outputSet)
		if dbWrite:
			#create source DB from big dataset
			loadDB(dbName, dataName, "Data")
			#prepare testing sets 
			prepareTestSet(dbName, outputSet, num)
		results = []
		for i in range(num):
			#create database for each learn file
			infoMsg("########## MULT set number " + str(i), True)
			dbName = outputSet + str(i) + "_data.db"
			dataName = outputSet + str(i) + "_learn.csv"
			loadDB(dbName, dataName, "Data")
			#create nodes table for faster searching
			createNode(dbName)
			#creaate prediction for each predict file
			predictName = outputSet + str(i) + "_predict.csv"
			predictDelays(dbName, predictName)
			#check the result with the control file
			controlName = outputSet + str(i) + "_control.csv"
			results.append(evaluatePrediction(dbName, controlName))
			#print report and write to the log
			evaluationReport(results[-1], predictName, False)
			#TODO allow export
			#exportName = outputSet + str(i) + "_export.csv"
			#exportDB(dbName, exportName)
		evaluationReport(results, outputSet, True)

	#single file load, final runs
	if testing:
		if dbWrite:
			#create DB from the learn file
			loadDB(dbName, dataName, "Data")
			#check DB for duplicities and remove if any
			removeDuplicity(dbName)
			#create nodes table for faster searching
			createNode(dbName)
		if fast:
			exportNodes(dbName, nodeName)
		#run the prediction
		predictDelays(dbName, predictName)
		#TODO wite results to the file
		#check the result with the control file
		evaluation = evaluatePrediction(dbName, controlName)
		#print report and write to the log
		evaluationReport(evaluation, predictName, False)
		#export result to the csv file
		#TODO export
		#exportDB(dbName, exportName)

	#single file, REAL run, no control, no report
	if real:
		print("jedeme na ostro")
		#TODO implement final run
		if not os.path.isfile(dbName):
			infoMsg("Database " + dbName +" was not found", True)
		if not os.path.isfile(predictName):
			infoMsg("File " + predictName + " was not found", True)
	#if everything was ok, return 0
	return(0)

main()
