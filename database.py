import os
import support as s
import time

class Database:
	'''
	Class is used to access the database
	
	tables: list of strings, names of tables in the databas
	names: list of strings, name of columns for data tables
	'''
	#definition of table's and column's names
	tables = ["Data", "Predict", "Nodes", "Edges", "Result", "Control"]
	names = ["carrier", "fltno", "dep_apt", "arr_apt", 
			"month", "day", "hour", "sch_dep", "delay" ]

	def __init__(self, fileName, force):
		'''
		Function initialize Database class and creates empty tables.

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
				if str(table) in ['Data']:
					for name in self.names:
						query += name
						if name == "delay":
							query += " INT)"							
						else:
							query += " TEXT, "
					cur.execute(query)
					continue
				#init data tables
				if str(table) in ['Predict']:
					for name in self.names[:-1]:
						query += name
						if name == self.names[-2]:
							query += " TEXT)"
						else:
							query += " TEXT, "
					cur.execute(query)
					continue
				#init output tables
				if table in ["Result", "Control"]:
					#skip unused columns
					if name in ["month", "day", "hour"]:
						continue
					for name in self.names:
						query += name
						if name == "delay":
							query += " INT)"
						else:
							query += " TEXT, "
					cur.execute(query)
					continue
				else:
					#TODO use infomsg
					print("ERR wrong table name \"" + table + "\"")
					return(-1)
		return(None)

	def loadcsv(self, table, fileName):
		'''
		Function loads csv file with flight data to the selected
		table. It is used to load data for learning and for
		the prediction.

		table: string, name of the selected table
		fileName: string, path to the csv file
		'''

		#write only to defined tables
		if not table in ['Data', 'Predict']:
			#TODO use infomsg
			print("ERR " + table + "is not valid for csv loading")
			return(-1)
		#open file with data
		dataFile = open(fileName, "r")
		totalLines = int(os.stat(fileName).st_size / 66)
		con = sql.connect(self.dbName)
		#writing the database
		with con:
			cur = con.cursor()

			#clean the tablequery

			cur.execute("DELETE FROM " + table)
			#read the first line of csv file
			line = dataFile.readline()
			element = line.split(",")
			if element[0] == "carrier":
				line = dataFile.readline()
				element = line.split(",")
			else:
				#TODO use infomsg for error
				print("ERR")
				return(1)
			#iterate through lines
			fault = 0
			while (line != ""):
				#container for data writing
				data = []
				#skip lines with missing actual_departure
				if element[-1][:-1] == "":
					fault += 1
				else:
					delay = 0
					#if loading csv dataset without trailing coma
					if element[-1] == "":
						element.pop(-1)
					#wrong length of element
					if len(element) < 5 or len(element) > 7:
						#TODO use infomsg
						print("ERR")
						return(-1)
					#Predict dataset
					if len(element) == 6:
						element[5] = element[5][:-1]
					#Learn dataset				
					else:
						delay = s.calcDelay(element[5], element[6][:-1])
					#split time to more relevant chunks
					t = time.strptime(str(element[5]), "%Y-%m-%d %H:%M:%S" )
					month = t[1]
					wday = t[6] #weekday
					hour = int(t[3]/6) #hour range 0-6, 6-12, 12-18, 18-24
					#create data tuple
					data = [element[0], element[1],	element[2], element[3],
							str(month), str(wday), str(hour), element[5]]
					#write to Predict table - delay is not needed
					if table == "Predict":
						cur.execute("INSERT INTO " + table + " VALUES" +
									"(?, ?, ?, ?, ?, ?, ?, ?)", data)
					#write to Learn table including delay
					else:
						data.append(delay)
						cur.execute("INSERT INTO " + table + " VALUES" +
									"(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
				#next line
				line = dataFile.readline()
				element = line.split(",")
			#closing
			con.commit()
		con.close()
		dataFile.close()
		return(0)
