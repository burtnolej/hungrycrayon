
import unittest
import sys
from database_util import get_db_tables, create_db,create_db_from_schema, sqlite3, NAME_ATTRIB, get_db_table_columns, insert_rows_from_file, \
     get_db_table_rows, db_add_table_complex, get_db_cursor, db_insert_table_rows
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from xml_utils import get_xml_elements, get_xml_element
from os import remove

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class TestDatabase(unittest.TestCase):
    
    def test_create_pk_table(self):

        database="test"
        table="XYZ"
        fields=[("id","TEXT"),
                ("A","INTEGER"),
                ("B","INTEGER"),
                ("C","INTEGER")]
        
        fields2=["id","A","B","C"]
        
        pk=["id"]
        datarows = (("\"A1\"",1,2,3),
                    ("\"A2\"",4,5,6),
                    ("\"A3\"",7,8,9),
                    ("\"A4\"",10,11,12),
                    ("\"A5\"",13,14,15),
                    ("\"A6\"",16,17,18),
                    ("\"A7\"",19,20,21),
                    ("\"A8\"",22,23,24),
                    ("\"A9\"",25,26,27))          

        # run test; this will create and close the db_file
        db_file = create_db(database,table,pk,fields)
        
        conn,c = get_db_cursor(db_file)

        db_insert_table_rows(c,table,fields2,datarows)
        
        conn.commit()
        conn.close()
        #remove(db_file)

    
class TestDatabaseFromSchema(unittest.TestCase):

    def setUp(self):
        pass
 

    def tearDown(self):
        pass


    def test_create_simple_database(self):
        
        ''' 1 table, 1 column ; this is also serves as a test for creating a database as you cannot create a database
        without creating a table '''
        
        schema = "test_create_simple_database_schema.xml"
        
        # run test; this will create and close the db_file
        db_file = create_db_from_schema(schema)
        
        # open the db and query the tables
        conn = sqlite3.connect(db_file)
        c = conn.cursor()  
        
        # get a list of all the tables created in sqlite
        db_tables =  get_db_tables(c)
                        
        # using the schema; get the tables and columns that should have been created and assert existence of each
        xml_tables = get_xml_elements(schema,".//Table")
        
        for xml_table in xml_tables:
            
            # get the actual name of the table
            xml_table_name = xml_table.attrib[NAME_ATTRIB]
            
            # test that a table of that name exists in the sqlite db
            self.assertTrue(db_tables.has_key(xml_table_name))
            
            # from the sqlite db; get the columns created for that table
            db_table_columns = get_db_table_columns(c,xml_table_name)

            # from the schema; get the columns that should have been created 
            xml_columns = get_xml_elements(schema,".//Column",xml_table)
            
            for xml_column in xml_columns:
                
                # pull out the actual column name
                xml_column_name = xml_column.attrib[NAME_ATTRIB]
                
                # test that a column of that name exists in the sqlite db 
                self.assertTrue(db_table_columns.has_key(xml_column_name))

        conn.close()
        remove(db_file)
        


    def test_insert_numeric_into_simple_database(self):
        
        ''' insert a numeric value (1 row) into a column of type INTEGER '''
        
        schema = "test_insert_numeric_into_simple_database_schema.xml"
        
        # run test; this will create and close the db_file
        db_file = create_db_from_schema(schema)
        
        # insert rows from file
        insert_rows_from_file(schema,db_file)
        
        # open the db and query the tables
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # using the schema; get the tables and columns that should have been created and assert existence of each
        xml_tables = get_xml_elements(schema,".//Table")
        
        for xml_table in xml_tables:
            
            # get the actual name of the table
            xml_table_name = xml_table.attrib[NAME_ATTRIB]
            
            # get the data rows inserted into the sqlite database
            db_rows_keys,db_rows_values = get_db_table_rows(c,xml_table_name)

            # from the schema; get the values that should have been inserted 
            xml_rows = get_xml_elements(schema,".//Row",xml_table)
            
            for xml_row in xml_rows:
                
                xml_fields = get_xml_elements(schema,".//Field",xml_row)
            
        conn.close()
        remove(db_file)
        
    def test_insert_multi_numeric_into_simple_database(self):
        #
        # insert a numeric value (1 row) into a column of type INTEGER 
        #
        
        schema = "test_insert_multi_numeric_into_simple_database_schema.xml"
        
        # run test; this will create and close the db_file
        db_file = create_db_from_schema(schema)
        
        # insert rows from file
        insert_rows_from_file(schema,db_file)
        
        # open the db and query the tables
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # using the schema; get the tables and columns that should have been created and assert existence of each
        xml_tables = get_xml_elements(schema,".//Table")
        
        for xml_table in xml_tables:
            
            # get the actual name of the table
            xml_table_name = xml_table.attrib[NAME_ATTRIB]

            print(get_db_table_rows(c,xml_table_name))
                  
            
        conn.close()
        remove(db_file)
            
class TestTablePrimaryKeyFromSchema(unittest.TestCase):

    def setUp(self):
        pass
 

    def tearDown(self):
        pass
        
    def test_create_pk_table(self):
        #
        # create a table with 2 columns both of which are part of a clustered key
        #
        
        schema = "test_create_pk_table_schema.xml"
        
        # run test; this will create and close the db_file
        db_file = create_db_from_schema(schema)

        # open the db and query the tables
        conn = sqlite3.connect(db_file)
        c = conn.cursor()  
     
        # using the schema; get the tables and columns that should have been created and assert existence of each
        xml_table = get_xml_elements(schema,".//Table")[0]
        
        # get the actual name of the table
        xml_table_name = xml_table.attrib[NAME_ATTRIB]
            
        # from the schema get the columns used for the key

        xml_index = get_xml_element(schema,".//Index",xml_table)
        xml_keys = get_xml_elements(schema,".//Key",xml_index)
        pk_defn = [xml_key.text for xml_key in xml_keys]

        # get the defn of the table created in the db
        d = get_db_table_columns(c,xml_table_name)   
        
        for key in pk_defn:
            
            # test that the pk column exists as a column
            self.assertTrue(d.has_key(key))
            
            # test that the column is flagged as part of a key
            self.assertNotEquals(d[key]['pk_index'],0)
        
        conn.close()
        remove(db_file)
        
    def test_insert_multi_rows_into_pk_table(self):
        #
        # insert 2 valid rows (different keys) into a table with a primary key
        #
        schema = "test_insert_multi_rows_into_pk_table_schema.xml"
        
        # run test; this will create and close the db_file
        db_file = create_db_from_schema(schema)
        
        # insert rows from file
        insert_rows_from_file(schema,db_file)
        
        # open the db and query the tables
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # using the schema; get the tables and columns that should have been created and assert existence of each
        xml_tables = get_xml_elements(schema,".//Table")
        
        for xml_table in xml_tables:
            
            # get the actual name of the table
            xml_table_name = xml_table.attrib[NAME_ATTRIB]
            
            print(get_db_table_rows(c,xml_table_name))              
            
        conn.close()
        remove(db_file)
    
    '''
    def test_insert_multi_rows_into_pk_table_fail(self):
        #
        # insert 1 VALID then 1 INVALID row (dupe keys) into a table with a primary key
        #
        schema = "test_insert_multi_rows_into_pk_table_schema_fail.xml"
        
        # run test; this will create and close the db_file
        db_file = create_db_from_schema(schema)
        
        # insert rows from file
        insert_rows_from_file(schema,db_file)
        
        # open the db and query the tables
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        # using the schema; get the tables and columns that should have been created and assert existence of each
        xml_tables = get_xml_elements(schema,".//Table")
        
        for xml_table in xml_tables:
            
            # get the actual name of the table
            xml_table_name = xml_table.attrib[NAME_ATTRIB]
            
            now we can properly look up the rows as we have a unique key by which to identify them
            
            print get_db_table_rows(c,xml_table_name)                    
            
        conn.close()
        remove(db_file)
    '''
if __name__ == "__main__":

    #unittest.main()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestTablePrimaryKey)
    unittest.TextTestRunner(verbosity=2).run(suite)
    