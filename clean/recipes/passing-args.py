
import unittest

from getopt import getopt, GetoptError, gnu_getopt

class TestPassingArgs(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_kwargs(self):
        
        class myclass():
            def func(self, obj,**kwargs):
                return(kwargs)
        
        results = myclass().func('foobar',
                                 a=1,
                                 b=2,
                                 c=3,
                                 d={'z':1,
                                    'y':2})
        print results
        
  
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestPassingArgs)
    
    unittest.TextTestRunner(verbosity=2).run(suite)