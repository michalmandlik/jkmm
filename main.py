# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 08:22:05 2016

@author: mma
"""

import pandas as pd
from datetime import datetime
from array import array
import timeit
import matplotlib.pyplot as plt
#import numpy as np
     
     
start = timeit.default_timer()    



NROWS = 20000000
df = pd.read_csv('delays_dataset.csv', nrows = NROWS, low_memory=False)
carrier = df.carrier #you can also use df['column_name']
fltno = df.fltno
dep_apt = df.dep_apt
arr_apt = df.arr_apt
sched_departure_date = df.sched_departure_date
scheduled_departure = df.scheduled_departure
actual_departure = df.actual_departure
stop = timeit.default_timer()   

# 
#delay = array("f")
#for idx in range(NROWS):
#    if  not isinstance(actual_departure[idx], float ):
#        d_schDep = datetime.strptime(scheduled_departure[idx], "%Y-%m-%d %H:%M:%S")
#        d_actDep = datetime.strptime(actual_departure[idx], "%Y-%m-%d %H:%M:%S")
#        time = d_schDep - d_actDep      # time difference
#        delay.insert(idx, (time.total_seconds()/ 60 /60))
#    #   print time.total_seconds()       # format minutes seconds
#    #    print d
#    #    print d.year
#    #    print d.month
#    #    print d.day
#    #    print d.hour
#    #    print d.minute
#    #    print d.second
#    #else:
#        #delay.insert(idx, 0.0)
#    #     print 'nema zpozdeni'
# 
#
#    
#print min(delay)
#print max(delay)
#
#
#
#    
#### visual
#plt.figure(1)                # the first figure
##plt.plot(delay)
#plt.hist(delay, 1000, normed=1, facecolor='g', alpha=0.75)
#
#plt.show()

print stop - start 


