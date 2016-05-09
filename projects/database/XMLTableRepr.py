import unittest
import xml.etree.ElementTree as xmltree

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file, file2string

class XMLTableRepr():
    def __init__(self,xmlparser,ns=None):

        self.tree = xmlparser.tree
        self.xmlparser = xmlparser
        self.table_header = []
        self.table = []
        self.table_row = -1
        self.table_col = -1
        
    def _init_row(self,parent_row_id,parent_tag):
        self.table_row = self._get_next_row_id()
        _row = [self.table_row,parent_row_id, parent_tag]
        self.table.append(_row)
    
        # if this is a root row push table_col to 3 otherwise retain current table_col value
        if self.table_col==-1:
            self.table_col=3

    def _get_next_row_id(self):
        return(len(self.table))
        
    def _add_cell(self,element,link,value=""):
                
        if link==True:
            value = "#"+str(self._get_next_row_id())
        if value==None:
            value =""
    
        # if a child row has just been completed and cursor has moved back to parent
        # we need to append blank cells until caught up.
        if len(self.table[self.table_row])-1 < self.table_col:
            for i in range(len(self.table[self.table_row]),self.table_col):
                self.table[self.table_row].append("")
                
        self.table[self.table_row].append(value + ";" + self.xmlparser._get_attrs_str(element))
        self.table_col+=1
    
    def get_table(self,parent=None,parent_tag="root",parent_row_id=-1):     

        if parent==None:
            parent = self.tree.getroot()

        if not hasattr(self,"table"):
            raise Exception("use the table constructor")
            
        self._init_row(parent_row_id,parent_tag)
        
        for child in parent._children:
            
            if self.xmlparser._has_children(child):
                self._add_cell(child,True) 
                self.get_table(child,child.tag,self.table_row)
                
            else:
                value = child.text
                self._add_cell(child,False,value)
                    
        self.table_row = parent_row_id
        