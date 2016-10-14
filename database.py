import sqlite3 as sql
import sys
import os

class Database:
	#definition of table's and column's names
	tables = ["Data", "Prediction", "Nodes", "Edges", "Result", "Control"]
	names = ["carrier", "dep_apt", "arr_apt", 
			"month", "day", "hour",
			"sch_dep", "delay" ]

	def __init__(self, fileName, force):
		'''
		Function initialize Database class

		fileName: string, path to the database file
		force: bool, if you want to write DB with no prompt set true
		'''
		self.dbName = fileName
		if not force:
			#check if file already exists
			if os.path.isfile(self.dbName):
				#TODO use infomsg
				print("File \"" + self.dbName + " already exists.")
				q = input("Do you want to owerwrite it (y/[n]): ")
				if q == "y":
					os.remove(self.dbName)
				else:	
					return(None)		
		#init tables
		con = sql.connect(self.dbName)
		with con:
			cur = con.cursor()
			#prepare database table
			for table in self.tables:
				cur.execute("DROP TABLE IF EXISTS " + table)
				query = "CREATE TABLE " + table + "("
				#init graph tables
				if table in ["Nodes", "Edges"]:
					query += "name TEXT, delay BLOB)"
					cur.execute(query)
					continue
				#init data tables
				#CONTINUE HERE - if is not working
				if str(table) in ['Data', 'Prediction']:
					for name in self.names:
						query += name
						if name != "delay":
							query += " TEXT, "
						else:
							query += " INT)"
					cur.execute(query)
					continue
				#init output tables
				if table in ["Result", "Control"]:
					#skip unused columns
					if name in ["month", "day", "hour"]:
						continue
					for name in self.names:
						query += name
						if name != "delay":
							query += " TEXT, "
						else:
							query += " INT)"
					cur.execute(query)
					continue
				else:
					#TODO use infomsg
					print("ERR wrong table name \"" + table + "\"")
					return(-1)
		return(None)

	def loadcsv(table, fileName):
		'''
		Function loads csv file with flight data to the selected
		table. It is used to load data for learning and for
		the prediction.

		table: string, name of the selected table
		fileName: string, path to the csv file
		'''

		#write only to defined tables
		if not table in tables[:2]:
			#TODO use infomsg
			print("ERR " + table + "is not valid for csv loading")
			return(-1)
		#open file with data
		dataFile = open(fileName, "r")
		totalLines = int(os.stat(fileName).st_size / 66)
		con = lite.connect(self.dbName)
		#writing the database
		with con:
			cur = con.cursor()
			#clean the table
			cur.execute("DELETE * FROM " + table)

			#closing
			con.commit()
			con.close()
		dataFile.close()
		return(0)

	def printtable(table):
		'''
		function prints selected table to the stdout

		table: string, name of the table
		'''
		return(0)