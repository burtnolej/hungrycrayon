import sys

import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils import IDGenerator, generic, os_file_get_wildcard, os_file_to_string, read_pickle, \
     write_pickle, Singleton, enum

import unittest
import time

class test_class():
    attr1=123
    attr2=456
    def myfunc(self):
        return("boo")

class TestPickle(unittest.TestCase):
    
    def setUp(self):
        import pickle
        
        self.obj = test_class()
        self.filename = "/tmp/testpickle.dat"
        
        with open(self.filename, 'w') as f:
            pickle.dump(self.obj, f)  
            
    def test_read_pickle(self):
        obj = read_pickle(self.filename)
        self.assertEquals(obj.myfunc(),'boo')
        
    def test_write_pickle(self):
        write_pickle(self.obj,self.filename)
        self.newobj = read_pickle(self.filename)
        self.assertEquals(self.newobj.myfunc(),'boo')
        
class TestIDGenerator(unittest.TestCase):

    def setUp(self):
        IDGenerator().reset()
        self.idfile = '.id.dat'
        self.idgen = IDGenerator()
        self.idgen.size = 10

    def tearDown(self):
        IDGenerator().reset()
        pass

    def _create_ids(self,num_ids):
        for i in range(num_ids):
            self.idgen.getid()
   
    def test_create30_generatefile(self):
        
        self._create_ids(30)
        
        self.idgen.__del__()
        del self.idgen
        
        self.assertTrue(ospath.isfile(self.idfile))
        
    def test_create10_recover_count10(self):
        
        self._create_ids(10)
        self.idgen.__del__()
        del self.idgen
        self.idgen = IDGenerator()

        self.assertEquals(self.idgen.num_ids(),10)
        self.idgen.__del__()
        del self.idgen
        
    def test_recover_add22_count44(self):

        self._create_ids(22)
        self.idgen.__del__()
        del self.idgen
        
        self.idgen = IDGenerator()
        self._create_ids(22)

        self.assertEquals(self.idgen.num_ids(),44)
        
        self.idgen.__del__()
        del self.idgen
        
    def test_destructor(self):
        self._create_ids(22)
        self.idgen.__del__()
        self.assertTrue(ospath.isfile(self.idfile))
        
    def test_max_retry(self):
        self.idgen.size = 1
        with self.assertRaises(Exception):
            self._create_ids(20)
            
    def test_create10_via_generic(self):
        # this is also testing generic
        class myclass(generic): pass
        
        for i in range(10):
            mc = myclass(__idgen__=True)

        self.assertEquals(self.idgen.num_ids(),10)
        

class TestSingleton(unittest.TestCase):

    def test_basic(self):
        
        class myclass():
            __metaclass__ = Singleton
            
        class myclass_normal():
            pass
        
        address1 = myclass()
        address2 = myclass()
 
        self.assertEqual(address1,address2)
        
        address1 = myclass_normal()
        address2 = myclass_normal()
        
        self.assertNotEqual(address1,address2)
            
class TestIDGeneratorScale(unittest.TestCase):

    def setUp(self):
        IDGenerator().reset()
        self.idfile = '.id.dat'
        self.idgen = IDGenerator()
        self.idgen.size = 10

    def tearDown(self):
        IDGenerator().reset()

    def _create_ids(self,num_ids):
        for i in range(num_ids):
            self.idgen.getid()
   
    def test_create1000(self):
        
        self._create_ids(1000)
        del self.idgen
        
    def test_create1000objects_with_ids(self):
        # this is also testing generic
        class myclass(generic): pass
        
        for i in range(1000):
            mc = myclass(__idgen__=True)
            
        self.assertEquals(self.idgen.num_ids(),1000)
        

class Test_enum(unittest.TestCase):
    ''' enum is a sub class of generic. needs to use the basic
    constructor as it does not need id's etc '''       
    def test_enum(self):
        self.e = enum.basic(blue=1,green=5,yellow=7)
        results = self.e.get_attr(notcallable=True,
                                  notinternal=False)
        self.assertListEqual([('blue',1),('green',5),('yellow',7)],results)
        

class TestOSFiles(unittest.TestCase):
    def setUp(self):
        
        self.dir = "/tmp"
        self.test_file = ospath.join(self.dir,"tmp.txt")
        self.match = ".txt"
        import os
        open(os.path.join(self.dir, 'foobar' + self.match),"w").close()
        open(os.path.join(self.dir, 'foobar2' + self.match),"w").close()
        
    def test_os_file_get_wildcard(self):
        print os_file_get_wildcard(self.dir,self.match)
        
    def test_os_file_to_string_remove_tab(self):
        
        s = "foobar\tfoobar"
        
        fh = open(self.test_file,'w+')
        with (fh):
            fh.write(s)
            
        expected_s = "foobarfoobar"
        new_s = os_file_to_string(self.test_file,["\t"])
        
        self.assertEquals(new_s,expected_s)
        
    def test_os_fileTestIDGeneratorScale_to_string_remove_tab_and_string(self):
        
        s = "fo o b ar\tfo o b ar"
        
        fh = open(self.test_file,'w+')
        with (fh):
            fh.write(s)
            
        expected_s = "foobarfoobar"
        new_s = os_file_to_string(self.test_file,["\t"," "])
        
        self.assertEquals(new_s,expected_s)

    def test_os_file_to_string(self):
        
        s = "foobarfoobar"
        
        fh = open(self.test_file,'w+')
        with (fh):
            fh.write(s)
            
        expected_s = "foobarfoobar"
        new_s = os_file_to_string(self.test_file)
        
        self.assertEquals(new_s,expected_s)
    
if __name__ == "__main__":

    #unittest.main()
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIDGenerator))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestOSFiles))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPickle))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSingleton))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIDGeneratorScale))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_enum))
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)
    
