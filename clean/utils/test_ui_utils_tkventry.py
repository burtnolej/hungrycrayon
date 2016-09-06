from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from Tkinter import Entry as Tkentry
from ttk import *

import tkFont
import unittest

sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from ui_utils_tkventry import TkValidEntry, Validator
from ui_utils import geometry_get,  tkwidgetfactory, geometry_get_dict


#fontscale = enum(sy = 2500,sx = 3500,
#                 minfpt = 8,maxfpt = 64,
#                 minwy=50,minwx=50)

defaultmaster = dict(height=300,width=200,x=100,y=100)

defaultframe = dict(height=300,width=200,x=0,y=0)

fullscreenmaster = dict(height=2500,width=3500,x=0,y=0)

class TestTkValidEntry(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.ventry = TkValidEntry(self.master,'foobar',
                                   8,0,Tkentry)
        self.ventry.grid(row=0,sticky=NSEW)
        self.gte40lte60 = Validator(name='40>=x<=60',
                                    ubound=60,lbound=40)
                    
        self.ventry.register_validator(self.gte40lte60)
        
        self.ventry.entry.focus_set()
        
        self.ventry2 = TkValidEntry(self.master,'foobar2',
                                   8,'barfoo2',Tkentry)
        self.ventry2.grid(row=1,sticky=NSEW)
        
        self.master.rowconfigure(0,uniform='foo2')
        self.master.rowconfigure(1,uniform='foo2')
        
    def test_(self):
        self.master.mainloop()
        
    def tearDown(self):
        self.master.destroy()


        
if __name__ == "__main__":

    suite = unittest.TestSuite()
    
    # Test helper
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkValidEntry))

    unittest.TextTestRunner(verbosity=2).run(suite)