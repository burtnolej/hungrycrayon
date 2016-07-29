
import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from xml_utils import get_xml_elements,get_xml_element,get_xml_child_elements, get_xml_root
from misc_utils import os_file_exists, print_dict_of_dict, enum, get_obj_attr_names

db_enum = enum(name_attrib="Name", # keywords used in the schema xml file
               db_type="DBType", # keywords used in the schema xml file
               s3_tbl_attrib=["type","name", "tbl_name","rootpage","sql"], # internal db table columns
               s3_col_attrib=enum(cid=0,column_name=1,data_type=2,\
                                  nullable=3,default_value=4,pk_index=5)) # internal db table columns & index

# keywords used in the schema xml file
col_type_enum = enum(integer="integer",
                     varchar="text")

class Database():
    
    def __init__(self,db_name,remove_flag=False):
        self.name = db_name
        self.remove_flag = remove_flag # remove database on exit (for testing)
   
    def __enter__(self):
        self.open()
        
    def __exit__(self,type,value,traceback):
        self.connection.commit()
        self.connection.close()
        
        if self.remove_flag == True:
            self.remove()
            
    def description(self):
        return(self.cursor.description)
    
    def execute(self,sql_str,singleval=False):
        '''purpose: run a query on the db
              args: sql_str     : sql test to send to sqlite engine
                  : singleval   : true if expecting one field on one row (like a count)
           returns: sql_result  : whatever sqlite returns - usually nested lists'''
        
        if singleval==False:
            sql_result = self.cursor.execute(sql_str).fetchall()
        else:
            sql_result = self.cursor.execute(sql_str).fetchone()[0]
        return(sql_result)
            
    def open(self):
        '''purpose: if filename does not exist it creates it; but at least one table needs to be 
            added for the db to persist'''
        self.connection = sqlite3.connect(self.name+".sqlite")
        self.cursor = self.connection.cursor()

    def remove(self):
        '''purpose: deletes the file on the filesystem containing the sqlite db'''
        from os import remove as osremove
        osremove(self.name+".sqlite")
        
    def tbl_get(self):
        '''purpose: queries db internal table to retreive list of created tables
           returns              : creates member attribute of type dict'''
        sql_result = self.execute("select * from sqlite_master where type='table'")
        
        self.tbl = {}
        for tbl_name in sql_result: 
            _d = {}
            for i in range(len(db_enum.s3_tbl_attrib)):
                _d[db_enum.s3_tbl_attrib[i]]=tbl_name[i]
            self.tbl[_d["name"]] = _d
        
        
    def tbl_exists(self,tbl_name):
        '''purpose: determines if a table exists
              args: tbl_name     : table to detect
           returns:              : true/false '''

        self.tbl_get()
        return(self.tbl.has_key(tbl_name))

def tbl_index_count(database,tbl_name):
    '''purpose: get the number of indexes on a particular table
       returns: creates member attribute of type dict'''
    sql_str = "select count(*) from sqlite_master "
    sql_str += "where type='index'and tbl_name=\"{tbl_name}\"".format(tbl_name=tbl_name)
    
    sql_result = database.execute(sql_str)
    return(sql_result[0][0])

def tbl_index_defn_get(database,tbl_name):
    '''purpose: get the defn of the index on a particular table
       returns: a list containing the column names that make up the key'''
    sql_str = "PRAGMA table_info({tbl_name})".format(tbl_name=tbl_name)
    
    sql_result = database.execute(sql_str)
    
    return([row[db_enum.s3_col_attrib.column_name] for row in sql_result \
           if row[db_enum.s3_col_attrib.pk_index]<>0])
            
def tbl_create(database,tbl_name,col_defn,tbl_pk_defn=[]):
    
    '''purpose: create a table in the database; create index if specificied
          args: database    : object containing db handle
                tbl_name    : name of initial table to create db with; database cannot
                            : be created without a table
                col_defn    : list of tuples of the form (<col_name>,<col_type>) where col_type is
                            : in col_type_enum
                tbl_pk_name : name of the column that contains the primary key if the table
                              has one.
       returns: sql_result  : whatever sqlite returns - usually nested lists'''
    sql_col_str = ",".join([str(col_name) + " " + str(col_type) for col_name,col_type in col_defn])

    sql_str = "CREATE TABLE {tbl_name} ({sql_col_str})".format(tbl_name=tbl_name,\
                                                               sql_col_str=sql_col_str)
    
    # check if a primary key had been specified.
    if len(tbl_pk_defn)<>0:
        sql_pk_str  = ",".join(tbl_pk_defn)
        
        # take off the last ')' and add primary key defn
        sql_str = sql_str[:-1] + ",PRIMARY KEY (" + sql_pk_str + "))"
        
    sql_result = database.execute(sql_str)
    return(sql_result) 

def schema_read(schema_file):
    '''purpose: read in database, table definition from an xml file
          args: xml file
       returns: a dict of the form <name<tbl_name><col_defn,pk_defn,tbl_name>'''
    
    # name shortening ...
    name_enum = db_enum.name_attrib
    type_enum = db_enum.db_type
    
    xml = get_xml_elements
    child_xml = get_xml_child_elements
    
    config = {}
    
    # for each database in the schema file
    _names = [(db_xml.attrib[name_enum],db_xml) for db_xml in xml(schema_file,".//Database")]

    for name,db_xml in _names:
        tbl_config = config[name] = {}

        _tbl_names = [(tbl_xml.attrib[name_enum],tbl_xml) for tbl_xml in xml(schema_file,".//Table",db_xml)]
        
        for tbl_name,tbl_xml in _tbl_names:

            # if there is an index; create a list of the column names
            try:
                tbl_pk_defn = [_key.text for _key in xml(schema_file,".//Key",tbl_xml)]
            except:
                tbl_pk_defn = []

            tbl_col_defn = [(col_xml.attrib[name_enum], child_xml(col_xml)[type_enum]) for col_xml in xml(schema_file,".//Column",tbl_xml)]

            tbl_config[tbl_name] = [tbl_col_defn,tbl_pk_defn,tbl_name]
            
    return(config)

def schema_get(schema):
    '''purpose: get the databases defined by the schema
          args: schema   : in memory representation / dict
       returns: a list'''
    return(schema.keys())

def schema_tbl_get(schema,name):
    '''purpose: get the tables defined by the schema for a particular database
          args: schema   : in memory representation / dict
              : name     : database name
       returns: a list'''
    return([_tbl_name for _tbl_name in schema[name].keys()])

def schema_col_get(schema,name, tbl_name):
    '''purpose: get the columns defined by the schema for a particular database and table
          args: schema   : in memory representation / dict
              : name     : database name
              : tbl_name : table name
       returns: a list'''
    return(schema[name][tbl_name][0])

def schema_tbl_pk_get(schema,name, tbl_name):
    '''purpose: get the index/pk defined by the schema for a particular database and table
          args: schema   : in memory representation / dict
              : name     : database name
              : tbl_name : table name
       returns: a list'''
    return(schema[name][tbl_name][1])

def schema_data_get(schema_file,tbl_name):
    '''purpose: get the data rows defined by the schema for a particular database and table
          args: schema   : xml file
              : name     : database name
              : tbl_name : table name
       returns: tbl_col_name : a list of column names
              : tbl_rows : a list of tuples containing data rows [('250772', 'cycling'), ('260772', 'rowing')]'''
    # name shortening ...    
    xml = get_xml_elements
    child_xml = get_xml_child_elements
        
    rows = [xml(schema_file,".//Field",row_xml) for row_xml in xml(schema_file,".//Row") 
            if row_xml.attrib['Table'] == tbl_name]
    
    tbl_col_name = [child_xml(_row)['Key'] for _row in rows[0]]
    tbl_rows = [tuple(child_xml(_row)['Value'] for _row in row) for row in rows]
    
    return tbl_col_name, tbl_rows
           
def schema_print(schema):
    '''purpose: print out the schema
          args: schema   : in memory representation / dict'''
    print "\n"
    for name,_db in schema.iteritems():
        for tbl_name,_tbl in _db.iteritems():
            for col_name in _tbl[0]:
                print name.ljust(10),tbl_name.ljust(10),col_name

def schema_execute(schema_file):
    '''purpose: create databases and tables as defined in the schema
          args: schema   : xml file'''
    config = schema_read(schema_file)
    for name in config.keys():
        database = Database(name)
        with database:
            for tbl_name in config[name]:
                tbl_col_defn,tbl_pk_defn,_ = config[name][tbl_name]
                tbl_create(database,tbl_name,tbl_col_defn,tbl_pk_defn)

