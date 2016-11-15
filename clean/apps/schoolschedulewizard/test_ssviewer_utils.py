import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest
import ssviewer_utils

class Test_getpage(unittest.TestCase):
    
    # 1 attribute displayed for each record ('subject')
    
    def setUp(self):
        
        self.grid = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q']
        
    def test_(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,4)
        
    def test_page2(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,2)
        
        self.assertEqual(srow,5)
        self.assertEqual(erow,9)
        
    def test_page_last(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,4)
        
        self.assertEqual(srow,15)
        self.assertEqual(erow,16)
        
    def test_numrows_less_than1page(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,20,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,16)
        
    def test_page_too_high(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,5,5)
        
        self.assertEqual(srow,12)
        self.assertEqual(erow,16)
        
    def test_pagelen_2(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,2,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,2)
        
    def test_pagelen_2(self):
        
        srow,erow = ssviewer_utils._getpage(self.grid,2,2)
        
        self.assertEqual(srow,2)
        self.assertEqual(erow,3)
        
    def test_1sourcerow(self):
        
        srow,erow = ssviewer_utils._getpage(['a'],30,1)
        
        self.assertEqual(srow,0)
        self.assertEqual(erow,0)
        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_getpage))

    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


