import sys
import os
from os import path as ospath
from misc_utils_generic import GenericBase

import unittest
import time

class Test_generic_basic(unittest.TestCase):
    ''' basic operation, pass in dynamic attributes but not flagged
    as data members'''
    def setUp(self):
        self.g = GenericBase(attr1=123,attr2=456)
    
    def tearDown(self):
        pass
        
    def test_construct(self):
        self.assertTrue(hasattr(self.g,'attr1'))
        self.assertEquals(123,getattr(self.g,'attr1'))
        self.assertTrue(hasattr(self.g,'attr2'))
        self.assertEquals(456,getattr(self.g,'attr2'))            

class Test_generic_datamembers(unittest.TestCase):
    ''' using the datamembers constructor to set special attributes 
    ; using the attr_get_keyval method will strip of the _dm_ mangle that is applied to keep them separate '''
    def setUp(self):
        self.dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm=self.dm)
    
    def tearDown(self):
        pass
    
    def test_hasattr_foo(self):
        self.assertTrue(hasattr(self.dmg,'foo'))
        
    def test_getattr_foo_bar(self):        
        self.assertEquals('bar',getattr(self.dmg,'foo')) 

    def test_hasattr_boo(self):
        self.assertTrue(hasattr(self.dmg,'boo'))
        
    def test_getattr_fboo_hah(self):        
        self.assertEquals('hah',getattr(self.dmg,'boo'))

    def test_getattr_datamembers(self):        
        self.assertEquals(self.dm,getattr(self.dmg,'dm'))

class Test_generic_basic_and_datamembers(unittest.TestCase):
    ''' object with dm attrs and non-dm attrs; using the attr_get_keyval 
    method will strip of the _dm_ mangle that is applied to keep them separate '''
    def setUp(self):
        self.dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm=self.dm,attr1=123,attr2=456)
    
    def tearDown(self):
        pass
    
    def test_hasattr_foo(self):
        self.assertTrue(hasattr(self.dmg,'foo'))
        
    def test_getattr_foo_bar(self):        
        self.assertEquals('bar',getattr(self.dmg,'foo')) 

    def test_hasattr_boo(self):
        self.assertTrue(hasattr(self.dmg,'boo'))
        
    def test_getattr_fboo_hah(self):        
        self.assertEquals('hah',getattr(self.dmg,'boo')) 

    def test_hasattr_attr1(self):
        self.assertTrue(hasattr(self.dmg,'attr1'))
        
    def test_getattr_attr1_123(self):        
        self.assertEquals(123,getattr(self.dmg,'attr1')) 
        
    def test_hasattr_attr2(self):
        self.assertTrue(hasattr(self.dmg,'attr2'))
        
    def test_getattr_attr2_456(self):        
        self.assertEquals(456,getattr(self.dmg,'attr2'))  


class Test_generic_datamembers_no_other_args(unittest.TestCase):
    ''' test to see if kwargs can be passed as None'''
    def setUp(self):
        self.dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm=self.dm)
    
    def tearDown(self):
        pass
    
    def test_hasattr_foo(self):
        self.assertTrue(hasattr(self.dmg,'foo'))
        
    def test_getattr_foo_bar(self):        
        self.assertEquals('bar',getattr(self.dmg,'foo')) 

    def test_hasattr_boo(self):
        self.assertTrue(hasattr(self.dmg,'boo'))
        
    def test_getattr_fboo_hah(self):        
        self.assertEquals('hah',getattr(self.dmg,'boo')) 

class Test_generic_datamembers_errors(unittest.TestCase):
    ''' make sure usual errors are detected and caught'''
    def testarg_not_dict(self):
        dm = [('foo','bar'),('boo','hah')]
        
        with self.assertRaises(Exception):
            GenericBase.datamembers(dm)
            
    def testarg_conflicts_with_regular_arg(self):
        dm = {'foo':'bar','boo':'hah'}
        with self.assertRaises(Exception):
            GenericBase.datamembers(dm,foo='bar')
            
class Test_generic_attr_get(unittest.TestCase):
    ''' get  callable and non-callable attrs
    using the attr_get_keyval method will strip of the _dm_ mangle
    that is applied to keep them separate '''
    def setUp(self):
        dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm=dm,attr1=123,attr2=456)

    def test_attr_get(self):
        exp_res = ['_setattr','attr_get_keyval','datamembers',
                   'foo','boo','attr1','attr2','log','id']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval()]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)
        
    def test_attr_exclude_callable(self):
        exp_res = ['foo','boo','attr1','attr2','log','id']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)
        
    def test_attr_get_datamembers(self):
        exp_res = ['foo','boo']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False,
                                                                include_nondataattr=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)


class Test_generic_attr_get_from_derived(unittest.TestCase):
    ''' test that we can distinguish between a base class attribute 
    and a derived class attribute '''
    def setUp(self):
        class DerivedGenericBase(GenericBase):
            staticattr = "imstatic"
            
        _datamembers = {'foo':'bar','boo':'hah'}
        self.dmg = DerivedGenericBase.datamembers(dm=_datamembers,
                                                  attr1=123,attr2=456) 
        
    def test_attr_get_from_derived_class_only(self):
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False)]
        _attr.sort()
        
        exp_res = ['foo','boo','attr1','attr2','log','id']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False,
                                                                include_baseattr=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)

    
class Test_generic_attr_get_no_datamembers(unittest.TestCase):
    '''no datamembers '''
    def setUp(self):
        self.dmg = GenericBase(attr1=123,attr2=456)

    def test_attr_get(self):
        exp_res = ['attr1','attr2','log','id']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)
                  
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_basic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_datamembers))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_basic_and_datamembers))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_datamembers_errors))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_attr_get))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_attr_get_from_derived))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_datamembers_no_other_args))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_attr_get_no_datamembers))


    
    unittest.TextTestRunner(verbosity=2).run(suite)
        
