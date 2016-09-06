import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from xml_utils import element_find_by_attrib_value, element_move, element_fuse, \
     element_parent_get, element_find_tags,element_find_children, xmltree

import pycurl
import curl
from io import BytesIO

#url: curl -H "Content-Type: application/xml" -d '<list><q>butter</q><max>25</max><offset>0</offset></list>' DEMO_KEY@api.nal.usda.gov/ndb/search

def urlpost(server,header,postfields,buffer,username=None,password=None):
    c = pycurl.Curl()
    c.setopt(c.URL, server)
    c.setopt(c.VERBOSE,True)
    c.setopt(c.HTTPHEADER,[header])
    
    if postfields <> None:
        c.setopt(c.POSTFIELDS,postfields)
    c.setopt(c.WRITEDATA, buffer)

    print password
    
    if username <> None and password <> None:
        
        c.setopt(c.USERPWD, '%s:%s' % (username, password))        
    c.perform()
    c.close()
    
    return(buffer.getvalue())


body = urlpost(server="https://api.github.com/users/burtnolej",
               header="Content-Type:application/json; charset=utf-8",
               postfields="",
               buffer = BytesIO(),
               username="burtnolej@googlemail.com",
               password="natwest1")

print body

exit()

body = urlpost(server="ZJjApBRrcjlz1dd3fw1PAoQghya6ia8GgCBUu7cC@api.nal.usda.gov/usda/ndb/search",
               header="Content-Type:application/xml",
               postfields="<list><q>butter,without salt</q><fg>Dairy and Egg Products</fg><max>25</max><offset>0</offset></list>",
               buffer = BytesIO())

xmlroot = xmltree.fromstring(body)

items = xmlroot.findall(".//item") 

for item in items:
    for child in item.getchildren():
        print child.tag,"=",child.text,
    print
    
#print items[0].getchildren()

exit()

body = urlpost(server="ZJjApBRrcjlz1dd3fw1PAoQghya6ia8GgCBUu7cC@api.nal.usda.gov/usda/ndb/reports",
               header="Content-Type:application/xml",
               postfields="<report><ndbno>01009</ndbno><type>f</type></report>",
               buffer = BytesIO())

xmlroot = xmltree.fromstring(body)

fat = ['Fatty acids, total saturated', 'Fatty acids, total monounsaturated',
       'Fatty acids, total polyunsaturated','Fatty acids, total trans',
       'Cholesterol']

nutrient_elements = xmlroot.findall(".//nutrient")

useful_attribs = ['group','name','value','unit']
for el in nutrient_elements:
    for us in useful_attribs:
        print el.attrib[us],
    
    
    for measure in  el.getchildren()[0].getchildren():
        print "[",measure.attrib['label'],"=",measure.attrib['value']+"]",
    print
    
    
    
