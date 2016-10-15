import database as db

x = db.Database("data/100_learn.db", False)

print('\033[91m' + x.dbName)

x.loadcsv('Data', 'data/100_learn.csv')

