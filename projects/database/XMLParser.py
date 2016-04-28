import unittest
import xml.etree.ElementTree as xmltree
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file

class XMLCreator():
    
    def __init__(self, root_tag, filen=None, ns=None):
        self.filen = filen
        self.tree = xmltree.Element(root_tag)

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
    def _getattr_value(value):
        items = value.split("=")
        if len(items)>2:
            raise Exception("must be of the form 'yeh=yeh'")
        return(items[0],items[1])    

    @staticmethod
    def _notset(value):    
        if value<>"":
            return True
        return False

    @classmethod
    def table(cls, root_tag,table, filen=None, ns=None):
        self.tree = xmltree.Element(root_tag)
        cls1 = cls.__init__(root_tag,filen,ns)
        return(cls1)
    
    def write(self): 
        write_text_to_file(self.filen,self.tree.dump())

    def dump(self):
        return(xmltree.tostring(self.tree))
        
    def add_child_tag(self,parent,tag):
        return(xmltree.SubElement(parent,tag))
                
    def add_child_element(self,element,child):    
        element.append(child)
    
    def add_attr(self,element,attr,attr_val):
        element.set(attr,attr_val)
    
    def update_element(self,element,text):
        element.text = text
        
    def table2xml(self):
    
        table = [["_id","_parent","_type","root-food","food-name","food-mfr","food-serving","food-calories"],
                 [1,"","root","#2;id=1","","","",""],
                 [2,1,"food","","Avocado Dip","Sunnydale","29;units=g","total=110,fat=100"],
                 [5,"","root","#6;id=5","","","",""],
                 [6,5,"food","","Bagels New York Style","Thompson","104;units=g","total=t350,fat=35"],
                 [9,"","root","#10;id=9","","","",""],
                 [10,9,"food","","Beef Frankfurter, Quarter Pound","Armitage","115;units=g","total=370,fat=290"]]

        # split the columns 1,2&3 (fixed ref) from the remaining n columns (variable data)
        ref_table = zip(*table)[:3]
        data_table = zip(*table)[3:]

        ref_table = zip(*ref_table)
        data_table = zip(*data_table)
        
        # separate out the headers
        data_table_headers = data_table[0]
        
        # remove the header rows
        ref_table = ref_table[1:]
        data_table = data_table[1:]
        
        root_rows=[] # list of ids containing the root rows
        data_table_width = len(data_table[0])
        table_depth = len(data_table)
        
        # process headers to classify as sub types
        # assume that column 1,2,3 are id,parent,type
        i=0
        _data_table_headers = data_table_headers
        data_table_headers = []
        
        for data_table_header in _data_table_headers:
            if self._isvalidheader(data_table_header):
                # its a column description (token1-token2) where token2 is a field 
                # in record token 1 
                data_table_headers.append(self._getheaderinfo(data_table_header))
            else:
                raise exception("header needs to be in the form 'token-token'")
            
        # pre process data rows
        records = {} # key is ID; value is dict with keys (parent,type,list(values)
        i=0
        for ref_row in ref_table:
            _id,_parent,_type = ref_row
            
            # store root ids separately
            # to process table and build xml; we take each root row and follow all lookups
            # until root is row is complete
            if self._isroottype(_type):
                root_rows.append(_id)
                
            d = {}
            # remove the empty columns; probably their because of a spreadsheet export to csv
            data_values = [value for value in data_table[i] if value<> ""]
            d['parent'] = _parent
            d['type'] = _type
            d['values'] = data_values
            records[_id] = d
            i+=1
        
        def _process_record(record_id):            
            
            values = records[int(record_id)]['values']
            
            for value in values:
                if self._containsattr(value):
                    # element contains attribute
                    tag_value,attr=self._getattr(value)
                else:
                    tag_value = value
                    attr = ""
                    
                index = values.index(value)
                tag = self._gettagname(data_table_headers[index])
                element = self.add_child_tag(self.tree,tag)
                
                if self._notset(attr):
                    attr_name,attr_value=self._getattr_value(attr)
                    
                    # add id attribute to the element
                    self.add_attr(element,attr_name,attr_value)
                    
                if self._isref(tag_value):
                    # then element has children; process child
                    _process_record(tag_value[1:])
                else:
                    # no children so just set text
                    self.update_element(element,tag_value)
                    

        for root_id in root_rows:
            _process_record(root_id)

        print self.dump()
        

     
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
        
    def test_table_to_xml(self):
        table = [["tag","tag_id","field_name","field_mfr","field_serving","field_calories"],
                 ["food","0001","Avocado Dip","Sunnydale","units=g;29","total=110,fat=100"]	,		
                 ["food","0002","Bagels New York Style","Thompson","units=g;104","total=350,fat=35"],
                 ["food","0003","Beef Frankfurter, Quarter Pound","Armitage","units=g;115","total=370,fat=290"],
                 ["food","0004","Chicken Pot Pie","Lakeson","units=g;198","total=410,fat=200"]]
        
        xmlcreator = XMLCreator("nutrition")
        xmlcreator.table2xml()

        
        xml = "<nutrition>\
        <food id=\"0001\">\
        <name>Avocado Dip</name>\
        <mfr>Sunnydale</mfr>\
        <serving units=\"g\">29</serving>\
        <calories total=\"110\" fat=\"100\"/>\
        </food><food id=\"0002\">\
        <name>Bagels New York Style</name>\
        <mfr>Thompson</mfr>\
        <serving units=\"g\">104</serving>\
        <calories total=\"300\" fat=\"35\"/>\
        </food><food id=\"0003\">\
        <name>Beef Frankfurter, Quarter Pound</name>\
        <mfr>Armitage</mfr>\
        <serving units=\"g\">115</serving>\
        <calories total=\"370\" fat=\"290\"/>\
        </food><food id=\"0004\">\
        <name>Chicken Pot Pie</name>\
        <mfr>Lakeson</mfr>\
        <serving units=\"g\">198</serving>\
        <calories total=\"410\" fat=\"200\"/>\
        </food>\
        </nutrition>"
        
        

class XMLParser():
    
    def __init__(self,schema, ns=None):
        self.tree = xmltree.parse(schema)
        
    def get_xml_root(self):
        ''' return the root node '''
        return(self.tree)
    
    def get_values(self,tag,ns=None):
        
        values=[]               
        for element in self.tree.iter(tag):
                values.append(element.text) 
            
        return values
    
    def get_elements(self,tag, attr=None,attr_val=None,attr_val_pred=None,ns=None):
        
        elements=[]               
        for element in self.tree.iter(tag):
                elements.append(element) 
            
        return elements
    
    def get_elements_by_attr(self,tag, attr,attr_val,attr_val_pred,ns=None):
        
        elements=[]               
        for element in self.tree.iter(tag):
                if element.attrib.has_key(attr):
                    if getattr(self,attr_val_pred)(int(element.attrib[attr]),int(attr_val)):
                        elements.append(element)
            
        return elements
    
    def get_values_by_attr(self,tag, attr,attr_val,attr_val_pred,ns=None):
        
        values=[]               
        for element in self.tree.iter(tag):
                if element.attrib.has_key(attr):
                    if getattr(self,attr_val_pred)(int(element.attrib[attr]),int(attr_val)):
                        values.append(element.attrib[attr])
            
        return values
    
    # Operator methods
    @staticmethod
    def gtequal(val1,val2):
        if val1 >= val2:
            return True
        return False
    
    @staticmethod
    def ltequal(val1,val2):
        if val1 <= val2:
            return True
        return False
    
    @staticmethod
    def equal(val1,val2):
        if val1 == val2:
            return True
        return False
    
    
    
class TestXMLParser(unittest.TestCase):
    
    ''' only provide literal predicates, no objects; i.e. return any elements where tag=SEARCH_TAG under the branch where tag=PREDICATE_TAG 
    therefore if PRED_TAG exists 3 times and each time has 1 descendent called SEARCH_TAG, then 3 elements will be returned
    
    
    | Test Variables
    ---------------------------------------------------------
    | return     | test cond| type  | searchby | pred_type | namespace |
    ---------------------------------------------------------
    | element(s) | bad tag  | pass  | tag      | n/a       | none      |
    | value(s)   | dupe val | fail  | attr_val | gtequal   | ns        |
    |            |          |       |          | ltequal   |           |
    |            |          |       |          | equal     |           |
    ---------------------------------------------------------
    
    | Test Combinations
    ----------------------------------------------------------------------------------------------------
    | return  | args    |type  | searchby  | pred    | test_name                         | function_under_test
    ----------------------------------------------------------------------------------------------------
    | element |         | pass  | tag      | n/a     | test_get_elements                 | get_elements
    | element |         | fail  | tag      | n/a     | test_get_elements                 | get_elements_fail
    | element | bad tag | pass  | tag      | n/a     | test_get_elements                 | get_elements_fail
    | value   |         | pass  | tag      | n/a     | test_get_values                   | get_values
    | value   |         | fail  | tag      | n/a     | test_get_values_fail              | get_values
    | value   | bad tag | pass  | tag      | n/a     | test_get_values_invalid_tag       | get_values
    | element |         | pass  | attr_val | gtequal | test_get_elements_by_attr_gtequal | get_elements_by_attr
    | element |         | pass  | attr_val | ltequal | test_get_elements_by_attr_ltequal | get_elements_by_attr
    | element |         | pass  | attr_val | equal   | test_get_elements_by_attr_equal   | get_elements_by_attr
    | values  |         | pass  | attr_val | gtequal | test_get_values_by_attr_gtequal   | get_values_by_attr
    |
    |
    ---------------------------------------------------------------------------------------------------- 
    
    | Other Tests
    ----------------------------------------------------------------------------------------------------
    | start_node | return  | type | scope | pred | test_name
    ----------------------------------------------------------------------------------------------------
    | root       | tree    | pass | all   | none | get_tree
    |
    ----------------------------------------------------------------------------------------------------
    '''
    
    def setUp(self):
        self.xmlparser = XMLParser("food.xml")
        
    def test_get_tree(self):
        self.assertIsInstance(self.xmlparser.tree,xmltree.ElementTree)
     
     
    # ----------------------------------------------------------   
    # testing the retreival of elements
    # ----------------------------------------------------------
    
    def test_get_elements(self):
        
        # test parameters
        test_tag="food"
        test_attribute="id"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["0001","0002","0003","0004","0005","0006","0007","0008","0009","0010"]
        
        # execute test
        child_elements = self.xmlparser.get_elements(test_tag)
        
        # build result set that can be asserted
        results = []
        for child_element in child_elements:
            results.append(child_element.attrib[test_attribute])
          
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_get_elements_fail(self):
        
        # test parameters
        test_tag="food"
        test_attribute="id"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["0001","0002","0003","0004","0005","0007","0008","0009","0010"]
        
        # execute test
        child_elements = self.xmlparser.get_elements(test_tag)
        
        # build result set that can be asserted
        results = []
        for child_element in child_elements:
            results.append(child_element.attrib[test_attribute])
          
        # assert correctness
        self.assertNotEqual(results,expected_results)
        
    def test_get_elements_invalid_tag(self):
        
        # test parameters
        test_tag="foobar"
        test_attribute="id"
        
        # set expected results
        expected_results = []
        
        # execute test
        elements = self.xmlparser.get_elements(test_tag)
        
        # assert correctness
        self.assertEqual(elements,expected_results)
        
    def test_get_elements_by_attr_gtequal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="300"
        test_attr_val_pred="gtequal"
        
        # set expected results: the number of elements returned 
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["300","370","410"]
        
        # execute test
        elements = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
        
        # build result set that can be asserted
        results = []
        for element in elements:
            results.append(element.attrib[test_attr])
            
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_get_elements_by_attr_ltequal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="300"
        test_attr_val_pred="ltequal"
        
        # set expected results: the number of elements returned 
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["110","300","20","70","200","150","160","220"]
        
        # execute test
        elements = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
        
        # build result set that can be asserted
        results = []
        for element in elements:
            results.append(element.attrib[test_attr])
            
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_get_elements_by_attr_equal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="70"
        test_attr_val_pred="equal"
        
        # set expected results: the number of elements returned 
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["70"]
        
        # execute test
        elements = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
        
        # build result set that can be asserted
        results = []
        for element in elements:
            results.append(element.attrib[test_attr])
            
        # assert correctness
        self.assertEquals(results,expected_results)
        
        
    
    # ----------------------------------------------------------
    # testing the retreival of values
    # ----------------------------------------------------------
    
    def test_get_values(self):
        
        # test parameters
        test_tag="name"
        
        # set expected results
        expected_results = ["Avocado Dip","Bagels New York Style","Beef Frankfurter, Quarter Pound","Chicken Pot Pie","Cole Slaw","Eggs","Hazelnut Spread","Potato Chips","Soy Patties, Grilled","Truffles, Dark Chocolate"]
        
        # execute test
        values = self.xmlparser.get_values(test_tag)
        
        # assert correctness
        self.assertEquals(values,expected_results)
        
    def test_get_values_fail(self):
        
        # test parameters
        test_tag="name"
        
        # set expected results
        expected_results = ["Avocado Dip","Beef Frankfurter, Quarter Pound","Bagels New York Style","Chicken Pot Pie","Cole Slaw","Eggs","Hazelnut Spread","Potato Chips","Soy Patties, Grilled","Truffles, Dark Chocolate"]
        
        # execute test
        values = self.xmlparser.get_values(test_tag)
        
        # assert correctness
        self.assertNotEqual(values,expected_results)
        
    def test_get_values_invalid_tag(self):
        
        # test parameters
        test_tag="foobar"
        test_attribute="id"
        
        # set expected results
        expected_results = []
        
        # execute test
        elements = self.xmlparser.get_values(test_tag)
        
        # assert correctness
        self.assertEqual(elements,expected_results)
        
    def test_get_values_by_attr_gtequal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="300"
        test_attr_val_pred="gtequal"
        
        # set expected results: the number of elements returned 
        expected_results = ["300","370","410"]
        
        # execute test
        values = self.xmlparser.get_values_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
            
        # assert correctness
        self.assertEquals(values,expected_results)
    
if __name__ == "__main__":
    

    suite = unittest.TestSuite()
    '''
    suite.addTest(TestXMLParser("test_get_elements"))
    suite.addTest(TestXMLParser("test_get_elements_fail"))
    suite.addTest(TestXMLParser("test_get_elements_invalid_tag"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_gtequal"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_ltequal"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_equal"))
    suite.addTest(TestXMLParser("test_get_values"))
    suite.addTest(TestXMLParser("test_get_values_fail"))    
    suite.addTest(TestXMLParser("test_get_values_invalid_tag"))    
    suite.addTest(TestXMLParser("test_get_values_by_attr_gtequal"))  

    
    suite.addTest(TestXMLCreator("test_init_tree")) 
    suite.addTest(TestXMLCreator("test_add_child_tag")) 
    suite.addTest(TestXMLCreator("test_update_element"))
    suite.addTest(TestXMLCreator("test_add_attr"))
    suite.addTest(TestXMLCreator("test_add_child_element"))
    '''

    suite.addTest(TestXMLCreator("test_table_to_xml"))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    