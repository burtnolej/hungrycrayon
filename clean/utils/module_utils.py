#/usr/bin/python

import xml.etree.ElementTree as xmltree

def _getclassmethods(clsobj,inverse=False):
    ''' inverse will return anything not a class method - so a member variable'''
    from inspect import ismethod
    return([key for key, obj in _getmembers(clsobj).iteritems() 
            if ismethod(obj) <> inverse])

def _getclasses(module,filename):
    from inspect import isclass
    from sys import modules
    from os.path import splitext,basename
    
    classes = [name for name in _dir(module) if isclass(getattr(module,name))]
    imported_sysclasses_remove(classes,filename)
    return classes

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
    from os.path import abspath
    
    st = tokenize.generate_tokens(open(abspath(file)).readline)

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

def __getuserloadedmodules__():
    ''' 3 types of modules; modules the system loads, system modules the 
    user specifically loads with import and user defined modules 
    this function creates a list of the last 2 types ''' 
    
    python27builtin = ["copy_reg", "sre_compile", "_sre", "encodings", "site", \
                       "__builtin__", "sysconfig", "__main__", \
                       "encodings.encodings", "abc", "posixpath", "_weakrefset", \
                       "errno", "encodings.codecs", "sre_constants", "re", \
                       "_abcoll", "types", "_codecs", "encodings.__builtin__", \
                       "_warnings", "genericpath", "stat", "zipimport", \
                       "_sysconfigdata", "warnings", "UserDict", "encodings.utf_8", \
                       "sys", "codecs","_locale", "signal", \
                       "traceback", "linecache", "posix", "encodings.aliases", \
                       "exceptions", "sre_parse", "os", "_weakref"]
        
    python27alwaysloaded = ['heapq', '_sha512', 'functools', 'random', 'unittest.types', \
                            'unittest.pprint',  'pprint', 'collections', 'unittest.sys', \
                            'unittest.main', 'unittest.functools',\
                            'unittest.util', 'unittest.StringIO', 'unittest.re', 'cStringIO',\
                            'unittest.difflib', 'math', 'unittest.case', 'unittest.suite',\
                            'unittest.runner', 'unittest.loader', '_functools', \
                            'StringIO', 'unittest.signal', 'weakref', 'itertools', 'marshal', \
                            '__future__', '_collections', 'unittest','operator', \
                            '_heapq', 'unittest.collections', 'binascii', '_sha256', \
                            'unittest.fnmatch', '_struct', 'hashlib', \
                            'keyword', 'unittest.weakref', 'fnmatch',
                            '_random', '_md5', 'unittest.result', 
                            'unittest.time', '_sha', 'unittest.signals', 'difflib', 'unittest.warnings', 
                            'time', 'unittest.traceback', 'unittest.os']
    
    
    
    from sys import modules
    mods = modules.keys()
    
    for builtinmod in python27builtin:
        try:
            mods.remove(builtinmod)
        except:
            print "info: could not pop builtin mod",builtinmod
        
    for alwaysloaded in python27alwaysloaded:
        try:
            mods.remove(alwaysloaded)
        except:
            print "info: could not pop alwaysloaded mod",alwaysloaded
            
    return(mods)
    
def __getsourceaslist__(module_filename,module):
    from inspect import isclass, isroutine
    tokens = __tokenize__(module_filename)
    
    token=[]
    
    for item in _dir(module):
        obj = getattr(module,item)
        if isclass(obj):
            if isuserclass(item,module_filename):
                token.append(item)
                for m in _getclassmethods(obj):
                    token.append(m)
                    token.append(_getargsfromsource(getattr(obj,m),tokens))
                    token.append(_getvarfromsource(getattr(obj,m)))
                # this gets member vars
                token.append(_getclassmethods(obj,True))
        elif isroutine(obj):
            if isuserfunc(item,module_filename):
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

def imported_sysclasses_remove(classes,thisfilename):
    from sys import modules
    from os.path import splitext    
    usermodules = __getuserloadedmodules__()
    
    for cls in list(classes):
        for usermod in usermodules:
            if hasattr(modules[usermod],cls) and usermod <> splitext(thisfilename)[0]:
                print "remove cls",cls,"from",classes,usermod
                try:
                    classes.remove(cls)
                except:
                    pass
                
def isuserclass(clsname,thisfilename):
    from sys import modules
    from os.path import splitext, basename
    usermodules = __getuserloadedmodules__()
    
    for usermod in usermodules:
        if hasattr(modules[usermod],clsname) and usermod <> basename(splitext(thisfilename)[0]):
            return False
    return True
                
def isuserfunc(funcname,thisfilename):
    from sys import modules
    from os.path import splitext, basename
    usermodules = __getuserloadedmodules__()
    
    for usermod in usermodules:
        try:
            dir(modules[usermod]).index(funcname)
            if usermod <> basename(splitext(thisfilename)[0]):
                return False
        except ValueError:
            pass
        #if hasattr(dir(usermod),funcname) and usermod <> basename(splitext(thisfilename)[0]):
            
    return True
    
def __load_module__(module_abspathname,allowdupe=False):
    
    from importlib import import_module    
    from sys import modules
    from os.path import basename, splitext, join, realpath
    import os
    import sys
    
    reldir = realpath(join(module_abspathname,".."))
    module_name, ext = splitext(basename(module_abspathname))
    
    if modules.has_key(module_name) and allowdupe==False:
        raise Exception("dupe module",module_name)
        
    sys.path.append(reldir)
    import_module(module_name)
    
    globals()[module_name] = modules[module_name] 
    
    return(modules[module_name])

def __convert_filename__(module_filename,new_ext):
    from os.path import basename, splitext
    
    module, ext = splitext(basename(module_filename))
    return(module + ".xml")

if __name__ == "__main__":
    import sys
    
    module_filename = sys.argv[1]
    py2xml(module_filename)    
