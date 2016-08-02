
import sys
from os.path import isfile, abspath
from getopt import getopt, GetoptError, gnu_getopt
import xml.etree.ElementTree as xmltree

sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/scripts/xml2freemind")
from module_utils import __getsourceaslist__, __load_module__, isuserfunc, \
     isuserclass, __tokenize__, _dir, __add_element__, _getargsfromsource, \
     _getvarfromsource, __convert_filename__, __xmltofile__, _getclassmethods
from xml2freemind import xml2freemind

class py2xml():
    def py2xml(self,**kwargs):
        
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
                
        if not hasattr(self,'module'):
            self.module = __load_module__(self.input_filename,allowdupe=True)
            
        from inspect import getmembers, isclass, isroutine
                
        tokens = __tokenize__(self.input_filename)
        root = xmltree.Element('root')
        
        for item in _dir(self.module):
            obj = getattr(self.module,item)
            
            if isclass(obj):
                if isuserclass(item,self.input_filename):
                    cls_element = __add_element__(root,item,'class')
                    for m in _getclassmethods(obj):
                        clsmth_element = __add_element__(cls_element,m,'method')
                        
                        for arg in _getargsfromsource(getattr(obj,m),tokens):
                            __add_element__(clsmth_element,arg,'arg')
                        
                        for var in _getvarfromsource(getattr(obj,m)):
                            __add_element__(clsmth_element,var,'var')
        
                    for memvar in _getclassmethods(obj,True):
                        __add_element__(cls_element,memvar,'var')
                    
            elif isroutine(obj):
                if isuserfunc(item,self.input_filename):
                    def_element = __add_element__(root,item,'def')
                    
                    for arg in _getargsfromsource(obj,tokens):
                        __add_element__(def_element,arg,'arg')
                    
                    for var in _getvarfromsource(obj):
                        __add_element__(def_element,var,'var')        
            else:
                __add_element__(root,item,'var')
        
        output_filename = __convert_filename__(self.input_filename,".xml")
        __xmltofile__(root,output_filename)
        
        return(output_filename)


def printusage(msg):
    print "\nusage: --input=<python file>"
    print msg
    exit()
        
rules = ['input=','verbosity=']
input_file = None

try:
    options,remainder = getopt(sys.argv[1:],'',rules)
except GetoptError, e:
    printusage("error:"+e.msg)

args={}
for option, value in options:
    if option == '--input':
        args['input_filename'] = abspath(value)
    if option == '--verbosity':
        args['verbosity'] = value

if not args.has_key('input_filename') or not isfile(args['input_filename']):
    printusage("error: --input arg must be set to a real file")
    
xmlfile = py2xml().py2xml(**args)
print "info: passing",xmlfile,"to xml2freemind"

args['input_filename'] = abspath(xmlfile)
fmfile = xml2freemind.convert(**args).output_filename
print "info: result written to",fmfile


