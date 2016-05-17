import unittest
import xml.etree.ElementTree as xmltree

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file, file2string, gettype
from XMLTableRepr import XMLTableRepr

class XMLParser():
    
    '''
    sample xml for used for illustrative purposes in the documentation:
    
    xml form :
    
    <tag>
      <child id="blah blah">
        <gchild attrib="hmmm">FOO</gchild1>
        <gchild1>BAR</gchild2>
      </child>
      <child id="yeh yeh">
        <gchild> attrib="oooo">FOO2</gchild1>
        <gchild1>BAR2</gchild2>
      </child>
    </tag>
    
    
    table form:
    
    | _id | _parent | _type | root-tag | tag-child         | child-gchild       | child-gchild2
    ------------------------ ----------------------------- -----------------------------------------------
    |  0  | -1      |       | #1       |                   |                    |
    |  1  | 0       | tag   |          | #2;id="blah blah" |                    |
    |  2  | 1       | child |          |                   | FOO;attrib="hmmm"  | BAR;
    |  2  | 1       | child |          |                   | FOO2;attrib="oooo" | BAR2;
    -----------------------------------------------------------------------------------------------------
    
    
    ----------------------------------------------------------------------------------------------------
    | Glossary of terms
    ----------------------------------------------------------------------------------------------------
    | name    | type    | class                | Notes                        | Examples
    ----------------------------------------------------------------------------------------------------
    | element | object  | ElementTree.Element  |                              | Element("<tag><child id="X">Y
    |         |         |                      |                              | </child></tag>")
    | value   | str     |                      | 'tag' value (Element.Text)   | Y
    | tag     | str     |                      | 'tag' name  (Element.Tag)    | child
    | attr    | str     |                      | 'attrib' name (.Attrib[??]   | id
    | attr_val| str     |                      | 'attrib' value (.Attrib[name]| X
    | table   | 2d array| List                 | table representation of Tree | see table above
    -----------------------------------------------------------------------------------------------------
    
    ----------------------------------------------------------------------------------------------------
    | Public Member Functions
    --------------------------------------------------------------------------------------------------------------------------
    | name        | args                | description                                                    | tests
    ---------------------------------------------------------------------------------------------------------------------------
    | get_values  |                     | returns a list containing all the values found in the tree for | test_get_values
    |             |                     | tag=tag.For example : get_values("child") would return:        | test_get_values_fail
    |             |                     |               ["FOO","FOO2"]                                   | test_get_values_invalid_tag
    |-------------|---------------------|----------------------------------------------------------------|----------------------
    | get_elements|                     | returns a list containing all the elements found in the tree   | test_get_elements
    |             |                     | for tag=tag. For example get_elements("gchild") would return:  | test_get_elements_fail
    |             |                     |               Element("<gchild attrib="hmmm">FOO</gchild1>"),  | test_get_elements_invalid_tag
    |             |                     |               Element("<gchild> attrib="oooo">FOO2</gchild1>')]| 
    |-------------|---------------------|----------------------------------------------------------------|---------------------
    | get_        |                     | returns a list containing all the elements found in the tree   | test_get_elements_by_attr_gtequal
    | elements_   |                     | where tag=tag & attr_val=attr_val.                             | test_get_elements_by_attr_ltequal
    | by_attr     |                     | For exmple get_elements_by_attr("gchild","attrib","hmmm")retrns| test_get_elements_by_attr_equal 
    |             |                     |               [Element("<gchild attrib="hmmm">FOO</gchild1>")] | 
    |---------------------------------- |----------------------------------------------------------------|---------------------
    | get_values_ |                     | returns a list containing all the values found in the tree whre| test_get_values_by_attr_gtequal
    | by_attr     |                     | tag=tag & attr_val=attr_val                                    |
    |             |                     | For example get_values_by_attr("gchild","attrib","hmmm")returns| 
    |             |                     |               ["FOO"]                                          |
    |---------------------------------- |----------------------------------------------------------------|---------------------
    | get_        | parent_element=None:| returns a list of the form parent_tag-child_tag for each child | test_get_tags
    | tags        | defaults to root    | tag of the element passed in as an arg. defaults to the tree   |
    |             |                     | root if nothing passed. must be passed elem,ents that only     |
    |             |                     | have single offspring throughout the tree to avoid dupes       |
    |---------------------------------- |----------------------------------------------------------------|---------------------
    | get_table   |                     | for a given attribute value; return a table, with a tags       | test_get_table
    |             |                     | children on 1 row with references to other rows that represent |
    |             |                     | other descendents                                              |
    |---------------------------------- |----------------------------------------------------------------|---------------------
    
    ----------------------------------------------------------------------------------------------------
    | To Do
    --------------------------------------------------------------------------------------------------------------------------
    | Take out the _by_attr functions for elements and values and add them as parameters to the  regular methods, like in get_tags
    --------------------------------------------------------------------------------------------------------------------------
    
    '''
    
    def __init__(self,schema, ns=None):
        self.tree = xmltree.parse(schema)
        
    @classmethod
    def table(cls,schema,ns=None):  
        cls1 = cls(schema,ns)
        cls1.xmltablerepr = XMLTableRepr.fromxml(cls1)
        cls1.table = cls1.xmltablerepr.table
        
        return(cls1)
    
    def get_xml_root(self):
        ''' return the root node '''
        return(self.tree)
    
    def get_values(self,tag,ns=None):
        ''' returns a list containing all the values found in the tree
        for tag=tag. For example : get_values("gchild") would return ["FOO","FOO2"]
        '''
        values=[]               
        for element in self.tree.iter(tag):
                values.append(gettype(element.text)) 
            
        return values
    
    def get_elements(self,tag, attr=None,attr_val=None,attr_val_pred=None,ns=None):
        ''' returns a list containing all the elements found in the tree for tag=tag.
        For example get_elements("gchild") would return: 
           [Element("<gchild attrib="hmmm">FOO</gchild1>"),
            Element("<gchild> attrib="oooo">FOO2</gchild1>')] 
        '''
        elements=[]               
        for element in self.tree.iter(tag):
                elements.append(element) 
            
        return elements
    
    def get_elements_by_attr(self,tag, attr,attr_val,attr_val_pred,ns=None):
        ''' returns a list containing all the elements found in the tree where tag=tag & attr_val=attr_val
        For example get_elements_by_attr("gchild","attrib","hmmm") would return: 
           [Element("<gchild attrib="hmmm">FOO</gchild1>")] 
        '''       
        elements=[]               
        for element in self.tree.iter(tag):
                if element.attrib.has_key(attr):
                    if getattr(self,attr_val_pred)(int(element.attrib[attr]),int(attr_val)):
                        elements.append(element)
            
        return elements
    
    def get_values_by_attr(self,tag, attr,attr_val,attr_val_pred,ns=None):
        ''' returns a list containing all the values found in the tree where tag=tag & attr_val=attr_val
        For example get_values_by_attr("gchild","attrib","hmmm") would return: 
           ["FOO"] 
        '''       
        values=[]               
        for element in self.tree.iter(tag):
                if element.attrib.has_key(attr):
                    if getattr(self,attr_val_pred)(int(element.attrib[attr]),int(attr_val)):
                        values.append(element.attrib[attr])
            
        return values
        
    def _get_tags(self,parent_element,parent_tag,child_tags):
        ''' append any children to the child tag list'''
        if len(parent_element._children)>0:
            for child in parent_element._children:
                child_tags.append(parent_tag + "-" + child.tag)
                self._get_tags(child,child.tag,child_tags)
        
    def get_tags(self,parent_element=None,ns=None):
        ''' returns a list of the form parent_tag-child_tag for each child tag of the element passed 
        in as an arg. defaults to the tree root if nothing passed. DOES NOT HANDLE DUPE TAGS'''
        if parent_element==None:
            parent_element = self.tree.getroot()
        
        child_tags = []
        self._get_tags(parent_element,parent_element.tag,child_tags)

        return(child_tags)

        
    def get_table(self,parent=None,parent_tag="root",parent_row_id=-1):  
        self.xmltablerepr.get_table(parent,parent_tag,parent_row_id)
        
    def print_table(self):  
        self.xmltablerepr.print_table()
        
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
    
    @staticmethod
    def _num_children(element):
        return(len(element._children))

    @staticmethod
    def _has_children(element):
        if len(element._children)>0:
            return True
        return False

    @staticmethod
    def _num_children(element):
        return(len(element._children))

    @staticmethod
    def _get_attr_value(element,attr):
        ''' return the value of a specific attr '''
        if XMLParser._attr_exists(attr):
            return element.attrib[attr]

    @staticmethod
    def _attr_exists(element,attr):
        ''' check if a specific attr exists '''
        if element.attrib.has_key(attr):
            return True
        return False

    @staticmethod
    def _attrs_exist(element):
        ''' check if any attrs exists '''
        if len(element.attrib.keys()) > 0:
            return True
        return False

    @staticmethod
    def _get_attrs(element):
        ''' return a list of tuples (key,value) '''
        return [(key,value) for key, value in element.attrib.iteritems()]

    @staticmethod
    def _get_attrs_str(element):
        ''' return a string of the form ;key='value',key='value' etc '''
        _attr = XMLParser._get_attrs(element)

        if XMLParser._attrs_exist(element):
            return(";" + ",".join(key+"=\""+str(value)+"\"" for key,value in _attr))
        return("") 
    
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
        
    def test_get_tags(self):
        ''' represent the tag names as field headers '''

        # test input
        self.xmlparser = XMLParser("food_tmp.xml")
        
        # test parameters
        test_tag="food"
        test_attr="id"
        test_attr_val="0002"
        test_attr_val_pred="equal"
        
        # set expected results: the number of elements returned 
        self.xmltablerepr = XMLTableRepr.fromfile("test_get_tags.csv")
        expected_results = self.xmltablerepr.table_header

        # execute test
        element = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)[0]        
        values = self.xmlparser.get_tags(element)

        # assert correctness
        self.assertEquals(values,expected_results)
        
            
class TestXMLParserTableRepr(unittest.TestCase):
    ''' tests the ability to parse entire branches of trees and return data in
    tabular form'''
        
    def test_get_table(self):
        ''' represent a subset of the xml tree as a table'''
        
        # test input
        self.xmlparser = XMLParser.table("food.xml")
        
        # test parameters
        test_tag="food"
        test_attr="id"
        test_attr_val="0002"
        test_attr_val_pred="equal"
        
        # set expected results: the number of elements returned 
        self.xmltablerepr = XMLTableRepr.fromfile("test_get_table.csv")
        expected_results = self.xmltablerepr.table
        
        # execute test        
        element = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)[0] 
        self.xmlparser.get_table(element)
        values = self.xmlparser.table
            
        # assert correctness
        self.assertEquals(values,expected_results)
        
    def test_get_table_root(self):
        '''represent the entire xml tree as a table'''
        
        # test input
        self.xmlparser = XMLParser.table("food_tmp.xml")
                
        # set expected results: the number of elements returned 
        self.xmltablerepr = XMLTableRepr.fromfile("test_get_table_root.csv")
        expected_results = self.xmltablerepr.table
        
        # execute test        
        self.xmlparser.get_table()
        values = self.xmlparser.table
        
        # assert correctness
        self.assertEquals(values,expected_results)


    def test_test_get_all_tagvalues_by_unique_tag(self):
        pass
        
if __name__ == "__main__":
    
    suite = unittest.TestSuite()

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
    suite.addTest(TestXMLParser("test_get_tags"))
    suite.addTest(TestXMLParserTableRepr("test_get_table"))
    suite.addTest(TestXMLParserTableRepr("test_get_table_root"))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
    
    need to change non table tests to expects ints/floats where possible