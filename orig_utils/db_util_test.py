'''
Created on 4 Aug 2014

@author: burtnolej
'''
from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from db_util import DBErrorDupePKeyInsert, DBErrorRecSchemaInvalid
from misc_util import Logger
from error_util import Notification
from stack_util import get_exception_info
import unittest
                
class DBUtilScenarioTests(unittest.TestCase):
   
    def setUp(self): 
        '''
        used instead of setUp as it will only be called once when the class
        is instantiated rather than after every test
        '''  
        class Football(Database):
            pass
                    
        self.football = Football("/Users/burtnolej/gadfly/scripts/","auto")

    def tearDown(self):
        self.football.close()
        self.football.delete_db()
        
    def _compare_pkey_dicts(self,setA,setB,pkey):
        '''
        setA is in the format [{},{},{},,,,]
        setB is in the format {'keya':{},'keyb':{},,,}
        where key is the pkey
        '''
        for _rowA in setA:
            pkey_val = _rowA[pkey]
            _rowB = setB[pkey_val]
            for _fnameA,_fvalA in _rowA.iteritems():
                if _rowB[_fnameA] != _fvalA:
                    print _fnameA,_fvalA,_rowB[_fnameA]
                    return False
                
                
        if len(setA) != len(setB.keys()):
            return False
        return True

    def assertResult(self,table,_exp_results,_posneg):
        
        pkey = table._get_pk()
        self.football.execute("select * from " + table._table_name)
        _act_results = self.football.fetchall_pkey_dict(pkey)
        func = self.assertTrue
        
        if not _posneg:
            func = self.assertFalse
            
        func(self._compare_pkey_dicts(_exp_results,_act_results,pkey))
        func(self._compare_pkey_dicts(_exp_results,self.players._get_table_record_dict(),pkey))

    class Players(DatabaseTable):
        def __init__(self):
            super(DBUtilScenarioTests.Players,self).__init__()
            self._set_pk("last_name")
                              
    def test_create_table_with_pkey(self):
        '''
        this can only be done by adding at least 1 row, as the schema
        is auto generated from the first row
        '''    
        _players = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(DBUtilScenarioTests.Players) # create table object instance   
        self.players.add_list(_players) # add record to table obj inst
        self.football.init_objects_in_db() # create table in gadflydb
        self.football.commit_to_gf() # add records to gadflydb

        self.assertResult(self.players,_players,True)
        
    def test_create_table_with_pkey_NEG(self):
        '''
        this can only be done by adding at least 1 row, as the schema
        is auto generated from the first row
        '''    
        _players = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(DBUtilScenarioTests.Players) # create table object instance   
        self.players.add_list(_players) # add record to table obj inst
        self.football.init_objects_in_db() # create table in gadflydb
        self.football.commit_to_gf() # add records to gadflydb

        _player2 = [{'last_name':'bale','goals':500,'debut':'1/10/13'}]

        self.assertResult(self.players,_player2,False)

    def test_insert_row_table_with_pkey(self):
        '''
        add a schema conforming row
        ''' 
        _player1 = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(DBUtilScenarioTests.Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        _player2 = [{'last_name':'messi','goals':1500,'debut':'1/12/13'}]
        self.players.add_list(_player2)
        self.football.commit_to_gf()
        
        self.assertResult(self.players,_player1+_player2,True)

    def test_insert_dupe_row_table_with_pkey(self):
        '''
        amend on dupe key insert is True so result should be 1 row
        with an amended field
        '''        
        _player1 = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(DBUtilScenarioTests.Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        _player2 = [{'last_name':'bale','goals':300,'debut':'1/12/13'}]
        self.players.add_list(_player2)
        self.football.commit_to_gf()
        
        self.assertResult(self.players,_player2,True)
        
    def test_insert_dupe_row_table_with_pkey_ADI_False(self):
        '''
        amend on dupe key insert is False so should get an exception
        ''' 
        class Players(DatabaseTable):
            def __init__(self):
                super(Players,self).__init__(_allow_amend_dupe_insert=False)
                self._set_pk("last_name")
                #self._allow_amend_dupe_insert = False
                #self._allow_schema_invalid = False
             
        _player1 = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        _player2 = [{'last_name':'bale','goals':300,'debut':'1/12/13'}]
        with self.assertRaises(DBErrorDupePKeyInsert) as e:
            self.players.add_list(_player2)
            self.football.commit_to_gf()
             
        self.assertEqual(e.exception.message, 'bale')
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        _exp_results = self.football.fetchall_pkey_dict(pkey)
        
        self.assertTrue(self._compare_pkey_dicts(_player1,_exp_results,pkey))
        
        #self._compare_pkey_dicts(_exp_results,self.players._get_table_record_dict(),pkey)
        
    
        
    def test_insert_multiple_dupe_rows(self):
        '''
        insert multiple dupes on the same pkey different fields updated
        ''' 
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = False
             
        _player1 = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        _player2 = [{'last_name':'bale','goals':300,'debut':'1/12/13'}]
        self.players.add_list(_player2)
        self.football.commit_to_gf()
        
        _player3 = [{'last_name':'bale','goals':300,'debut':'2/12/13'}]
        self.players.add_list(_player3)
        self.football.commit_to_gf()       
        
        _player4 = [{'last_name':'bale','goals':500,'debut':'2/12/13'}]
        self.players.add_list(_player4)
        self.football.commit_to_gf()
         
        l = Logger('/tmp/log.txt')
        self.football.logmeta.pprint(l.stk_log_handle)
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        results = self.football.fetchall_pkey_dict(pkey)
        
        self.assertTrue(self._compare_pkey_dicts(_player4,results,pkey))
        self.assertTrue(self._compare_pkey_dicts(_player4,self.players._get_table_record_dict(),pkey))
        self.assertTrue(self.players.get_rec_version('bale'),4)
        
        self.football.execute("select _version from players where last_name = 'bale'")
        results = self.football.fetchall_single_val()
        self.assertEqual(results,4)

    def test_insert_multiple_mixed_rows(self):
        '''
        insert multiple dupes on the same pkey different fields updated
        insert dupes on other rows
        insert normal new rows
        ''' 
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = False
             
        _players = [{'last_name':'bale','goals':0,'debut':'1/10/13'},
                    {'last_name':'messi','goals':100,'debut':'2/12/10'}]
        
        self.players = self.football.table(Players)        
        self.players.add_list(_players)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()  
        
        _player4 = [{'last_name':'bale','goals':500,'debut':'2/12/13'}]
        self.players.add_list(_player4)
        self.football.commit_to_gf()
         
        _player5 = [{'last_name':'messi','goals':200,'debut':'2/12/13'}]
        self.players.add_list(_player5)
        self.football.commit_to_gf()
        
        _player6 = [{'last_name':'maradona','goals':500,'debut':'2/12/93'}]
        self.players.add_list(_player6)
        self.football.commit_to_gf()   
         
        l = Logger('/tmp/log.txt')
        self.football.logmeta.pprint(l.stk_log_handle)
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        results = self.football.fetchall_pkey_dict(pkey)
        
        _all_players = _player4+_player5+_player6
        self.assertTrue(self._compare_pkey_dicts(_all_players,results,pkey))
        
        self.assertTrue(self._compare_pkey_dicts(_all_players,self.players._get_table_record_dict(),pkey))
        
    def test_update_field(self):
        '''
        update a field on a specific record
        '''
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = False
             
        _players = [{'last_name':'bale','goals':0,'debut':'1/10/13'},
                    {'last_name':'messi','goals':100,'debut':'2/12/10'}]
        
        self.players = self.football.table(Players)        
        self.players.add_list(_players)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()  
        
        self.players.update_rec('messi','goals',500)
        self.football.commit_to_gf()
        
        self.football.execute("select goals from players where last_name = 'messi'")
        results = self.football.fetchall_single_val()
        self.assertEquals(results,500)
           
        self.football.execute("select _version from players where last_name = 'messi'")
        results = self.football.fetchall_single_val()
        self.assertEqual(results,2)     
        
    def test_delete_record(self):
        '''
        update a field on a specific record
        '''
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = False
             
        _players = [{'last_name':'bale','goals':0,'debut':'1/10/13'},
                    {'last_name':'messi','goals':100,'debut':'2/12/10'}]
        
        self.players = self.football.table(Players)        
        self.players.add_list(_players)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()  
        
        self.players.delete_rec('messi')
        self.football.commit_to_gf()
        
        _players = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]
        
        l = Logger('/tmp/log.txt')
        self.football.logmeta.pprint(l.stk_log_handle)
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        results = self.football.fetchall_pkey_dict(pkey)
        self.assertTrue(self._compare_pkey_dicts(_players,results,pkey))
        
        # then test in memory representation too
        self.assertTrue(self._compare_pkey_dicts(_players,self.players._get_table_record_dict(),pkey))
        
    #def test_delete_rows(self):
    #    pass
    #def test_non_pkey(self):
    #    pass
    #def test_cluster_pkey(self):
    #    pass
    #def test_insert_row_schema_invalid(self)
#        pass     
    # need to test that in mem is also ok not just gadfly db
    # need to make sure can insert rows after main operation has been completed
    
    def test_insert_row_allow_schema_invalid_False(self):
        '''
        add a schema conforming row with schema_valid flag set to True
        ''' 
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = False
             
        _player1 = [{'last_name':'messi','goals':0,'debut':'1/10/13'}]
        
        self.players = self.football.table(Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        _player2 = [{'last_name':'messi','goals':'five hundred','debut':'1/12/13'}]
        self.assertRaises(DBErrorRecSchemaInvalid, self.players.add_list(_player2))
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        results = self.football.fetchall_pkey_dict(pkey)
        self.assertTrue(self._compare_pkey_dicts(_player1,results,pkey))
        
    def test_insert_multi_word_string_fields(self):
        '''
        ie field_value = 'the big brown cat'
        ''' 
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = True
             
        _player1 = [{'last_name':'messi','goals':'the big brown cat','debut':'1/12/13'}]
   
        self.players = self.football.table(Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        results = self.football.fetchall_pkey_dict(pkey)
        self.assertTrue(self._compare_pkey_dicts(_player1,results,pkey))
        
    def test_insert_row_allow_schema_invalid_True(self):
        '''
        add a schema conforming row with schema_valid flag set to True
        ''' 
        class Players(DatabaseTable):
            def __init__(self,*args,**kwargs):
                super(Players,self).__init__(*args,**kwargs)
                self._set_pk("last_name")
                self._allow_amend_dupe_insert = True
                self._allow_schema_invalid = True
             
        _player1 = [{'last_name':'messi','goals':0,'debut':'1/10/13'}]
   
        l = Logger('/tmp/log.txt')
             
        self.players = self.football.table(Players)        
        self.players.add_list(_player1)
        self.football.init_objects_in_db()
        self.football.commit_to_gf()
        
        _player2 = [{'last_name':'messi','goals':'five hundred','debut':'1/12/13'}]
        self.players.add_list(_player2)
        self.football.logmeta.pprint(l.stk_log_handle)
        self.football.commit_to_gf()
        
        pkey = self.players._get_pk()
        self.football.execute("select * from players")
        results = self.football.fetchall_pkey_dict(pkey)
        self.assertTrue(self._compare_pkey_dicts(_player2,results,pkey))
        
if __name__ == "__main__":
    # All not verbose
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    
    # All verbose
    #suite = unittest.TestLoader().loadTestsFromTestCase(DBUtilScenarioTests)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Specific test verbose
    suite = unittest.TestSuite()
    #suite.addTest(DBUtilScenarioTests('test_create_table_with_pkey'))
    #suite.addTest(DBUtilScenarioTests('test_create_table_with_pkey_NEG'))
    #suite.addTest(DBUtilScenarioTests('test_insert_row_table_with_pkey'))
    #suite.addTest(DBUtilScenarioTests('test_insert_dupe_row_table_with_pkey'))
    #suite.addTest(DBUtilScenarioTests('test_insert_multiple_mixed_rows'))
    #suite.addTest(DBUtilScenarioTests('test_insert_multiple_dupe_rows'))
    suite.addTest(DBUtilScenarioTests('test_insert_dupe_row_table_with_pkey_ADI_False'))
    #suite.addTest(DBUtilScenarioTests('test_insert_row_allow_schema_invalid_True'))
    #suite.addTest(DBUtilScenarioTests('test_insert_row_allow_schema_invalid_False'))
    #suite.addTest(DBUtilScenarioTests('test_insert_multi_word_string_fields'))
    #suite.addTest(DBUtilScenarioTests('test_delete_record'))
    unittest.TextTestRunner(verbosity=2).run(suite)


    