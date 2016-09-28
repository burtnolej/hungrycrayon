import unittest
import sys
from http_utils import urlpost

class TestUrlPost(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_nonamekey_fail(self):
        
        with self.assertRaises(Exception):
            self.mintype = RealInt()

if __name__ == "__main__":

    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUrlPost))
 
    unittest.TextTestRunner(verbosity=2).run(suite)
