import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")

from Tkinter import *
from ttk import *

import unittest

from sswizard import schoolschedgeneric, WizardUI, teachers
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory
from misc_utils import Log

from shutil import copyfile
from os import remove, path

class Test_Grid_Behaviour_Focus(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('test')
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.database, self.of)
        
        parent_name = self.ui.entrygrid.widgets[0][0].winfo_parent()
        self.parent_widget = self.ui.entrygrid.widgets[0][0]._nametowidget(parent_name)
        self.parent_widget.update()
    
    def test_rightarrow_moveright(self):
        
        self.ui.entrygrid.widgets[0][0].event_generate("<Right>")
        _,new_x,new_y = str(self.parent_widget.focus_get()).split(",")
               
        self.assertEqual(new_x,'0')
        self.assertEqual(new_y,'1')
        
        
    def test_rightarrow_moveright1_down1(self):
        
        self.ui.entrygrid.widgets[0][0].event_generate("<Right>")
        self.parent_widget.focus_get().event_generate("<Down>")
        
        _,new_x,new_y = str(self.parent_widget.focus_get()).split(",")
              
        self.assertEqual(new_x,'1')
        self.assertEqual(new_y,'1')
        
    def tearDown(self):
        self.ui.destroy()
        
class Test_Grid_Behaviour_Update_Combobox(unittest.TestCase):
    def setUp(self):
        
        self.database = Database('test')
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.database, self.of)
        
        parent_name = self.ui.entrygrid.widgets[0][0].winfo_parent()
        self.parent_widget = self.ui.entrygrid.widgets[0][0]._nametowidget(parent_name)
        self.parent_widget.update()
        
        self.ui.entrygrid.widgets[0][0].event_generate("<Right>")
        self.parent_widget.focus_get().event_generate("<Down>")
        
        self.widget = self.parent_widget.focus_get()
    
    def test_rightarrow_moveright(self):

        # need to input char by char for the complete to fire
        self.widget.insert(0,'n')
        self.widget.insert(1,'a')

        self.assertEqual(self.widget.sv.get(),'NATHANIEL')

        self.assertEqual(self.widget['style'],'InFocus.Valid.TCombobox')
        
    def tearDown(self):
        self.ui.destroy()
        
class Test_Base(unittest.TestCase):
    def setUp(self):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_10rows'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.database = Database(self.dbfilename)
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.database, self.of)       
        
    def tearDown(self):
        self.ui.destroy()
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        
class Test_Input_New_Save_Persist(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        self.ui.dbname_entry_sv.set('tmp')
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30-9:10')
        self.ui.entrygrid.widgets[0][1].sv.set('Stan')
        self.ui.entrygrid.widgets[1][1].sv.set('NATHANIEL')
        
        self.ui.save()
        self.ui.persist()
    
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', 'Stan'], 
                            ['9:11-9:51'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)    
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 0]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
    def test_grid_contents(self):
        
        expected_results =[['Stan'],
                        ['8:30-9:10', 'NATHANIEL']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
    
class Test_Input_New_Save_Change_Save_Persist(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        self.ui.dbname_entry_sv.set('tmp')
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30-9:10')
        self.ui.entrygrid.widgets[0][1].sv.set('Stan')
        self.ui.entrygrid.widgets[1][1].sv.set('NATHANIEL')
        
        self.ui.save()
        
        self.ui.entrygrid.widgets[1][1].sv.set('TRISTAN')
        
        self.ui.persist()
    
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', 'Stan'], 
                            ['9:11-9:51'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)    
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 0],
                           [u'8:30-9:10', u'TRISTAN', u'Stan', u'Tuesday', 1]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
    def test_grid_contents(self):
        
        expected_results =[['Stan'],
                        ['8:30-9:10', 'TRISTAN']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
 
     
class Test_Load(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_grid_contents(self):
        self.ui.load()
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                                   ['8:30-9:10', 'NATHANIEL', 'ORIG', 'TRISTAN', 'COBY', 'YOSEF'],
                                   ['9:11-9:51', 'LUCY', 'DONOVAN', 'BOOKER', 'ASHER', 'JAKE']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)

    '''def test_update_queue(self):
        self.ui.load(0)
        expected_results = [['',('Stan', 1), ('Galina', 1),('Samantha', 1),('Amelia',1),('Paraic',1)],
                            [('8:30-9:10', 1),('NATHANIEL', 1),('ORIG', 1),('TRISTAN', 1),('COBY', 1),('YOSEF', 1)],
                            [('9:11-9:51', 1),('LUCY', 1),('DONOVAN', 1),('BOOKER', 1), ('ASHER', 1),('JAKE', 1)]]
                              
        
        values,bgcolor =  self.ui.updates_get('entrygrid')
        
        self.assertListEqual(values,expected_results)'''
     
class Test_Load_Save(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)

        self.ui.load_save()
        
    def test_objectrepr_type(self):
        expected_results = ['lesson','schedule','dow','subject','lessontype','objtype',
                            'userobjid','period','student','saveversion','teacher']
        
        expected_results.sort()

        
        results = self.of.query()
        results.sort()

        self.assertListEqual(results, expected_results)
        
    def test_objectrepr_student_object(self):
        
        results = self.of.query('student')
        
        for obj in results:
            self.assertEqual(obj.__class__.__name__,'student')
        
    def test_objectrepr_student_attr(self):
        
        
        results = self.of.query('student')
        
        student_obj = results[0]
        name = getattr(student_obj,'name')
        
        self.assertEquals(name,getattr(student_obj,'objid'))
        self.assertEquals(name,getattr(student_obj,'userobjid'))
        self.assertEquals('student',getattr(student_obj,'objtype'))
        
        self.assertEqual('ObjFactory', getattr(student_obj,'of').__class__.__name__)
        self.assertEqual('Log', getattr(student_obj,'log').__class__.__name__)

    def test_objectrepr_lesson_attr(self):
             
        
        results = self.of.query('lesson')
        
        lesson_obj = results[0]
        objid = getattr(lesson_obj,'objid')

        self.assertEquals(objid,getattr(lesson_obj,'userobjid'))
        self.assertEquals('lesson',getattr(lesson_obj,'objtype'))
        self.assertEquals('Tuesday',getattr(lesson_obj,'dow'))
        self.assertEquals('MATH',getattr(lesson_obj,'subject'))
        self.assertEquals('wp',getattr(lesson_obj,'lessontype'))
        self.assertIn(getattr(lesson_obj,'teacher'),teachers)
        self.assertEqual('ObjFactory', getattr(lesson_obj,'of').__class__.__name__)
        self.assertEqual('Log', getattr(lesson_obj,'log').__class__.__name__)
     
    def test_objectrepr_num_lesson(self):
        # test that the objects created have the correct member attr and attrvals
        results = self.of.query('lesson')
        self.assertEqual(len(results),10)
        
    def test_objectrepr_num_teacher(self):
        # test that the objects created have the correct member attr and attrvals
        results = self.of.query('teacher')
        self.assertEqual(len(results),5)
        
    def test_objectrepr_num_student(self):
        # test that the objects created have the correct member attr and attrvals
        
        results = self.of.query('student')
        self.assertEqual(len(results),10)
        
    def test_grid_contents(self):
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                                   ['8:30-9:10', 'NATHANIEL', 'ORIG', 'TRISTAN', 'COBY', 'YOSEF'],
                                   ['9:11-9:51', 'LUCY', 'DONOVAN', 'BOOKER', 'ASHER', 'JAKE']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
        
    '''def test_update_queue(self):
        self.ui.load_save(0)
        expected_results = [['',('Stan', 1), ('Galina', 1),('Samantha', 1),('Amelia',1),('Paraic',1)],
                            [('8:30-9:10', 1),('NATHANIEL', 1),('ORIG', 1),('TRISTAN', 1),('COBY', 1),('YOSEF', 1)],
                            [('9:11-9:51', 1),('LUCY', 1),('DONOVAN', 1),('BOOKER', 1), ('ASHER', 1),('JAKE', 1)]]
                              
        
        values,bgcolor =  self.ui.updates_get('entrygrid')
        
        self.assertListEqual(values,expected_results)'''
    
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', u'Stan', u'Samantha', u'Galina', u'Amelia', u'Paraic'], 
                            ['9:11-9:51', u'Samantha', u'Stan', u'Paraic', u'Amelia', u'Galina'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)    
        
class Test_Load_Change_Save_Single_Value(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        self.ui.load()
    
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
    
        self.ui.save()
        
        self.ui.persist()
        
    '''def test_update_queue(self):
        
        expected_results = [[('Stan,Galina',2),('Samantha',1),'',('Galina',1),('Amelia',1),'','',('Paraic',1),'','','',''],
                            ['','','','','',('Samantha',1),'','',('Stan',1),('Paraic',1),('Amelia',1),('Galina',1)]]
        
        expected_colors = [['red','lightgreen','','lightgreen','lightgreen','','','lightgreen','','','',''],
                            ['','','','','','lightgreen','','','lightgreen','lightgreen','lightgreen','lightgreen']]

        
        values,bgcolor = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_results,values)
        self.assertListEqual(expected_colors,bgcolor)'''
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 0], 
                           [u'8:30-9:10', u'ORIG', u'Galina', u'Tuesday', 0], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 0], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 0], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 0], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 0], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 0], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 0], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 0], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 0],
                           [u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 1], 
                           [u'8:30-9:10', u'NATHANIEL', u'Galina', u'Tuesday', 1], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 1], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 1], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 1], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 1], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 1], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 1], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 1], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 1]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
        
    def test_entrygrid_contents(self):
        
        expected_results =[[              'Stan',    'Galina',   'Samantha', 'Amelia', 'Paraic'],
                           ['8:30-9:10', 'NATHANIEL', 'NATHANIEL', 'TRISTAN', 'COBY', 'YOSEF'],
                           ['9:11-9:51', 'LUCY', 'DONOVAN', 'BOOKER', 'ASHER', 'JAKE']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)        
        
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', u'Stan,Galina', u'Samantha', u'Amelia','Paraic'], 
                            ['9:11-9:51', u'Samantha', u'Stan', u'Paraic', u'Amelia', u'Galina'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)
        
class Test_Load_Save_Change_Save_Change_Save_Single_Value(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        self.ui.load_save()
    
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
    
        self.ui.save()
        
        self.ui.entrygrid.widgets[1][3].sv.set('COBY')
    
        self.ui.save()
        
        self.ui.entrygrid.widgets[2][2].sv.set('LUCY')
    
        self.ui.save()


        
        self.ui.persist()
        
    '''def test_update_queue(self):
        
        expected_results = [[('Stan,Galina',2),('Samantha',1),'',('Galina',1),('Amelia',1),'','',('Paraic',1),'','','',''],
                            ['','','','','',('Samantha',1),'','',('Stan',1),('Paraic',1),('Amelia',1),('Galina',1)]]
        
        expected_colors = [['red','lightgreen','','lightgreen','lightgreen','','','lightgreen','','','',''],
                            ['','','','','','lightgreen','','','lightgreen','lightgreen','lightgreen','lightgreen']]

        
        values,bgcolor = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_results,values)
        self.assertListEqual(expected_colors,bgcolor)'''
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 0], 
                           [u'8:30-9:10', u'ORIG', u'Galina', u'Tuesday', 0], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 0], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 0], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 0], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 0], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 0], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 0], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 0], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 0], 
                           [u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 1], 
                           [u'8:30-9:10', u'NATHANIEL', u'Galina', u'Tuesday', 1], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 1], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 1], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 1], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 1], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 1], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 1], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 1], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 1]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
        
    def test_entrygrid_contents(self):
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                           ['8:30-9:10', 'NATHANIEL', 'NATHANIEL', 'COBY', 'COBY', 'YOSEF'],
                           ['9:11-9:51', 'LUCY', 'LUCY', 'BOOKER', 'ASHER', 'JAKE']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)        
        
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', u'Stan,Galina', u'Samantha,Amelia', u'Galina', u'Amelia', u'Paraic'], 
                            ['9:11-9:51', u'Samantha', u'Stan', u'Paraic', u'Amelia', u'Galina,Samantha'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)  
        
class Test_Load_Save_Change_Save_Single_Value(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        self.ui.load_save()
    
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
    
        self.ui.save()
        
        self.ui.persist()
        
    '''def test_update_queue(self):
        
        expected_results = [[('Stan,Galina',2),('Samantha',1),'',('Galina',1),('Amelia',1),'','',('Paraic',1),'','','',''],
                            ['','','','','',('Samantha',1),'','',('Stan',1),('Paraic',1),('Amelia',1),('Galina',1)]]
        
        expected_colors = [['red','lightgreen','','lightgreen','lightgreen','','','lightgreen','','','',''],
                            ['','','','','','lightgreen','','','lightgreen','lightgreen','lightgreen','lightgreen']]

        
        values,bgcolor = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_results,values)
        self.assertListEqual(expected_colors,bgcolor)'''
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 0], 
                           [u'8:30-9:10', u'ORIG', u'Galina', u'Tuesday', 0], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 0], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 0], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 0], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 0], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 0], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 0], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 0], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 0], 
                           [u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 1], 
                           [u'8:30-9:10', u'NATHANIEL', u'Galina', u'Tuesday', 1], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 1], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 1], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 1], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 1], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 1], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 1], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 1], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 1]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
        
    def test_entrygrid_contents(self):
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                           ['8:30-9:10', 'NATHANIEL', 'NATHANIEL', 'TRISTAN', 'COBY', 'YOSEF'],
                           ['9:11-9:51', 'LUCY', 'DONOVAN', 'BOOKER', 'ASHER', 'JAKE']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)        
        
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', u'Stan,Galina', u'Samantha', u'Galina', u'Amelia', u'Paraic'], 
                            ['9:11-9:51', u'Samantha', u'Stan', u'Paraic', u'Amelia', u'Galina'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)  
        
class Test_Load_Save_Change_Save_New_Row(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        self.ui.load_save()
    
        self.ui.entrygrid.widgets[3][0].sv.set('9:52-10:32')
        self.ui.entrygrid.widgets[3][1].sv.set('NICK')
        self.ui.entrygrid.widgets[3][2].sv.set('DONOVAN')
        self.ui.entrygrid.widgets[3][3].sv.set('ASHER')
        self.ui.entrygrid.widgets[3][4].sv.set('JAKE')
        self.ui.entrygrid.widgets[3][5].sv.set('YOSEF')
    
        self.ui.save()
        
        self.ui.persist()
        
    '''def test_update_queue(self):
        
        expected_results = [[('Stan,Galina',2),('Samantha',1),'',('Galina',1),('Amelia',1),'','',('Paraic',1),'','','',''],
                            ['','','','','',('Samantha',1),'','',('Stan',1),('Paraic',1),('Amelia',1),('Galina',1)]]
        
        expected_colors = [['red','lightgreen','','lightgreen','lightgreen','','','lightgreen','','','',''],
                            ['','','','','','lightgreen','','','lightgreen','lightgreen','lightgreen','lightgreen']]

        
        values,bgcolor = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_results,values)
        self.assertListEqual(expected_colors,bgcolor)'''
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 0], 
                           [u'8:30-9:10', u'ORIG', u'Galina', u'Tuesday', 0], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 0], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 0], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 0], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 0], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 0], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 0], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 0], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 0], 
                           [u'8:30-9:10', u'NATHANIEL', u'Stan', u'Tuesday', 1], 
                           [u'8:30-9:10', u'ORIG', u'Galina', u'Tuesday', 1], 
                           [u'8:30-9:10', u'TRISTAN', u'Samantha', u'Tuesday', 1], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 1], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 1], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 1], 
                           [u'9:11-9:51', u'DONOVAN', u'Galina', u'Tuesday', 1], 
                           [u'9:11-9:51', u'BOOKER', u'Samantha', u'Tuesday', 1], 
                           [u'9:11-9:51', u'ASHER', u'Amelia', u'Tuesday', 1], 
                           [u'9:11-9:51', u'JAKE', u'Paraic', u'Tuesday', 1],
                           [u'9:52-10:32', u'NICK', u'Stan', u'Tuesday', 1], 
                           [u'9:52-10:32', u'DONOVAN', u'Galina', u'Tuesday', 1], 
                           [u'9:52-10:32', u'ASHER', u'Samantha', u'Tuesday', 1], 
                           [u'9:52-10:32', u'JAKE', u'Amelia', u'Tuesday', 1], 
                           [u'9:52-10:32', u'YOSEF', u'Paraic', u'Tuesday', 1]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
    def test_grid_contents(self):
        self.ui.load(0)
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                           ['8:30-9:10', 'NATHANIEL', 'ORIG', 'TRISTAN', 'COBY', 'YOSEF'],
                           ['9:11-9:51', 'LUCY', 'DONOVAN', 'BOOKER', 'ASHER', 'JAKE'],
                           ['9:52-10:32', 'NICK', 'DONOVAN', 'ASHER', 'JAKE', 'YOSEF']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)            
        
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', u'Stan', u'Samantha', u'Galina', u'Amelia', u'Paraic'], 
                            ['9:11-9:51', u'Samantha', u'Stan', u'Paraic', u'Amelia', u'Galina'], 
                            ['9:52-10:32', 'Paraic', 'Amelia', 'Samantha', 'Galina', 'Stan'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
        
    
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)       
        

        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Focus))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Update_Combobox))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save))        
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Change_Save_Single_Value))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save_Change_Save_Single_Value))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save_Change_Save_New_Row))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save_Change_Save_Change_Save_Single_Value))

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Input_New_Save_Persist))
    
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Input_New_Save_Change_Save_Persist))
    
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


