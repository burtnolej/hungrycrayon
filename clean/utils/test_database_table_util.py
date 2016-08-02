
import unittest
from sqlite3 import IntegrityError as S3IntegrityError
import sys

from database_util import Database, tbl_create, tbl_index_count, \
     tbl_index_defn_get, schema_read, schema_get, schema_tbl_get, \
     schema_col_get, schema_tbl_pk_get, schema_print, schema_execute, \
     schema_data_get

from database_table_util import tbl_rows_get, tbl_rows_insert, \
     tbl_rows_insert_from_schema, tbl_cols_get, tbl_col_add

sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import enum
from os import remove

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

test_db = enum(name="db_name_test",
               tbl_name="tbl_name_test",
               col_defn=[("col_name1","integer"),
                         ("col_name2","integer"),
                         ("col_name3","integer"),
                         ("col_name4","integer")],
               col_name=["col_name1","col_name2",
                         "col_name3","col_name4",],    
               tbl_pk_defn = ["col_name1","col_name2"],
               tbl_rows=[(1,2,3,4),
                         (5,6,7,8)],
               tbl_rows_dupe_key=[(1,2,3,4),
                                 (1,2,7,8)])

test_db_str = enum(name="db_name_test",
                   tbl_name="tbl_name_test",
                   col_defn=[("col_name1","text")],
                   col_name=["col_name1"],
                   tbl_rows=[("\'foobar\'")])

class TestTableInsert(unittest.TestCase):
    
    def setUp(self):
        self.schema_file = "./test_misc/test_schema_simple.xml"
    
    def test_tbl_rows_insert(self):

        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn)
            tbl_rows_insert(database,test_db.tbl_name,test_db.col_name,
                            test_db.tbl_rows)

        database = Database(test_db.name,True)
        with database:
            col_name,tbl_rows = tbl_rows_get(database,test_db.tbl_name)        
            self.assertListEqual(col_name,test_db.col_name)
            self.assertListEqual(tbl_rows,test_db.tbl_rows)
            
    def test_tbl_rows_insert_str(self):

        database = Database(test_db_str.name)
        
        with database:
            tbl_create(database,test_db_str.tbl_name,test_db_str.col_defn)
            tbl_rows_insert(database,test_db_str.tbl_name,test_db_str.col_name,
                            test_db_str.tbl_rows)

        database = Database(test_db_str.name,True)
        with database:
            self.assertEquals('foobar',database.execute("select col_name1 from tbl_name_test",True))
            
    def test_tbl_rows_insert_dupe_key(self):

        database = Database(test_db.name, True)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn, test_db.tbl_pk_defn)
            
            with self.assertRaises(S3IntegrityError):
                tbl_rows_insert(database,test_db.tbl_name,
                                test_db.col_name,
                                test_db.tbl_rows_dupe_key)
                
    def test_tbl_rows_insert_from_schema(self):
        
        schema_execute(self.schema_file)
        
        database = Database('fitness')
        
        with database:
            tbl_rows_insert_from_schema(database,self.schema_file,'workout')
            
        database = Database('fitness',True)
            
        with database:
            tbl_col_name, tbl_rows = tbl_rows_get(database,'workout')
            self.assertListEqual(tbl_rows,[(250772, 'cycling'), (260772, 'rowing')])
                
        # this is there to force the delete of the 2nd db created but does
        database = Database('diet',True)
        with database:
            pass
        
class TestTableColumnAdd(unittest.TestCase):
    
    def setUp(self):
        self.schema_file = "./test_misc/test_schema_simple.xml"
        
    def test_tbl_cols_get(self):
        
        schema_execute(self.schema_file)
        
        database = Database('fitness', True)
        
        with database:
            self.assertListEqual([('date', 'datetime'), ('type', 'text')],
                                 tbl_cols_get(database,'workout'))
            
        database = Database('diet',True)
        
        with database:
            self.assertListEqual([('name','text'), ('calories','integer')],
                                   tbl_cols_get(database,'food'))
            self.assertListEqual([('type','text'), ('time','datetime')],
                                 tbl_cols_get(database,'meals'))
            
    def test_tbl_col_add(self):
        
        schema_execute(self.schema_file)
        
        database = Database('fitness')
        
        with database:
            tbl_col_add(database,'workout','foobar','text')
        
        database = Database('fitness',True)
            
        with database:
            self.assertListEqual([('date', 'datetime'), ('type', 'text'),('foobar','text')],
                                 tbl_cols_get(database,'workout'))
            
        # this is there to force the delete of the 2nd db created but does
        database = Database('diet',True)
        with database:
            pass
    
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestTableInsert)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTableColumnAdd))
    
    unittest.TextTestRunner(verbosity=2).run(suite)
    