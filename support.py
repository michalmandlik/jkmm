import datetime

def calcDelay (sch_dep, act_dep):
	'''
	Function returns dealy in minutes calculated from scheduled_departure
	and actual departure, both formated YYYY-MM-DD HH:MM:SS

	sch_dep: string scheduled departure
	act_dep: string, actual departure

	delay: int, number of minutes between sch_dep and act_dep
	'''
	#catch wrong data
	sch = sch_dep.split(" ")
	act = act_dep.split(" ")
	if sch == "" or act == "":
		return("zerodiv")
	if len(sch[1]) != 8 or len(act[1]) != 8:
		return("errlen")
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