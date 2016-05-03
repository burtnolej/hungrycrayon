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
    
    def _get_child_tags(self,parent_element,parent_tag,child_tags):
        ''' append any children to the child tag list'''
        if len(parent_element._children)>0:
            for child in parent_element._children:
                child_tags.append(parent_tag + "-" + child.tag)
                self._get_child_tags(child,child.tag,child_tags)
        
    def get_child_tags_by_attr(self,tag,attr,attr_val,ns=None):
        ''' for a given attribute value; return a list of all the child tags 
        expects to get 1 record back; works recursively down the tree '''
        parent_element = self.get_elements_by_attr(tag,attr,attr_val,"equal")
        
        if len(parent_element)>1:
            raise Exception("expected to only get 1 record returned; got",len(element))
        else:
            parent_element = parent_element[0]
            
        child_tags = []
        self._get_child_tags(parent_element,tag,child_tags)
            
        return(child_tags)

    @staticmethod
    def _has_children(element):
        if len(element._children)>0:
            return True
        return False
           
    @staticmethod 
    def _init_row(table,width,init_value):
        _new_row = []
        for i in range(width):
            _new_row.append(init_value)
        table.append(_new_row)
        return(len(table)-1)
        
    def _get_child_values(self,parent,parent_tag,child_values,row_id,col_id):
        ''' append any children to the child tag list'''
        
        # initialize a new row
        row_id = XMLParser._init_row(child_values,50,"")
            
        if XMLParser._has_children(parent):
            for child in parent._children:
                col_id += 1
                
                if XMLParser._has_children(child):
                    new_row_id, col_id = self._get_child_values(child,child.tag,child_values,\
                                                       row_id,col_id)
                    child_values[row_id][col_id] = "#" + str(new_row_id) + ";" "attrib"
                    
                else:
                    value = child.text
                    if value==None:
                        value="None"
                    child_values[row_id][col_id] = value + ";" + "attrib"
                    
        return(row_id,col_id)
        
    def get_child_values_by_attr(self,tag,attr,attr_val,ns=None):
        ''' for a given attribute value; return a list of all the child tags 
        expects to get 1 record back; works recursively down the tree '''
        parent_element = self.get_elements_by_attr(tag,attr,attr_val,"equal")
        row_id = 1
        col_id = 0
        
        if len(parent_element)>1:
            raise Exception("expected to only get 1 record returned; got",len(element))
        else:
            parent_element = parent_element[0]
            
        child_values = []
        
        # create root record
        row_id = XMLParser._init_row(child_values,50,"")
        child_values[row_id][0]=row_id
        child_values[row_id][2]=tag
        child_values[row_id][3]="#"+str(row_id+1)+";"

        self._get_child_values(parent_element,tag,child_values,row_id,col_id)
            
        return(child_values)
    
    def get_child_tagvalue_by_attr(self,tag,attr,attr_val,ns=None):
        ''' for a given attribute value; return a list of tuples of the form (tag,value)  
        expects to get 1 record back '''
        element = self.get_elements_by_attr(tag,attr,attr_val,"equal")
        
        if len(element)>1:
            raise Exception("expected to only get 1 record returned; got",len(element))
        
        return [(child.tag,child.text) for child in element[0]._children]
    
    
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
            
class TestXMLParserMulti(unittest.TestCase):
    ''' tests the ability to parse entire branches of trees and return data in
    tabular form'''
    
    def setUp(self):
        self.xmlparser = XMLParser("food.xml")
        
        self.expected_header_results = ["food-name",\
                                        "food-mfr",\
                                        "food-serving",\
                                        "food-calories",\
                                        "food-total-fat",\
                                        "food-saturated-fat",\
                                        "food-cholesterol",\
                                        "food-sodium",\
                                        "food-carb",\
                                        "food-fiber",\
                                        "food-protein",\
                                        "food-vitamins",\
                                        "vitamins-a",\
                                        "vitamins-c",\
                                        "food-minerals",\
                                        "minerals-ca",\
                                        "minerals-fe"]
        self.table_0002 = []
        #self.table_0002.append(["_id","_parent","_type","root-food"]+self.expected_header_results)
        self.table_0002.append([0,"","root","#2;id=0001","","","","","","","","","","","","","","","","",""]),
        self.table_0002.append([1,
                                0,
                                "food",
                                "",
                                "Bagels New York Style",\
                                "Thompson",\
                                "104;g",\
                                ";total=\"300\",fat=\"35\"",\
                                "4",\
                                "1",\
                                "0",\
                                "510",\
                                "54",\
                                "3",\
                                "11",\
                                "#3",\
                                "",\
                                "",\
                                "#4",\
                                "",\
                                ""])
        self.table_0002.append([2,
                                1,
                                "vitamins",
                                "",
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "0",\
                                "0",\
                                "",\
                                "",\
                                ""])
        self.table_0002.append([3,
                                2,
                                "minerals",
                                "",
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "",\
                                "8"
                                "2"])

    def test_get_child_tags_by_attr(self):
        
        # test parameters
        test_tag="food"
        test_attr="id"
        test_attr_val="0002"
        test_attr_val_pred="equal"
        
        # execute test
        values = self.xmlparser.get_child_tags_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
            
        # assert correctness
        self.assertEquals(values,self.expected_header_results)
        
    def test_get_child_values_by_attr(self):
        
        # test parameters
        test_tag="food"
        test_attr="id"
        test_attr_val="0002"
        test_attr_val_pred="equal"
        
        # set expected results: the number of elements returned 
        expected_results = self.table_0002
        
        # execute test
        values = self.xmlparser.get_child_values_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
            
        # assert correctness
        self.assertEquals(values,expected_results)
        
if __name__ == "__main__":
    

    suite = unittest.TestSuite()

    '''suite.addTest(TestXMLParser("test_get_elements"))
    suite.addTest(TestXMLParser("test_get_elements_fail"))
    suite.addTest(TestXMLParser("test_get_elements_invalid_tag"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_gtequal"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_ltequal"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_equal"))
    suite.addTest(TestXMLParser("test_get_values"))
    suite.addTest(TestXMLParser("test_get_values_fail"))    
    suite.addTest(TestXMLParser("test_get_values_invalid_tag"))    
    suite.addTest(TestXMLParser("test_get_values_by_attr_gtequal"))  '''
    
    suite.addTest(TestXMLParserMulti("test_get_child_values_by_attr"))


    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    