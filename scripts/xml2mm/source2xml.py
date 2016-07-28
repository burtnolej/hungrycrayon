import sys
from os.path import isfile
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
sys.path.append("/home/burtnolej/Development/pythonapps3/projects/database")

import xml.etree.ElementTree as xmltree
from XMLCreator import XMLCreator

def brackets_posn(element):
    # will raise an exception if either cannot be found
    return(element.index("("),element.index(")"))
    
def parse_signature(line):

    try:
        openb,closeb = brackets_posn(line)
        method_name = line[:openb]
        args = line[openb+1:closeb].split(",")
        return(method_name,args)
    except:
        # not preceded by brackets (import?)
        return(line,)
    
def parse(filename):
    
    f = open(filename,"r")
    
    for line in f:    
        
        tokens = tokens=line.strip().split(" ")
        
        # extract the first token to determine the purpose of this line
        line_type = tokens[0]
        
        # remove the used token and rejoin the remaining. also 
        # removes unnecessary spaces
        tokens.pop(0)
        line = "".join(tokens)
    
        if len(line) > 0:
            if line[0] == "=":
                code['var'].append((line_type,line[1:]))
            else:
                if not code.has_key(line_type):
                    code[line_type] = []
                    
                code[line_type].append(parse_signature(line))
                
    f.close()

def xmltostring(root):
    from xml.dom.minidom import parseString
    return parseString(xmltree.tostring(root)).toprettyxml() 

import tokenize
st = tokenize.generate_tokens(open('oo-example.py').readline)

# index by line_no
std = {}
for _st in st:
    if _st[0] == 1:
        line_no = _st[2][0]
        token = _st[1]

        if not std.has_key(line_no):
            std[line_no] = []
        std[line_no].append(token)
        

print std

'''code = {}
code['var'] = [] # theres always at least variables

root = xmltree.Element(sys.argv[1])

parse(sys.argv[1])

for line_type,type_instances in code.iteritems():
    
    subelement = xmltree.SubElement(root,line_type)

    for type_instance in type_instances:
        leafelement = xmltree.SubElement(subelement,line_type)
        leafelement.text = type_instance[0]

        print "adding tag",line_type,"with text",type_instance[0]


print xmltostring(root)
'''