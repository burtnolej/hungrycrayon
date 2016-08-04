
from lxml import etree
data = open('schedule.html','r').read()
doc = etree.HTML(data)

#for tr in doc.xpath('//table/tr[@class="trmenu1"]'):
for tbl in doc.xpath('//table'): 
    for tr in tbl.xpath('//tr'):    
        for element in tr.iter():
            if element.tag == "font" and element.text <> None:
                print element.text.replace("\n","").replace(" ","").replace("\t",""),
        print "tr finish"
    print "tbl finish"