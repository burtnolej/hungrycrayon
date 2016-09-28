import sys
from misc_utils_log import Log, logger, Singleton
from misc_utils import thisfuncname, os_file_to_list
from time import sleep
import unittest
import os

class Test_Logger_Member_Function(unittest.TestCase):
    def setUp(self):
        
        self.logdir = "/tmp/log"
        self.log = Log(cacheflag=True,logdir="/tmp/log",
                       pidlogname=False,proclogname=False,
                       reset="")
       
        @logger(self.log)
        def func_1sec(*args,**kwargs):
            sleep(1)
            return(100)
        
        @logger(self.log)
        def func1(*args,**kwargs):
            return(100)
        
        self.func1 = func1
        self.func_1sec = func_1sec
        

    def test_args(self):
        self.func1("xyz",123,list())
        
        logfile = os_file_to_list(self.log.logpath)
        expected_results = "xyz,123,[]".ljust(20) # 20 is size of field

        results = logfile[0].split("|")[7] 
        self.assertEqual(results,expected_results)

    def test_args_kwargs(self):
        self.func1("xyz",123,list(),abc="xyz")
        
        logfile = os_file_to_list(self.log.logpath)
        
        expected_results = "xyz,123,[]".ljust(20) # 20 is size of field

        results = logfile[0].split("|")[7] 
        self.assertEqual(results,expected_results)  
        
        expected_results = "[(\'abc\',\'xyz\')]".ljust(20) # 20 is size of field
        results = logfile[0].split("|")[8]
        self.assertEqual(results,expected_results)  
        
    def tearDown(self):
        self.log.log_clean()
        pass
        
    def test_noargs(self):
        self.func1()
        
        logfile = os_file_to_list(self.log.logpath)
        
        self.assertEquals(logfile[0].split("|")[2].strip(),"INFUNC")
        self.assertEquals(logfile[1].split("|")[2].strip(),"OUTFUNC")
        
    def test_kwargs(self):
        self.func1(abc="xyz")
        
        logfile = os_file_to_list(self.log.logpath)
        expected_results = "[(\'abc\',\'xyz\')]".ljust(20) # 20 is size of field

        results = logfile[0].split("|")[8]
        
        self.assertEqual(results,expected_results)  


    def test_userclassobj_args(self):
        
        class myclass(object):
            pass
        
        self.func1(myclass())
        
        logfile = os_file_to_list(self.log.logpath)
        expected_results = "myclass".ljust(20) # 20 is size of field

        results = logfile[0].split("|")[7] 
        self.assertEqual(results,expected_results)
        
    def test_etime(self):
        self.func_1sec()
        logfile = os_file_to_list(self.log.logpath)
        
        self.assertAlmostEqual(round(float(logfile[1].split("|")[5].strip()),0),1)

    def tearDown(self):
        self.log.log_clean()
        pass
    
class Test_Log(unittest.TestCase):
    
    def setUp(self):
        self.logdir = "/tmp/log"
        self.log = Log(verbosity=10,
                       cacheflag=True,logdir="/tmp/log",
                       pidlogname=False,proclogname=False,
                       reset="") # this forces the singleton to allow a new instance

    def test_debug(self):
        self.log.log(thisfuncname(),7)
        
        logfile = os_file_to_list(self.log.logpath)
        
        self.assertEquals(logfile[0].split("|")[2].strip(),"DEBUG")
        
    def test_extra_msg(self): 
        self.log.log(thisfuncname(),3,foobar='barfoo')
        expected_results = "[('foobar','barfoo')]"
        logfile = os_file_to_list(self.log.logpath)
        
        self.assertEquals(logfile[0].split("|")[9].strip(),expected_results)
        
    def tearDown(self):
        self.log.log_clean()
        pass
           

class Test_Misc(unittest.TestCase):
    
    def setUp(self):
        self.logdir = "/tmp/log"
        self.log = Log(verbosity=10,
                       cacheflag=True,logdir="/tmp/log",
                       pidlogname=False,proclogname=False,
                       reset="") # this forces the singleton to allow a new instance
        
    def test_func_arg(self):
        
        from database_table_util import tbl_col_add
        self.log.log(self,4,func=tbl_col_add,current_value="aaa",new_value="bbb")
        
        logfile = os_file_to_list(self.log.logpath)
        
        expected_results = "[('current_value','aaa'),('new_value','bbb'),('func','tbl_col_add')]"

        self.assertEquals(logfile[0].split("|")[9].strip(),expected_results)
        
    def tearDown(self):
        #self.log.log_clean()
        pass
           
           
class Test_Log_Multiple_Entries(unittest.TestCase):
    
    def setUp(self):
        
        self.logdir = "/tmp/log"
        self.log = Log(verbosity=10,
                       cacheflag=True,logdir="/tmp/log",
                       pidlogname=False,proclogname=False,
                       reset="")
        
        @logger(self.log)
        def func1(*args,**kwargs):
            return(100)
        
        self.func1  = func1
        
    
    def test_1000msg(self):
        
        for i in range(1000):
            self.log.log(thisfuncname(),7,)
            
        self.assertEqual(len(self.log.cache),1000)
        
        self.log.logfile.close()
        
        self.assertEqual(self.log.log_file_length(),999)
        self.log.log_clean()
        

    def test_1000msg_logger(self):
        
        for i in range(1000):
            self.func1()
        
        
        pid = os.getpid()
        self.assertEqual(self.log.stats[str(pid)]['func1']['no'],1000)
        self.log.log_clean()
        
class Test_Log_Names(unittest.TestCase):
    
    def setUp(self):
        
        self.logdir = "/tmp/log"
        self.log = Log(verbosity=10,
                       cacheflag=True,logdir="/tmp/log",
                       pidlogname=True,proclogname=True,
                       reset="")
        
        @logger(self.log)
        def func1(*args,**kwargs):
            return(100)
        
        self.func1  = func1
        
    def test_(self):
        
        logname = os.path.basename(self.log.logpath).split(".")
        self.assertEquals(logname[1],'test_misc_utils_log')
        
        
    
if __name__ == "__main__":

    suite = unittest.TestSuite()
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Logger_Member_Function))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Log))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Log_Multiple_Entries))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Misc))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Log_Names))
    
    unittest.TextTestRunner(verbosity=2).run(suite)
