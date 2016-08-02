import unittest

from testerror1 import DummyTest

class Test_TestE(unittest.TestCase):
    
    def setUp(self):
        self.dummytest = DummyTest()
        
    def test_test1(self):
        self.assertTrue(self.dummytest.dummy1(),1)
        
    def test_test2(self):
        self.assertTrue(self.dummytest.dummy2(),2)
        
class Test_Test2E(unittest.TestCase):
    def setUp(self):
        self.dummytest = DummyTest()
        
    def test_test1(self):
        self.assertTrue(self.dummytest.dummy3(),3)
        
    def test_test2(self):
        self.assertTrue(self.dummytest.dummy4(),4)

if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_TestE)
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Test2E)
    unittest.TextTestRunner(verbosity=2).run(suite)
