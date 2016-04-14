#!/usr/bin/python


import datetime
from sys import path,argv,exit
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import datetime_to_secs,secs_to_datetime, date_to_secs

currentdatetime = "09/08/2013 13:07:51"
currentdate = "09/08/2013"
#print currentdatetime

#currentdate,currenttime = currentdatetime.split()

#d,m,y = currentdate.split("/")
#h,m,s = currenttime.split(":")
#mydate = datetime.date(int(y),int(m),int(d))
#mydatetime = datetime.date(int(y),int(m),int(d),int(h),int(m),int(s))

#origin  = datetime.date(1970,1,1)
#secs =  (mydate-origin).total_seconds()

#print secs
#print datetime.datetime.utcfromtimestamp(secs).strftime('%d/%m/%Y')


secs = datetime_to_secs(currentdatetime)
print secs
secs = date_to_secs(currentdate)
print secs
dt = secs_to_datetime(secs)
print dt
