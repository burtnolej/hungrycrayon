
import unittest
import sys

from xml2freemind import xml2freemind
import xml.etree.ElementTree as xmltree
import filecmp

sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import os_file_to_string

class Test_xml2mm(unittest.TestCase):
    
    def setUp(self):
        self.output_xml="./tests/tmp.mm"
       
    def test_xml2mm_missing_key(self):
        #Format nodes must have SubElement with tag=Key
        self.input_xml="./tests/test1_input_missing_key.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/test1_output.mm"

        with self.assertRaises(Exception):
            
            xml2freemind(self.input_xml,self.output_xml)

    def test_xml2mm_missing_value(self):
        #Format nodes must have SubElement with tag=Value
        self.input_xml="./tests/test1_input_missing_value.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/test1_output.mm"

        with self.assertRaises(Exception):
            
            xml2freemind(self.input_xml,self.output_xml)
     
    def test_xml2mm_1node_short(self):

        self.input_xml="./tests/test0_input.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/test0_output.mm"

        xml2freemind(self.input_xml,self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_xml2mm_1node_short_formats(self):

        self.input_xml="./tests/test1_input.xml"
        self.output_xml="./tests/tmp.mm"
        self.expected_output_xml = "./tests/test1_output.mm"

        xml2freemind(self.input_xml,self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )

    def test_xml2mm_1node_long_formats(self):
        
        self.input_xml="./tests/test1_input.xml"
        self.expected_output_xml = "./tests/test2_output.mm"
        
        xml2freemind(self.input_xml,self.output_xml,True)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_xml2mm_3levels_no_text(self):
        
        self.input_xml="./tests/test4_input.xml"
        self.expected_output_xml = "./tests/test4_output.mm"
        
        xml2freemind(self.input_xml,self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        print self.output_as_str
        print self.expected_as_str 
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
    def test_xml2mm_3levels_no_text_siblings(self):
        
        self.input_xml="./tests/test5_input.xml"
        self.expected_output_xml = "./tests/test5_output.mm"
        
        xml2freemind(self.input_xml,self.output_xml)
            
        self.output_as_str = os_file_to_string(self.output_xml,["\n","\t"," "])
        self.expected_as_str = os_file_to_string(self.expected_output_xml,["\n","\t"," "])
        
        print self.output_as_str
        print self.expected_as_str 
        self.assertEquals(self.output_as_str,self.expected_as_str )
        
        
    '''
    def test_xml2mm_unrecognized_attr(self):
        
        self.input_xml="./tests/test2_input.xml"
        self.expected_output_xml = "./tests/test2_output.mm"
        
        convert(self.input_xml,self.output_xml,True)
        
        self.assertTrue(filecmp.cmp(self.output_xml,self.expected_output_xml))
    '''
    
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_xml2mm)
    unittest.TextTestRunner(verbosity=2).run(suite)
    