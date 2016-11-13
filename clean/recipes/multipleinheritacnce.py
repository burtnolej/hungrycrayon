

import unittest

class A(object):
    def __init__(self,arg=None):
        if arg:
            self.Aarg=arg
        print "init A",
        
    def func1A(self):
        return("func1A")
    
class B(object):
    def __init__(self,arg=None):
        if arg:
            self.Barg=arg
        print "init B",
        
    def func1B(self):
        return("func1B")


class C(A,B):
    def __init__(self,arg1=None,arg2=None):
        
        A.__init__(self,arg1)
        B.__init__(self,arg2)
        
class TestMultipleInheritance(unittest.TestCase):
    def setUp(self):
        self.c = C()
    
    def test_(self):
                
        self.assertEqual(self.c.func1A(),"func1A")
        self.assertEqual(self.c.func1B(),"func1B")
        
        
class TestMultipleInheritanceWithArgs(unittest.TestCase):
    def setUp(self):
        self.c = C("foo","bar")
    
    def test_(self):
        
        self.assertEqual(self.c.Aarg,"foo")
        self.assertEqual(self.c.Barg,"bar")
                

if __name__ == "__main__":

    suite = unittest.TestSuite()
     
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMultipleInheritance))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMultipleInheritanceWithArgs))
    
    unittest.TextTestRunner(verbosity=2).run(suite)