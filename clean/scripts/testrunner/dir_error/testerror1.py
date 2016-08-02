import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import generic

class DummyTest(generic):
    def dummy1(self):
        return(1/0)
    
    def dummy2(self):
        return(2)

    def dummy3(self):
        return(3)
    
    def dummy4(self):
        return(4)
