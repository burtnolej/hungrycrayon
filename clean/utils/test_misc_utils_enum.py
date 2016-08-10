import unittest
import sys
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils_enum import enum

class Test_Enum(unittest.TestCase):

    def setUp(self):
        self.e = enum(a=123,b=456,c=789)
        
    '''def test_enum_getattr_keyval(self):

        exp_results = [('a',123),('b',456),('c',789)]
        self.assertListEqual(self.e.attr_get_keyval(include_callable=False,
                                               include_nondataattr=False),exp_results)
        
    def test_enum_attr_vals(self):
        self.assertEquals(getattr(self.e,'_dm_a'),123)'''
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Enum))
    unittest.TextTestRunner(verbosity=2).run(suite)