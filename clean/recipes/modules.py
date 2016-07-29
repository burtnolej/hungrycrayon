#/usr/bin/python

import unittest
from random import randint
import pickle
import xml.etree.ElementTree as xmltree


def _getclassmethods(clsobj,inverse=False):
    ''' inverse will return anything not a class method - so a member variable'''
    from inspect import ismethod
    return([key for key, obj in _getmembers(clsobj).iteritems() 
            if ismethod(obj) <> inverse])

def _getmembers(module_obj=None):
    from inspect import getmembers, isclass
    from sys import modules
    d={}
    if module_obj==None:
        module_obj = getmembers(modules[__name__])
        
    for name,obj in getmembers(module_obj):    
        if not name.startswith('__'):
            d[name] = obj
            
    return(d)

def __xmltofile__(root,filename):
    from xml.dom.minidom import parseString    
    f = open(filename,"w+")
    f.write(parseString(xmltree.tostring(root)).toprettyxml())
    f.close()
    print "info: output written to ",filename

def __tokenize__(file):   
    import tokenize
    st = tokenize.generate_tokens(open(file).readline)

    # index by line_no
    std = {}
    for _st in st:
        if _st[0] == 1:
            line_no = _st[2][0]
            token = _st[1]
    
            if not std.has_key(line_no):
                std[line_no] = []
            std[line_no].append(token)
            
    return(std)

def _dir(module_obj=None):
    from inspect import getmembers, isclass
    from sys import modules
    l=[]
    if module_obj==None:
        module_obj = getmembers(modules[__name__])
        
    for name in dir(module_obj):    
        if not name.startswith('__'):
            l.append(name)
            
    return(l)

#def _getargsfromsource(modules,func,tokens):
def _getargsfromsource(obj,tokens):
    from inspect import getsourcelines
    
    # first zero is the actual zero
    # second zero is the first line of the source
    line = tokens[getsourcelines(obj)[-1]]
    
    return(line[2:])
    
def _getvarfromsource(obj):
    from inspect import getsourcelines
    
    source = getsourcelines(obj)[0]
    l=[]
    for line in source:
        line = line.replace(" ","")
        try:
            tokens = line.split("=")
            if len(tokens)>1:
                l.append(tokens[0])
        except:
            pass
    return(l) 

def __getsourceaslist__(module_filename,module):
    from inspect import isclass, isroutine
    tokens = __tokenize__(module_filename)
    
    token=[]
    
    for item in _dir(module):
        obj = getattr(module,item)
        token.append(item)
        if isclass(obj):
            for m in _getclassmethods(obj):
                token.append(m)
                token.append(_getargsfromsource(getattr(obj,m),tokens))
                token.append(_getvarfromsource(getattr(obj,m)))
            # this gets member vars
            token.append(_getclassmethods(obj,True))
        elif isroutine(obj):
            token.append(item)
            token.append(_getargsfromsource(getattr(module,item),tokens))
            token.append(_getvarfromsource(getattr(module,item)))
        else:
            token.append(item)  
            
    return(token)

def __add_element__(root,name,objtype):    
    subelement = xmltree.SubElement(root,objtype)
    subelement.set('Name',name) 
    return(subelement)

def code2xml(module, module_filename):
    from inspect import getmembers, isclass, isroutine
     
    tokens = __tokenize__("./tmp_module2.py")
    root = xmltree.Element('root')
    
    for item in _dir(module):
        obj = getattr(tmp_module2,item)
        
        if isclass(obj):
            cls_element = __add_element__(root,item,'class')
            for m in _getclassmethods(obj):
                clsmth_element = __add_element__(cls_element,m,'method')
                
                for arg in _getargsfromsource(getattr(obj,m),tokens):
                    __add_element__(clsmth_element,arg,'arg')
                
                for var in _getvarfromsource(getattr(obj,m)):
                    __add_element__(clsmth_element,var,'var')

            for memvar in _getclassmethods(obj,True):
                __add_element__(cls_element,m,'var')
            
        elif isroutine(obj):
            def_element = __add_element__(root,item,'def')
            
            for arg in _getargsfromsource(getattr(tmp_module2,item),tokens):
                __add_element__(def_element,arg,'arg')
            
            for var in _getvarfromsource(getattr(tmp_module2,item)):
                __add_element__(def_element,var,'var')        
        else:
            __add_element__(root,item,'var')
    
    output_filename = __convert_filename__(module_filename,".xml")
    __xmltofile__(root,output_filename)
    
    return(output_filename)

def __load_module__(module_filename):
    
    from importlib import import_module    
    from sys import modules
    from os.path import basename, splitext
    
    module, ext = splitext(basename(module_filename))
    import_module(module)
    globals()['tmp_module2'] = modules[module] 
    
    return(modules[module])

def __convert_filename__(module_filename,new_ext):
    from os.path import basename, splitext
    
    module, ext = splitext(basename(module_filename))
    return(module + ".xml")
    
class Test_Modules(unittest.TestCase):
    
    def test_get_loaded_modules(self):
        
        ''' these can start to fail if other tests get ran before
        and have imported modules that have not been previously been
        deleted'''
        
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
        
        classes = [name for name in _dir(tmp_module2) if isclass(getattr(tmp_module2,name))]
        
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
        
        self.assertListEqual(['foo'],_getvarfromsource(tmp_module2.myfunc))
        
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

        module_filename = "./tmp_module2.py"
        module = __load_module__(module_filename)
        code2xml(module, module_filename)      

        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Modules)
    unittest.TextTestRunner(verbosity=2).run(suite) 