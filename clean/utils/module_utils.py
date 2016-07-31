#/usr/bin/python

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

def py2xml(module_filename,module=None):
    from inspect import getmembers, isclass, isroutine
     
    if module==None:
        module = __load_module__(module_filename)
            
    tokens = __tokenize__(module_filename)
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

def __load_module__(module_abspathname):
    
    from importlib import import_module    
    from sys import modules
    from os.path import basename, splitext, join, realpath
    import os
    import sys
    
    reldir = realpath(join(module_abspathname,".."))
    module_name, ext = splitext(basename(module_abspathname))
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
