#generate testing data
filename = '../data/delays_dataset.csv'
readF = open(filename, 'r')

filename = '../data/10_dataset.csv'
writeF = open(filename, 'w')
i = 10
x = 0
while x < i :
	line = readF.readline()
	writeF.write (str(line))
	x +=1
writeF.close()

filename = '../data/100_dataset.csv'
writeF = open(filename, 'w')
i = 100
x = 0
while x < i :
	line = readF.readline()
	writeF.write (str(line))
	x +=1
writeF.close()

filename = '../data/1k_dataset.csv'
writeF = open(filename, 'w')
i = 1000
x = 0
while x < i :
	line = readF.readline()
	writeF.write (str(line))
	x +=1
writeF.close()

filename = '../data/10k_dataset.csv'
writeF = open(filename, 'w')
i = 10000
x = 0
while x < i :
	line = readF.readline()
	writeF.write (str(line))
	x +=1
writeF.close()

filename = '../data/100k_dataset.csv'
writeF = open(filename, 'w')
i = 100000
x = 0
while x < i :
	line = readF.readline()
	writeF.write (str(line))
	x +=1
writeF.close()

filename = '../data/1mio_dataset.csv'
writeF = open(filename, 'w')
i = 1000000
x = 0
while x < i :
	line = readF.readline()
	writeF.write (str(line))
	x +=1
writeF.close()

readF.close()
