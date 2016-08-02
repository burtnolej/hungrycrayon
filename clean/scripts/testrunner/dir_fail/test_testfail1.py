import unittest

from testfail1 import DummyTest

class Test_Test(unittest.TestCase):
    
    def setUp(self):
        self.dummytest = DummyTest()
        
    def test_test1(self):
        self.assertEquals(self.dummytest.dummy1(),11)
        
    def test_test2(self):
        self.assertEquals(self.dummytest.dummy2(),22)
        
class Test_Test2(unittest.TestCase):
    def setUp(self):
        self.dummytest = DummyTest()
        
    def test_test1(self):
        self.assertTrue(self.dummytest.dummy3(),3)
        
    def test_test2(self):
        self.assertTrue(self.dummytest.dummy4(),4)

if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Test)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Test2)
    unittest.TextTestRunner(verbosity=2).run(suite)
