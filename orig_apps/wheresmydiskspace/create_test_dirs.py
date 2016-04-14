from sys import path,stdout,argv
import sys
import os
path.append("/Users/burtnolej/Dev/pythonapps/util")
from filesystem_util import create_empty_file,gnu_du
from datetime_util import MyDT
import xml.etree.ElementTree as xmltree

def get_next_id():
    now_secs = MyDT.now(display_fmt='%S.%f').value
    now_secs = int(round(float(now_secs),4)*10000)
    now_secs = hex(now_secs)
    return(now_secs)

tree = xmltree.parse("./test_tree_1file.xml")

def p_dir(d):
    for f in d.getchildren():
        gni = get_next_id()
        if f.tag == 'dir':
            print 'dir',gni
            os.makedirs(gni)
            os.chdir(gni)
            p_dir(f)
        else:
            print 'file',gni
            create_empty_file(1024,int(f.text),gni)
    os.chdir('..')

top_dir = tree.find('dir')
p_dir(top_dir)
    

exit()
bs=1024
c=10
fid = get_next_id()
of = fid + "_" + str(bs*10/1024)
create_empty_file(bs,c,of)

#gnu_du(of)
