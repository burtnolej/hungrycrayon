
import sys
from os.path import isfile
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
import xml.etree.ElementTree as xmltree
from misc_utils import enum
from format_utils import burgundywhite18, darkbluelightblue16, greyblack18, \
     yellowburgundy14, lightblueburgundy16, blackgreen14, whiteblack14i
import format_utils
from getopt import getopt

class xml2freemind():
    
    def __init__(self,input_filename,output_filename,full_label=False):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.fmformat=enum()
        self.full_label = full_label
        self.convert()
        
    def convert(self):
    
        self.root = xmltree.parse(self.input_filename).getroot()
        self.parse_format()
        self.parse(self.root)
        
        self.root.tag = "map"
        self.root.set('version',"0.9.0")
        
        self.dump_tofile()
        
    def parse_format(self):
        for element in self.root.findall('Format'):
            
            _key = element.find('Key')
            _value = element.find('Key')
            
            if len(_key) == None:
                raise Exception (element.text, "does not have a Key subelement")
            elif len(_value) == None:
                raise Exception (element.text, "does not have a Value subelement")
            else:
                setattr(self.fmformat,element.find('Key').text,
                        element.find('Value').text)
            
        # remove all the format tags now that we have processed.
        # need to do this outside of the processing for loop
        # hence the dupe code
        for element in self.root.findall('Format'):
            self.root.remove(element)
                
    def parse(self,parent):
        for element in parent.getchildren():
            
            # add a new sub element for each attribute but ignore
            # font subelements that have just been added
            if len(element.attrib.keys()) > 0 and element.tag <> 'font':
                for key,value in element.attrib.iteritems():
                    # its added in the input style and then will be converted later
                    self.element_add_subelement(element,key + ":" + value)               
                    
            # apply formating
            self.element_add_attrib_format(element,element.tag)
            self.element_add_subelement_font(element,element.tag)
            
            # if a specific attribute is present, use it in the new tag name
            if element.attrib.has_key('Name') == True:
                if self.full_label == True:
                    attr_text = element.tag +":"+element.attrib['Name']
                    print "info: full_label=True so creating long label",attr_text
                else:
                    attr_text = element.attrib['Name']
                    print "info: full_label=False so creating short label",attr_text
                    
                element.attrib.pop('Name')            
            else:
                # otherwise just use the old tag as the new tag name
                attr_text = element.tag 
                if element.text <> None and self.full_label == True:
                    attr_text += ":" + element.text.strip()
    
            # set the new tag name (implemented as an ATTRIB in freemind)
            # call all tags 'node'
            if element.tag <> 'font':
                element.set('TEXT',attr_text)
                element.tag = 'node'
            element.text = ""
            
            # get next set of children
            self.parse(element)
            
    def element_add_attrib_format(self, element,output_format_type):
        
        if hasattr(self.fmformat,output_format_type): # else no format specified so ignore
            element_format = getattr(self.fmformat,output_format_type)
        
            for _key in ['STYLE','COLOR','BACKGROUND_COLOR']:
                element.set(_key,getattr(eval(element_format),_key))
                
                print "info: adding format attributes",_key," for:", output_format_type
        else:
            print "info: no format definition for",output_format_type
            
    def element_add_subelement_font(self,element,output_format_type):
        if hasattr(self.fmformat,output_format_type): # else no format specified so ignore
            element_format = getattr(self.fmformat,output_format_type)
        
            new_element = xmltree.SubElement(element,'font')
            for _key in ['BOLD','NAME','SIZE',"ITALIC"]:
                new_element.set(_key,getattr(eval(element_format).FONT,_key))
                
            print "info: adding font subelement for:", output_format_type
              
    def element_add_subelement(self,element,tag):
        print "info: adding attrib",tag," as node for element",element.tag
        return(xmltree.SubElement(element,tag))
    
    def dump_tofile(self):
        f = open(self.output_filename,"w+")
        f.write(xmltree.tostring(self.root))
        f.close()


if __name__ == "__main__":
    
    if not isfile(sys.argv[1]) or not isfile(sys.argv[2]):
        print "usage: xml2mm.py <input xml file> <output xml file> [-full]"
        exit()

    xml2freemind(sys.argv[1],sys.argv[2])