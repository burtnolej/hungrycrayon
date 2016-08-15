import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_enum import enum
from database_util import schema_data_get, db_enum, Database, \
     tbl_create, tbl_exists
from misc_utils_generic import GenericBase
from datetime import datetime
from types import StringType,IntType

test_db = enum(name="db_name_test",
               tbl_name="tbl_name_test",
               col_defn=[("col_name1","text"),
                         ("col_name2","integer"),
                         ("col_name3","integer"),
                         ("col_name4","integer")],
               tbl_pk_defn = ["col_name1","col_name2"])


class dbtblgeneric(GenericBase):
    '''DBGeneric is fixtures to allow a generic object to write itself into a sqlite3 db'''

    def __init__(self,**kwarg):
	if not kwarg.has_key('database') or not isinstance(kwarg['database'],Database):
	    raise Exception('Database onject must be passed as database=')
	
	self.database = kwarg['database']
	
	kwarg.pop('database')
	
	super(dbtblgeneric,self).__init__(**kwarg)
	
	# these need to be set for persist to work
	self.tbl_col_defn = None
	self.tbl_col_names = None
	self.tbl_row_values = None
	self.tbl_name = None

    def tbl_name_get(self):
	self.tbl_name = self.__class__.__name__

    def tbl_col_defn_get(self,include_internal=True):

	self.tbl_col_defn = []
	self.tbl_col_names = []
	attr = self.attr_get_keyval(include_callable=False,
	                            include_nondataattr=False)

	for _name,_val in attr:
	    _type = "text"
	    try:
		int(_val)
		_type = "integer"
	    except Exception:
		pass
	    self.tbl_col_defn.append((_name,_type))
	    self.tbl_col_names.append(_name)
	    
	# also include useful system info 
	if include_internal == True:
	    self.tbl_col_defn += [('__timestamp','text'),('__id','text')]
	    self.tbl_col_names += ['__timestamp','__id']
	
	
    def tbl_row_value_get(self,include_internal=True):
	#t = [_val for _key,_val in self.attr_get_keyval(include_callable=False,
	#                                                include_nondataattr=False)]
	
	t=[]
	for _key,_val in self.attr_get_keyval(include_callable=False,
	                                                include_nondataattr=False):
	    if isinstance(_val,StringType):
		t.append("\""+_val+"\"")
	    elif not isinstance(_val,IntType):
		if not hasattr(_val,"__repr__"):
		    raise Exception("objects to be written to db need a __repr__ defined")
		t.append("\""+str(_val)+"\"")
	    else:
		t.append(_val)
		
	# also include useful system info 
	if include_internal == True:
	    t.append("\"" + datetime.now().strftime("%H:%M:%S") + "\"")
	    t.append("\"" + self.id + "\"")
	    
	self.tbl_row_values = [t]
 
    def _metadata_set(self,include_internal=True):
	''' if meta data required for db write is not set then set it'''
	if self.tbl_col_defn == None or self.tbl_col_names == None:
	    self.tbl_col_defn_get(include_internal)

	if self.tbl_row_values == None:
	    self.tbl_row_value_get(include_internal)
	    
	if self.tbl_name == None:
	    self.tbl_name_get()
	    
    def persist(self,createtable=True):

	self._metadata_set()

	if not tbl_exists(self.database,self.tbl_name) ==True:
	    tbl_create(self.database,
	               self.tbl_name,
	               self.tbl_col_defn)

	
	tbl_rows_insert(self.database,
                        self.tbl_name,
                        self.tbl_col_names,
                        self.tbl_row_values)

	
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
	tbl_rows_str = "(" + ",".join(map(str,tbl_rows[0])) + ")"

    exec_str = "INSERT INTO {table} ({keys}) VALUES {rows}".format(table=tbl_name, \
                                                                       keys=col_name_str,\
                                                                       rows=tbl_rows_str)
    result = database.execute(exec_str)

    return(exec_str,result) 

def tbl_rows_get(database,tbl_name,fields=None):
    
    
    fieldstr="*"
    if fields<>None:
	fieldstr = ",".join(fields)

    exec_str = "select {fields} from {table}".format(fields=fieldstr,
                                                     table=tbl_name)
    
    results = database.execute(exec_str)
    
    keys = [description[0] for description in database.description()]
    return(keys,results)

def tbl_rows_insert_from_schema(database,schema_file,tbl_name):
    
    datarows = {'tbl_col_name':[],'tbl_rows':[]}
    
    schema_data_get(schema_file,tbl_name,datarows)
    tbl_rows_insert(database,tbl_name,datarows['tbl_col_name'],datarows['tbl_rows'])

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
