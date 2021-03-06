
import sys
from os.path import isfile
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
import xml.etree.ElementTree as xmltree
from misc_utils import enum
from format_utils import burgundywhite18, darkbluelightblue16, greyblack18, \
     yellowburgundy14, lightblueburgundy16, blackgreen14, whiteblack14i
import format_utils
from getopt import getopt

class ConvertXML2Freemind():
    
    def __init__(self,input_filename,output_filename):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.fmformat=enum()
        
    def convert(self,full_label=False):
    
        self.root = xmltree.parse(self.input_filename).getroot()
        self.parse_format()
        self.parse(self.root,full_label)
        
        self.root.tag = "map"
        self.root.set('version',"0.9.0")
        
    def parse_format(self):
        for element in self.root.findall('Format'):
            setattr(self.fmformat,element.find('Key').text,
                    element.find('Value').text)
            
        # remove all the format tags now that we have processed.
        # need to do this outside of the processing for loop
        # hence the dupe code
        for element in self.root.findall('Format'):
            self.root.remove(element)
                
    def parse(self,parent,full_label=True):
        for element in parent.getchildren():
            
            # add a new sub element for each attribute
            if len(element.attrib.keys()) > 0:
                for key,value in element.attrib.iteritems():
                    # its added in the input style and then will be converted later
                    self.element_add_subelement(element,key + ":" + value)               
                    
            # apply formating
            self.element_add_attrib_format(element,element.tag)
            self.element_add_subelement_font(element,element.tag)
            
            # if a specific attribute is present, use it in the new tag name
            if element.attrib.has_key('Name') == True:
                if full_label == True:
                    attr_text = element.tag +":"+element.attrib['Name']
                else:
                    attr_text = element.attrib['Name']
                    
                element.attrib.pop('Name')            
            else:
                # otherwise just use the old tag as the new tag name
                attr_text = element.tag 
                if element.text <> None and full_label == True:
                    attr_text += ":" + element.text.strip()
    
            # set the new tag name (implemented as an ATTRIB in freemind)
            # call all tags 'node'
            if element.tag <> 'font':
                element.set('TEXT',attr_text)
                element.tag = 'node'
            element.text = ""
            
            # get next set of children
            self.parse(element,full_label)
            
    def element_add_attrib_format(self, element,output_format_type):
        
        if hasattr(self.fmformat,output_format_type): # else no format specified so ignore
            element_format = getattr(self.fmformat,output_format_type)
        
            for _key in ['STYLE','COLOR','BACKGROUND_COLOR']:
                element.set(_key,getattr(eval(element_format),_key))

    def element_add_subelement_font(self,element,output_format_type):
        if hasattr(self.fmformat,output_format_type): # else no format specified so ignore
            element_format = getattr(self.fmformat,output_format_type)
        
            new_element = xmltree.SubElement(element,'font')
            for _key in ['BOLD','NAME','SIZE',"ITALIC"]:
                new_element.set(_key,getattr(eval(element_format).FONT,_key))
              
    def element_add_subelement(self,element,tag):
        return(xmltree.SubElement(element,tag))
    
    def dump_tofile(self):
        f = open(self.output_filename,"w+")
        f.write(xmltree.tostring(self.root))
        f.close()


if __name__ == "__main__":
    
    if not isfile(sys.argv[1]) or not isfile(sys.argv[2]):
        print "usage: xml2mm.py <input xml file> <output xml file> [-full]"
        exit()


    #print getopt(sys.argv)
    #exit()
    
    x2fm = ConvertXML2Freemind(sys.argv[1],sys.argv[2])
    x2fm.convert(True)
    x2fm.dump_tofile()