import sys

import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils import UniqueIDGenerator, get_obj_attr_vals, get_obj_attr_names, \
     get_obj_attr, generic, os_file_get_wildcard, os_file_to_string, read_pickle, \
     write_pickle

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
        
class TestUniqueIDGenerator(unittest.TestCase):

    def setUp(self):
        self.idfile = "uniqueid.dat"

    def tearDown(self):
        os.remove(self.idfile)

    def _increment_ids(self,uniqueid,num_ids):
        for i in range(num_ids):
            uniqueid.next()
           
    def _create_unique_ids(self,num_ids,size):
        uniqueid = UniqueIDGenerator(self.idfile,size)
        self._increment_ids(uniqueid,num_ids)
        old_num_ids,num_ids = uniqueid.write()
        del uniqueid
        return(old_num_ids,num_ids)
   
    def test_create30_generatefile(self):
        self._create_unique_ids(30,10)
        self.assertTrue(ospath.isfile(self.idfile))
        
    def test_create10_recover_count10(self):
        self._create_unique_ids(10,10)
        
        uniqueid = UniqueIDGenerator(self.idfile,10)
        self.assertEquals(uniqueid.num_ids(),10)
        
    def test_create10_recover_add22_count44(self):
        self._create_unique_ids(22,10)
        old_num_ids,num_ids = self._create_unique_ids(22,10)
        self.assertEquals(old_num_ids,22)
        self.assertEquals(num_ids,44)
        
        uniqueid = UniqueIDGenerator(self.idfile,10)
        self.assertEquals(uniqueid.num_ids(),44)
        del uniqueid
        
    def test_destructor(self):
        uniqueid = UniqueIDGenerator(self.idfile,10)
        self._increment_ids(uniqueid,10)
        del uniqueid
        self.assertTrue(ospath.isfile(self.idfile))
        
        
    def test_max_retry(self):
        
        with self.assertRaises(Exception):
            self._create_unique_ids(20,1)

class Test_get_obj_attr(unittest.TestCase):
    
    def setUp(self):
        self.testobj = test_class()
    
    def tearDown(self):
        pass
    
    def test_get_attr_names(self):
        expected_results = ['attr1','attr2','myfunc']
        
        self.assertListEqual(expected_results,get_obj_attr_names(self.testobj))
    
    def test_get_notcallable_attr_vals(self):
        expected_results = [123,456]
        self.assertListEqual(expected_results,get_obj_attr_vals(self.testobj))
        
    def test_get_notcallable_attr(self):
        expected_results = [('attr1',123),('attr2',456)]
        self.assertListEqual(expected_results,get_obj_attr(self.testobj))

class Test_generic(unittest.TestCase):
    
    def setUp(self):
        self.g = generic(attr1=123,attr2=456)
    
    def test_construct(self):
        self.assertTrue(hasattr(self.g,'attr1'))
        self.assertEquals(123,getattr(self.g,'attr1'))
        self.assertTrue(hasattr(self.g,'attr2'))
        self.assertEquals(456,getattr(self.g,'attr2'))        
    
    def test_get_attr_names(self):
        attr_names = self.g.__get_attr_names__(self.g)
        self.assertListEqual(['attr1','attr2'],attr_names)
        
    def test_get_attr(self):
        attr_names = self.g.__get_attr__(self.g)
        
        self.assertListEqual([('attr1',123),('attr2',456)],attr_names)
        
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
        
    def test_os_file_to_string_remove_tab_and_string(self):
        
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
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUniqueIDGenerator)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_get_obj_attr))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestOSFiles))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPickle))
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)
    
