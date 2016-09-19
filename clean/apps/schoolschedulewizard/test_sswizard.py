import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")

from Tkinter import *
from ttk import *

import unittest

from sswizard import schoolschedgeneric, WizardUI
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory

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
        self.widget.sv.insert(0,'n')
        self.widget.sv.insert(1,'a')

        self.assertEqual(self.widget.sv.get(),'NATHANIEL')

        self.assertEqual(self.widget['style'],'InFocus.Valid.TCombobox')
        
    def tearDown(self):
        self.ui.destroy()
        
class Test_Base(unittest.TestCase):
    def setUp(self,dbname):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = dbname
        self.dbfilename = path.join(dbpath,self.dbname)
        self.database = Database(self.dbfilename)
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.dbname, self.of)       
        self.ui.dbname_entry_sv.set(dbname)
        
    def tearDown(self):
        self.ui.destroy()
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        
class Test_Input_New_Save_Persist(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'tmp')
           
        self.ui.dbname_entry_sv.set(self.dbname)
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30')
        self.ui.entrygrid.widgets[0][1].sv.set('A')
        self.ui.entrygrid.widgets[1][1].sv.set('BR.AC.ST')
        
        self.ui.save()
        self.ui.persist()
    
    '''def test_balancegrid_contents(self):
        
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
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)    '''
        
    def test_dbwrite(self):
        
        expected_result = [[u'8:30-9:10', u'NATHANIEL', u'BR.AC.ST', u'Tuesday', 0]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
        
        
    '''def test_grid_contents(self):
        
        expected_results =[['Stan'],
                        ['8:30-9:10', 'NATHANIEL']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)'''

    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")

class Test_Input_New_Save_Change_Save_Persist(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,'tmp')
        
        self.ui.dbname_entry_sv.set(self.dbname)
        
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

    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")
        
class Test_Input_New_Save_Change_Save_Persist_Overbook_Teacher_Period(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,'tmp')
        
        self.ui.dbname_entry_sv.set(self.dbname)
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30-9:10')
        self.ui.entrygrid.widgets[0][1].sv.set('Stan')
        self.ui.entrygrid.widgets[1][1].sv.set('NATHANIEL')
        
        self.ui.save()
        self.ui.entrygrid.widgets[0][2].sv.set('Galina')
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
        self.ui.save()
        self.ui.persist()
    
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', 'Stan,Galina'], 
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
                           [u'8:30-9:10', u'NATHANIEL', u'Galina', u'Tuesday', 0]]
        
        cols = ['period','student','teacher','dow','saveversion']  
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)        
        
    def test_grid_contents(self):
        
        expected_results =[['Stan','Galina'],
                           ['8:30-9:10', 'NATHANIEL','NATHANIEL']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
 
    def test_grid_color(self):
        self.assertEqual(self.ui.balancegrid.widgets[1][1].cget('background'),'red')

    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")

class Test_Fill_Student(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'tmp')
        
        self.ui.dbname_entry_sv.set(self.dbname)
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30-9:10')
        self.ui.entrygrid.widgets[2][0].sv.set('9:11-9:51')
        self.ui.entrygrid.widgets[3][0].sv.set('9:52-10:32')
        self.ui.entrygrid.widgets[4][0].sv.set('10:33-11:13')
        self.ui.entrygrid.widgets[5][0].sv.set('11:13-11:45')
        self.ui.entrygrid.widgets[6][0].sv.set('11:45-12:25')
        self.ui.entrygrid.widgets[7][0].sv.set('12:26-1:06')
        self.ui.entrygrid.widgets[8][0].sv.set('1:07-1:47')
        self.ui.entrygrid.widgets[9][0].sv.set('1:48-2:28')
        self.ui.entrygrid.widgets[10][0].sv.set('2:30-3:00')        

        self.ui.entrygrid.widgets[0][1].sv.set('Stan')
        self.ui.entrygrid.widgets[1][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[2][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[3][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[4][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[5][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[6][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[7][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[8][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[9][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[10][1].sv.set('NATHANIEL')

        self.ui.save()
        self.ui.persist()
        
        
    def test_background(self):
        self.assertEqual('green',
                         self.ui.balancegrid.widgets[0][1].cget('background'))
        
    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")
    
class Test_Fill_Student_Unfill(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'tmp')
        
        self.ui.dbname_entry_sv.set(self.dbname)
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30-9:10')
        self.ui.entrygrid.widgets[2][0].sv.set('9:11-9:51')
        self.ui.entrygrid.widgets[3][0].sv.set('9:52-10:32')
        self.ui.entrygrid.widgets[4][0].sv.set('10:33-11:13')
        self.ui.entrygrid.widgets[5][0].sv.set('11:13-11:45')
        self.ui.entrygrid.widgets[6][0].sv.set('11:45-12:25')
        self.ui.entrygrid.widgets[7][0].sv.set('12:26-1:06')
        self.ui.entrygrid.widgets[8][0].sv.set('1:07-1:47')
        self.ui.entrygrid.widgets[9][0].sv.set('1:48-2:28')
        self.ui.entrygrid.widgets[10][0].sv.set('2:30-3:00')        

        self.ui.entrygrid.widgets[0][1].sv.set('Stan')
        self.ui.entrygrid.widgets[1][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[2][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[3][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[4][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[5][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[6][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[7][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[8][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[9][1].sv.set('NATHANIEL')
        self.ui.entrygrid.widgets[10][1].sv.set('NATHANIEL')

        self.ui.save()
        
        self.ui.entrygrid.widgets[2][1].sv.set('COBY')
  
        self.ui.persist()
        
        
    def test_background(self):
        self.assertEqual('white',
                         self.ui.balancegrid.widgets[0][1].cget('background'))
        
    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")

    
class Test_Fix_Overbooking(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'tmp')
        
        self.ui.dbname_entry_sv.set(self.dbname)
        
        self.ui.dbname_entry_sv.set(self.dbname)
        
        self.ui.entrygrid.widgets[1][0].sv.set('8:30-9:10')
        self.ui.entrygrid.widgets[0][1].sv.set('Stan')
        self.ui.entrygrid.widgets[1][1].sv.set('NATHANIEL')
        
        self.ui.save()
        self.ui.entrygrid.widgets[0][2].sv.set('Galina')
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
        self.ui.save()
        self.ui.entrygrid.widgets[1][2].sv.set('TRISTAN')
        self.ui.save()
        self.ui.persist()
    
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', 'Stan','Galina'], 
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
                           [u'8:30-9:10', u'TRISTAN', u'Galina', u'Tuesday', 0]]
        
        cols = ['period','student','teacher','dow','saveversion']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)        
        
    def test_grid_contents(self):
        
        expected_results =[['Stan','Galina'],
                           ['8:30-9:10', 'NATHANIEL','TRISTAN']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
 
    def test_grid_color(self):
        
        self.assertEqual(self.ui.balancegrid.widgets[1][1].cget('background'),'lightgreen')
        
    def tearDown(self):
        self.ui.destroy()
        os.remove(self.dbname+".sqlite")
             
class Test_Load(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,'test_sswizard')
        
    def test_grid_contents(self):
        self.ui.load()
        
        expected_results =[['A','B'],
                           ['830', 'TH.AC.ST', 'DA.AC.HU']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)

class Test_Load_Save(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,'test_sswizard')

        self.ui.load_save()
        
    def test_objectrepr_type(self):
        expected_results = ['lesson','schedule','dow','subject','lessontype','objtype','session',
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

    def test_objectrepr_lesson_attr(self):
             
        
        results = self.of.query('lesson')
        
        lesson_obj = results[0]
        objid = getattr(lesson_obj,'objid')

        self.assertEquals(objid,getattr(lesson_obj,'userobjid'))
        self.assertEquals('lesson',getattr(lesson_obj,'objtype'))
        self.assertEquals('Tuesday',getattr(lesson_obj,'dow'))
        self.assertEquals(2,getattr(lesson_obj,'subject'))
        self.assertEquals(0,getattr(lesson_obj,'lessontype'))
        self.assertEquals(3,getattr(lesson_obj,'teacher'))
        self.assertEqual('ObjFactory', getattr(lesson_obj,'of').__class__.__name__)
     
    def test_objectrepr_num_lesson(self):
        # test that the objects created have the correct member attr and attrvals
        results = self.of.query('lesson')
        self.assertEqual(len(results),2)
        
    def test_objectrepr_num_teacher(self):
        # test that the objects created have the correct member attr and attrvals
        results = self.of.query('teacher')
        self.assertEqual(len(results),2)
        
    def test_objectrepr_num_student(self):
        # test that the objects created have the correct member attr and attrvals
        
        results = self.of.query('student')
        self.assertEqual(len(results),2)
        
    def test_grid_contents(self):
        
        expected_results =[['A','B'],
                           ['830', 'TH.AC.ST', 'DA.AC.HU']]
        
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)
        
class Test_Load_Change_Save_Single_Value(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'test_sswizard')
        
        self.ui.load()
    
        self.ui.entrygrid.widgets[1][1].sv.set('DA.AC.HU')
    
        self.ui.save()
        
        self.ui.persist()
        
    def test_dbwrite(self):
        
        expected_result = [[830, u'A', 'DA.AC.HU', u'Tuesday', 1], 
                           [830, u'B', 'DA.AC.HU', u'Tuesday', 1]]
        
        cols = ['period','student','session','dow','saveversion']
        
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols,['saveversion','1'])

        self.assertListEqual(expected_result,rows)
        
        
    '''def test_entrygrid_contents(self):
        
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
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)'''
        
class Test_Load_Save_Change_Save_Change_Save_Single_Value(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'test_sswizard')
        
        self.ui.load_save()
    
        self.ui.entrygrid.widgets[1][1].sv.set('JA.CO.MV')
    
        self.ui.save()
        
        self.ui.entrygrid.widgets[1][2].sv.set('JE.AC.HU')
    
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
        
        expected_result = [[830, u'A', 'JA.CO.MV', u'Tuesday', 1], 
                           [830, u'B', 'JE.AC.HU', u'Tuesday', 1]]

     
        
        cols = ['period','student','session','dow','saveversion']
    
        with self.database:
                colndefn,rows = tbl_rows_get(self.database,'lesson',cols,['saveversion','1'])
    
        self.assertListEqual(expected_result,rows)


        
    '''def test_entrygrid_contents(self):
        
        expected_results =[['Stan', 'Galina', 'Samantha', 'Amelia', 'Paraic'],
                           ['8:30-9:10', 'NATHANIEL', 'NATHANIEL', 'COBY', 'COBY', 'YOSEF'],
                           ['9:11-9:51', 'LUCY', 'LUCY', 'BOOKER', 'ASHER', 'JAKE']]
                
        self.assertListEqual(self.ui.entrygrid.dump_grid(), expected_results)        
        
    def test_balancegrid_contents(self):
        
        expected_results = [['2:30-3:00', 'NATHANIEL', 'TRISTAN', 'SIMON A.', 'ORIG', 'COBY', 'BOOKER', 'ASHLEY', 'YOSEF', 'LUCY', 'JAKE', 'ASHER', 'DONOVAN', 'LIAM', 'SIMON B', 'NICK'], 
                            ['8:30-9:10', u'Stan,Galina','Samantha,Amelia','Paraic'], 
                            ['9:11-9:51', u'Samantha', u'Stan,Galina', u'Paraic', u'Amelia'], 
                            ['9:52-10:32'], 
                            ['10:33-11:13'], 
                            ['11:13-11:45'], 
                            ['11:45-12:25'], 
                            ['12:26-1:06'], 
                            ['1:07-1:47'], 
                            ['1:48-2:28'], 
                            ['2:30-3:00']]
                
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)  '''
        
class Test_Load_Save_Change_Save_Single_Value(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self,'test_10rows')
        
        self.ui.load_save()
    
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
    
        self.ui.save()
        
        self.ui.persist()
        
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
                           [u'8:30-9:10', u'COBY', u'Samantha', u'Tuesday', 1], 
                           [u'8:30-9:10', u'COBY', u'Amelia', u'Tuesday', 1], 
                           [u'8:30-9:10', u'YOSEF', u'Paraic', u'Tuesday', 1], 
                           [u'9:11-9:51', u'LUCY', u'Stan', u'Tuesday', 1], 
                           [u'9:11-9:51', u'LUCY', u'Galina', u'Tuesday', 1], 
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
                            ['8:30-9:10', u'Stan,Galina', u'Samantha', u'Amelia', u'Paraic'], 
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
        Test_Base.setUp(self,'test_sswizard')
        
        self.ui.load_save()
    
        self.ui.entrygrid.widgets[3][0].sv.set('911')
        self.ui.entrygrid.widgets[3][1].sv.set('DA.AC.HU')
        self.ui.entrygrid.widgets[3][2].sv.set('DA.AC.HU')
    
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
        
        expected_result = [[830, u'A',  'TH.AC.ST', u'Tuesday', 1], 
                           [830, u'B', 'DA.AC.HU', u'Tuesday', 1],

                           [911, u'A', 'DA.AC.HU', u'Tuesday', 1], 
                           [911, u'B', 'DA.AC.HU', u'Tuesday', 1]]
        
        cols = ['period','student','session','dow','saveversion']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols,['saveversion','1'])
        
        self.assertListEqual(expected_result,rows)
        
    '''def test_grid_contents(self):
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
        
    
        self.assertListEqual(self.ui.balancegrid.dump_grid(), expected_results)      ''' 
        

        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Focus))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Update_Combobox))
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Input_New_Save_Persist))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save))   
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Change_Save_Single_Value))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save_Change_Save_New_Row))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save_Change_Save_Change_Save_Single_Value))

        
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Save_Change_Save_Single_Value))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Fill_Student))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Fill_Student_Unfill))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Input_New_Save_Change_Save_Persist))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Input_New_Save_Change_Save_Persist_Overbook_Teacher_Period))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Fix_Overbooking))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


