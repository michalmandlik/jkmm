#!/usr/bin/python3

import sqlite3 as lite
import sys
import os
import datetime
import hashlib


def loadDB(dbName, dataName):
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
	#remove file if it already exists
	if os.path.isfile(dbName):
		print("File \"" + dbName + " already exists.")
		q = input("Do you want to owerwrite it (y/n): ")
		if q != "y":
			print("ERR")
			return(1) 
		os.remove(dbName)
	dataFile = open(dataName)
	con = lite.connect(dbName)
	infoMsg("LOAD started")
	#writing the database
	with con:
		cur = con.cursor()
		#prepare database table
		cur.execute("CREATE TABLE Data(carrier TEXT, fltno TEXT, " +
										"dep_apt TEXT, arr_apt TEXT, " +
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
		i = 0
		s = 0
		while (line != ""):
			if ele[6][:-1] == "":
				line = dataFile.readline()
				ele = line.split(",")
				s += 1
				continue
			delay = calcDelay(ele[5], ele[6][:-1])
			line = str(ele[0] + ele[1] + ele[2] + 
						ele[3] + ele[5]).encode('utf-8')
			lineHash = (hashlib.md5(line)).hexdigest()
			data.append((ele[0], ele[1], ele[2], ele[3],
						ele[5], delay))
						#next line
			line = dataFile.readline()
			ele = line.split(",")
			#every 1E6 lines, write to database
			i += 1
			if (i % 1E6) == 0 or line == "":
				infoMsg("LOAD " + str(int(i/1e6)) + "M lines written, " +
								str(int(100*((i+s)/1e6)/52)) + "% processed")
				cur.executemany("INSERT INTO Data VALUES"
								"(?, ?, ?, ?, ?, ?)", data)
				data = []
	infoMsg("LOAD done")
	return(0)


def printDB(dbName):
	'''
	Supporting function. It prints the database to the standart output.

	dbName: string, path to database file
	'''
	con = lite.connect(dbName)
	with con:	
		cur = con.cursor()
		cur.execute("SELECT * FROM Data")
		for row in cur:
			print(row)
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
	infoMsg("EXPO started")
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
		sch_dep = row[4][:9]
		act_dep = reverseDelay(row[4], int(row[5]))
		line = (row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," +
				sch_dep + "," + row[4] + "," + act_dep + "\n")
		exportFile.write(line)
		i += 1
		if (i % 1E6) == 0:
			infoMsg("EXPO " + str(int(i/1E6)) + "M lines exported")
	exportFile.close()
	infoMsg("EXPO done")
	return(0)

def removeDuplicity(dbName):
	'''
	Function search database and removes duplicit lines.
	If there are two or more lines with same data and just different
	actual_departure item, then only the line with lowes difference of
	scheduled departure - actual_departure will be loaded into the database.

	dbName: string, path to database file
	'''
	infoMsg("DUPL started")
	con = lite.connect(dbName)

	with con:	
		cur = con.cursor()
		cur.execute("SELECT Count() FROM Data")
		count = cur.fetchone()[0]
		#create backup table
		cur.execute("CREATE TABLE Backup(carrier TEXT, fltno TEXT, " +
		 								"dep_apt TEXT, arr_apt TEXT, " +
		 								"sch_dep TEXT, delay INT)")
		infoMsg("DUPL backup created")
		#write all lines from data to backup
		#if there is duplicity, take the one with max delay		
		cur.execute("INSERT INTO Backup " +
					"SELECT carrier,fltno,dep_apt,arr_apt,sch_dep, " + 
							"Max(delay) delay " +
		 			"FROM Data " +
		 			"GROUP BY carrier,fltno,dep_apt,arr_apt,sch_dep")
		infoMsg("DUPL duplicities removed")	
		#delete Data and rename Backup to Data
		cur.execute("DROP TABLE Data")
		cur.execute("ALTER TABLE Backup RENAME TO Data")
	infoMsg("DUPL done")
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
		time = (format(str(hours).zfill(2)) + ":" + format(str(minutes).zfill(2)) + ":" +"00")
		date = sch_dep.split(" ")
		act_dep = str(date[0] + " " + time)
	else:
		act_dep = datetime.datetime.strptime(sch_dep, "%Y-%m-%d %H:%M:%S")
		act_dep += datetime.timedelta(minutes = delay)
		act_dep = act_dep.strftime("%Y-%m-%d %H:%M:%S")
	return (act_dep)

def infoMsg(message):
	'''
	Supporting function prints actual time and defined message.

	message: string, message printed to the stdout
	'''
	t = datetime.datetime.now()
	print(t.strftime("%H:%M:%S") + " " + message)
	return(0)

def test(dbName):
	'''
	Supporting function for testing crazy ideas.
	'''
	con = lite.connect(dbName)
	with con:	
		cur = con.cursor()
		cur.execute("SELECT Count() FROM Data")
		total = cur.fetchone()[0]
		print(total)
##############################################################################

### THE PROGRAMM ###

#path to original dataset file
dataName = "data/delays_dataset.csv"

#path, where the database will be stored
dbName = "output/test.db"

#export cleaned dataset file
exportName = "output/clean.csv"

loadDB(dbName, dataName)
removeDuplicity(dbName)
exportDB(dbName, exportName)
