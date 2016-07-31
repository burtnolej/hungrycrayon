
import unittest
import sys

from xml2freemind import xml2freemind
import xml.etree.ElementTree as xmltree
import filecmp

sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import os_file_to_string

class Test_Test(unittest.TestCase):
    pass

if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    