from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
#from Tkinter import Entry as Tkentry
from ttk import *

import tkFont
import unittest

sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from ui_utils_tkventry import TkValidEntry, TkCombobox, TkEntry
from ui_utils import geometry_get,  tkwidgetfactory, geometry_get_dict
from type_utils import BoundRealInt, SetMember, SetMemberPartial, DBSetMember

#fontscale = enum(sy = 2500,sx = 3500,
#                 minfpt = 8,maxfpt = 64,
#                 minwy=50,minwx=50)

defaultmaster = dict(height=300,width=200,x=400,y=100)

defaultframe = dict(height=300,width=200,x=0,y=0)

fullscreenmaster = dict(height=2500,width=3500,x=0,y=0)
        
class TestTkcomboSetMember(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                                 'peach','pomegranate','passionfruit',
                                                                 'pear','grape','strawberry','raspberry',
                                                                 'rhubarb','mango','guava','apple',
                                                                 'Orange'])
        
        self.combo = TkCombobox(self.master,self.setmemberp)
        
    def test_(self):
        self.combo.sv.set('p')
        self.assertEqual(self.combo.label.cget('text'),9)
        
    def tearDown(self):
        self.master.destroy()
        
class TestTkcomboDBSetMember(unittest.TestCase):
    def setUp(self):
        dbname = '/data/food'
        tbl_name = 'food'
        fldname = 'food_name'
        self.dbsetmember = DBSetMember(dbname,tbl_name,
                                     fldname,
                                     name='x{dblist}')
        
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.combo = TkCombobox(self.master,self.dbsetmember)
        
    def test_(self):
        #self.master.mainloop()
        self.combo.sv.set('d')
        self.assertEqual(self.combo.label.cget('text'),65)
        
    def tearDown(self):
        self.master.destroy()
        
class TestTkValidEntryBInt(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.boundint = BoundRealInt(name='40>=x<=60',ubound=60,lbound=40)

        self.ventry = TkValidEntry(self.master,'foobar',8,0,self.boundint)
        self.ventry.grid(row=0,sticky=NSEW)
        self.ventry.entry.focus_set()
        
        self.master.rowconfigure(0,uniform='foo2')
        
    def test_55_True(self):
        self.ventry.sv.set(55)
        self.assertEqual(self.ventry.statuslabel.cget('background'),'lime')
        self.master.mainloop()
        
    def test_65_True(self):
        self.ventry.sv.set(65)
        self.assertEqual(self.ventry.statuslabel.cget('background'),'pink')
        #self.master.mainloop()
        
    def tearDown(self):
        self.master.destroy()
        
class TestTkValidEntrySetMember(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                                 'peach','pomegranate','passionfruit',
                                                                 'pear','grape','strawberry','raspberry',
                                                                 'rhubarb','mango','guava','apple',
                                                                 'Orange'])
        
        self.ventry = TkValidEntry(self.master,'foobar',8,0,self.setmemberp)
        self.ventry.grid(row=0,sticky=NSEW)
        self.ventry.entry.focus_set()
        
        self.master.rowconfigure(0,uniform='foo2')
        
    def test_55_True(self):
        self.master.mainloop()
        pass
        
    def tearDown(self):
        self.master.destroy()

class TestTkValidEntryMulti(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.boundint = BoundRealInt(name='40>=x<=60',
                                       ubound=60,lbound=40)

        self.ventry = TkValidEntry(self.master,'foobar',
                                   8,0,Tkentry,self.boundint)
        self.ventry.grid(row=0,sticky=NSEW)
        #self.gte40lte60 = Validator(name='40>=x<=60',
        #                            ubound=60,lbound=40)
        


                    
        #self.ventry.register_validator(self.gte40lte60)
        
        self.ventry.entry.focus_set()
        
        #self.ventry2 = TkValidEntry(self.master,'foobar2',
        #                           8,'barfoo2',Tkentry)
        #self.ventry2.grid(row=1,sticky=NSEW)
        
        self.master.rowconfigure(0,uniform='foo2')
        #self.master.rowconfigure(1,uniform='foo2')
        
    def test_(self):
        self.master.mainloop()
        
    def tearDown(self):
        self.master.destroy()        
if __name__ == "__main__":

    suite = unittest.TestSuite()
    

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkValidEntryBInt))

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkValidEntrySetMember))


    
    


    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkcomboSetMember))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkcomboDBSetMember))
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)