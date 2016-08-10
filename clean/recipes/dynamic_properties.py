import unittest
import sys
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")

class myclass(object):
    
    def __init__(self):
        self._dm_a = 123
    
    def __getattribute__(self,attr):

        return super(myclass, self).__getattribute__("_dm_"+attr)
               
class Test_DynamicProperties(unittest.TestCase):
    
    def test_getattr(self):
        
        mc = myclass()
        self.assertEquals(mc.a,123)
        
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DynamicProperties))
    unittest.TextTestRunner(verbosity=2).run(suite)