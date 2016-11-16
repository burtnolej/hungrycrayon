import sys

import unittest

from database_util import Database
from database_table_util import tbl_rows_get

import sswizard_query_utils


class Test_DBID2UserObjID(unittest.TestCase):
    
    def setUp(self):
        self.database = Database("test_DBID2UserObjID")
        
    def test_(self):
        
        expected_results = [[u'02504FB1', u'1.1.2.2.4'], [u'05541D68', u'1.2.2.31.6'], [u'01E0C85F', u'1.4.2.2.4'], [u'01976BA6', u'1.3.2.8.8'], [u'0440F555', u'1.5.2.8.20'], [u'056C78E3', u'1.4.2.2.4'], [u'04AF26D1', u'1.1.2.2.4'], [u'056F4DAD', u'1.2.2.31.6'], [u'0551E950', u'1.5.2.8.20'], [u'01F9F9E6', u'1.3.2.8.8']]
        
        with self.database:
            results = sswizard_query_utils._dbid2userdefid(self.database)
        
        self.assertListEqual(expected_results,results)
        
class Test_asdict(unittest.TestCase):
    
    def setUp(self):
        self.database = Database("test_DBID2UserObjID")
        
    def test_(self):
        
        expected_results = {u'01F9F9E6': u'1.3.2.8.8', u'01976BA6': u'1.3.2.8.8', u'0440F555': u'1.5.2.8.20', u'05541D68': u'1.2.2.31.6', u'0551E950': u'1.5.2.8.20', u'056F4DAD': u'1.2.2.31.6', u'02504FB1': u'1.1.2.2.4', u'056C78E3': u'1.4.2.2.4', u'04AF26D1': u'1.1.2.2.4', u'01E0C85F': u'1.4.2.2.4'}
        
        with self.database:
            _results = sswizard_query_utils._dbid2userdefid(self.database)
            
        results = sswizard_query_utils._asdict(_results)
        
        self.assertEqual(expected_results,results)
        
    def test_asdict(self):
        
        expected_results = {u'01F9F9E6': u'1.3.2.8.8', u'01976BA6': u'1.3.2.8.8', u'0440F555': u'1.5.2.8.20', u'05541D68': u'1.2.2.31.6', u'0551E950': u'1.5.2.8.20', u'056F4DAD': u'1.2.2.31.6', u'02504FB1': u'1.1.2.2.4', u'056C78E3': u'1.4.2.2.4', u'04AF26D1': u'1.1.2.2.4', u'01E0C85F': u'1.4.2.2.4'}
        
        with self.database:
            results = sswizard_query_utils._dbid2userdefid(self.database,asdict=True)
            
        self.assertEqual(expected_results,results)
        
    
if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBID2UserObjID))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_asdict))
    
    

    unittest.TextTestRunner(verbosity=2).run(suite) 