
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")

from database_util import get_db_tables, create_db_from_schema, sqlite3, NAME_ATTRIB, get_db_table_columns, insert_rows_from_file, \
     get_db_table_rows, db_add_table_complex, db_insert_table_rows, get_db_cursor

from datetime_util import MyDT

schema = "test_schema.xml"

# this will create and close the db_file
db_file = create_db_from_schema(schema)

# insert rows from file
insert_rows_from_file(schema,db_file)

table_calendar_fields = ['day','month','start_hour', 'start_minute', 'end_hour', 'end_minute']

def schedule_class_series(num_instances, frequency, duration, hr_of_day, 
                          min_of_hr, day_of_month, month_of_year):
    ''' a series is a recurring set of events that can be defined by number of instances
    frequency and time and day of the week 
    
    num_instances integer : the number of classes in the series
    frequency integer     : how often the meeting occurs in days (so 7 for weekly)
    day_of_month integer  : day of the first instance
    month_of_year integer : month of the first instance
    '''
    
    # create a date object specifying the time of the first event
    
    dt_str = "{0}/{1}/2016 {2}:{3}:0".format(day_of_month, month_of_year, hr_of_day, min_of_hr)
    mydt = MyDT.str('US/Eastern',dt_str=dt_str,dt_str_fmt='%m/%d/%Y %H:%M:%S')
                    
    #mydt = MyDT.now('US/Eastern')
    #mydt.replace_time(hr_of_day,min_of_day)    
    
    db_rows=[]
    for i in range(num_instances - 1):
        
        if mydt.dt.minute+duration>59:
            mins_left_in_hour = 60-mydt.dt.minute
            end_minute = duration - mins_left_in_hour
            end_hour = mydt.dt.hour+1
        else:
            end_minute = mydt.dt.minute + duration
            end_hour = mydt.dt.hour
            
        db_rows.append([mydt.dt.day, mydt.dt.month, mydt.dt.hour, mydt.dt.minute, end_minute, end_hour])
        
        mydt.adddelta(7) 
        
    conn,c = get_db_cursor(db_file)    
    db_insert_table_rows(c,'calendar',table_calendar_fields,db_rows)
    conn.commit()
    conn.close()

def enroll_student_in_class_series():
    pass

schedule_class_series(20,7,30,9,0,5,21)

# uniqueids


exit()
    
    
    
    