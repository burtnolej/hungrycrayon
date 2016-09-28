
from database_table_util import tbl_rows_get,tbl_create,tbl_rows_insert
from database_util import Database
from time import sleep

lesson_columns = ['dow','lessontype','objtype','period','saveversion','schedule','session',
                  'student','subject','teacher','userobjid','__timestamp','__id']

dows = ['MO','TU','WE','TH','FR']

# loop over dow to keep select statement below max size
for dow in dows:
    store = {}

    database = Database("htmlparser.092816")
    
    with database:
        
        # get the row id's
        columns =  lesson_columns[-2:]
        print columns
        _,ids,_ = tbl_rows_get(database,'lesson',columns,[["dow","=","\""+dow+"\""]])
        
        # get the data columns
        
        columns = lesson_columns[:-2] # take off the auto generated columns
        print columns
        _,rows,_ = tbl_rows_get(database,'lesson',columns,[["dow","=","\""+dow+"\""]])
                
        for i in range(len(rows)):
            unique_key = "^".join(rows[i])
            
            if store.has_key(unique_key) == False:
                store[unique_key] = ids[i]
            else:
                # we can ignore as we only need 1 copy
                pass
            
    database = Database("htmlparser")
    
    # add a new column
    new_lesson_columns = list(lesson_columns)
    new_lesson_columns.insert(0,"prep")
    
    with database:
        try: # create table if it does not exist
            tbl_create(database,'lesson',zip(new_lesson_columns,["text"]*14))
        except:
            pass
        
        rows=[]
        for key in store.keys():
            row=['5']  # add a default value for the new column
            for value in key.split("^")+store[key]:
                row.append("\""+value+"\"")

            rows.append(row)
            
        #print rows
        tbl_rows_insert(database,
                        'lesson',
                        new_lesson_columns,
                        rows)