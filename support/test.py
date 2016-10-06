import datetime

def test():
	date = "2016-04-05 16:23:00"
	print(date)
	date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	print(date)
	x = 6000
	date += datetime.timedelta(minutes = x)
	print(date)