import sys

import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/utils")
from misc_utils import UniqueIDGenerator

import unittest
import time

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
        
    def test_max_retry(self):
        
        with self.assertRaises(Exception):
            self._create_unique_ids(20,1)

        
if __name__ == "__main__":

    unittest.main()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUniqueIDGenerator)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
