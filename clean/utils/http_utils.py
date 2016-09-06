import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from xml_utils import element_find_by_attrib_value, element_move, element_fuse, \
     element_parent_get, element_find_tags,element_find_children, xmltree

import pycurl
from io import BytesIO

def urlpost(server,header,postfields,buffer):
    c = pycurl.Curl()
    c.setopt(c.URL, server)
    c.setopt(c.VERBOSE,True)
    c.setopt(c.HTTPHEADER,[header])
    c.setopt(c.POSTFIELDS,postfields)
    c.setopt(c.WRITEDATA, buffer)

    c.perform()
    c.close()

    return(buffer.getvalue())