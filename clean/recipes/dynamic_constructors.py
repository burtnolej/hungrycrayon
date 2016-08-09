import unittest
import sys

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
    
class myfactory():
    def new(self,clsname,**kwarg):
        
        if not kwarg.has_key('constructor'):
            # use default
            mc =  getattr(sys.modules[__name__],clsname)(**kwarg)
        else:
            const = kwarg['constructor']
            kwarg.pop('constructor')
            _cls = getattr(sys.modules[__name__],clsname)
            mc = getattr(_cls,const)(**kwarg)
        return(mc)
        
class Test_DynConst_basic(unittest.TestCase):
    
    def test_default(self):
        mc = myclass(attr1=123,attr2=456)
        self.assertTrue(hasattr(mc,'attr1'))
        self.assertEquals(getattr(mc,'attr2'),456)
        
    def test_constructor(self):
        mc = myclass.myconstructor(arg1='xyz',attr1=123,attr2=456)
        self.assertTrue(hasattr(mc,'attr1'))
        self.assertEquals(getattr(mc,'attr2'),456)
        self.assertEquals(getattr(mc,'arg1'),'xyz')
        
    def test_dynamic_object_default(self):
        clsname = 'myclass'
        mc =  getattr(sys.modules[__name__],clsname)(attr1=123,attr2=456)
        self.assertTrue(hasattr(mc,'attr1'))
        self.assertEquals(getattr(mc,'attr2'),456)
        
    def test_dynamic_object_explicit_constructor(self):
        clsname = 'myclass'
        constname = 'myconstructor'
        _cls = getattr(sys.modules[__name__],clsname)
        mc = _cls.myconstructor(arg1='xyz',attr1=123,attr2=456) 
        self.assertEquals(getattr(mc,'attr2'),456)
        self.assertEquals(getattr(mc,'arg1'),'xyz')
        
    def test_dynamic_object_dynamic_constructor(self):
        clsname = 'myclass'
        constname = 'myconstructor'
        _cls = getattr(sys.modules[__name__],clsname)
        mc = getattr(_cls,constname)(arg1='xyz',attr1=123,attr2=456)
        self.assertEquals(getattr(mc,'attr2'),456)
        self.assertEquals(getattr(mc,'arg1'),'xyz')
        
class Test_DynConst_factory(unittest.TestCase):
    def test_default(self):
        mf = myfactory()
        mc = mf.new('myclass',attr1=123,attr2=456)
        self.assertTrue(hasattr(mc,'attr1'))
        self.assertEquals(getattr(mc,'attr2'),456)
        
    def test_constructor(self):
        mf = myfactory()
        mc = mf.new('myclass',
                    constructor='myconstructor',
                    arg1='xyz',attr1=123,attr2=456)
        self.assertEquals(getattr(mc,'attr2'),456)
        self.assertEquals(getattr(mc,'arg1'),'xyz')
        
                
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DynConst_basic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DynConst_factory))
    unittest.TextTestRunner(verbosity=2).run(suite)
    