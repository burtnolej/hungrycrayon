
import sys
from scheduler_util import enum
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from datetime_util import MyDT, MyTZ

calendar_enum = enum(tz="US/Eastern",
                     weekdays=[1,2,3,4,5],
                     start_hour=9,
                     start_min=0,
                     end_hour=16,
                     end_min=59)

day_enum = enum(day_name = "day_name", # Monday, Tuesday ...
                day_month = "day_month", # 1-12
                day_year = "day_year", # 2016, 2017 ..
                day_day = "day_day") # 1-28/29/30/31

event_type_enum = enum(freetime=0,
                       academic=1)

def get_days_of_year(year=2016,weekends=False,ignore_holidays=True):
    
    dt_str = "1/1/{0}".format(year)
    mydt = MyDT.str(calendar_enum.tz,dt_str=dt_str,dt_str_fmt='%m/%d/%Y')
    
    days_of_year=[]
    while mydt.dt.year ==year:
        if mydt.dt.isoweekday() in calendar_enum.weekdays:
            day={}
            day[day_enum.day_name] = mydt.dt_to_str_fmt("%A",MyTZ(calendar_enum.tz))
            day[day_enum.day_month] = mydt.dt.month
            day[day_enum.day_year] = mydt.dt.year
            day[day_enum.day_day] = mydt.dt.day
            
            days_of_year.append(day)
        mydt.adddelta(1)
    
    return(days_of_year)