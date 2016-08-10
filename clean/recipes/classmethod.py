
import unittest

from getopt import getopt, GetoptError, gnu_getopt

class myclass(object):
    
    def __init__(self,**kwarg):
        from inspect import getmembers
        for k,v in kwarg.iteritems():
            setattr(self,k,v)
        
    @classmethod
    def myconstructor(cls,**kwarg):
        _v = kwarg.pop('arg1')
        cls1 = cls(**kwarg)
        setattr(cls1,'arg1',_v)
        return(cls1)

class TestClassmethod(unittest.TestCase):
    
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