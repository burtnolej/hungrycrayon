
import unittest
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from type_utils import IntType, BIntType

class TestIntTypeNoName(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_nonamekey_fail(self):
        
        with self.assertRaises(Exception):
            self.mintype = IntType()
    
class TestIntType(unittest.TestCase):
    def setUp(self):
        self.myintype = IntType(name='bint')
 
    def test_bintname(self):
        self.assertEquals(self.myintype.validations[0].name,'bint')    

    def test_123true(self):
        self.assertTrue(self.myintype(123))
        
    def test_AAAfalse(self):
        self.assertFalse(self.myintype('aaa'))
        
class TestBIntType(unittest.TestCase):
    ''' if inheriting correctly should fail on 
    first test, not int'''
    def setUp(self):
        self.mybintype = BIntType(name='40>=x<=60',
                                  ubound=60,lbound=40)
    
    def test_aaafalse(self):
        self.assertFalse(self.mybintype('aaa'))

class TestBIntTypeGtltBadargs(unittest.TestCase):
    ''' between an upper and lower bound '''
    def setUp(self):
        pass
    
    def test_(self):
        with self.assertRaises(Exception):
            BIntType(name='40>=x<=60')
        
class TestBIntTypeGtlt(unittest.TestCase):
    ''' between an upper and lower bound '''
    def setUp(self):
        self.mybintype = BIntType(name='40>=x<=60',
                                  ubound=60,lbound=40)
        
    
    def test_ubound59true(self):
        self.assertTrue(self.mybintype(59))

    def test_ubound60true(self):
        self.assertTrue(self.mybintype(60))

    def test_ubound61false(self):
        self.assertFalse(self.mybintype(61))

    def test_lbound41true(self):
        self.assertTrue(self.mybintype(41))

    def test_lbound40true(self):
        self.assertTrue(self.mybintype(40))

    def test_lbound39false(self):
        self.assertFalse(self.mybintype(39))

class TestBIntTypeGt(unittest.TestCase):

    def setUp(self):
        self.mybintype = BIntType(name='40>=x',lbound=40)
        
    def test_lboundMassivetrue(self):
        self.assertTrue(self.mybintype(10000))

    def test_lbound41true(self):
        self.assertTrue(self.mybintype(41))

    def test_lbound40true(self):
        self.assertTrue(self.mybintype(40))

    def test_lbound39false(self):
        self.assertFalse(self.mybintype(39))

if __name__ == "__main__":

    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIntTypeNoName))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIntType))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBIntType))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBIntTypeGtlt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBIntTypeGt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBIntTypeGtltBadargs))
  
    unittest.TextTestRunner(verbosity=2).run(suite)
