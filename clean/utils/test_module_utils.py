#/usr/bin/python

import unittest
from random import randint
import pickle
from module_utils import __load_module__, _getmembers, \
     _getvarfromsource, __tokenize__, _getargsfromsource, __getsourceaslist__, \
     _dir, _getclassmethods, __getuserloadedmodules__, imported_sysclasses_remove, \
     _getclasses, isuserclass, isuserfunc
from os.path import join

class Test_ModuleUtils(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = "/home/burtnolej/Development/pythonapps3/clean/utils"
        
    def test_get_loaded_modules(self):
        
        #these can start to fail if other tests get ran before
        #and have imported modules that have not been previously been
        #deleted
        
        # detecting local modules
        from sys import modules
        self.assertFalse(modules.has_key('email'))
        self.assertFalse(modules.has_key('json'))
        
        import json        
        self.assertTrue(modules.has_key('json'))
        
        # when you select a component does the module get loaded too
        from threading import current_thread
        self.assertTrue(modules.has_key('threading'))
        
        # detecting global modules loaded
        # import pickle        
        self.assertTrue(modules.has_key('pickle'))
        
    def test_get_loaded_modules_components(self):
        from sys import modules
        from inspect import getmembers
        
        # detecting components of local modules loaded
        from datetime import tzinfo
        
        m = _getmembers(modules[__name__])
        
        # the module gets loaded anyway
        self.assertTrue(modules.has_key('datetime'))
        # but is not in the namespace
        self.assertFalse(locals().has_key('datetime'))

        # the component however is in the namespace
        self.assertTrue(locals().has_key('tzinfo'))
                
        # detecting components of global modules loaded
        self.assertTrue(globals().has_key('randint'))

    def test_module_dynamic_loading(self):
        
        from importlib import import_module    
        from sys import modules
        from os.path import basename, splitext
        
        module_filename = "tmp_module.py"
        module, ext = splitext(basename(module_filename))
        
        # load module dynamically
        import_module(module)
        self.assertTrue(modules.has_key(module)) 
        
        # make accessible in the global namespace
        self.assertEqual(modules['tmp_module'].foobar().boo(),"boo")
        globals()['tmp_module'] = modules[module]
        self.assertEqual(tmp_module.foobar().boo(),"boo")

    def test_get_module_contents(self):
        
        from inspect import getmembers
        
        module_filename = "tmp_module.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        self.assertEquals(['foobar'],[member for member in dir(module) if not member.startswith('__')])
    
        # get methods of a module member
        self.assertEquals(['boo'],[member[0] for member in getmembers(module.foobar) if not member[0].startswith('__')])

        # and using a diff function to load members
        self.assertEquals(['boo'],_getmembers(module.foobar).keys()) 
        
    def test_get_module_classes(self):

        from inspect import isclass
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])

        
    def test_get_module_class_methods(self):
        from inspect import isclass
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        m=[]
        for cls in classes:
            m = m + _getclassmethods(getattr(module,cls))

        self.assertListEqual(['boo','boohoo','boo2','boo3'],m)
          
    def test_get_module_class_method_args(self):
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        tokens = __tokenize__(join(self.test_dir,"tmp_module2.py"))
        
        args = _getargsfromsource(module.foobar2.boohoo,tokens)
        self.assertListEqual(['self','banana'],args)
        
        
    def test_get_module_class_method_vars(self):
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        vars = _getvarfromsource(module.foobar2.boo2)
        self.assertListEqual(['a','b'],vars)
        
    def test_get_module_class_vars(self):
        
        from inspect import isclass, ismethod
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        v=[]
        _m = _getmembers(module.foobar)
        
        for key, obj in _m.iteritems():
            if not ismethod(obj):
                v.append(key)
         
        self.assertListEqual(['blahblah'],v)
        
    def test_get_module_functions(self):

        from inspect import isroutine
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        routines = [name for name in _dir(module) if isroutine(getattr(module,name))]
        
        self.assertListEqual(routines,['myfunc'])
        
    def test_get_variables_in_function(self):

        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        
        self.assertListEqual(['foo'],_getvarfromsource(module.myfunc))
        
    def test_get_proc_signature(self):
        
        module_filename = "tmp_module2.py"
        module = __load_module__(module_filename,allowdupe=True)
        tokens = __tokenize__(join(self.test_dir,"tmp_module2.py"))
        
        self.assertListEqual(['fe','fi','fo','fum'],_getargsfromsource(module.myfunc,tokens))

    def test_get_module_info_all(self):

        #need to put tmp_module to test_get_module_info_all.py
        #as we are picking up tmp_module from a previous load
        
        module_filename = join(self.test_dir,"./test_misc/test_get_module_info_all.py")
        
        module = __load_module__(module_filename,allowdupe=True)
        
        tokens = __getsourceaslist__(join(self.test_dir,module_filename), module)
                
        self.assertListEqual(['foobart', 'boo', ['self'], [], ['blahblah'], 
                              'foobart2', 'boohoo', ['self', 'banana'], [], 'boo2', ['self'], ['a', 'b'], [], 
                              'foobart3', 'boo3', ['self'], ['self.foobar'], [], 
                              'mybaser', [], 
                              'myfuncy',  ['fe', 'fi', 'fo', 'fum'], ['foo'], 
                              'mylocaly'],tokens)   

    def test_load_module_not_in_cwd_abspath(self):
        # if module.py in /home/burtnolej; move cwd to /tmp and load
        # /home/burtnolej/module.py
        import os
        from inspect import isclass
        _cwd = os.getcwd()
        os.chdir("/tmp")
        module_filename = "tmp_module3.py"
        module_path = os.path.join(_cwd,"tmp_module3.py")
        module = __load_module__(module_path,allowdupe=True)
        os.chdir(_cwd)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])
        
    def test_load_module_not_in_cwd_relpath(self):
        # if module.py in /home/burtnolej; move cwd to /home and load
        # ./burtnolej/module.py
        import os
        from inspect import isclass
        _cwd = os.getcwd()
        _basecwd = os.path.basename(_cwd)
        os.chdir("..")
        module_filename = "tmp_module3.py"
        module_path = os.path.join(_basecwd,"tmp_module3.py")
        
        module = __load_module__(module_path,allowdupe=True)
        
        os.chdir(_cwd)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])
           
    def test_load_module_not_in_cwd_relpath_forced(self):
        # force the module to not be in the current path
        import os
        from inspect import isclass

        module_filename = join(self.test_dir,"./.tmp/tmp_module4.py")
        
        module = __load_module__(module_filename,allowdupe=True)

        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])
        
    def test_load_module_same_module_twice(self):
        # force the module to not be in the current path
        import os
        from inspect import isclass

        module_filename = join(self.test_dir,"./.tmp/tmp_module5.py")
        module = __load_module__(module_filename)

        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
    
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])

        module_filename = "./.tmp_dupe/tmp_module5.py"
        with self.assertRaises(Exception):
            module = __load_module__(module_filename)
            
            
class Test_ModuleUtilsImports(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = "/home/burtnolej/Development/pythonapps3/clean/utils"
        
    def test_getusermodules(self):
        
        print __getuserloadedmodules__()
        
    def test_get_module_classes_with_imports(self):

        from inspect import isclass
        test_module = "test_get_module_classes_with_imports.py"
        
        module_filename = join(self.test_dir+"/test_misc",test_module)
        module = __load_module__(module_filename,allowdupe=True)        
        classes = _getclasses(module,test_module)
                    
        self.assertEquals(classes,['foobar10'])
    
    def test_isuserdefnclass(self):

        from inspect import isclass
        test_module = "test_get_module_classes_with_imports.py"
        
        module_filename = join(self.test_dir+"/test_misc",test_module)
        module = __load_module__(module_filename,allowdupe=True)        
                    
        self.assertTrue(isuserclass('foobar10',test_module))
        self.assertFalse(isuserclass('GetoptError',test_module))
        
    def test_isuserfunc(self):

        from inspect import isclass
        test_module = "test_get_module_classes_with_imports.py"
        
        module_filename = join(self.test_dir+"/test_misc",test_module)
        module = __load_module__(module_filename,allowdupe=True)        
                    
        self.assertTrue(isuserfunc('myfunk',test_module))
        self.assertFalse(isuserfunc('gnu_getopt',test_module))
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_ModuleUtils)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ModuleUtilsImports))
    unittest.TextTestRunner(verbosity=2).run(suite) 