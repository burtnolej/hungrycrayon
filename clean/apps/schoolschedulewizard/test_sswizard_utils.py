import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from Tkinter import *
from ttk import *

import unittest

from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from misc_utils import nxnarraycreate
from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO

from database_util import Database
from database_table_util import tbl_rows_get, tbl_query

from sswizard_utils import dropdown_build

class UI(Tk):
    def __init__(self,database):       
        Tk.__init__(self)
        
        self.maxrows=9 # rows in the grid
        self.maxcols=10 # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*20 # master height
        wmwidth=wwidth*20 # master width 
    
        geom = geometry_get(wmheight,wmwidth,0,0)
        self.geometry(geom)
        
        widget_args=dict(background='white')
        
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        widgetcfg = dropdown_build(database,widgetcfg)

        setmemberp = SetMemberPartial(name='x{mylist}',set=[])

        self.entrygrid = TkImageLabelGrid(self,'entrygrid',setmemberp,wmwidth,wmheight,
                                          0,0,self.maxrows,self.maxcols,
                                          {},widgetcfg)
        self.entrygrid.grid(row=0,sticky=NSEW)      


class Test_(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('quadref')
        self.classtbl = 'class'
        
    '''def test_(self):
        
        input = [[{},{}],
                 [{},{}]]
        
        p1 = {'values':['Da-Hum','Br-STEM','Jk-Mvmt']}
        p2 = {'values':['Da-Hum','Br-STEM','Jk-WP']}

        expected_results = [[p1,p1],
                            [p2,p2]]
        
        results = dropdown_build(self.database,input)
        
        self.assertEqual(expected_results,results)'''
        
        
    def test_col1(self):
        widget_args=dict(background='white')
        
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
       
        expected_results = ['Da-Hum','Br-STEM','Jk-Mvmt','Th-STEM','Js-Hum']
        self.assertEqual(widgetcfg[0][0]['values'],expected_results)

    def test_col2(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Da-Hum','Br-STEM']
        self.assertEqual(widgetcfg[1][0]['values'],expected_results)
         
    def test_col3(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-SPED','Th-STEM','Js-Hum']
        self.assertEqual(widgetcfg[2][0]['values'],expected_results)

    def test_col4(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Jk-SPED','Th-STEM','Js-Hum']
        self.assertEqual(widgetcfg[3][0]['values'],expected_results)

    def test_col5(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-Mvmt']
        self.assertEqual(widgetcfg[4][0]['values'],expected_results)

    def test_col6(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-SPED']
        self.assertEqual(widgetcfg[5][0]['values'],expected_results)
    
    def test_col7(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Da-Hum','Br-STEM']
        self.assertEqual(widgetcfg[6][0]['values'],expected_results)

    def test_col8(self):
        widget_args=dict(background='white')
         
        widgetcfg = nxnarraycreate(8,10,widget_args)
        widgetcfg = dropdown_build(self.database,widgetcfg)
        
        expected_results = ['Da-Hum','Br-STEM','Jk-AP']
        self.assertEqual(widgetcfg[7][0]['values'],expected_results)

class Test_UI(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('quadref')
        self.ui = UI(self.database)
        
    def test_(self):
        
        print self.ui.entrygrid.widgets[0][0]['values']
        self.ui.mainloop()
        #pass

if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_UI))

    unittest.TextTestRunner(verbosity=2).run(suite) 


