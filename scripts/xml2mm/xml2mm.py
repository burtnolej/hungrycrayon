
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
import xml.etree.ElementTree as xmltree
from xml_utils import get_xml_elements, \
     get_xml_element,get_xml_child_elements, \
     get_xml_root


tree = xmltree.parse('test_schema_simple.xml')

root = tree.getroot()

color=enum(blue="#0000ff",
           yellow="#0000ff",
           red="#FF0000",
           black="#000000",
           white="#FFFFFF")

blueyellow = enum(STYLE="bubble",
                  COLOR=color.yellow,
                  BACKGROUND_COLOR=color.blue)

redblack = enum(STYLE="bubble",
                  COLOR=color.black,
                  BACKGROUND_COLOR=color.red)

blueblack = enum(STYLE="bubble",
                  COLOR=color.black,
                  BACKGROUND_COLOR=color.green)

blackwhite = enum(STYLE="bubble",
                  COLOR=color.white,
                  BACKGROUND_COLOR=color.black)

ss10=enum(BOLD="true",
          NAME="SansSerif",
          SIZE="10")

ss14=enum(BOLD="true",
          NAME="SansSerif",
          SIZE="14")

ss18=enum(BOLD="true",
          NAME="SansSerif",
          SIZE="18")


Table=
Database=
Column=
Key=
Row=

def _getchildren(parent,depth):
    depth = depth+5
    for element in parent.getchildren():
        
                
        if element.attrib.has_key('Name') == True:
            text_attrib_val = element.tag +":"+element.attrib['Name']
            element.attrib.pop('Name')
        else:
            text_attrib_val = element.tag + ":" + element.text.strip()
            
        element.set('TEXT',text_attrib_val)
        element.tag = 'node'
        element.text = ""

        #print " ".ljust(depth),
        #print element.tag.strip(), element.attrib, element.text.strip()
        _getchildren(element, depth)
    
_getchildren(root,-5)

print xmltree.tostring(root)
    #element.tag = 'node'
    #print dir(element)
    
    #new_element = tree.SubElement(parent,'TEXT')
    #new_element.text = 'foobar'
    
    

#root = get_xml_element('test_schema_simple.xml','root')
#root = get_xml_root('test_schema_simple.xml')
#print dir(root)
#children = get_xml_child_elements(root)
#print children
    