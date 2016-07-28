import unittest
import xml.etree.ElementTree as xmltree

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file, file2string

class XMLCreator():
    
    def __init__(self, root_tag, filen=None, ns=None):
        self.filen = filen
        self.tree = xmltree.Element(root_tag)


    # helper methods to keep codde readable
    # ------------------------------------------------------------
    
    @staticmethod
    def _isroottype(value):
        if value == "root":
            return True
        return False

    @staticmethod
    def _contains(source_str,search_char):
        try:
            source_str.index(search_char)
            return True
        except:
            return False
    
    @staticmethod
    def _gettagname(value):
        # get the corresponding header for this column
        # index 0 contains the record_type which is not required for processing
        return(value[1])

    @staticmethod
    def _isvalidheader(value):
        # so value #3 means this tag has children represented in row 3
        if XMLCreator._contains(value,"-"):
            return True
        return(False)
    
    @staticmethod
    def _getheaderinfo(value):
        items = value.split("-")
        if len(items)>2:
            raise Exception("must be of the form 'eek-eek'")
        return((items[0],items[1]))  

    @staticmethod
    def _isref(value):
        # so value #3 means this tag has children represented in row 3
        if value.startswith("#"):
            return True
        return(False)

    @staticmethod
    def _containsattr(value):
        # so 24;"unit=g" represents an element tag has an attribute
        if XMLCreator._contains(value,";"):
            return True
        return False

    @staticmethod
    def _getattr(value):
        items = value.split(";")
        if len(items)>2:
            raise Exception("must be of the form 'blah;blah'")
        return(items[0],items[1])
    
    
    @staticmethod
    def _getattr2(value):
        # value is of the form <tag>;<attr=attrval>,<attr=attrval>....
        attrs=[]
        items = value.split(";")
        if len(items)>2:
            raise Exception("must be of the form 'blah;blah'")
        
        tag = items[0]
        if len(items)==2:
            attrs = items[1].split(",")
        return(tag,attrs)

    @staticmethod
    def _getattr_value(value):
        items = value.split("=")
        if len(items)>2:
            raise Exception("must be of the form 'yeh=yeh'")
        return(items[0],items[1])    

    @staticmethod
    def _hasattr(value):    
        if len(value)<>0:
            return True
        return False

    @staticmethod
    def _isset(value):
        if value<>"":
            return True
        return False
    

    @staticmethod
    def _isnotset(value):
        if value=="":
            return True
        return False
    
    @staticmethod
    def _removetrailingblanks(row):
        # remove any trailing empty columns; probably their because of a spreadsheet export to csv
        for i in range(len(row)-1,-1,-1): # need to set -1 as end to get a zero
            if XMLCreator._isset(row[i]):
                new_row = list(row[:i+1])
                return (new_row)

    # constructors
    # ------------------------------------------------------------

    @classmethod
    def table(cls, root_tag,table, filen=None, ns=None):
        cls1 = cls(root_tag,filen,ns)
        #cls1.table = table
        
        # interim tables to drive the _table2xml member method
        cls1.table_root_ids=[] # list of ids containing the root rows
        cls1.table_records = {}
        
        # split the columns 1,2&3 (fixed ref) from the remaining n columns (variable data)
        ref_table = zip(*table)[:3]
        data_table = zip(*table)[3:]
        
        ref_table = zip(*ref_table)
        data_table = zip(*data_table)
    
        # separate out the headers
        cls1.data_table_headers = data_table[0]
    
        # remove the header rows
        cls1.ref_table = ref_table[1:]
        cls1.data_table = data_table[1:]
    
        # calc lengths to iter over latere
        cls1.data_table_width = len(data_table[0])
        cls1.table_depth = len(data_table)

        return(cls1)
    
    
    # private member methods
    # ---------------------------------------------------
    def _table2xml(self,record_id,parent):            

        values = self.table_records[int(record_id)]['values']
        
        if values<>None:

            for value in values:
                if XMLCreator._isset(value):
                    # ignore blanks; they represent fields that are not used for this type of record
    
                    tag_value,attrs = self._getattr2(value)
    
    
    
                    index = values.index(value)
                    tag = self._gettagname(self.data_table_headers[index])
                    element = self.add_child_tag(parent,tag)
    
                    if self._hasattr(attrs):
                        for attr in attrs:    
                            attr_name,attr_value=self._getattr_value(attr)
    
                            # add attribute to the element
                            self.add_attr(element,attr_name,attr_value)
    
                    if self._isref(tag_value):
                        # then element has children; process child
                        self._table2xml(tag_value[1:],element)
                    else:
                        # no children so just set text
                        if tag_value<>"":
                            self.update_element(element,tag_value)
                        
    # public member methods
    # ------------------------------------------------------------
    def write(self): 
        write_text_to_file(self.filen,self.tree.dump())

    def dump(self,root=None):
        if root==None:
            root=self.tree
        return(xmltree.tostring(root))
        
    def pprint(self,root=None):        
        from xml.dom.minidom import parseString
        
        if root==None:
            root=self.tree
            
        return(parseString(xmltree.tostring(root)).toprettyxml())        

    def add_child_tag(self,parent,tag):
        return(xmltree.SubElement(parent,tag))
                
    def add_child_element(self,element,child):    
        element.append(child)
    
    def add_attr(self,element,attr,attr_val):
        element.set(attr,attr_val)
    
    def update_element(self,element,text):
        element.text = text
                  
    def table2xml(self):
        ''' takes a raw table and populates 2 member attributes
        table_root_ids : a list of root ids (children of the actual)
        records : a dict indexed by root ids 
        data_table_headers : column headers being used as tags '''
        
        # process headers to classify as sub types
        # assume that column 1,2,3 are id,parent,type
        i=0
        _data_table_headers = self.data_table_headers
        self.data_table_headers = []
        
        for data_table_header in _data_table_headers:
            if self._isvalidheader(data_table_header):
                # its a column description (token1-token2) where token2 is a field 
                # in record token 1 
                self.data_table_headers.append(self._getheaderinfo(data_table_header))
            else:
                raise exception("header needs to be in the form 'token-token'")
            
        # pre process data rows
        i=0
        for ref_row in self.ref_table:
            _id,_parent,_type = ref_row
            
            # store root ids separately
            # to process table and build xml; we take each root row and follow all lookups until root is row is complete
            if self._isroottype(_type):
                self.table_root_ids.append(_id)
                
            d = {}
            data_values = self._removetrailingblanks(self.data_table[i])
            d['parent'] = _parent
            d['type'] = _type
            d['values'] = data_values
            self.table_records[_id] = d
            i+=1
        

        for root_id in self.table_root_ids:
            self._table2xml(root_id,self.tree)

        return(self.dump())
        
class TestXMLCreatorTable2XML(unittest.TestCase):   
    
    def test_table_to_xml_single_child_tag(self):
        ''' test : 1: adding children to elements, 2: adding an attribute to an element '''
        
        table = [["_id","_parent","_type","root-food","food-name"],
                 [1,"","root","#2;id=1","","","",""],
                 [2,1,"food","","Avocado Dip"]]
  
        # set expected results
        expected_results = file2string("test_basic_xmlcreator_single_child_tag.xml")
    
        # test prep
        xmlcreator = XMLCreator.table("nutrition",table)
    
        # execute test
        results = xmlcreator.table2xml()
    
    
        # assert correctness
        self.assertEqual(expected_results.rstrip(),results.rstrip())
        
    def test_table_to_xml_single_grandchild(self):
        ''' test 1: adding grandchildren to elements '''
        
        table = [["_id","_parent","_type","root-food","food-foo","foo-bar"],
                 [1,"","root","#2;id=1","",""],
                 [2,1,"food","","#3","",""],
                 [3,2,"foo","","","foobar"]]
  
        # set expected results
        expected_results = file2string("test_basic_xmlcreator_single_gchild_tag.xml")
  
        # test prep
        xmlcreator = XMLCreator.table("nutrition",table)
  
        # execute test
        results = xmlcreator.table2xml()
  
        # assert correctness
        self.assertEqual(expected_results.rstrip(),results.rstrip())
    
    def test_table_to_xml_multiattribute(self):
        ''' test 1: adding multiple attributes to 1 element'''    
          
        table = [["_id","_parent","_type","root-food","food-name"],
                 [1,"","root","#2;id=1","","","",""],
                 [2,1,"food","","Avocado Dip;foo=1,bar=2,foobar=3,ahaa=4"]]
  
        # set expected results
        expected_results = file2string("test_basic_xmlcreator_multiattr.xml")
  
        # test prep
        xmlcreator = XMLCreator.table("nutrition",table)
  
        # execute test
        results = xmlcreator.table2xml()
  
        # assert correctness
        self.assertEqual(expected_results.rstrip(),results.rstrip())
        
    def test_table_to_xml_notext_element(self):
        ''' test 1: element with no text'''    
          
        table = [["_id","_parent","_type","root-food","food-name"],
                 [1,"","root","#2;id=1","",""],
                 [2,1,"food","",""]]
  
        # set expected results
        expected_results = file2string("test_basic_xmlcreator_no_text.xml")
  
        # test prep
        xmlcreator = XMLCreator.table("nutrition",table)
  
        # execute test
        results = xmlcreator.table2xml()
  
        # assert correctness
        self.assertEqual(expected_results.rstrip(),results.rstrip())
        
        '''
        [5,"","root","#6;id=5","","","",""],
        [6,5,"food","","Bagels New York Style","Thompson","104;units=g",";total=350,fat=35"],
        [9,"","root","#10;id=9","","","",""],
        [10,9,"food","","Beef Frankfurter, Quarter Pound","Armitage","115;units=g",";total=370,fat=290"]]
        '''

    
class TestXMLCreator(unittest.TestCase):     

    def test_init_tree(self):
        
        # test parameters
        test_root_tag="nutrition"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition />"
        
        # execute test
        xmlcreator = XMLCreator(test_root_tag)
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)

    def test_add_child_tag(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food /></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        
        # execute test
        xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_update_element(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food>foobar</food></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        xmlelement = xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        
        # execute test
        xmlcreator.update_element(xmlelement,"foobar")
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_add_attr(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food foo=\"bar\" /></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        xmlelement = xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        
        # execute test
        xmlcreator.add_attr(xmlelement,"foo","bar")
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
        
    def test_add_child_element(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        test_new_child_tag="blah"
        test_new_gchild_tag="yeh yeh"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food><blah><yeh yeh /></blah></food></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        xmlelement = xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        
        xmlchildelement = XMLCreator(test_new_child_tag)
        xmlgchildelement = xmlcreator.add_child_tag(xmlchildelement.tree,test_new_gchild_tag)
        
        # execute test
        xmlcreator.add_child_element(xmlelement,xmlchildelement.tree)
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
  

if __name__ == "__main__":
    

    suite = unittest.TestSuite()

    suite.addTest(TestXMLCreator("test_init_tree")) 
    suite.addTest(TestXMLCreator("test_add_child_tag")) 
    suite.addTest(TestXMLCreator("test_update_element"))
    suite.addTest(TestXMLCreator("test_add_attr"))
    suite.addTest(TestXMLCreator("test_add_child_element"))

    suite.addTest(TestXMLCreatorTable2XML("test_table_to_xml_single_child_tag"))
    suite.addTest(TestXMLCreatorTable2XML("test_table_to_xml_single_grandchild"))
    suite.addTest(TestXMLCreatorTable2XML("test_table_to_xml_multiattribute"))
    suite.addTest(TestXMLCreatorTable2XML("test_table_to_xml_notext_element"))
    
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    