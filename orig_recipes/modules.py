#/usr/bin/python

def printmembers(module_obj=None):
    from inspect import getmembers, isclass
    from sys import modules
    
    if module_obj==None:
        module_obj = getmembers(modules[__name__])
        
    for name,obj in getmembers(module_obj):    
        if not name.startswith('__'):
            print name, isclass(obj),obj,obj.__doc__

def test_importlib_in_namespace(module_filename):
    from importlib import import_module    
    from sys import modules
    from os.path import basename, splitext
    
    module, ext = splitext(basename(module_filename))
    
    import_module(module)
    globals()['tmp_module'] = modules[module]   
    printmembers(tmp_module)
  
def test_importlib():
    from importlib import import_module    
    from inspect import getmembers
    from sys import modules
    
    import_module('tmp_module')
    
    tmp_module = getmembers(modules['tmp_module'])
    
    for i in range(len(tmp_module)):
        name,obj = tmp_module[i]
    
        if not name.startswith('__'):
            print name
     
    del modules['tmp_module']     
    del getmembers, modules
    
            
def test_import():
    from inspect import getmembers
    from sys import modules
    
    import tmp_module
     
    tmp_module = getmembers(tmp_module)
    
    for i in range(len(tmp_module)):
        name,obj = tmp_module[i]
    
        if not name.startswith('__'):
            print name    
            
    del getmembers, modules, tmp_module


#test_importlib()
#test_import()
test_importlib_in_namespace('tmp_module.py')
printmembers()