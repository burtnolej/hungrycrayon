import sys
import inspect
import types
from os.path import basename, splitext
import xml.etree.ElementTree as xmltree

def __type_as_string__(obj,name):
    if inspect.isclass(obj):
        return("class")
        
    elif inspect.isroutine(obj):
        return("def")
        
    elif inspect.ismodule(obj):
        return("module")
        
    elif inspect.ismethod(obj):
        return("method")

    elif type(obj) is types.StringType:
        return("string")
    
    elif type(obj) is types.ListType:
        return("list")
    else:
        pass
    
def __xmltostring__(root):
    from xml.dom.minidom import parseString
    return parseString(xmltree.tostring(root)).toprettyxml() 

def __add_element__(root,name,objtype):    
    subelement = xmltree.SubElement(root,objtype)
    subelement.set('Name',name) 
    return(subelement)

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

def __get_args__(obj,tokens):
    try:
        return(tokens[inspect.getsourcelines(obj)[-1]][2:])
        
    except:
        return([])
    
def __get_members__(obj,element,tokens):
   
    for name, _obj in inspect.getmembers(obj) :
        
        objtype = __type_as_string__(_obj,name)
        
        if not name.startswith("__") and not name.startswith("func_"):
            
            subelement = __add_element__(element,name,objtype)
            
            if objtype in ['class','def']:
                for _name, __obj in inspect.getmembers(_obj) :
                    if not _name.startswith("__") and not _name.startswith("func_"):
                        _objtype = __type_as_string__(__obj,_name)
                        _sub_element = __add_element__(subelement,_name,_objtype)
                        
                        for arg in __get_args__(__obj,tokens):
                            __add_element__(_sub_element,arg,'var')
                        
                for arg in __get_args__(_obj,tokens):
                    __add_element__(subelement,arg,'var')

def code2xml(module_pathname):
    
    import importlib
    
    module_filename = basename(module_pathname)
    
    sysmodule, ext = splitext(module_filename)
    
    importlib.import_module(sysmodule)
    
    print "info: imported module",sysmodule
    
    
        
    
    
    output_file = sysmodule + ".xml"
    print "info: writing output to",output_file
    
    print "info: converting module",sysmodule,"to xml"
    root = xmltree.Element(module_filename)
    tokens = __tokenize__(module_pathname)
    __get_members__(sysmodule,root,tokens)
    
    f = open(output_file,"w+")
    f.write(__xmltostring__(root))
    f.close()

    
if __name__ == "__main__":
    code2xml(sys.argv[1])