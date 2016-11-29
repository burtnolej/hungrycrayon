import xml.etree.ElementTree as xmltree
import unittest
from xml_utils import element_find_by_attrib_value, element_move, element_fuse, \
     element_parent_get, element_find_tags,element_find_children, grid2xml, xml2string, record2xml
    
from collections import OrderedDict

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
        
    def test_allstring_content_basic(self):
        
        grid = [["A"]]
        
        expected_results = "<root><row><cell>A</cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_allstring_content(self):
        
        grid = [["A","B","C","D"],["E","F","G","H"]]
        
        expected_results = "<root><row><cell>A</cell><cell>B</cell><cell>C</cell><cell>D</cell></row><row><cell>E</cell><cell>F</cell><cell>G</cell><cell>H</cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_allstring_content_with_ids_basic(self):
        
        grid = [["A"]]
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\">A</cell></row></root>"
        
        xml = grid2xml(grid,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_allstring_content_with_ids(self):
        
        grid = [["A","B","C","D"],["E","F","G","H"]]
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\">A</cell><cell id=\"1.2\">B</cell><cell id=\"1.3\">C</cell><cell id=\"1.4\">D</cell></row><row id=\"2\"><cell id=\"2.1\">E</cell><cell id=\"2.2\">F</cell><cell id=\"2.3\">G</cell><cell id=\"2.4\">H</cell></row></root>"
        
        xml = grid2xml(grid,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)

    def test_allint_content_basic(self):
        
        grid = [[1]]
        
        expected_results = "<root><row><cell>1</cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_allint_content(self):
        
        grid = [[1,2,3,4],[5,6,7,8]]
        
        expected_results = "<root><row><cell>1</cell><cell>2</cell><cell>3</cell><cell>4</cell></row><row><cell>5</cell><cell>6</cell><cell>7</cell><cell>8</cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllist_content_basic(self):
        
        grid = [[["A",1]]]
        
        expected_results = "<root><row><cell><subcell>A</subcell><subcell>1</subcell></cell></row></root>"
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllistofdicts_content_basic(self):
        
        grid = [[[dict(A=1)]]]
        
        expected_results = "<root><row><cell><subcell><A>1</A></subcell></cell></row></root>"
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllistofdicts_content_basic_with_ids(self):
        
        grid = [[[dict(A=1)]]]
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><subcell id=\"1.1.1\"><A>1</A></subcell></cell></row></root>"
        xml = grid2xml(grid,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)

    def test_alllistofdicts_content_basic_uneven(self):
        
        grid = [[[dict(A=1),dict(B=2,C=3)]]]
        
        expected_results = "<root><row><cell><subcell><A>1</A></subcell><subcell><C>3</C><B>2</B></subcell></cell></row></root>"
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllistofdicts_content_2subrows_2subcells(self):
        
        grid = [[[dict(A=1),dict(B=2)],[dict(C=3),dict(D=4)]]]
        
        expected_results = "<root><row><cell><subrow><subcell><A>1</A></subcell><subcell><B>2</B></subcell></subrow><subrow><subcell><C>3</C></subcell><subcell><D>4</D></subcell></subrow></cell></row></root>"
        
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)

    def test_alllist_content(self):
        
        grid = [[["A",1],["B",2]],[["C",3],["D",4]]]
        
        expected_results = "<root><row><cell><subcell>A</subcell><subcell>1</subcell></cell><cell><subcell>B</subcell><subcell>2</subcell></cell></row><row><cell><subcell>C</subcell><subcell>3</subcell></cell><cell><subcell>D</subcell><subcell>4</subcell></cell></row></root>"
        xml = grid2xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllist_content_with_ids_basic(self):
        
        grid = [[["A",1]]]
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><subcell id=\"1.1.1\">A</subcell><subcell id=\"1.1.2\">1</subcell></cell></row></root>"
        
        xml = grid2xml(grid,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllist_content_with_ids(self):
        
        grid = [[["A",1],["B",2]],[["C",3],["D",4]]]
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><subcell id=\"1.1.1\">A</subcell><subcell id=\"1.1.2\">1</subcell></cell><cell id=\"1.2\"><subcell id=\"1.2.1\">B</subcell><subcell id=\"1.2.2\">2</subcell></cell></row><row id=\"2\"><cell id=\"2.1\"><subcell id=\"2.1.1\">C</subcell><subcell id=\"2.1.2\">3</subcell></cell><cell id=\"2.2\"><subcell id=\"2.2.1\">D</subcell><subcell id=\"2.2.2\">4</subcell></cell></row></root>"
        xml = grid2xml(grid,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)

    def test_alldict_content_basic(self):
        
        expected_results = "<root><row><cell><A>1</A></cell></row></root>"
        
        grid = [[dict(A=1)]]
        xml = grid2xml(grid)
         
        self.assertEqual(xml2string(xml),expected_results)
        
    def test_alldict_content(self):
        
        expected_results = "<root><row><cell><A>1</A><B>2</B></cell></row><row><cell><C>3</C><D>4</D></cell></row></root>"
        
        grid = [[dict(A=1,B=2)],[dict(C=3,D=4)]]
        xml = grid2xml(grid)
         
        self.assertEqual(xml2string(xml),expected_results)
        
    def test_alllist_content_added_tags_basic(self):
        
        grid = [[(1,'red')]]
        
        tags = ["value","fgcolor"]
        
        expected_results = "<root><row><cell><value>1</value><fgcolor>red</fgcolor></cell></row></root>"
        xml = grid2xml(grid,tags=tags)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alllist_content_added_tags(self):
        
        grid = [[(1,'red','yellow'),(5,'blue','green')]]
        
        tags = ["value","fgcolor","bgcolor"]
        
        expected_results = "<root><row><cell><value>1</value><fgcolor>red</fgcolor><bgcolor>yellow</bgcolor></cell><cell><value>5</value><fgcolor>blue</fgcolor><bgcolor>green</bgcolor></cell></row></root>"
        xml = grid2xml(grid,tags=tags)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_alldict_content_actualexample(self):
        
        expected_results = "<root><row><cell><bgcolor>FAFF33</bgcolor><fgcolor>251151</fgcolor><Value>row1cell1</Value></cell></row></root>"
        
        grid = [[dict(Value='row1cell1',bgcolor='FAFF33',fgcolor='251151')]]
        xml = grid2xml(grid)
         
        self.assertEqual(xml2string(xml),expected_results)
        
    def test_alllist_content_added_tags_basic_with_ids(self):
        
        grid = [[(1,'red')]]
        
        tags = ["value","fgcolor"]
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><value>1</value><fgcolor>red</fgcolor></cell></row></root>"
        xml = grid2xml(grid,tags=tags,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)

class Test_Grid_to_XML_function(unittest.TestCase):
       
    def test_1row_1col_1subrow_1subcol_formats(self):
     
        '''
        <root>
          <row id="1">
            <cell id="1.1">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value />
             </cell>
             <cell id="1.2">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value>MO</value>
             </cell>
           </row>
           <row id="2">
             <cell id="2.1">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value>830-910</value>
             </cell>
             <cell id="2.2">
               <subrow id="2.2.1">
                 <subcell id="2.2.1.1">
                   <bgcolor>#ffcc99</bgcolor>
                   <fgcolor>#ffffff</fgcolor>
                   <value>ELA</value>
                 </subcell>
               </subrow>
             </cell>
           </row>
         </root>
         '''
         
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id=\"1.2\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>MO</value></cell></row><row id=\"2\"><cell id=\"2.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id=\"2.2\"><subrow id=\"2.2.1\"><subcell id=\"2.2.1.1\"><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row></root>"
         
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                             [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},)]]]
         
        xml = grid2xml(grid,ids=True)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)         

    def test_1row_1col_2subrow_1subcol_formats(self):
    
        '''
        <root>
          <row id="1">
            <cell id="1.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id="1.2">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id="2">
            <cell id="2.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id="2.2">
              <subrow id="2.2.1">
                <subcell id="2.2.1.1">
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id="2.2.2">
                <subcell id="2.2.2.1">
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
              </subrow>
            </cell>
          </row>
        </root>
        '''
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id=\"1.2\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>MO</value></cell></row><row id=\"2\"><cell id=\"2.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id=\"2.2\"><subrow id=\"2.2.1\"><subcell id=\"2.2.1.1\"><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow><subrow id=\"2.2.2\"><subcell id=\"2.2.2.1\"><bgcolor>#99ffcc</bgcolor><fgcolor>#ffffff</fgcolor><value>Math</value></subcell></subrow></cell></row></root>"
        
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]]]
        
        xml = grid2xml(grid,ids=True)
        
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_2row_1col_2subrow_1subcol_formats(self):
        
        '''
        <root>
          <row id="1">
            <cell id="1.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id="1.2">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id="2">
            <cell id="2.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id="2.2">
              <subrow id="2.2.1">
                <subcell id="2.2.1.1">
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id="2.2.2">
                <subcell id="2.2.2.1">
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
              </subrow>
            </cell>
          </row>
          <row id="3">
            <cell id="3.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>910-950</value>
            </cell>
            <cell id="3.2">
              <subrow id="3.2.1">
                <subcell id="3.2.1.1">
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id="3.2.2">
                <subcell id="3.2.2.1">
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
              </subrow>
            </cell>
          </row>
        </root>

        '''
        
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id=\"1.2\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>MO</value></cell></row><row id=\"2\"><cell id=\"2.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id=\"2.2\"><subrow id=\"2.2.1\"><subcell id=\"2.2.1.1\"><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow><subrow id=\"2.2.2\"><subcell id=\"2.2.2.1\"><bgcolor>#99ffcc</bgcolor><fgcolor>#ffffff</fgcolor><value>Math</value></subcell></subrow></cell></row><row id=\"3\"><cell id=\"3.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>910-950</value></cell><cell id=\"3.2\"><subrow id=\"3.2.1\"><subcell id=\"3.2.1.1\"><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow><subrow id=\"3.2.2\"><subcell id=\"3.2.2.1\"><bgcolor>#99ffcc</bgcolor><fgcolor>#ffffff</fgcolor><value>Math</value></subcell></subrow></cell></row></root>"
        
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'910-950'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'},)]]]
        
        xml = grid2xml(grid,ids=True)
    
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_1row_1col_2subrow_2subcol_formats(self):
        
        '''
        <root>
          <row id="1">
            <cell id="1.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id="1.2">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id="2">
            <cell id="2.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell><cell id="2.2">
              <subrow id="2.2.1">
                <subcell id="2.2.1.1">
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
                <subcell id="2.2.1.2">
                  <bgcolor>#006600</bgcolor>
                  <fgcolor>#00ff00</fgcolor>
                  <value>Amelia</value>
                </subcell>
              </subrow>
              <subrow id="2.2.2">
                <subcell id="2.2.2.1">
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
                <subcell id="2.2.2.2">
                  <bgcolor>#d3d3d3</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Aaron</value>
                </subcell>
              </subrow>
            </cell>
          </row>
        </root>
        '''
        expected_results = "<root><row id=\"1\"><cell id=\"1.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id=\"1.2\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>MO</value></cell></row><row id=\"2\"><cell id=\"2.1\"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id=\"2.2\"><subrow id=\"2.2.1\"><subcell id=\"2.2.1.1\"><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell><subcell id=\"2.2.1.2\"><bgcolor>#006600</bgcolor><fgcolor>#00ff00</fgcolor><value>Amelia</value></subcell></subrow><subrow id=\"2.2.2\"><subcell id=\"2.2.2.1\"><bgcolor>#99ffcc</bgcolor><fgcolor>#ffffff</fgcolor><value>Math</value></subcell><subcell id=\"2.2.2.2\"><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Aaron</value></subcell></subrow></cell></row></root>";
        
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                            [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'}, {'bgcolor': '#006600', 'fgcolor': '#00ff00', 'value': u'Amelia'}), 
                                                                                               ({'bgcolor': '#99ffcc', 'fgcolor': '#ffffff', 'value': u'Math'}, {'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Aaron'})]]]
        
        xml = grid2xml(grid,ids=True)
        
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_nrow_ncol_1subrow_2subcol_formats(self):
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'??'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Karolina'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Paraic'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Issey'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'[Paraic,Rahul]'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'Amelia'}], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [], [], [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'})]], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'910-950'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#666600', 'fgcolor': '#ffffff', 'value': u'Core'})], [], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'950-1030'}, [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#006600', 'fgcolor': '#ffffff', 'value': u'Science'})], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'1030-1110'}, [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ff99cc', 'fgcolor': '#ffffff', 'value': u'History'})], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'1110-1210'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#663300', 'fgcolor': '#ffffff', 'value': u'Computer Time'})], [], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'1210-100'}, [], [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'??'})], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'100-140'}, [], [], [], [], [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'})]], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'140-220'}, [], [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ccff99', 'fgcolor': '#ffffff', 'value': u'Counseling'})], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'220-300'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#ff99cc', 'fgcolor': '#ffffff', 'value': u'Movement'})], [], [], [], [], []], [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'300-330'}, [({'bgcolor': '#d3d3d3', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#663300', 'fgcolor': '#ffffff', 'value': u'Computer Time'})], [], [], [], [], []]]  
        
        xml = grid2xml(grid,ids=True)
    
        #print xmltree.tostring(xml)
        
class Test_Grid_to_XML_resize(unittest.TestCase):
       
    def test_1row_1col_1subrow_1subcol_formats(self):
     
        '''
        <root>
          <row id="1">
            <cell id="1.1">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value />
             </cell>
             <cell id="1.2">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value>MO</value>
             </cell>
           </row>
           <row id="2">
             <cell id="2.1">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value>830-910</value>
             </cell>
             <cell id="2.2">
               <subrow id="2.2.1">
                 <subcell id="2.2.1.1">
                   <shrinkfont>5</shrinkfont>
                   <bgcolor>#ffcc99</bgcolor>
                   <fgcolor>#ffffff</fgcolor>
                   <value>ELA</value>
                 </subcell>
               </subrow>
             </cell>
           </row>
         </root>
         '''
         
        expected_results = '<root><row id="1"><cell id="1.1"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id="1.2"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>MO</value></cell></row><row id="2"><cell id="2.1"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id="2.2"><subrow id="2.2.1"><subcell id="2.2.1.1"><shrinkfont>5</shrinkfont><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row></root>';
         
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'MO'}], 
                             [{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'fgcolor': '#ffffff', 'value': u'ELA'},)]]]
         
        xml = grid2xml(grid,ids=True,shrinkfont=5)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
class Test_Grid_to_XML_valuetype(unittest.TestCase):
       
    def test_1row_1col_1subrow_1subcol_formats(self):
     
        '''
        <root>
          <row id="1">
            <cell id="1.1">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value />
             </cell>
             <cell id="1.2">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value>MO</value>
               <valuetype>dow</valuetype>
             </cell>
           </row>
           <row id="2">
             <cell id="2.1">
               <bgcolor>#ffffff</bgcolor>
               <fgcolor>#000000</fgcolor>
               <value>830-910</value>
               <valuetype>period</valuetype>
             </cell>
             <cell id="2.2">
               <subrow id="2.2.1">
                 <subcell id="2.2.1.1">
                   <shrinkfont>5</shrinkfont>
                   <bgcolor>#ffcc99</bgcolor>
                   <fgcolor>#ffffff</fgcolor>
                   <value>ELA</value>
                   <valuetype>subject</valuetype>
                 </subcell>
               </subrow>
             </cell>
           </row>
         </root>
         '''
         
        schema = dict(xaxis='period',yaxis='dow',ztypes='subject')
        
        expected_results = '<root><row id="1"><cell id="1.1"><bgcolor>#ffffff</bgcolor><valuetype>dow</valuetype><fgcolor>#000000</fgcolor><value /></cell><cell id="1.2"><bgcolor>#ffffff</bgcolor><valuetype>dow</valuetype><fgcolor>#000000</fgcolor><value>MO</value></cell></row><row id="2"><cell id="2.1"><bgcolor>#ffffff</bgcolor><valuetype>period</valuetype><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id="2.2"><subrow id="2.2.1"><subcell id="2.2.1.1"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row></root>'
         
        grid = [[{'bgcolor': '#ffffff', 'valuetype': 'dow', 'fgcolor': '#000000', 'value': ''}, {'bgcolor': '#ffffff', 'valuetype': 'dow', 'fgcolor': '#000000', 'value': u'MO'}], [{'bgcolor': '#ffffff', 'valuetype': 'period', 'fgcolor': '#000000', 'value': u'830-910'}, [({'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'},)]]]
         
        xml = grid2xml(grid,ids=True,schema=schema)
        
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
        
class Test_Grid_to_XML_nopivot(unittest.TestCase):
       
    def test_1lesson(self):
     
        '''
        <root>
          <row id="1">
            <cell id="1.1">
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>status</value>
            </cell>
            <cell id="1.2"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>recordtype</value></cell><cell id="1.3"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>period</value></cell><cell id="1.4"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>substatus</value></cell><cell id="1.5"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>source</value></cell><cell id="1.6"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>session</value></cell><cell id="1.7"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>adult</value></cell><cell id="1.8"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>student</value></cell><cell id="1.9"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>objtype</value></cell><cell id="1.10"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>dow</value></cell><cell id="1.11"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>userobjid</value></cell><cell id="1.12"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>subject</value></cell></row><row id="2"><cell id="2.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="2.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="2.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>1030-1110</value></cell><cell id="2.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="2.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="2.6"><bgcolor>#362e37</bgcolor><valuetype>session</valuetype><fgcolor>#f2e813</fgcolor><value>Dylan.Game Period.Monday.1030-1110</value></cell><cell id="2.7"><bgcolor>#362e37</bgcolor><valuetype>adult</valuetype><fgcolor>#f2e813</fgcolor><value>Dylan</value></cell><cell id="2.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Clayton</value></cell><cell id="2.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="2.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>MO</value></cell><cell id="2.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>4.1.2.37.37</value></cell><cell id="2.12"><bgcolor>#d3d3d3</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Game Period</value></cell></row></root>
        '''
        
        expected_results = '<root><row id="1"><cell id="1.1"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>status</value></cell><cell id="1.2"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>recordtype</value></cell><cell id="1.3"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>period</value></cell><cell id="1.4"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>substatus</value></cell><cell id="1.5"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>source</value></cell><cell id="1.6"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>session</value></cell><cell id="1.7"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>adult</value></cell><cell id="1.8"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>student</value></cell><cell id="1.9"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>objtype</value></cell><cell id="1.10"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>dow</value></cell><cell id="1.11"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>userobjid</value></cell><cell id="1.12"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>subject</value></cell></row><row id="2"><cell id="2.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="2.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="2.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>1030-1110</value></cell><cell id="2.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="2.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="2.6"><bgcolor>#362e37</bgcolor><valuetype>session</valuetype><fgcolor>#f2e813</fgcolor><value>Dylan.Game Period.Monday.1030-1110</value></cell><cell id="2.7"><bgcolor>#362e37</bgcolor><valuetype>adult</valuetype><fgcolor>#f2e813</fgcolor><value>Dylan</value></cell><cell id="2.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Clayton</value></cell><cell id="2.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="2.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>MO</value></cell><cell id="2.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>4.1.2.37.37</value></cell><cell id="2.12"><bgcolor>#d3d3d3</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Game Period</value></cell></row></root>';
        
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#362e37', 'valuetype': 'session', 'fgcolor': '#f2e813', 'value': u'Dylan.Game Period.Monday.1030-1110'}, {'bgcolor': '#362e37', 'valuetype': 'adult', 'fgcolor': '#f2e813', 'value': u'Dylan'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.1.2.37.37'}, {'bgcolor': '#d3d3d3', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Game Period'}]]

        xml = grid2xml(grid,ids=True)
        
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_2lessons(self):
        
        expected_results = '<root><row id="1"><cell id="1.1"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>status</value></cell><cell id="1.2"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>recordtype</value></cell><cell id="1.3"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>period</value></cell><cell id="1.4"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>substatus</value></cell><cell id="1.5"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>source</value></cell><cell id="1.6"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>session</value></cell><cell id="1.7"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>adult</value></cell><cell id="1.8"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>student</value></cell><cell id="1.9"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>objtype</value></cell><cell id="1.10"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>dow</value></cell><cell id="1.11"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>userobjid</value></cell><cell id="1.12"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>subject</value></cell></row><row id="2"><cell id="2.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="2.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="2.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>100-140</value></cell><cell id="2.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="2.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="2.6"><bgcolor>#006600</bgcolor><valuetype>session</valuetype><fgcolor>#00ff00</fgcolor><value>Amelia.ELA.Monday.100-140</value></cell><cell id="2.7"><bgcolor>#006600</bgcolor><valuetype>adult</valuetype><fgcolor>#00ff00</fgcolor><value>Amelia</value></cell><cell id="2.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Clayton</value></cell><cell id="2.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="2.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>MO</value></cell><cell id="2.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>7.1.2.6.1</value></cell><cell id="2.12"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></cell></row><row id="3"><cell id="3.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="3.2"><bgcolor>#00ff00</bgcolor><valuetype>recordtype</valuetype><fgcolor>#ffffff</fgcolor><value>wp</value></cell><cell id="3.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>140-220</value></cell><cell id="3.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="3.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="3.6"><bgcolor>#006600</bgcolor><valuetype>session</valuetype><fgcolor>#00ff00</fgcolor><value>Amelia.ELA.Monday.140-220</value></cell><cell id="3.7"><bgcolor>#006600</bgcolor><valuetype>adult</valuetype><fgcolor>#00ff00</fgcolor><value>Amelia</value></cell><cell id="3.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Clayton</value></cell><cell id="3.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="3.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>MO</value></cell><cell id="3.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>8.1.2.6.1</value></cell><cell id="3.12"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></cell></row></root>'
     
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#006600', 'valuetype': 'session', 'fgcolor': '#00ff00', 'value': u'Amelia.ELA.Monday.100-140'}, {'bgcolor': '#006600', 'valuetype': 'adult', 'fgcolor': '#00ff00', 'value': u'Amelia'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.1.2.6.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#00ff00', 'valuetype': 'recordtype', 'fgcolor': '#ffffff', 'value': u'wp'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'140-220'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#006600', 'valuetype': 'session', 'fgcolor': '#00ff00', 'value': u'Amelia.ELA.Monday.140-220'}, {'bgcolor': '#006600', 'valuetype': 'adult', 'fgcolor': '#00ff00', 'value': u'Amelia'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'8.1.2.6.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}]]
     
        xml = grid2xml(grid,ids=True)
          
        self.assertEqual(xmltree.tostring(xml),expected_results)
        
    def test_17lessons(self):
        grid = [[{'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'status'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'recordtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'period'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'substatus'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'source'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'session'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'adult'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'student'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'objtype'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'dow'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'userobjid'}, {'bgcolor': '#ffffff', 'fgcolor': '#000000', 'value': 'subject'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Monday.1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.1.9.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jack'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TU'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.2.8.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.4.9.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Wednesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.4.4.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Thursday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Bruno'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.3.3.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Thursday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Peter'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.3.7.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Tuesday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TU'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.2.9.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Student News.Wednesday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Clayton'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.4.2.1.5'}, {'bgcolor': '#003333', 'valuetype': 'subject', 'fgcolor': '#ffff99', 'value': u'Student News'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Wednesday.1030-1110'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'WE'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'4.4.9.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Thursday.950-1030'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'3.3.9.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.ELA.Monday.100-140'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'MO'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'7.1.4.1.1'}, {'bgcolor': '#ffcc99', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'ELA'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Thursday.220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Jake'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'9.3.9.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}], [{'bgcolor': '#ffffff', 'valuetype': 'row', 'fgcolor': '#000000', 'value': u'master'}, {'bgcolor': '#99ffff', 'valuetype': 'recordtype', 'fgcolor': '#0000ff', 'value': u'subject'}, {'bgcolor': '#d3d3d3', 'valuetype': 'period', 'fgcolor': '#ffffff', 'value': u'220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'substatus', 'fgcolor': '#ffffff', 'value': u'complete'}, {'bgcolor': '#d3d3d3', 'valuetype': 'source', 'fgcolor': '#ffffff', 'value': u'dbinsert'}, {'bgcolor': '#d3d3d3', 'valuetype': 'session', 'fgcolor': '#ffffff', 'value': u'Aaron.Activity Period.Thursday.220-300'}, {'bgcolor': '#d3d3d3', 'valuetype': 'adult', 'fgcolor': '#ffffff', 'value': u'Aaron'}, {'bgcolor': '#d3d3d3', 'valuetype': 'student', 'fgcolor': '#ffffff', 'value': u'Orig'}, {'bgcolor': '#d3d3d3', 'valuetype': 'objtype', 'fgcolor': '#ffffff', 'value': 'lesson'}, {'bgcolor': '#d3d3d3', 'valuetype': 'dow', 'fgcolor': '#ffffff', 'value': u'TH'}, {'bgcolor': '#d3d3d3', 'valuetype': 'userobjid', 'fgcolor': '#ffffff', 'value': u'9.3.4.1.9'}, {'bgcolor': '#cccc00', 'valuetype': 'subject', 'fgcolor': '#ffffff', 'value': u'Activity Period'}]]
        
        expected_results = '<root><row id="1"><cell id="1.1"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>status</value></cell><cell id="1.2"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>recordtype</value></cell><cell id="1.3"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>period</value></cell><cell id="1.4"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>substatus</value></cell><cell id="1.5"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>source</value></cell><cell id="1.6"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>session</value></cell><cell id="1.7"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>adult</value></cell><cell id="1.8"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>student</value></cell><cell id="1.9"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>objtype</value></cell><cell id="1.10"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>dow</value></cell><cell id="1.11"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>userobjid</value></cell><cell id="1.12"><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>subject</value></cell></row><row id="2"><cell id="2.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="2.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="2.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>1030-1110</value></cell><cell id="2.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="2.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="2.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.ELA.Monday.1030-1110</value></cell><cell id="2.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="2.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jake</value></cell><cell id="2.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="2.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>MO</value></cell><cell id="2.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>4.1.9.1.1</value></cell><cell id="2.12"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></cell></row><row id="3"><cell id="3.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="3.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="3.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>100-140</value></cell><cell id="3.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="3.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="3.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Activity Period.Tuesday.100-140</value></cell><cell id="3.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="3.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jack</value></cell><cell id="3.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="3.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TU</value></cell><cell id="3.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>7.2.8.1.9</value></cell><cell id="3.12"><bgcolor>#cccc00</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Activity Period</value></cell></row><row id="4"><cell id="4.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="4.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="4.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>950-1030</value></cell><cell id="4.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="4.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="4.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Student News.Wednesday.950-1030</value></cell><cell id="4.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="4.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jake</value></cell><cell id="4.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="4.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>WE</value></cell><cell id="4.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>3.4.9.1.5</value></cell><cell id="4.12"><bgcolor>#003333</bgcolor><valuetype>subject</valuetype><fgcolor>#ffff99</fgcolor><value>Student News</value></cell></row><row id="5"><cell id="5.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="5.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="5.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>100-140</value></cell><cell id="5.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="5.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="5.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.ELA.Wednesday.100-140</value></cell><cell id="5.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="5.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Orig</value></cell><cell id="5.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="5.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>WE</value></cell><cell id="5.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>7.4.4.1.1</value></cell><cell id="5.12"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></cell></row><row id="6"><cell id="6.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="6.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="6.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>950-1030</value></cell><cell id="6.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="6.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="6.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Student News.Thursday.950-1030</value></cell><cell id="6.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="6.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Bruno</value></cell><cell id="6.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="6.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TH</value></cell><cell id="6.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>3.3.3.1.5</value></cell><cell id="6.12"><bgcolor>#003333</bgcolor><valuetype>subject</valuetype><fgcolor>#ffff99</fgcolor><value>Student News</value></cell></row><row id="7"><cell id="7.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="7.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="7.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>950-1030</value></cell><cell id="7.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="7.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="7.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Student News.Thursday.950-1030</value></cell><cell id="7.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="7.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Peter</value></cell><cell id="7.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="7.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TH</value></cell><cell id="7.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>3.3.7.1.5</value></cell><cell id="7.12"><bgcolor>#003333</bgcolor><valuetype>subject</valuetype><fgcolor>#ffff99</fgcolor><value>Student News</value></cell></row><row id="8"><cell id="8.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="8.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="8.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>100-140</value></cell><cell id="8.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="8.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="8.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Activity Period.Tuesday.100-140</value></cell><cell id="8.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="8.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jake</value></cell><cell id="8.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="8.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TU</value></cell><cell id="8.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>7.2.9.1.9</value></cell><cell id="8.12"><bgcolor>#cccc00</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Activity Period</value></cell></row><row id="9"><cell id="9.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="9.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="9.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>950-1030</value></cell><cell id="9.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="9.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="9.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Student News.Wednesday.950-1030</value></cell><cell id="9.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="9.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Clayton</value></cell><cell id="9.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="9.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>WE</value></cell><cell id="9.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>3.4.2.1.5</value></cell><cell id="9.12"><bgcolor>#003333</bgcolor><valuetype>subject</valuetype><fgcolor>#ffff99</fgcolor><value>Student News</value></cell></row><row id="10"><cell id="10.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="10.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="10.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>1030-1110</value></cell><cell id="10.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="10.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="10.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.ELA.Wednesday.1030-1110</value></cell><cell id="10.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="10.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jake</value></cell><cell id="10.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="10.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>WE</value></cell><cell id="10.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>4.4.9.1.1</value></cell><cell id="10.12"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></cell></row><row id="11"><cell id="11.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="11.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="11.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>950-1030</value></cell><cell id="11.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="11.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="11.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Activity Period.Thursday.950-1030</value></cell><cell id="11.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="11.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jake</value></cell><cell id="11.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="11.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TH</value></cell><cell id="11.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>3.3.9.1.9</value></cell><cell id="11.12"><bgcolor>#cccc00</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Activity Period</value></cell></row><row id="12"><cell id="12.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="12.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="12.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>100-140</value></cell><cell id="12.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="12.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="12.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.ELA.Monday.100-140</value></cell><cell id="12.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="12.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Orig</value></cell><cell id="12.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="12.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>MO</value></cell><cell id="12.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>7.1.4.1.1</value></cell><cell id="12.12"><bgcolor>#ffcc99</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>ELA</value></cell></row><row id="13"><cell id="13.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="13.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="13.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>220-300</value></cell><cell id="13.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="13.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="13.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Activity Period.Thursday.220-300</value></cell><cell id="13.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="13.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Jake</value></cell><cell id="13.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="13.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TH</value></cell><cell id="13.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>9.3.9.1.9</value></cell><cell id="13.12"><bgcolor>#cccc00</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Activity Period</value></cell></row><row id="14"><cell id="14.1"><bgcolor>#ffffff</bgcolor><valuetype>row</valuetype><fgcolor>#000000</fgcolor><value>master</value></cell><cell id="14.2"><bgcolor>#99ffff</bgcolor><valuetype>recordtype</valuetype><fgcolor>#0000ff</fgcolor><value>subject</value></cell><cell id="14.3"><bgcolor>#d3d3d3</bgcolor><valuetype>period</valuetype><fgcolor>#ffffff</fgcolor><value>220-300</value></cell><cell id="14.4"><bgcolor>#d3d3d3</bgcolor><valuetype>substatus</valuetype><fgcolor>#ffffff</fgcolor><value>complete</value></cell><cell id="14.5"><bgcolor>#d3d3d3</bgcolor><valuetype>source</valuetype><fgcolor>#ffffff</fgcolor><value>dbinsert</value></cell><cell id="14.6"><bgcolor>#d3d3d3</bgcolor><valuetype>session</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron.Activity Period.Thursday.220-300</value></cell><cell id="14.7"><bgcolor>#d3d3d3</bgcolor><valuetype>adult</valuetype><fgcolor>#ffffff</fgcolor><value>Aaron</value></cell><cell id="14.8"><bgcolor>#d3d3d3</bgcolor><valuetype>student</valuetype><fgcolor>#ffffff</fgcolor><value>Orig</value></cell><cell id="14.9"><bgcolor>#d3d3d3</bgcolor><valuetype>objtype</valuetype><fgcolor>#ffffff</fgcolor><value>lesson</value></cell><cell id="14.10"><bgcolor>#d3d3d3</bgcolor><valuetype>dow</valuetype><fgcolor>#ffffff</fgcolor><value>TH</value></cell><cell id="14.11"><bgcolor>#d3d3d3</bgcolor><valuetype>userobjid</valuetype><fgcolor>#ffffff</fgcolor><value>9.3.4.1.9</value></cell><cell id="14.12"><bgcolor>#cccc00</bgcolor><valuetype>subject</valuetype><fgcolor>#ffffff</fgcolor><value>Activity Period</value></cell></row></root>'
        
        xml = grid2xml(grid,ids=True)
        
        self.assertEqual(xmltree.tostring(xml),expected_results)
                
        
class Test_Pageto_XML(unittest.TestCase):
       
    def test_1lesson(self):

        '''<root><parser><value>drawform</value></parser><item id="1"><value>master</value><valuetype>status</valuetype></item><item id="2"><value>830-910</value><valuetype>period</valuetype></item><item id="3"><value>Issey.Student News.Thursday.830-910</value><valuetype>session</valuetype></item><item id="4"><value>Issey</value><valuetype>adult</valuetype></item><item id="5"><value>Stephen</value><valuetype>student</valuetype></item><item id="6"><value>00A49216</value><valuetype>id</valuetype></item><item id="7"><value>Student News</value><valuetype>subject</valuetype></item><item id="8"><value>subject</value><valuetype>recordtype</valuetype></item><item id="9"><value>complete</value><valuetype>substatus</valuetype></item><item id="10"><value>dbinsert</value><valuetype>source</valuetype></item><item id="11"><value>lesson</value><valuetype>objtype</valuetype></item><item id="12"><value>TH</value><valuetype>dow</valuetype></item><item id="13"><value>1.3.5.20.5</value><valuetype>userobjid</valuetype></item></root>'''
        
        expected_result = '<root><parser><value>drawform</value></parser><item id="1"><value>master</value><valuetype>status</valuetype></item><item id="2"><value>830-910</value><valuetype>period</valuetype></item><item id="3"><value>Issey.Student News.Thursday.830-910</value><valuetype>session</valuetype></item><item id="4"><value>Issey</value><valuetype>adult</valuetype></item><item id="5"><value>Stephen</value><valuetype>student</valuetype></item><item id="6"><value>00A49216</value><valuetype>id</valuetype></item><item id="7"><value>Student News</value><valuetype>subject</valuetype></item><item id="8"><value>subject</value><valuetype>recordtype</valuetype></item><item id="9"><value>complete</value><valuetype>substatus</valuetype></item><item id="10"><value>dbinsert</value><valuetype>source</valuetype></item><item id="11"><value>lesson</value><valuetype>objtype</valuetype></item><item id="12"><value>TH</value><valuetype>dow</valuetype></item><item id="13"><value>1.3.5.20.5</value><valuetype>userobjid</valuetype></item></root>'
        
        header = "<root><parser><value>drawform</value></parser></root>"    

        page = {'status': u'master', 'recordtype': u'subject', 'period': u'830-910', 'substatus': u'complete', 'source': u'dbinsert', 'session': u'Issey.Student News.Thursday.830-910', 'adult': u'Issey', 'student': u'Stephen', 'id': u'00A49216', 'objtype': 'lesson', 'dow': u'TH', 'userobjid': u'1.3.5.20.5', 'subject': u'Student News'}

        xml = record2xml(page,header=header)
        
        self.assertEqual(xmltree.tostring(xml),expected_result)
        
        
if __name__ == "__main__":

    suite = unittest.TestSuite()
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_XML))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_XML_xpath))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_to_XML))
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_to_XML_function))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_to_XML_resize))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_to_XML_valuetype))
    '''
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_to_XML_nopivot))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Pageto_XML))
                  
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)