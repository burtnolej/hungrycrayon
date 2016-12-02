import sqlite3
from sqlite3 import OperationalError as DBException

import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)

from misc_utils_enum import enum
from database_util import schema_data_get, db_enum, Database, \
     tbl_create, tbl_exists, tbl_remove, tbl_rename
from misc_utils_generic import GenericBase
from datetime import datetime
from types import StringType,IntType, UnicodeType

test_db = enum(name="db_name_test",
               tbl_name="tbl_name_test",
               col_defn=[("col_name1","text"),
                         ("col_name2","integer"),
                         ("col_name3","integer"),
                         ("col_name4","integer")],
               tbl_pk_defn = ["col_name1","col_name2"])


def dbtblfactory(name):
    def __init__(self,**kwargs):
	dbtblgeneric.__init__(self,**kwargs)
	
    newclass = type(name, (dbtblgeneric,),{'__init__':__init__})
    return newclass    
    
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
	    if isinstance(_val,StringType) or isinstance(_val,UnicodeType):
		t.append("\""+_val+"\"")
	    elif isinstance(_val,IntType):
		t.append(_val)
	    elif not isinstance(_val,IntType):
		if not hasattr(_val,"objid"):
		    raise Exception("objects to be written to db need a objid attribute")
		t.append("\""+str(_val.objid)+"\"")
	    else:
		raise Exception("dont know how to persist this type",_val,type(_val))
		
		
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
	    
    @logger(log)
    def persist(self,createtable=True):

	self._metadata_set()

	if not tbl_exists(self.database,self.tbl_name) ==True:
	    tbl_create(self.database,
	               self.tbl_name,
	               self.tbl_col_defn)

	
	result,exec_str = tbl_rows_insert(self.database,
	                         self.tbl_name,
	                         self.tbl_col_names,
	                         self.tbl_row_values)
	
	return(result,exec_str)

	
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

@logger(log)
def tbl_rows_update(database,tbl_name,row,dryrun=False):
    ''' col_name is name of field to update. pkcol_name is the primary key
    values is a 4 x n grid; 1=field,2=fieldval,3=pkname,4=pkval'''
    exec_str = "UPDATE {table} SET {field}={value} WHERE {pkfield}={pkvalue}".format(table=tbl_name,
                                                                                     field=row[0],
                                                                                     value=row[1],
                                                                                     pkfield=row[2],
                                                                                     pkvalue=row[3])
    
    
    if dryrun==False:
	result = database.execute(exec_str)
	return(exec_str,result) 
    return(exec_str,"")

@logger(log)
def tbl_query(database,exec_str):
    
    results = database.execute(exec_str)
    
    try:
	keys = [description[0] for description in database.description()]
    except TypeError:
	# could be an update
	keys =[]
    
    return(keys,results,exec_str)    


@logger(log)
def tbl_row_delete(database,tbl_name,whereclause=None):
    
    exec_str = "delete from {table}".format(table=tbl_name)
    
    if whereclause <> None and whereclause <> []:
	
	if isinstance(whereclause[0],list) <> True:
	    raise Exception("list of list needs to be provide; changed 9/22")
	
	exec_str = exec_str + " where {0} {1} {2}".format(whereclause[0][0],
	                                                  whereclause[0][1],
	                                                  whereclause[0][2])
    results = database.execute(exec_str)
    
    return(exec_str)


@logger(log)
def tbl_rows_get(database,tbl_name,fields=None,whereclause=None,orderby=None):
    
    fieldstr="*"
    if fields<>None:
	fieldstr = ",".join(fields)

    exec_str = "select {fields} from {table}".format(fields=fieldstr,
                                                     table=tbl_name)
    
    if whereclause <> None and whereclause <> []:
	
	if isinstance(whereclause[0],list) <> True:
	    raise Exception("list of list needs to be provide; changed 9/22")
	
	
	exec_str = exec_str + " where {0} {1} {2}".format(whereclause[0][0],
	                                                  whereclause[0][1],
	                                                  whereclause[0][2])
	
	for i in range(1,len(whereclause)):
	    
	    exec_str = exec_str + " and {0} {1} {2}".format(whereclause[i][0],
		                                              whereclause[i][1],
		                                              whereclause[i][2])

    if orderby <> None:
	exec_str = exec_str + " order by {0}".format(orderby)
	
    #print exec_str
    
    results = database.execute(exec_str)
    
    keys = [description[0] for description in database.description()]
    return(keys,results,exec_str)

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

@logger(log)
def tbl_col_add(database,tbl_name,col_name,col_type="TEXT"):

    exec_str = "ALTER TABLE {table} ADD COLUMN '{column}' {column_type}".format(table=tbl_name,\
                                                                                column=col_name,\
                                                                                column_type=col_type)
    result = database.execute(exec_str)
    return(result) 



def _quotestrs(rows):
    ''' needed if you want to prepare a list of strings for insertion as they will
    need to be double double quoted to be written correctly'''
    newrows=[]
    for row in rows:
	newrow=[]
	for field in row:
	    
	    ''' uncomment this section if you want to keep int's as int's '''
	    try:
	    	int(field)
		newrow.append(field)
	    except:
		newrow.append("'"+str(field)+"'")
	newrows.append(newrow)
    return(newrows)

def _gencoldefn(row,colnames):
    ''' take a row of values and colnames and determine best type; same algorithm as
    used in dbtblgeneric '''
    coldefn=[]
    for i in range(len(colnames)):
	_type = "text"
	try:
	    int(row[i])
	    _type = "integer"
	except Exception:
	    pass
	coldefn.append((colnames[i],_type))
    return coldefn

def tbl_col_update(database,tbl_name,old_col_name,new_col_name):
    ''' sqlite does not support change column name so have implemented a simple
    version; does not handle complex db features which we will not be needing currently'''
       
    col_defn = tbl_cols_get(database,tbl_name)

    new_col_defn=[]
    
    for colname,coltype in col_defn:
	if colname == old_col_name:
	    new_col_defn.append((new_col_name,coltype))
	else:
	    new_col_defn.append((colname,coltype))
	    
    # try to drop tmp table in case left behind from prev run
    try:
	tbl_remove(database,tbl_name+"_new")
    except:
	pass
    
    tbl_create(database,tbl_name+"_new",new_col_defn)
    
    colnames,rows,exec_str = tbl_rows_get(database,tbl_name)
    colindex = colnames.index(old_col_name)
    
    colnames.remove(old_col_name)
    colnames.insert(colindex,new_col_name)

    rows = _quotestrs(rows)
    
    tbl_rows_insert(database,tbl_name+"_new",colnames,rows)
    tbl_remove(database,tbl_name)
    tbl_rename(database,tbl_name+"_new",tbl_name)

def tbl_move(database,database_new,tbl_name,overwrite=False):
    
    # get old table details
    with database:
	col_defn = tbl_cols_get(database,tbl_name)    
	colnames,rows,exec_str = tbl_rows_get(database,tbl_name)
   
    with database_new:
	# create new table details
	if overwrite == True:
	    try:
		tbl_remove(database_new,tbl_name)
	    except:
		pass
	tbl_create(database_new,tbl_name,col_defn)
	
	# insert new data
	rows = _quotestrs(rows)
	tbl_rows_insert(database_new,tbl_name,colnames,rows)

if __name__ == "__main__":
    pass
