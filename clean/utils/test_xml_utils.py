import xml.etree.ElementTree as xmltree
import unittest
from xml_utils import element_find_by_attrib_value, element_move, element_fuse, \
     element_parent_get, element_find_tags,element_find_children
    
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
        
        
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_XML)
    unittest.TextTestRunner(verbosity=2).run(suite)