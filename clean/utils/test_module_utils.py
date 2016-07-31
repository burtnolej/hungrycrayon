#/usr/bin/python

import unittest
from random import randint
import pickle
from module_utils import __load_module__, _getmembers, py2xml,\
     _getvarfromsource, __tokenize__, _getargsfromsource, __getsourceaslist__, \
     _dir, _getclassmethods

class Test_ModuleUtils(unittest.TestCase):
    
    def test_get_loaded_modules(self):
        
        #these can start to fail if other tests get ran before
        #and have imported modules that have not been previously been
        #deleted
        
        # detecting local modules
        from sys import modules
        self.assertFalse(modules.has_key('inspect'))
        self.assertFalse(modules.has_key('sqlite3'))
        
        import sqlite3        
        self.assertTrue(modules.has_key('sqlite3'))
        
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
        
        module_filename = "./tmp_module.py"
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
        
        module_filename = "./tmp_module.py"
        module = __load_module__(module_filename)
        
        self.assertEquals(['foobar'],[member for member in dir(module) if not member.startswith('__')])
    
        # get methods of a module member
        self.assertEquals(['boo'],[member[0] for member in getmembers(module.foobar) if not member[0].startswith('__')])

        # and using a diff function to load members
        self.assertEquals(['boo'],_getmembers(module.foobar).keys()) 
        
    def test_get_module_classes(self):

        from inspect import isclass
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])
        
    def test_get_module_class_methods(self):
        from inspect import isclass
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        m=[]
        for cls in classes:
            m = m + _getclassmethods(getattr(module,cls))

        self.assertListEqual(['boo','boohoo','boo2','boo3'],m)
          
    def test_get_module_class_method_args(self):
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        tokens = __tokenize__("./tmp_module2.py")
        
        args = _getargsfromsource(module.foobar2.boohoo,tokens)
        self.assertListEqual(['self','banana'],args)
        
    def test_get_module_class_method_vars(self):
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        vars = _getvarfromsource(module.foobar2.boo2)
        self.assertListEqual(['a','b'],vars)
        
    def test_get_module_class_vars(self):
        
        from inspect import isclass, ismethod
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        v=[]
        _m = _getmembers(module.foobar)
        
        for key, obj in _m.iteritems():
            if not ismethod(obj):
                v.append(key)
         
        self.assertListEqual(['blahblah'],v)
        
    def test_get_module_functions(self):

        from inspect import isroutine
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        routines = [name for name in _dir(module) if isroutine(getattr(module,name))]
        
        self.assertListEqual(routines,['myfunc'])
        
    def test_get_variables_in_function(self):

        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        self.assertListEqual(['foo'],_getvarfromsource(module.myfunc))
        
    def test_get_proc_signature(self):
        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        tokens = __tokenize__("./tmp_module2.py")
        
        self.assertListEqual(['fe','fi','fo','fum'],_getargsfromsource(module.myfunc,tokens))
    
    def test_get_module_info_all(self):

        
        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        
        tokens = __getsourceaslist__(module_filename, module)
        
        self.assertListEqual(['foobar', 'boo', ['self'], [], ['blahblah'], 
                              'foobar2', 'boohoo', ['self', 'banana'], [], 'boo2', ['self'], ['a', 'b'], [], 
                              'foobar3', 'boo3', ['self'], ['self.foobar'], [], 
                              'mybase', [], 
                              'myfunc', 'myfunc', ['fe', 'fi', 'fo', 'fum'], ['foo'], 
                              'mylocal', 'mylocal'],tokens)
        
    def test_xml_generator(self):
        import os
        print os.getcwd()
        module_filename = "./tmp_module2.py"
        py2xml(module_filename)      

    def test_load_module_not_in_cwd_abspath(self):
        # if module.py in /home/burtnolej; move cwd to /tmp and load
        # /home/burtnolej/module.py
        import os
        from inspect import isclass
        _cwd = os.getcwd()
        os.chdir("/tmp")
        module_filename = "./tmp_module3.py"
        module_path = os.path.join(_cwd,"./tmp_module3.py")
        module = __load_module__(module_path)
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
        module_filename = "./tmp_module3.py"
        module_path = os.path.join(_basecwd,"./tmp_module3.py")
        
        module = __load_module__(module_path)
        
        os.chdir(_cwd)
        
        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])
           
    def test_load_module_not_in_cwd_relpath_forced(self):
        # force the module to not be in the current path
        import os
        from inspect import isclass

        module_filename = "./tmp/tmp_module4.py"
        
        module = __load_module__(module_filename)

        classes = [name for name in _dir(module) if isclass(getattr(module,name))]
        
        self.assertEquals(classes,['foobar','foobar2','foobar3','mybase'])

        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_ModuleUtils)
    unittest.TextTestRunner(verbosity=2).run(suite) 