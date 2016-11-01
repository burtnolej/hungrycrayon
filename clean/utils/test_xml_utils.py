import xml.etree.ElementTree as xmltree
import unittest
from xml_utils import element_find_by_attrib_value, element_move, element_fuse, \
     element_parent_get, element_find_tags,element_find_children, grid2xml, xml2string
    
class Test_XML(unittest.TestCase):

    def setUp(self):
        
        self.xml = "<node><childA><gchildA name='brian'/><gchildB /></childA></node>"
        self.root = xmltree.fromstring(self.xml)
        
    def test_element_find_tags(self):
        xml = "<node><child><gchildA name='brian'/><gchildB /></child><child><gchildB name='david'/><gchildB /></child></node>"
        self.root = xmltree.fromstring(xml)
        results = element_find_tags('','child',self.root)
        self.assertEqual(len(results),2)
        
    def test_element_find_children(self):
        xml = "<node><childA>blahblah<gchildA name='brian'/><gchildB /></childA><childB>foobar<gchildB name='david'/><gchildB /></childB></node>"
        self.root = xmltree.fromstring(xml)
        results = element_find_children(self.root)
        self.assertEqual(results,{'childA':'blahblah','childB':'foobar'})
        
    def test_tree_find_unique_tag(self):
        # note that find(<tag>) will only search direct descendents
        # so use xpath
        element = self.root.find(".//gchildA")
        self.assertEquals(element.attrib['name'],'brian')

        
        
    def test_element_create_new_child(self):
        parent = self.root.find(".//childA")
        xmltree.SubElement(parent,"gchildC")
        expected_result = "<node><childA><gchildA name=\"brian\"/><gchildB /><gchildC /></childA></node>"
        
        # take out the white space as it can confuse comparisons
        self.assertEqual(xmltree.tostring(self.root).replace(" ",""),
                         expected_result.replace(" ",""))
        
    def test_element_copypaste_at_0(self):
        # insert a copy of an element at child posn 1
        
        #<node>
        #    <gchildA name="brian" />
        #    <childA>
        #        <gchildA name="brian" />
        #        <gchildB />
        #    </childA>
        #</node>

        expected_result = "<node><gchildA name=\"brian\"/><childA><gchildA name=\"brian\"/><gchildB /></childA></node>"
       
        element = self.root.find(".//gchildA")
        children = self.root.insert(0,element)
        self.assertEqual(xmltree.tostring(self.root).replace(" ",""),
                         expected_result.replace(" ",""))         

    def test_element_copypaste_at_end(self):
        # insert a copy of an element at child posn 1
        
        #<node>
        #    <childA>
        #        <gchildA name="brian" />
        #        <gchildB />
        #    </childA>
        #    <gchildA name="brian" />
        #</node>
        
        expected_result = "<node><childA><gchildA name=\"brian\"/><gchildB /></childA><gchildA name=\"brian\"/></node>"

        element = self.root.find(".//gchildA")
        children = self.root.append(element)
        
        #self.root.remove(element)
        self.assertEqual(xmltree.tostring(self.root).replace(" ",""),
                         expected_result.replace(" ",""))
        
    def test_element_remove_child(self):
        expected_result = "<node />"

        element = self.root.find(".//childA")
        self.root.remove(element)
        
        self.assertEqual(xmltree.tostring(self.root),expected_result)
        
        # if we try to remove something that is not a child it wont work
        with self.assertRaises(ValueError):
            element = self.root.find(".//gchildA")
            self.root.remove(element)
        
    def test_element_parent_get(self):
        
        element = self.root.find(".//gchildA")
        
        parent = element_parent_get(self.root,element)
        self.assertEqual(parent.tag,'childA')
        
    def test_element_move_at_end(self):
        # move the element to new parent and end posn
        
        #<node>
        #    <childA>
        #        <gchildB />
        #    </childA>
        #    <gchildA name="brian" />
        #</node>
        
        element = self.root.find(".//gchildA")

        element_move(self.root,element,self.root)
        expected_result = "<node><childA><gchildB /></childA><gchildA name=\"brian\"/></node>"
        
        self.assertEqual(xmltree.tostring(self.root).replace(" ",""),
                         expected_result.replace(" ",""))
        
    def test_element_fuse_between(self):
        # move an element and have it assume the children of its new parent
        
        #<node>
        #    <userpA>
        #       <childA>
        #            <gchildA name='brian'/>
        #            <gchildB>blahblah</gchildB>
        #        </childA>
        #    </userpA>
        #</node>
        
        expected_result = "<node><userpA><childA><gchildA name=\"brian\"/><gchildB/></childA></userpA></node>"

        new_root = element_fuse(self.root,"userpA",self.root)
        self.assertEqual(xmltree.tostring(new_root).replace(" ",""),
                         expected_result.replace(" ",""))
        
    def test_element_fuse_between_with_multiple_children(self):
        # move an element and have it assume the children of its new parent
        
        #<node>
        #    <userpA>
        #       <childA>
        #            <gchildA name='brian'/>
        #            <gchildB>blahblah</gchildB>
        #        </childA>
        #        <childB />
        #    </userpA>
        #</node>
        xml = "<node><childA><gchildA name='brian'/><gchildB /></childA><childB /></node>"
        expected_result = "<node><userpA><childA><gchildA name=\"brian\"/><gchildB/></childA><childB /></userpA></node>"
        self.root = xmltree.fromstring(xml)
        
        new_root = element_fuse(self.root,"userpA",self.root)
        self.assertEqual(xmltree.tostring(new_root).replace(" ",""),
                         expected_result.replace(" ",""))
        
    def test_element_parent_get(self):
        element = self.root.find(".//gchildA")
        parent = element_parent_get(self.root,element)
        self.assertEqual(parent.tag,'childA')
        
    def test_element_attrib_add(self):
        element = self.root.find(".//gchildB")
        element.set('foobar','barfoo')
        expected_result = "<node><childA><gchildA name=\"brian\"/><gchildB foobar=\"barfoo\"/></childA></node>"
    
        self.assertEqual(xmltree.tostring(self.root).replace(" ",""),
                         expected_result.replace(" ",""))        

    def test_element_find_by_attrib_value(self):

        xml="<node><child name='jon'>44</child><child name='quinton'>4</child><child name='nancy'>45</child></node>"
        self.root = xmltree.fromstring(xml)
        
        element = element_find_by_attrib_value(self.root,'child','name','jon')
        self.assertEquals(element.text,"44")
        
    def test_build_tree(self):
        
        expected_result="<root><child><gchild /></child></root>"
        self.root = xmltree.Element('root')
        element = xmltree.SubElement(self.root,"child")
        subelement = xmltree.SubElement(element,"gchild")
        
        self.assertEqual(xmltree.tostring(self.root).replace(" ",""),
                         expected_result.replace(" ",""))
        
    def test_iter(self):
        
        elements = [element.tag for element in self.root.iter()]
        
        self.assertEqual(elements,['node','childA','gchildA','gchildB'])   
        
        
    def test_find_leaf(self):
        
        leaf = [element.tag for element in self.root.iter() if len(element) == 0]
        
        self.assertEqual(leaf,['gchildA','gchildB'])   
        
        
        
class Test_XML_xpath(unittest.TestCase):

    def setUp(self):
        self.test_xml = "/home/burtnolej/Development/pythonapps3/clean/utils/test_misc/test_xpath.xml"        
        self.root = xmltree.parse(self.test_xml)        
        
    def test_element_getall_children(self):
        # from a non root tag get its children using xpath
        parent = element_find_by_attrib_value(self.root,'table','name','a')
        self.assertEqual(len(self.root.findall('.//table[@name=\"a\"]/*')),2)
        self.assertEqual(len(parent.findall("*")),2)
        
    def test_element_getall_grandchildren(self):
        # from a non root tag get its children using xpath
        self.assertEqual(len(self.root.findall('.//table[@name=\"a\"]/tr/*')),6)

class Test_Grid_to_XML(unittest.TestCase):
    
    def setUp(self):
        pass
        
    
    def test_allstring_content(self):
        
        grid = [["A","B","C","D"],["E","F","G","H"]]
        
        expected_results = "<root><row><cell>A</cell><cell>B</cell><cell>C</cell><cell>D</cell></row><row><cell>E</cell><cell>F</cell><cell>G</cell><cell>H</cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_allint_content(self):
        
        grid = [[1,2,3,4],[5,6,7,8]]
        
        expected_results = "<root><row><cell>1</cell><cell>2</cell><cell>3</cell><cell>4</cell></row><row><cell>5</cell><cell>6</cell><cell>7</cell><cell>8</cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllist_content(self):
        
        grid = [[["A",1],["B",2]],[["C",3],["D",4]]]
        
        expected_results = "<root><row><cell><subcell>A</subcell><subcell>1</subcell></cell><cell><subcell>B</subcell><subcell>2</subcell></cell></row><row><cell><subcell>C</subcell><subcell>3</subcell></cell><cell><subcell>D</subcell><subcell>4</subcell></cell></row></root>"
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)

    def test_alldict_content(self):
        
        expected_results = "<root><row><cell><A>1</A><B>2</B></cell></row><row><cell><C>3</C><D>4</D></cell></row></root>"
        
        grid = [[dict(A=1,B=2)],[dict(C=3,D=4)]]
        xml = grid2xml(grid)
         
        self.assertEqual(xml2string(xml),expected_results)
        
if __name__ == "__main__":

    suite = unittest.TestSuite()
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_XML))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_XML_xpath))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_to_XML))
    
    unittest.TextTestRunner(verbosity=2).run(suite)