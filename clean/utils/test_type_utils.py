
import unittest
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from type_utils import RealInt, BoundRealInt, SetMember, \
     DBSetMember, TextAlphaNum, SetMemberPartial, isadatatype

class TestRealIntNoName(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_nonamekey_fail(self):
        
        with self.assertRaises(Exception):
            self.mintype = RealInt()
    
class TestRealInt(unittest.TestCase):
    def setUp(self):
        self.myintype = RealInt(name='bint')
 
    def test_bintname(self):
        self.assertEquals(self.myintype.validations[0].name,'bint')    

    def test_123true(self):
        self.assertTrue(self.myintype(123))
        
    def test_AAAfalse(self):
        self.assertFalse(self.myintype('aaa'))
        
class TestBoundRealInt(unittest.TestCase):
    ''' if inheriting correctly should fail on 
    first test, not int'''
    def setUp(self):
        self.mybintype = BoundRealInt(name='40>=x<=60',
                                  ubound=60,lbound=40)
    
    def test_aaafalse(self):
        self.assertFalse(self.mybintype('aaa'))

class TestBoundRealIntGtltBadargs(unittest.TestCase):
    ''' between an upper and lower bound '''
    def setUp(self):
        pass
    
    def test_(self):
        with self.assertRaises(Exception):
            BoundRealInt(name='40>=x<=60')
        
class TestBoundRealIntGtlt(unittest.TestCase):
    ''' between an upper and lower bound '''
    def setUp(self):
        self.mybintype = BoundRealInt(name='40>=x<=60',
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

class TestBoundRealIntGt(unittest.TestCase):

    def setUp(self):
        self.mybintype = BoundRealInt(name='40>=x',lbound=40)
        
    def test_lboundMassivetrue(self):
        self.assertTrue(self.mybintype(10000))

    def test_lbound41true(self):
        self.assertTrue(self.mybintype(41))

    def test_lbound40true(self):
        self.assertTrue(self.mybintype(40))

    def test_lbound39false(self):
        self.assertFalse(self.mybintype(39))
        
class TestSetMemberNoList(unittest.TestCase):
    ''' SetMember needs a set attribute to be provided '''
    def setUp(self):
        pass
    
    def test_nolist(self):
        
        with self.assertRaises(Exception):
            self.setmember = SetMember(name='x{mylist}')
        
class TestSetMember(unittest.TestCase):

    def setUp(self):
        self.setmember = SetMember(name='x{mylist}',set=['cherry','banana','grape'])
        
    def test_cherry_true(self):
        self.assertTrue(self.setmember('cherry'))

    def test_plum_false(self):
        self.assertFalse(self.setmember('plum'))
        
class TestSetMemberPartial(unittest.TestCase):

    def setUp(self):
        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['cherry','banana','grape','apple'])
        
    def test_er_true(self):
        self.assertTrue(self.setmemberp('er'))

    def test_ap_false(self):
        self.assertFalse(self.setmemberp('ap'))
        
    def test_ER_true(self):
        self.assertTrue(self.setmemberp('ER'))

class TestDBSetMember(unittest.TestCase):

    def setUp(self):
        dbname = '/data/food'
        tbl_name = 'food'
        fldname = 'food_name'
        self.dbsetmember = DBSetMember(dbname,tbl_name,
                                     fldname,
                                     name='x{dblist}')
        
    def test_spinach_true(self):
        self.assertTrue(self.dbsetmember('spinach'))
        
    def test_Spinach_false(self):
        self.assertFalse(self.dbsetmember('Spinach'))

class TestTextAlphaNum(unittest.TestCase):
    def setUp(self):
        self.mytextalphanum = TextAlphaNum(name='textalphanum')
 
    def test_Peanut(self):
        self.assertTrue(self.mytextalphanum('Peanut'))
        
    def test_Peanut_Butter(self):
        self.assertFalse(self.mytextalphanum('Peanut_Butter'))
        
class TestIsDatatype(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_TextAlphaNum_True(self):
        self.assertTrue(isadatatype(TextAlphaNum))
        
    def test_Foobar_False(self):
        class Foobar(object):
            pass
        
        self.assertFalse(isadatatype(Foobar))
        
    def test_Myvar_instance_true(self):
        
        myvar = TextAlphaNum(name='textalphanum')
        
        self.assertTrue(isadatatype(myvar))

        
if __name__ == "__main__":

    suite = unittest.TestSuite()

    # RealInt & BoundRealInt

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRealInt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBoundRealInt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBoundRealIntGtlt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBoundRealIntGt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBoundRealIntGtltBadargs))
    
    # SetMember
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetMember))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBSetMember))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetMemberPartial))

    # AlphaNum
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTextAlphaNum))
    
    # Validations 
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestIsDatatype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSetMemberNoList))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRealIntNoName))
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)
