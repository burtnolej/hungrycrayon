
import unittest
import sys

from xml2freemind import xml2freemind
import xml.etree.ElementTree as xmltree
import filecmp

sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import os_file_to_string

class Test_xml2mm(unittest.TestCase):
    
    def setUp(self):
        self.output_xml="./tests/tmp.mm"
        self.verbosity=1
      
    def test_xml2mm_missing_key(self):
        #Format nodes must have SubElement with tag=Key
        self.input_xml="./tests/test1_input_missing_key.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/test1_output.mm"

        with self.assertRaises(Exception):
            
            xml2freemind.convert(self.input_xml,
                                 verbosity = self.verbosity,
                                 output_filename =self.output_xml)

    def test_xml2mm_missing_value(self):
        #Format nodes must have SubElement with tag=Value
        self.input_xml="./tests/test1_input_missing_value.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/test1_output.mm"

        with self.assertRaises(Exception):
            
            xml2freemind.convert(self.input_xml,
                                 verbosity = self.verbosity,
                                 output_filename = self.output_xml)
          
    def test_xml2mm_1node_short_name(self):

        #<root>
        #    <Database Name="foobar"/>
        #</root>
        
        #<map version="0.9.0">
        #    <node TEXT="foobar">
        #         <nodeTEXT="Name:foobar"/>
        #     </node>
        #</map>

        self.input_xml="./tests/1node_short_format.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/1node_short_format.mm"

        xml2freemind.convert(self.input_xml,
                             verbosity = self.verbosity,
                             output_filename = self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )

    def test_xml2mm_1node_long_name(self):
        
        #<root>
        #    <Database Name="foobar"/>
        #</root>
        
        #<map version="0.9.0"> 
        #     <node TEXT="Database:foobar"> 
        #          <node TEXT="Name:foobar" /> 
        #      </node> 
        #</map>
        
        self.input_xml="./tests/1node_long_format.xml"
        self.expected_output_xml = "./tests/1node_long_format.mm"
        
        xml2freemind.convert(self.input_xml,
                             verbosity = self.verbosity,
                             output_filename = self.output_xml,
                             full_label =True)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_xml2mm_3levels_no_text(self):
        
        self.input_xml="./tests/test4_input.xml"
        self.expected_output_xml = "./tests/test4_output.mm"
        
        xml2freemind.convert(self.input_xml,
                             verbosity = self.verbosity,
                             output_filename = self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_xml2mm_3levels_no_text_siblings(self):
        
        self.input_xml="./tests/test5_input.xml"
        self.expected_output_xml = "./tests/test5_output.mm"
        
        xml2freemind.convert(self.input_xml,
                             verbosity = self.verbosity,
                             output_filename = self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_xml2mm_verbose(self):
        
        self.input_xml="./tests/test5_input.xml"
        self.expected_output_xml = "./tests/test5_output.mm"
        
        xml2freemind.convert(self.input_xml,
                             verbosity = 5,
                             output_filename = self.output_xml)
        
    def test_xml2mm_multiple_roots(self):
        
        #<root>
        #    <Database Name="foobar">
        #        <Table Name="barfoo">
        #            <Column Name="dohdoh" />
        #        </Table>
        #        <Test Name="ooh"/>
        #        <Test Name="ahh"/>
        #    </Database>
        #    <Database Name="foobarsaunders">
        #        <Table Name="yippee">
        #            <Column Name="blah" />
        #        </Table>
        #    </Database>
        #</root>
        
        #<map version="0.9.0">
        #    <multiple_roots> 
        #        <node TEXT="foobar"> 
        #            <node TEXT="barfoo"> 
        #                <node TEXT="dohdoh"> 
        #                    <node TEXT="Name:dohdoh" /> 
        #                </node> 
        #                <node TEXT="Name:barfoo" /> 
        #            </node> 
        #            <node TEXT="ooh"> 
        #                <node TEXT="Name:ooh" /> 
        #            </node>
        #            <node TEXT="ahh"> 
        #                <node TEXT="Name:ahh" /> 
        #            </node>
        #            <node TEXT="Name:foobar" /> 
        #        </node>
        #        <node TEXT="foobarsaunders"> 
        #            <node TEXT="yippee"> 
        #                <node TEXT="blah"> 
        #                    <node TEXT="Name:blah" /> 
        #                </node> 
        #                <node TEXT="Name:yippee" /> 
        #            </node>
        #            <node TEXT="Name:foobarsaunders" /> 
        #        </node>
        #    </multiple_roots>
        #</map>

        self.input_xml="./tests/multiple_roots.xml"
        self.expected_output_xml = "./multiple_roots.mm"
        
        xml2freemind.convert(self.input_xml,
                             verbosity = 5,
                             output_filename = self.output_xml)
        
    def test_supress_name_attrib(self):
        
        #<root>
        #    <Database Name="foobar"/>
        #</root>
        
        #<map version="0.9.0">
        #    <node TEXT="foobar" />
        #</map>

        self.input_xml="./tests/supress_name_attrib.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/supress_name_attrib.mm"

        xml2freemind.convert(self.input_xml,
                             verbosity = self.verbosity,
                             output_filename = self.output_xml,
                             suppress_attrib=['Name'])
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )

    def test_format_node(self):
        
        #<root>
        #    <Database Name="foobar"/>
        #    <Format Name="Database"burgundywhite18</Format>
        #</root>
        
        #<map version="0.9.0">
        #      <node BACKGROUND_COLOR="#85144B" \
        #            COLOR="#FFFFFF" \
        #            STYLE="bubble" \
        #            TEXT="foobar">
        #            <font BOLD="false" 
        #                  ITALIC="False" 
        #                  NAME="SansSerif"
        #                  SIZE="18" />
        #      </node>
        #</map>

        self.input_xml="./tests/formats.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/formats.mm"

        xml2freemind.convert(self.input_xml,
                             verbosity = 5,
                             output_filename = self.output_xml,
                             suppress_attrib=['Name'])
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_unit_parse_add_groupby(self):
        #<root>
        #    <Database Name="foobar">
        #           <Table Name="barfoo">
        #                <Column Name="boohoo" />
        #           </Table>
        #    </Database>
        #    <Database Name="foobar2">
        #           <Table Name="barfoo2">
        #                <Column Name="boohoo2" />
        #           </Table>
        #    </Database>
        #</root>
        
        #<root>
        #    <Database Name="foobar">
        #           <Table Name="barfoo">
        #                <Column Name="boohoo" />
        #           </Table>
        #    </Database>
        #    <Database Name="foobar2">
        #           <Table Name="barfoo2">
        #                <Column Name="boohoo2" />
        #           </Table>
        #    </Database>
        #    <gbyDatabase>
        #          <foobar />
        #          <foobar2 />
        #    </gbyDatabase>
        #</root>
        
        xml = "<root><Database Name=\"foobar\"><Table Name=\"barfoo\"><Column Name=\"boohoo\" /></Table></Database><Database Name=\"foobar2\"><Table Name=\"barfoo2\"><Column Name=\"boohoo2\" /></Table></Database><gbyDatabase><foobar /><foobar2 /></gbyDatabase></root>"

        self.input_xml="./tests/groupby.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/groupby.mm"
         
        x2fm = xml2freemind.groupby(self.input_xml,
                                    verbosity = 5,
                                    output_filename = self.output_xml,
                                    suppress_attrib=['Name'],
                                    groupby_tag = ['Database'])
        
        self.assertEqual(xmltree.tostring(x2fm.root).replace(" ",""),xml.replace(" ",""))

        
    def test_groupby(self):
        #<root>
        #    <Database Name="foobar">
        #           <Table Name="barfoo">
        #                <Column Name="boohoo" />
        #           </Table>
        #    </Database>
        #    <Database Name="foobar2">
        #           <Table Name="barfoo2">
        #                <Column Name="boohoo2" />
        #           </Table>
        #    </Database>
        #</root>

        #<map version="0.9.0">
        #      <node TEXT="groupby">
        #      <node TEXT="foobar">
        #            <node TEXT="barfoo>
        #                 <node TEXT="boohoo" />
        #            </node>
        #      </node>
        #      <node TEXT="foobar2">
        #            <node TEXT="barfoo2>
        #                 <node TEXT="boohoo2" />
        #            </node>
        #      </node>
        #      <node TEXT="Database">
        #            <node TEXT="foobar"/>
        #            <node TEXT="foobar2"/>
        #      </node>
        #      <node TEXT="Table">
        #            <node TEXT="barfoo"/>
        #            <node TEXT="barfoo2"/>
        #      </node>
        #      <node TEXT="Column">
        #            <node TEXT="boohoo"/>
        #            <node TEXT="boohoo2"/>
        #      </node>
        #      </node>
        #</map>
        

        self.input_xml="./tests/groupby.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/groupby.mm"
         
        x2fm = xml2freemind.convert(self.input_xml,
                                    verbosity = 5,
                                    output_filename = self.output_xml,
                                    suppress_attrib=['Name'],
                                    groupby_tag = ['Database'])
        
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
        
    def test_groupby_multi(self):
        #<root>
        #    <Database Name="foobar">
        #           <Table Name="barfoo">
        #                <Column Name="boohoo" />
        #           </Table>
        #    </Database>
        #    <Database Name="foobar2">
        #           <Table Name="barfoo2">
        #                <Column Name="boohoo2" />
        #           </Table>
        #    </Database>
        #</root>

        #<map version="0.9.0">
        #      <node TEXT="groupby">
        #      <node TEXT="foobar">
        #            <node TEXT="barfoo>
        #                 <node TEXT="boohoo" />
        #            </node>
        #      </node>
        #      <node TEXT="foobar2">
        #            <node TEXT="barfoo2>
        #                 <node TEXT="boohoo2" />
        #            </node>
        #      </node>
        #      <node TEXT="Database">
        #            <node TEXT="foobar"/>
        #            <node TEXT="foobar2"/>
        #      </node>
        #      <node TEXT="Table">
        #            <node TEXT="barfoo"/>
        #            <node TEXT="barfoo2"/>
        #      </node>
        #      <node TEXT="Column">
        #            <node TEXT="boohoo"/>
        #            <node TEXT="boohoo2"/>
        #      </node>
        #      </node>
        #</map>
        
        self.input_xml="./tests/groupby.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/groupby_multi.mm"
         
        x2fm = xml2freemind.convert(self.input_xml,
                                    verbosity = 5,
                                    output_filename = self.output_xml,
                                    suppress_attrib=['Name'],
                                    groupby_tag = ['Database','Table','Column'])
        
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )


if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_xml2mm)
    unittest.TextTestRunner(verbosity=2).run(suite)
    