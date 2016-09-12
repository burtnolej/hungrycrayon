import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")

from Tkinter import *
from ttk import *

import unittest

from dbtableviewer import DBTableUI
from database_util import Database
from database_table_util import tbl_rows_get
from misc_utils_objectfactory import ObjFactory
from misc_utils import Log

from shutil import copyfile
from os import remove, path

class Test_Grid_Behaviour_Focus(unittest.TestCase):
    def setUp(self):
        
        self.ui = DBTableUI()
        
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
        
class Test_Grid_Behaviour_Update_Entry(unittest.TestCase):
    def setUp(self):
        
        self.ui = DBTableUI()
        
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

        self.assertEqual(self.widget['style'],'InFocus.Changed.TEntry')
        
    def tearDown(self):
        self.ui.destroy()
        
class Test_Load_From_Database(unittest.TestCase):

    def setUp(self):
        
        self.ui = DBTableUI()
        
        self.ui.dbname_entry_sv.set('test')
        
        
    def test_from_db_to_grid(self):
        
        expected_results = [['dow', 'lessontype', 'objtype', 'period', 'saveversion', 'schedule', 'student', 'subject', 'teacher', 'userobjid', '__timestamp', '__id'],
                            ['Tuesday','wp','lesson','8:30-9:10','0','1','NATHANIEL','MATH','Stan','1,1,1','19:43:00','04C3B4EF'],
                            ['Tuesday','wp','lesson','8:30-9:10','0','1','ORIG','MATH','Galina','1,4,2','19:43:01','009AB6A8'],
                            ['Tuesday','wp','lesson','8:30-9:10','0','1','TRISTAN','MATH','Samantha','1,2,3','19:43:01','0500B49E'],
                            ['Tuesday','wp','lesson','8:30-9:10','0','1','COBY','MATH','Amelia','1,5,4','19:43:01','049C2F17'],
                            ['Tuesday','wp','lesson','8:30-9:10','0','1','YOSEF','MATH','Paraic','1,8,5','19:43:01','00DC72C2'],
                            ['Tuesday','wp','lesson','9:11-9:51','0','1','LUCY','MATH','Stan','2,9,1','19:43:01','03E6EDFD'],
                            ['Tuesday','wp','lesson','9:11-9:51','0','1','DONOVAN','MATH','Galina','2,12,2','19:43:01','00CF3412'],
                            ['Tuesday','wp','lesson','9:11-9:51','0','1','BOOKER','MATH','Samantha','2,6,3','19:43:01','01600099'],
                            ['Tuesday','wp','lesson','9:11-9:51','0','1','ASHER','MATH','Amelia','2,11,4','19:43:01','040E9236'],
                            ['Tuesday','wp','lesson','9:11-9:51','0','1','JAKE','MATH','Paraic','2,10,5','19:43:01','03537F99']]

        self.ui.load()
        
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertListEqual(values, expected_results)
        
    '''def test_create_all_object_types_after_save(self):
        # test just that of has created an index for each type of object expected #
        expected_results = ['lesson','schedule','dow','subject','lessontype','objtype',
                            'userobjid','period','student','saveversion','teacher']
        
        expected_results.sort()
        
        self.ui.load_save(0)
        
        results = self.of.query()
        results.sort()

        self.assertListEqual(results, expected_results)
        
    def test_student_object_after_save(self):
        # test that objects of type student are being created
        
        self.ui.load_save(0)
        
        results = self.of.query('student')
        
        for obj in results:
            self.assertEqual(obj.__class__.__name__,'student')
            
    def test_student_object_attr_after_save(self):
        # test that the objects created have the correct member attr and attrvals
        
        self.ui.load_save(0)
        
        results = self.of.query('student')
        
        student_obj = results[0]
        name = getattr(student_obj,'name')
        
        self.assertEquals(name,getattr(student_obj,'objid'))
        self.assertEquals(name,getattr(student_obj,'userobjid'))
        self.assertEquals('student',getattr(student_obj,'objtype'))
        
        self.assertEqual('ObjFactory', getattr(student_obj,'of').__class__.__name__)
        self.assertEqual('Log', getattr(student_obj,'log').__class__.__name__)\
            
    def test_lesson_object_attr_after_save(self):
        # test that the objects created have the correct member attr and attrvals
        
        self.ui.load_save(0)
        
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
        
    def test_num_lesson_objects_save(self):
        # test that the objects created have the correct member attr and attrvals
        self.ui.load_save(0)
        results = self.of.query('lesson')
        self.assertEqual(len(results),10)
        
    def test_num_teacher_objects_save(self):
        # test that the objects created have the correct member attr and attrvals
        self.ui.load_save(0)
        results = self.of.query('teacher')
        self.assertEqual(len(results),5)
        
    def test_num_student_objects_save(self):
        # test that the objects created have the correct member attr and attrvals
        self.ui.load_save(0)
        results = self.of.query('student')
        self.assertEqual(len(results),10)
        
    def test_balancegrid_after_save(self):
        #self.master.mainloop()
        #[['NATHANIEL','TRISTAN','SIMON A.','ORIG','COBY','BOOKER','ASHLEY','YOSEF','LUCY','JAKE','ASHER','DONOVAN','LIAM','SIMON B','NICK'],
        
        expected_results = [['Stan','Samantha','','Galina','Amelia','','','Paraic','','','',''],
                            ['','','','','','Samantha','','','Stan','Paraic','Amelia','Galina']]
        
        self.ui.load_save(0)
    
        values,_ = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_results,values)
        
    def test_balancegrid_after_save_overload_Nathaniel(self):
        
        expected_values = [['Stan,Galina','Samantha','','Galina','Amelia','','','Paraic','','','',''],
                            ['','','','','','Samantha','','','Stan','Paraic','Amelia','Galina']]
        
        expected_colors = [['red','lightgreen','','lightgreen','lightgreen','','','lightgreen','','','',''],
                            ['','','','','','lightgreen','','','lightgreen','lightgreen','lightgreen','lightgreen']]
        
        self.ui.load_save(0)
        
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
        
        self.ui.save()
        
        values,bgcolor = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_values,values)
        self.assertListEqual(expected_colors,bgcolor)
        
    def test_balancegrid_after_save_add_newrow_952_save(self):
        # test that changes made are written to in memory objects correctly
        # test that a new row (period) can be created

        
        #[['NATHANIEL','TRISTAN','SIMON A.','ORIG','COBY','BOOKER','ASHLEY','YOSEF','LUCY','JAKE','ASHER','DONOVAN','LIAM','SIMON B','NICK'],

        expected_values = [['Stan','Samantha','','Galina','Amelia','','','Paraic','','','','','','',''],
                        ['','','','','','Samantha','','','Stan','Paraic','Amelia','Galina','','',''],
                        ['','','','','','','','Paraic','','Amelia','Samantha','Galina','','','Stan']]
        
        expected_colors = [['lightgreen','lightgreen','','lightgreen','lightgreen','','','lightgreen','','','','','','',''],
                           ['','','','','','lightgreen','','','lightgreen','lightgreen','lightgreen','lightgreen','','',''],
                           ['','','','','','','','lightgreen','','lightgreen','lightgreen','lightgreen','','','lightgreen']]
        
        self.ui.load_save(0)
        
        self.ui.entrygrid.widgets[3][0].sv.set('9:52-10:32')
        self.ui.entrygrid.widgets[3][1].sv.set('NICK')
        self.ui.entrygrid.widgets[3][2].sv.set('DONOVAN')
        self.ui.entrygrid.widgets[3][3].sv.set('ASHER')
        self.ui.entrygrid.widgets[3][4].sv.set('JAKE')
        self.ui.entrygrid.widgets[3][5].sv.set('YOSEF')
        
        self.ui.save()
        
        values,bgcolor = self.ui.updates_get('balancegrid',ignoreaxes=True)
        
        self.assertListEqual(expected_values,values)
        self.assertListEqual(expected_colors,bgcolor)

        results = self.of.query('lesson')
        self.assertEqual(len(results),15)
        
        self.assertEquals(self.of.object_get('lesson','3,15,1').student,'NICK')
        self.assertEquals(self.of.object_get('lesson','3,12,2').student,'DONOVAN')
        self.assertEquals(self.of.object_get('lesson','3,8,5').student,'YOSEF')'''
        
    def tearDown(self):
        self.ui.destroy()
        
'''class Test_Load_Change_Save_Load(unittest.TestCase):
    
    def setUp(self):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        dbname = path.join(dbpath,'test')
        self.tmpdbname = path.join(dbpath,'test_tmp')
        copyfile(dbname+".sqlite",self.tmpdbname+".sqlite")
    
        self.database = Database(self.tmpdbname)
        self.of = ObjFactory(True)
        self.ui = WizardUI(self.database, self.of)
        
        
    def test_(self):
        self.ui.load_save(0)
        self.ui.entrygrid.widgets[1][2].sv.set('NATHANIEL')
        self.ui.save("1")
        self.ui.persist()
        
        cols = ['period','student','teacher','dow']
        
        expected_results =[['8:30-9:10', 'NATHANIEL','Stan','Tuesday'],
                           ['8:30-9:10', 'NATHANIEL','Galina','Tuesday'],
                           ['8:30-9:10', 'TRISTAN','Samantha','Tuesday'],
                           ['8:30-9:10', 'COBY','Amelia','Tuesday'],
                           ['8:30-9:10', 'YOSEF','Paraic','Tuesday'],
                           ['9:11-9:51', 'LUCY','Stan','Tuesday'],
                           ['9:11-9:51', 'DONOVAN','Galina','Tuesday'],
                           ['9:11-9:51', 'BOOKER','Samantha','Tuesday'],
                           ['9:11-9:51', 'ASHER','Amelia','Tuesday'],
                           ['9:11-9:51', 'JAKE','Paraic','Tuesday']]    

        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols,
                                         ('saveversion',"1"))
            
        self.assertListEqual(expected_results,rows)

    def tearDown(self):
        os.remove(self.tmpdbname+".sqlite")
        self.ui.destroy()'''
     
if __name__ == "__main__":
    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Focus))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Update_Entry))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_From_Database))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Change_Save_Load))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


