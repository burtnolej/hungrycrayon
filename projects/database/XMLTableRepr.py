import unittest
import xml.etree.ElementTree as xmltree

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file, file2string, read_text_from_file, gettype

class XMLTableRepr():
    def __init__(self,ns=None):
        self.table_header = []
        self.table = []
        
    @classmethod
    def fromxml(cls,xmlparser):
        ''' constructor to create table from XML tree'''
        cls1 = cls()
        cls1.tree = xmlparser.tree
        cls1.xmlparser = xmlparser
        cls1.table_row = -1
        cls1.table_col = -1
        return(cls1)
        
    @classmethod
    def fromfile(cls,filename):
        ''' costructor to read in a table from a file; primarilly used in testing'''
        cls1 = cls()
        raw_data = read_text_from_file(filename,"^")
        cls1.table = raw_data[1:]
        cls1.table_header = raw_data[0]
        return(cls1)
            
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
        
        _cell_value = str(value) + self.xmlparser._get_attrs_str(element)    
        
        # store as an int/float if possible
        self.table[self.table_row].append(gettype(_cell_value))
            
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
                value = gettype(child.text)
                self._add_cell(child,False,value)
                    
        self.table_row = parent_row_id
        
    def print_table(self):
        ''' output a table to the screen; used for debugging'''
        print
        for _row in self.table:
            print _row
        

class TestXMLTableRepr(unittest.TestCase):
    
    def setUp(self):
        self.expected_results = [['_id','_parent','_type','food-name','food-mfr','food-serving','food-calories','food-total-fat','food-saturated-fat','food-cholesterol','food-sodium','food-carb','food-fiber','food-protein','food-vitamins','vitamins-a','vitamins-c','food-minerals','minerals-ca','minerals-fe'],
                                 [0,-1,'root','#1;id="0002"'],
                                 [1,0,'food','','Bagels New York Style','Thompson','104;units="g"',';total="300",fat="35"',4,1,0,510,54,3,11,'#2','','','#3'],
                                 [2,1,'vitamins','','','','','','','','','','','','','',0,0],
                                 [3,1,'minerals','','','','','','','','','','','','','','','','',8,20]]        
    
    def tearDown(self):
        pass
    
    def test_fromfile(self):
        ''' basic test '''
        self.xmltablerepr = XMLTableRepr.fromfile("test_fromfile.csv")
        values = self.xmltablerepr.table
        
        # set expected results: the number of elements returned 
        _expected_results = self.expected_results[1:]

        # assert correctness
        self.assertEquals(values,_expected_results)
        
        
        
if __name__ == "__main__":
    
    suite = unittest.TestSuite()
    suite.addTest(TestXMLTableRepr("test_fromfile"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    