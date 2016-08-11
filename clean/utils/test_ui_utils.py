from Tkinter import *
from ttk import *

import unittest

from ui_utils import tk_create_config, tkfrm_cfg, \
     tk_create_frame

def _dumpwgt(tk):
    #tk = getattr(wgt,'tk')
    for attr in dir(tk):
        if not callable(getattr(tk,attr)):
            print attr,getattr(tk,attr)
    
class TestUIBasic(unittest.TestCase):
    
    def setUp(self):
        self.master = Tk()
        
    def test_draw_frame(self):
        self.frame = Frame(self.master)
        
        self.assertEquals(self.frame.widgetName,'ttk::frame')
        self.assertEquals(self.frame.children,{})
        self.assertEquals(self.frame.master,'.')
        
    def test_draw_frame_with_config(self):
        self.frame = Frame(self.master)
        
        frame_style = Style()
        
        tk_create_config(frame_style,tkfrm_cfg,'myframe')
        tk_create_frame(self.master,'myframe')
        pass
    
    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()
        


class TestUIGrid(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.frame = Frame(self.master)
        
    def test_add_grid(self):
        self.frame.grid(row=2,column=2)

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()

class TestUIWidgets(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.frame = Frame(self.master)
        self.frame.grid(row=2,column=2)

    def test_button(self):
        button = Button(self.frame,text="foobar")
        button.grid(row=1,column=1)   
        self.assertTrue(isinstance(self.frame.children[button._name],Button))
        
        self.assertEquals(button,'button')
        #_dumpwgt(button)
        #self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
    
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIWidgets))
    unittest.TextTestRunner(verbosity=2).run(suite)
