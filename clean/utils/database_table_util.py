import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import enum
from database_util import schema_data_get, db_enum

test_db = enum(name="db_name_test",
               tbl_name="tbl_name_test",
               col_defn=[("col_name1","text"),
                         ("col_name2","integer"),
                         ("col_name3","integer"),
                         ("col_name4","integer")],
               tbl_pk_defn = ["col_name1","col_name2"])

def tbl_rows_insert(database,tbl_name,tbl_col_name,tbl_rows):
    '''purpose: insert 1 or more data rows into a table
	  args: tbl_name    : table to insert into
	      : tbl_col_name: list of columns by name ['start_hour', 'start_minute', 'end_hour', 'end_minute']
	      : tbl_rows    : list of lists of col values [[9, 1, 10, 0], [10, 1, 11, 0]]
       returns: sql_result  : whatever sqlite returns - usually nested lists'''
    col_name_str = ",".join(tbl_col_name)
    if len(tbl_rows)>1:
	tbl_rows_str=",".join(["(" + ",".join(map(str,row)) + ")" for row in tbl_rows])
    else:
	tbl_rows_str = "(" + ",".join(tbl_rows) + ")"

    exec_str = "INSERT INTO {table} ({keys}) VALUES {rows}".format(table=tbl_name, \
                                                                       keys=col_name_str,\
                                                                       rows=tbl_rows_str)
    result = database.execute(exec_str)

    return(exec_str,result) 

def tbl_rows_get(database,tbl_name):
    results = database.execute("select * from " + tbl_name)    
    keys = [description[0] for description in database.description()]
    return(keys,results)

def tbl_rows_insert_from_schema(database,schema_file,tbl_name):
    tbl_col_name, tbl_rows = schema_data_get(schema_file,tbl_name)
    tbl_rows_insert(database,tbl_name,tbl_col_name, tbl_rows)

def tbl_cols_get(database,tbl_name):
    '''purpose: get the column definition for a particular table
       returns: a list containing the column names and types'''
    sql_str = "PRAGMA table_info({tbl_name})".format(tbl_name=tbl_name)

    sql_result = database.execute(sql_str)

    return([(row[db_enum.s3_col_attrib.column_name], row[db_enum.s3_col_attrib.data_type])
            for row in sql_result])

def tbl_col_add(database,tbl_name,col_name,col_type):

    exec_str = "ALTER TABLE {table} ADD COLUMN '{column}' {column_type}".format(table=tbl_name,\
                                                                                column=col_name,\
                                                                                column_type=col_type)
    result = database.execute(exec_str)
    return(result) 

if __name__ == "__main__":
    pass
