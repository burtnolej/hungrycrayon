from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from Tkinter import Entry as Tkentry
from ttk import *
import unittest
from entry_widget import Validator, TkValidEntry, \
     rematch, TkCombobox
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from ui_utils import TkImageWidget, TkImageLabelGrid, geometry_get, font_scale, \
     tkwidgetfactory, geometry_get_dict, tkwidgetimage_set, fontscale

defaultmaster = dict(height=100,width=100,
                     x=400,y=100)
        
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
        

class TestRematch(unittest.TestCase):
    def setUp(self):
        self.mylist = ['pineapple','grapefruit','banana',
            'peach','pomegranate','passionfruit',
            'pear','grape','strawberry','raspberry',
            'rhubarb','mango','guava','apple',
            'Orange']
        
        self.mylist.sort()
    
    def test_basic(self):
        
        match = rematch('apple',self.mylist)
        self.assertListEqual(match,['apple',
                                    'pineapple'])
        
    def test_matchendchars(self):
        
        match = rematch('berry$',self.mylist)
        self.assertListEqual(match,['raspberry',
                                    'strawberry'])

    def test_matchstartchars(self):
        
        match = rematch('^pe',self.mylist)
        self.assertListEqual(match,['peach',
                                     'pear'])

    def test_matchall(self):
        
        match = rematch('a',self.mylist)
        self.assertListEqual(match,self.mylist)

    def test_matchlarge(self):
        mylist = ['foobar' for i in range(1000)]
            
        match = rematch('foobar',mylist)
        self.assertEquals(len(match),1000)
        
    def test_matchenorm(self):
        
        from time import time
        starttime = time()
        mylist = ['foobar' for i in range(100000)]
        
        match = rematch('^foo',mylist)
        
        exectime = time() - starttime
        print exectime
        self.assertEquals(len(match),100000)

    def test_matchanycase_Orange(self):
        
        self.tomatch = 'orange'
        
        match = rematch('orange',self.mylist)
        self.assertListEqual(match,['Orange'])
        
    def test_matchanycase_ORANGE(self):
        
        self.tomatch = 'ORANGE'
        
        match = rematch('orange',self.mylist)
        self.assertListEqual(match,['Orange'])        

    def test_matchmiddle(self):
        
        self.tomatch = 'be'
        
        match = rematch(self.tomatch,self.mylist)
        self.assertListEqual(match,['raspberry','strawberry'])  
        
    def tearDown(self):
        pass
    

class TestTkcombo(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.mylist = ['pineapple','grapefruit','banana',
            'peach','pomegranate','passionfruit',
            'pear','grape','strawberry','raspberry',
            'rhubarb','mango','guava','apple',
            'Orange']
        self.combo = TkCombobox(self.master,self.mylist)
        
    def test_(self):
        self.master.mainloop()
        


class TestTkRWEntry(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.mytable = [('pineapple','single',45,100),
                        ('grapefruit','single',23,33),
                        ('banana','bunch',45,67),
                        ('peach','single',23,12),
                        ('pomegranate','6pack',45,67)]

        self.combo = TKRWGrid(self.master,self.mytable)
        
    def test_(self):
        self.master.mainloop()
        
if __name__ == "__main__":

    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestValidateGtLt))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestValidateGt))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkValidEntry))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRematch))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkcombo))
  
    unittest.TextTestRunner(verbosity=2).run(suite)
