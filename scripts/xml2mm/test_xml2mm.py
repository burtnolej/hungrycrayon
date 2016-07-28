
import unittest
import sys

from xml2mm import convert
import filecmp

sys.path.append("/home/burtnolej/Development/pythonapps3/utils")


class Test_xml2mm(unittest.TestCase):
    
    def setUp(self):
        self.output_xml="tmp.mm"
       
    def test_xml2mm_1node_short(self):

        self.input_xml="test1_input.xml"
        self.output_xml="tmp.mm"
        self.expected_output_xml = "test1_output.mm"

        convert(self.input_xml,self.output_xml)
        
        self.assertTrue(filecmp.cmp(self.output_xml,self.expected_output_xml))

    def test_xml2mm_1node_long(self):
        
        self.input_xml="test1_input.xml"
        self.expected_output_xml = "test2_output.mm"
        
        convert(self.input_xml,self.output_xml,True)
        
        self.assertTrue(filecmp.cmp(self.output_xml,self.expected_output_xml))
        
    def test_xml2mm_unrecognized_attr(self):
        
        self.input_xml="test2_input.xml"
        self.expected_output_xml = "test2_output.mm"
        
        convert(self.input_xml,self.output_xml,True)
        
        self.assertTrue(filecmp.cmp(self.output_xml,self.expected_output_xml))
    
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_xml2mm)
    unittest.TextTestRunner(verbosity=2).run(suite)
    