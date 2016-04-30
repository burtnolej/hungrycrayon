import unittest
import xml.etree.ElementTree as xmltree

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file, file2string

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

    suite.addTest(TestXMLCreatorTable2XML("test_table_to_xml_single_child_tag"))
    suite.addTest(TestXMLCreatorTable2XML("test_table_to_xml_single_grandchild"))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    