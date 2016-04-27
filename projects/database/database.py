import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from xml_utils import get_xml_elements,get_xml_element,get_xml_child_elements, get_xml_root
from misc_utils import file_exists, print_dict_of_dict

DB_SCHEMA="./schema.xml"
TEST_DB_SCHEMA="./test_schema.xml"
NAME_ATTRIB='Name'
DB_TYPE="DBType"
DB_TABLE_ATTR=["type","name", "tbl_name","rootpage","sql"]
DB_COLUMN_ATTR=['cid', 'column_name', 'data_type', 'nullable', 'default_value', 'pk_index']

def get_db_cursor(db_file):
    
    if file_exists(db_file):
        conn = sqlite3.connect(db_file)
        return(conn,conn.cursor())
    else:
        raise Exception("file:",db_file," does not exist")
            
def get_db_table_columns(db_cursor,table_name,printout=False):
    columns = db_cursor.execute("PRAGMA table_info("+table_name+")").fetchall()
        
    d = {}
    for column in columns: 
        _d = {}
        for i in range(len(DB_COLUMN_ATTR)):
            _d[DB_COLUMN_ATTR[i]]=column[i]
        d[_d["column_name"]] = _d
    
    if printout: 
        print_dict_of_dict(d)
    
    return(d)

def get_db_tables(db_cursor):
    tables = db_cursor.execute("select * from sqlite_master").fetchall()
    
    d = {}
    for table in tables: 
        _d = {}
        for i in range(len(DB_TABLE_ATTR)):
            _d[DB_TABLE_ATTR[i]]=table[i]
        d[_d["name"]] = _d
    
    return(d)


def get_db_table_rows(db_cursor,table_name):
    values = db_cursor.execute("select * from " + table_name).fetchall()
    
    keys = [description[0] for description in db_cursor.description]
    l=[]
    d={}
    #for i in range(len(values)):
    #    d[keys[i]
    return(keys,values)
    
def db_table_exists(db_cursor,table_name):
    if get_db_tables(db_cursor).has_key(table_name):
        return True
    return False

    
def db_table_column_exists(db_cursor, table_name,column_name):
    if get_db_table_columns(db_cursor,table_name).has_key(column_name):
        return True
    return False
    

def db_table_column_attr(db_cursor, table_name,column_name, column_attr):
    
    return(get_db_table_columns(db_cursor,table_name)[column_name][column_attr])
    
def db_add_table_simple(db_cursor,table,column,column_type):
            
    exec_str = "CREATE TABLE {table} ({column} {column_type})".format(table=table,\
                                                                      column=column,\
                                                                      column_type=column_type)  

    result = db_cursor.execute(exec_str).fetchall()
    return(exec_str,result) 


def db_add_table_complex(db_cursor,table,columns,pk_column_name):
    
    ''' creates a table with multiple columns; provided in arg:columns in a 2d array where column1 is name and 2 type
    column_name is a list containing the names that make up the key. The list will be of length 1 if the pk is not 
    clustered and it will be 0 if there is no pk 
    CREATE TABLE mytable (field1 TEXT,field2 INTEGER,field3 BLOB,PRIMARY KEY (field2, field1)) '''
    
    column_str = ",".join([str(column_name) + " " + str(column_key) for column_name,column_key in columns])
    pk_str  = ",".join(pk_column_name)
    
    if len(pk_column_name)<>0:
        exec_str = "CREATE TABLE {table} ({column},PRIMARY KEY ({pk}))".format(table=table,\
                                                                              column=column_str,\
                                                                              pk=pk_str)
    else:
        exec_str = "CREATE TABLE {table} ({column})".format(table=table,\
                                                            column=column_str)        

    result = db_cursor.execute(exec_str).fetchall()
    return(exec_str,result) 

        

def db_add_table_simple_column(db_cursor,table,column_name,column_type):
    
    exec_str = "ALTER TABLE {table} ADD COLUMN '{column}' {column_type}".format(table=table,\
                                                                                column=column_name,\
                                                                                column_type=column_type)
    result = db_cursor.execute(exec_str).fetchall()
    return(exec_str,result) 

def db_insert_table_rows(db_cursor,table,keys,values):
    
    key_str = ",".join(keys)
    value_str = ",".join(map(str,values))
    
    exec_str = "INSERT INTO {table} ({keys}) VALUES ({values})".format(table=table, \
                                                                       keys=key_str,\
                                                                       values=value_str)
    result = db_cursor.execute(exec_str).fetchall()
    return(exec_str,result) 

def create_db_from_schema(schema):
    
    # for each database in the schema file
    databases = get_xml_elements(schema,".//Database")
    for database in databases:
        
        # get the database name from the schema and construct the dbfile name
        db_file = database.attrib[NAME_ATTRIB] + ".sqlite"
        
        # open a connection to the database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()    
    
        # get the tables from the schema
        xml_tables = get_xml_elements(schema,".//Table")
        for xml_table in xml_tables:
            
            table_name = xml_table.attrib[NAME_ATTRIB]
            
            # if there is an index; create a list of the column names
            try:
                xml_index = get_xml_element(schema,".//Index",xml_table)
                xml_keys = get_xml_elements(schema,".//Key",xml_index)
                pk_defn = [xml_key.text for xml_key in xml_keys]
            except:
                pk_defn = []
            
            col_defn=[]
            
            # from the schema get the name and type of each of the tables columns
            xml_columns = get_xml_elements(schema,".//Column",xml_table)
            for xml_column in xml_columns:
                
                column_name=xml_column.attrib[NAME_ATTRIB]            
                column_type = get_xml_child_elements(xml_column)[DB_TYPE]
                
                # create a list of tuples
                col_defn.append((column_name,column_type))
                
            # create the table
            db_add_table_complex(c,table_name,col_defn,pk_defn)
    
    conn.commit()
    conn.close()
    
    return(db_file)


def _get_values_from_file(data_file,table_name):
    ''' Extracts from a schema file the row value information required to insert into a table
    returns those values in 2 lists, 1 for column names and 1 for values. This allows us to separate
    the data extraction from xml from the data insertion into the DB. Which is useful at least
    for testing where we want to extract the values and assert their existence in a db without inserting'''
    

    rows = get_xml_elements(data_file,".//Row",table)
         
    for row in rows:
        
        key_list = []
        value_list = []
        
        fields = get_xml_elements(data_file,".//Field",row)

        for field in fields:
            field_attrs = get_xml_child_elements(field)    
        
            column_type = db_table_column_attr(c, table_name,str(field_attrs["Key"]), "data_type")
                
            key_list.append(field_attrs["Key"])
            
            if column_type == "INTEGER":
                try:
                    field_val = int(field_attrs["Value"])
                except:
                    raise Exception
            else:
                field_val = field_attrs["Value"]
                
            value_list.append(field_val)    


        return(key_list,value_list)
         
def insert_rows_from_file(data_file,db_file):
    
    conn,c = get_db_cursor(db_file)
    
    tables = get_xml_elements(data_file,".//Table")
    for table in tables:

        table_name = table.attrib[NAME_ATTRIB]  
        rows = get_xml_elements(data_file,".//Row",table)
        
        for row in rows:
            
            key_list = []
            value_list = []
            
            fields = get_xml_elements(data_file,".//Field",row)
    
            for field in fields:
                field_attrs = get_xml_child_elements(field)    
            
                column_type = db_table_column_attr(c, table_name,str(field_attrs["Key"]), "data_type")
                    
                key_list.append(field_attrs["Key"])
                
                if column_type == "INTEGER":
                    try:
                        field_val = int(field_attrs["Value"])
                    except:
                        raise Exception
                else:
                    field_val = field_attrs["Value"]
                    
                value_list.append(field_val)
                
        
            db_insert_table_rows(c, table_name,key_list,value_list)


    conn.commit()
    conn.close()


if __name__ == "__main__":
    #create_db_from_schema(TEST_DB_SCHEMA)
    insert_rows_from_file(TEST_DB_SCHEMA,"test_db.sqlite")