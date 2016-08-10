
import sys
from os.path import isfile, splitext, basename
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
import xml.etree.ElementTree as xmltree
from misc_utils_enum import enum
from misc_utils_generic import GenericBase

from format_utils import burgundywhite18, darkbluelightblue16, greyblack18, \
     yellowburgundy14, lightblueburgundy16, blackgreen14, whiteblack14i
import format_utils
from xml_utils import element_fuse, element_parent_get, element_attrib_as_string
from getopt import getopt
from datetime import datetime
from copy import deepcopy
from inspect import getmembers, isclass
from types import InstanceType
from pprint import pprint

class xml2freemind(GenericBase):

    def __init__(self,**kwargs):
        
        for k,v in kwargs.iteritems():
            setattr(self,k,v)

        #self.input_filename =arg[0]
        
        self.fmformat=enum()
        self.root = xmltree.parse(self.input_filename).getroot()
        self.input_base = basename(self.input_filename)
        
        date = datetime.now().strftime("%H%M%S")
                   
        if not hasattr(self,'output_filename') or self.output_filename == None:
            self.output_filename = splitext(self.input_filename)[0]+".mm"
            
        if not hasattr(self,'verbosity'):
            self.verbosity = 1

        self.log_filename = splitext(self.output_filename)[0]+".log." + date
        self.log = open(self.log_filename,"w+")
        
        #self._log(3,"args set:",kwargs)
        
    @classmethod
    def convert(cls,*arg,**kwarg):
        cls1 = cls(*arg,**kwarg)
        cls1._convert()
        return(cls1)
    
    @classmethod
    def groupby(cls,*arg,**kwarg):
        cls1 = cls(*arg,**kwarg)
        cls1.parse_add_groupby()
        return(cls1)
    
    @classmethod
    def inputformat(cls,*arg,**kwarg):
        cls1 = cls(*arg,**kwarg)
        cls1.parse_format_file()
        return(cls1)

        
    def __del__(self):
        self.log.close()
        
    def _log(self,priority,*args):
        from inspect import stack
        from os.path import basename
        
        if priority < self.verbosity:
            listargs = []
            
            if priority == 3:
                listargs.append("info".ljust(6))
            
            now = datetime.now().strftime("%H%M%S")
            
            listargs.append(now.ljust(8))
            callerframe = stack()[1]
            listargs.append(callerframe[3].ljust(30))
            listargs.append(str(callerframe[2]).ljust(4))
            listargs.append(" ".join(list(args)))
            listargs.append(" ("+basename(callerframe[1]) + ")")
    
            self.log.write("".join(listargs)+"\n")
        
    def _convert(self):
        # add any groupby branches to original xml
        if hasattr(self,'groupby_tag'): self.parse_add_groupby()
        
        # insert a universal parent in the event that the root has
        # more than 1 child. this is because freemind ignores the 1 node (tag=map)
        if len(self.root.getchildren()) > 1:
            self.root = element_fuse(self.root,self.input_base,self.root)

        self.parse_format_file()
        self.parse_format()        
        self.parse()
        
        self.root.tag = "map"
        self.root.set('version',"0.9.0")
        
        self.dump_tofile(self.root)
        
    def parse_format_file(self):
        if hasattr(self,'input_format_filename'):
            formatxmltree = xmltree.parse(self.input_format_filename).getroot()
            for format in formatxmltree.getchildren():
                self.root.append(format)
            
    def parse_format(self,root=None):
        
        if root==None:
            root=self.root
            
        for element in root.findall('.//Format'):
            if not element.attrib.has_key('Name'):
                self._log(1,"malformed format; no Name attrib") 
                next
                
            _name = element.attrib['Name']
            _value = element.text
            
            if not hasattr(format_utils,_value):
                self._log(1,"malformed format;value",_value,'not in format_utils')
                next    
            
            setattr(self.fmformat,_name,_value)
            self._log(3,"format",_value," added for",_name)
            
        # remove all the format tags now that we have processed.
        # need to do this outside of the processing for loop
        # hence the dupe code

        for element in root.findall('.//Format'):
            parent = element_parent_get(root,element)
            parent.remove(element)
                
    def parse_add_groupby(self,root=None):
        
        # shorten
        
        el_add_sub = self.element_add_subelement
        
        if root==None:
            root=self.root
            
        root_copy = deepcopy(self.root)
        
        for element in root.iter():
            
            # if the tag is one of the groupby tags append it to the respective
            # groupby branch

            if element.tag in self.groupby_tag:
                self._log(3,element.tag,"is a groupby tag")
                element_groupbys = root_copy.findall('.//groupby')
                element_groupby=None
                
                if len(element_groupbys) == 0:
                    self._log(3,"no groupby parent detected for",element.tag)
                    element_groupby = el_add_sub(root_copy,"groupby",('Name',element.tag))
                    element_groupbys.append(element_groupby)
                    
                _str = element_attrib_as_string(element) 
                
                for _element_groupby in element_groupbys:
                    if _element_groupby.attrib['Name'] == element.tag:            
                        element_groupby = el_add_sub(_element_groupby,element.tag,('Name',_str))
                    else:
                        self._log(3,"cannot identify node as no tag=Name",element.tag)
                        
                if element_groupby == None:
                    self._log(3,"groupby nodes exist but not for tag=",element.tag)
                    _element_groupby = el_add_sub(root_copy,"groupby",('Name',element.tag))            
                    element_groupby = el_add_sub(_element_groupby,element.tag,('Name',_str))

                    
        self.root = root_copy

    def parse(self,parent=None):
        
        if parent==None:
            parent=self.root
            
        for element in parent.getchildren():
            
            # add a new sub element for each attribute but ignore
            # font subelements that have just been added
            if len(element.attrib.keys()) > 0 and element.tag <> 'font':
                for key,value in element.attrib.iteritems():
                    if not hasattr(self,'suppress_attrib') or key not in self.suppress_attrib:
                        # its added in the input style and then will be converted later
                        self.element_add_subelement(element,key + ":" + value)
                    else:
                        self._log(3,"supressing attrib:",key,element.tag)                        
                    
            # apply formating
            self.element_add_attrib_format(element,element.tag)
            self.element_add_subelement_font(element,element.tag)
            
            # if a specific attribute is present, use it in the new tag name
            if element.attrib.has_key('Name') == True:
                if hasattr(self,'full_label') and self.full_label == True:
                        attr_text = element.tag +":"+element.attrib['Name']
                        self._log(3,"full_label=True so creating long label",
                                     attr_text)
                else:
                    attr_text = element.attrib['Name']
                    self._log(3,"full_label=False so creating short label",
                              attr_text)
                
                element.attrib.pop('Name')            
            else:
                # otherwise just use the old tag as the new tag name
                attr_text = element.tag 
                if element.text <> None and self.full_label == True:
                    attr_text += ":" + element.text.strip() 

            # set the new tag name (implemented as an ATTRIB in freemind)
            # call all tags 'node'
            # ignore 'specials' like font and groupbys
            if element.tag <> 'font' and element.tag <> 'Format':
                element.set('TEXT',attr_text)
                element.tag = 'node'
            element.text = ""
            
            self.parse(element)
        
    
        
    def element_add_attrib_format(self, element,output_format_type):
        
        if hasattr(self.fmformat,output_format_type): # else no format specified so ignore
            element_format = getattr(self.fmformat,output_format_type)
            
            format_attribs = eval(element_format).attr_get_keyval(include_callable=False,
                                                                  include_nondataattr=False)
            
            for _key,_value in format_attribs:
                if _key <> "FONT":
                    # ignore font as it is separataly added as its
                    # own node
                    element.set(_key,_value)
                
                self._log(3,"adding format attributes",
                          _key,
                          " for:",
                          output_format_type)
        else:
            self._log(3, "no format definition for ",
                      output_format_type)
            
            
    def element_add_subelement_font(self,element,output_format_type):
        if hasattr(self.fmformat,output_format_type): # else no format specified so ignore
            element_format = getattr(self.fmformat,output_format_type)
        
            new_element = xmltree.SubElement(element,'font')
            for _key in ['BOLD','NAME','SIZE',"ITALIC"]:
                new_element.set(_key,getattr(eval(element_format).FONT,_key))
                
            self._log(3,"adding font subelement for:",
                      output_format_type)
              
    def element_add_subelement(self,element,tag,attrib=None):
        ''' attrib is a tuple of namevalue '''
        self._log(3,"adding sub element=",
                  tag,
                  "as node for element=",
                  element.tag,
                  "with attribs=",
                  str(attrib))
        element = xmltree.SubElement(element,tag)
        if attrib <> None:
            element.set(attrib[0],attrib[1])
        
        return(element)
    
    def dump_tofile(self,tree=None):
        
        f = open(self.output_filename,"w+")
        
        if tree<>None:
            f.write(xmltree.tostring(tree))
        else:
            f.write(xmltree.tostring(self.root))
        f.close()


if __name__ == "__main__":

    def printusage(msg):
        print "\nusage: --input=<python file> --output=<python file>"
        print msg
        exit()
            
    rules = ['input=']
    input_file = None
    
    try:
        options,remainder = getopt(sys.argv[1:],'',rules)
    except GetoptError, e:
        printusage("error:",e.msg)
    
    args={}
    for option, value in options:
        if option == '--input':
            args['input_filename'] = value
        if option == '-output':
            args['output_filename'] = value
    
    if not args.has_key('input_filename') or not isfile(args['input_filename']):
        printusage("error: --input arg must be set to a real file")
        
    if args.has_key('output_filename') and not isfile(args['output_filename']):
        printusage("error: --output arg must be set to a real file")

    xmlfile = xml2freemind.convert(**args)

    #fmfile = xml2freemind(xmlfile,1).output_filename
    #print "info: result written to",fmfile

