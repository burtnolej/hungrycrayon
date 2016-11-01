import sys
import os
from os import path as ospath

from ssloader import SSLoader, SSLoaderRuleException, SSLoaderRecordEndException, SSLoaderNoMatchException, \
     SSLoaderNoRulesMatchException   

from database_table_util import tbl_rows_get, tbl_query
from database_util import Database, tbl_remove, tbl_exists
from sswizard_query_utils import _pivotexecfunc, _rowcount
from sswizard_utils import dbbulkloader, _isenum, dbinsert_direct


from Tkinter import *
from ttk import *
from shutil import copyfile

from collections import OrderedDict

import unittest

class Test_Base(unittest.TestCase):
    def setUp(self,prep=5):
        self.databasename = "test_ssloader"
        self.ssloader = SSLoader(self.databasename,prep)    
    
class Test_String2Records(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_single_dollar(self):
        
        records = self.ssloader.string2records("foo^foo")
        
        self.assertListEqual(records,['foo','^','foo'])
        
    def test_spreadsheet_multi_newline(self):
        
        records = self.ssloader.string2records("foo&&&&&bar")
        
        self.assertListEqual(records,['foo','bar'])
        
    def test_spreadsheet_cell_delim(self):
        
        records = self.ssloader.string2records("foo&foo^bar")
        
        self.assertListEqual(records,['foo','foo','^','bar'])
        
    def test_spreadsheet_newline_before_cell_delim(self):
        
        records = self.ssloader.string2records("foo&foo&&&^bar")
        
        self.assertListEqual(records,['foo','foo','^','bar'])
        
    def test_spreadsheet_cell_delim(self):
        
        records = self.ssloader.string2records("foo&foo&foo&foo^bar")
        
        self.assertListEqual(records,['foo','foo','foo','foo','^','bar'])
        
    def test_with_concat(self):
        
        records = self.ssloader.string2records("foobar with&blahblah")
        
        self.assertListEqual(records,['foobar with blahblah'])
        
    def test_with_concat_space(self):
        
        records = self.ssloader.string2records("foobar with &blahblah")
        
        self.assertListEqual(records,['foobar with blahblah'])
        
    
class Test_String2Records_Prep41Period(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        fileasstring = self.ssloader.file2string("prep5data_test1period.csv")
        self.records = self.ssloader.string2records(fileasstring)
        
        self.expected_results = ['09/19/16','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday',
                                 '8:30- 9:10','PERIOD 1',
                                 '^','ELA: Nathaniel (Amelia)','Math: CLayton, (Stan)','Engineering: Orig, Stephen, Oscar (Paraic)','Work Period: Peter, Jack, Jake','Movement: Bruno','^',
                                 'Math: Nathaniel (Stan)','Counseling: Clayton','Student News: Bruno, Orig, Oscar','Counseling: Stephen (Alexa)','Work Period: Peter, Jack','Science: Jake (Paraic)','^',
                                 'ELA: Nathaniel (Amelia)','Math: Clayton (Stan)','Engineering: Orig, Stephen, Oscar (Paraic)','Work Period: Peter, Jack, Jake','^',
                                 'Math: Nathaniel (Stan)','Movement: Clayton','Student News: Orig, Oscar, Stephen','Work Period: Peter, Jack','Science: Jake (Paraic)','Core: Bruno','^',
                                 'Humanities: Orig, Jake, Nathaniel, Stephen (A)','Music: Coby, THomas, Yosef(D)','STEM: Tris, Ashley, Simon, Booker, Omer (C)','ART: Clayton, Bruno, Oscar, Peter, Jack (B)']


    def test_(self):
        
        # 5 = 1 x '^' per data cell
        # 11 for the header
        # 2 for period field
        # 25 data rows
        
        self.assertListEqual(self.expected_results,self.records)            
        self.assertEqual(len(self.records),43)
        
class Test_String2Records_Prep4100(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        fileasstring = self.ssloader.file2string("prep5data_test100.csv")
        self.records = self.ssloader.string2records(fileasstring)
        
    def test_num_records(self):
        
        # 20 = 1 x '^' per data cell
        # 11 for the header
        # 8 for period field
        # 111 data rows
        
        self.assertEqual(len(self.records),150)


class Test_String2Records_Prep4ComputerTime(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        fileasstring = self.ssloader.file2string("prep5data_testcomputertime.csv")
        self.records = self.ssloader.string2records(fileasstring)
        
    def test_num_records(self):
        
        # 10 = 1 x '^' per data cell
        # 11 for the header
        # 2 = 1 x for period field
        # 15 data rows
        
        # theres computer time missing on Friday
        self.assertEqual(len(self.records),37)
        
        
class Test_ApplyRules(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_teachertype(self):
        self.rules = [(":",1),("\(",1),("\)",1)]
        self.inputstr = "ELA: Nathaniel (Amelia)"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_teachertype_multi_student(self):
        self.rules = [(":",1),("\(",1),("\)",1)]
        self.inputstr = "Science: Oscar, Peter (Paraic)"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_datetype(self):
        self.rules = [("/",2)]
        self.inputstr = "09/19/16"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_periodtype(self):  
        self.rules = [(":",2),("-",1)]
        self.inputstr = "\"8:30- 9:10"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_noteachertype(self):
        self.rules = [(":",1),("\(",0),("\)",0)]
        self.inputstr = "ELA: Nathaniel"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_staff(self):
        self.rules = [("\+",2)]
        self.inputstr = "Moira++"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
        
class Test_ApplyRules_Fails(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_colon(self):
        
        self.inputstr = "ELA Nathaniel (Amelia)"
        self.rules = [(":",1),("\(",1),("\)",1)]
    
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
            
    def test_more_than_one_colon(self):
        
        self.inputstr = "ELA :Nathaniel : (Amelia)"
        self.rules = [(":",1),("\(",1),("\)",1)]
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
            
    def test_no_open_bracket(self):
        
        self.inputstr = "ELA :Nathaniel : Amelia)"
        self.rules = [(":",1),("\(",1),("\)",1)]
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_no_close_bracket(self):
        
        self.inputstr = "ELA :Nathaniel : (Amelia"
        self.rules = [(":",1),("\(",1),("\)",1)]
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
    
class Test_teachertype_1student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "ELA: Nathaniel (Amelia)"

    def test_subject(self):
    
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"ELA")
        
    def test_subject_abbrev(self):
        # teacher already removed
        self.inputstr = "ELA: Nathaniel"
        
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"ELA")
        
    def test_teacher(self):
    
        teacher,_ = self.ssloader.extract_teacher(self.inputstr)
        
        self.assertEqual(teacher,"Amelia")
        
    def test_teacher_abbrev(self):
        # subject already removed
        self.inputstr = "Nathaniel (Amelia)"
    
        teacher,_ = self.ssloader.extract_teacher(self.inputstr)
        
        self.assertEqual(teacher,"Amelia")   

    def test_students(self):
        
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
        teacher,_rest = self.ssloader.extract_teacher(_rest)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,['Nathaniel'])
        
class Test_teachertype_edgecasestudent(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "Science: Oscar, Peter, (Paraic)"

    def test_subject(self):
    
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
        teacher,_rest = self.ssloader.extract_teacher(_rest)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,["Oscar","Peter"])
        
class Test_teachertype_edgecase_quotes(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "Science: Jake (Paraic) \""

    def test_subject(self):
    
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
        teacher,_rest = self.ssloader.extract_teacher(_rest)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,["Jake"])     
        
    def test_teacher(self):
    
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
        teacher,_rest = self.ssloader.extract_teacher(_rest)
        
        self.assertListEqual(teacher,Paraic)  
        
class Test_teachertype_multi_student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "Science: Oscar, Peter (Paraic)"

    def test_subject(self):
    
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"Science")
        
    def test_subject_abbrev(self):
        # teacher already removed
        self.inputstr = "Science: Oscar, Peter"
        
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"Science")
        
    def test_teacher(self):
    
        teacher,_ = self.ssloader.extract_teacher(self.inputstr)
        
        self.assertEqual(teacher,"Paraic")
        
    def test_teacher_abbrev(self):
        # subject already removed
        self.inputstr =  "Oscar, Peter (Paraic)"
    
        teacher,_ = self.ssloader.extract_teacher(self.inputstr)
        
        self.assertEqual(teacher,"Paraic")   

    def test_students(self):
        
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
        teacher,_rest = self.ssloader.extract_teacher(_rest)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,["Oscar","Peter"])

class Test_periodtype(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "8:30 \n-9:10"
        
    def test_(self):
        
        period = self.ssloader.extract_period(self.inputstr)
        self.assertEqual(period,"830-910")

class Test_extract_staff(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "Moira++"

    def test_subject(self):
    
        subject = self.ssloader.extract_staff(self.inputstr)
        
        self.assertEqual(subject,"Moira")
        
    def test_student(self):
    
        subject = self.ssloader.extract_staff("Moira**")
        
        self.assertEqual(subject,"Moira")
        
class Test_nonacademic_1_student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "History: Oscar"

    def test_subject(self):
    
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"History")

    def test_students(self):
        
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,['Oscar'])
        
class Test_nonacademic_multi_student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.inputstr = "Student News: Peter, Jack "

    def test_subject(self):
    
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"Student News")

    def test_students(self):
        
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,['Peter','Jack'])
        
class Test_extractteacher_Fails(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.rules = [(":",1),("(",1),(")",1)]
        self.ruletype = "teacher"

    def test_wrong_record_end(self):
        
        self.inputstr = "ELA :Nathaniel (Amelia) foobar"
    
        with self.assertRaises(SSLoaderRecordEndException):
            teacher,_ = self.ssloader.extract_teacher(self.inputstr)
        
class Test_LoadRefObjects(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        rows = self.ssloader.loadrefobjects("quadref","subject")
        
        expected_results = ['Math Activity Period',u'ELA', 'Psychology','Psychology Reading','Biology','Spanish','Italian','Debate',u'Drama', 'Reading',u'Engineering', u'Math', u'Student News', u'Counseling', u'Science', u'Movement', u'Activity Period', u'Speech', u'History', u'OT', u'Core', u'Chess', u'Lunch Computer Time', u'Music', u'??', u'Independent Reading', 'Independent Art',u'Piano', u'Art', u'STEM', u'Humanities', u'Work Period']

        expected_results.sort()
        
        self.assertListEqual(expected_results,rows)
        
    def test_synonyms(self):
        
        rows = self.ssloader.loadrefobjects("quadref","subject",True)
        
        expected_results = [u'WP', 'W Period', u'Work P', u'AP', u'APeriod', u'SN', u'SNews', u'Activity P', u'Student N', 'Independent Art',u'Movement / Chess', u'Movement/chess', u'Debate Elective','Math Activity Period',u'ELA', 'Psychology','Psychology Reading','Biology','Spanish','Italian','Debate',u'Drama', 'Reading',u'Engineering', u'Math', u'Student News', u'Counseling', u'Science', u'Movement', u'Activity Period', u'Speech', u'History', u'OT', u'Core', u'Chess', u'Lunch Computer Time', u'Music', u'??', u'Independent Reading', u'Piano', u'Art', u'STEM', u'Humanities', u'Work Period']

        expected_results.sort()
        
        self.assertListEqual(expected_results,rows)
        
class Test_LoadSynonyms(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        rows = self.ssloader.addsynonyms("quadref","subject")
        rows.sort()
        
        expected_results = [u'WP', 'W Period', u'Work P', u'AP', u'APeriod', u'SN', u'SNews', u'Activity P', u'Student N', u'Movement / Chess', u'Movement/chess', u'Debate Elective']
        
        expected_results.sort()

        self.assertListEqual(expected_results,rows)
        
class Test_ValidateTokens_Teacher(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.ssloader.inputfile = "test_ssloader.py"
        
        self.valid_subjects = self.ssloader.loadrefobjects('quadref','adult')
        
    def test_exact_match(self):
        
        validated_token = self.ssloader.validate_token2('Eric',self.valid_subjects)
        
        self.assertEqual(validated_token,'Eric')
        
class Test_ValidateTokens_Subject(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.ssloader.inputfile = "test_ssloader.py"
        
        self.valid_subjects = self.ssloader.loadrefobjects('quadref','subject')
        
    def test_exact_match(self):
        
        validated_token = self.ssloader.validate_token2('Math',self.valid_subjects)
        
        self.assertEqual(validated_token,'Math')
        
    def test_leading_space(self):
        
        validated_token = self.ssloader.validate_token2(' Humanities',self.valid_subjects)
        
        self.assertEqual(validated_token,'Humanities')
        
    def test_case_match(self):
        
        validated_token = self.ssloader.validate_token2('MATH',self.valid_subjects)
        
        self.assertEqual(validated_token,'Math')
        
    def test_mispel_match(self):
        
        validated_token = self.ssloader.validate_token2('Msth',self.valid_subjects)
        
        self.assertEqual(validated_token,'Math')
        
    def test_mispel_match2(self):
        
        validated_token = self.ssloader.validate_token2('Hmanities',self.valid_subjects)
        
        self.assertEqual(validated_token,'Humanities')
                
    def test_missing_char_match(self):
        
        validated_token = self.ssloader.validate_token2('Hstory',self.valid_subjects)
        
        self.assertEqual(validated_token,'History')
        
    def test_badly_mispel_match(self):
        
        with self.assertRaises(SSLoaderNoMatchException):
            validated_token = self.ssloader.validate_token2('Fsth',self.valid_subjects)
        
    def test_misc(self):
        
        validated_token = self.ssloader.validate_token2('Reading',self.valid_subjects)
        
        self.assertEqual(validated_token,'Reading')
        
    def test_badly_mispel_match_fail(self):
        
        with self.assertRaises(SSLoaderNoMatchException):
            validated_token = self.ssloader.validate_token2('Fsxh',self.valid_subjects)
            
        
class Test_ValidateTokens_Multi(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.ssloader.inputfile = "test"
        self.valid_students = self.ssloader.loadrefobjects('quadref','student')
        
        self.record = ['830-910','Monday','WP','Amelia',['Nathaniel'],'teacher']
        
    def test_(self):
        new_record = self.ssloader.validate_tokens(self.record)
        expected_results = ['830-910','Monday','Work Period','Amelia',['Nathaniel'],'teacher']
        self.assertListEqual(new_record,expected_results)
        
        
class Test_ValidateTokens_Student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        self.ssloader.inputfile = "test"
        
        self.valid_students = self.ssloader.loadrefobjects('quadref','student')
        
    '''def test_exact_match(self):
        
        validated_token = self.ssloader.validate_token('Cleyton',self.valid_students)
        
        self.assertEqual(validated_token,'Clayton')'''
        
    def test_extra_letter(self):
        
        validated_token = self.ssloader.validate_token2('Simon A',self.valid_students)
        
        self.assertEqual(validated_token,'Simon A')
        
    def test_missing_letter(self):
        
        validated_token = self.ssloader.validate_token2('McKenzie',self.valid_students)
        
        self.assertEqual(validated_token,'Mackenzie')
  
class Test_RelSize(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_same(self):
        
        result,value = self.ssloader._match_num_chars_same_location("foobar","foobar")

        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
    def test_matcher_bigger(self):
        
        result,value = self.ssloader._match_rel_size("foobar","foobarrr")

        self.assertEquals(result,True)
        self.assertEquals(value,0.33)
        
    def test_matcher_maxbigger(self):
        
        result,value = self.ssloader._match_rel_size("foobar","foobarrrr")

        self.assertEquals(result,True)
        self.assertEquals(value,0.5)
        
    def test_matcher_toobig(self):
        
        result,value = self.ssloader._match_rel_size("foobar","foobarrrrr")

        self.assertEquals(result,False)
        self.assertEquals(value,0.67)
        
    def test_matcher_smaller(self):
        
        result,value = self.ssloader._match_rel_size("foobar","fooba")

        self.assertEquals(result,True)
        self.assertEquals(value,0.2)
         
    def test_matcher_maxsmaller(self):
        
        result,value = self.ssloader._match_rel_size("foobar","foob")

        self.assertEquals(result,True)
        self.assertEquals(value,0.5)
        
    def test_matcher_toosmall(self):
        
        result,value = self.ssloader._match_rel_size("foobar","foo")

        self.assertEquals(result,False)
        self.assertEquals(value,1)

class Test_NumCharsSamelLocation(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_all(self):
        
        result,value = self.ssloader._match_num_chars_same_location("foobar","foobar")

        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
    def test_none(self):
        
        result,value = self.ssloader._match_num_chars_same_location("foobar","zzzzzz")

        self.assertEquals(result,False)
        self.assertEquals(value,0)
        
    def test_1charmissing_middle(self):
        
        result,value = self.ssloader._match_num_chars_same_location("fobar","foobar")

        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
    def test_1charadded_middle(self):
        
        result,value = self.ssloader._match_num_chars_same_location("fozbar","foobar")

        self.assertEquals(result,True)
        self.assertAlmostEqual(value,0.83)
        
    def test_1char_missing_end(self):
        
        result,value = self.ssloader._match_num_chars_same_location("fooba","foobar")

        self.assertEquals(result,True)
        self.assertAlmostEqual(value,0.83)
        
    def test_1char_missing_start(self):
        
        result,value = self.ssloader._match_num_chars_same_location("oobar","foobar")

        print value
        self.assertEquals(result,True)
        self.assertAlmostEqual(value,0.83)
        
    def test_2charsdiff_not_consecutive(self):
        
        result,value = self.ssloader._match_num_chars_same_location("fozbzr","foobar")

        self.assertEquals(result,False)
        self.assertAlmostEqual(value,0.5)
        
    def test_bigger_matchee_with_diff_first_char_many_same_at_end(self):

        result,value = self.ssloader._match_num_chars_same_location("zblahfoobar","foobar")
        self.assertEquals(result,True)
        
class Test_NumCharsSame(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_identical(self):
        
        result,value = self.ssloader._match_num_chars_same("foobar","foobar")
        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
    def test_samechars_different_order(self):
        
        result,value = self.ssloader._match_num_chars_same("raboof","foobar")
        self.assertEquals(result,True)
        self.assertEquals(value,1)
    
    def test_samechars_different_order_different_lengths(self):
        
        result,value = self.ssloader._match_num_chars_same("raboof","foobarxy")
        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
    def test_1char_diff(self):
        
        result,value = self.ssloader._match_num_chars_same("abzde","abcde")

        self.assertEquals(result,True)
        self.assertEquals(value,0.8)
        
    def test_1char_more(self):
        
        result,value = self.ssloader._match_num_chars_same("abczde","abcde")

        self.assertEquals(result,True)
        self.assertAlmostEqual(round(value,2),0.83)
        
    def test_too_big_size_difference(self):
        
        result,value = self.ssloader._match_num_chars_same("reading","engineering")

        self.assertEquals(result,False)
        
    def test_space_difference(self):
        
        result,value = self.ssloader._match_num_chars_same("Simon A","SimonA")

        self.assertEquals(result,True)
        
    def test_2charsdiff_not_consecutive(self):
        
        result,value = self.ssloader._match_num_chars_same("fozbzr","foobar")

        self.assertEquals(result,False)

class Test_NumCharsLocationSame(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_identical(self):
        
        result,value = self.ssloader._match_num_chars_same_location("foobar","foobar")
        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
class Test_RecordIdentifcation(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        fileasstring = self.ssloader.file2string("prep5data_test.csv")
        self.records = self.ssloader.string2records(fileasstring)
   
        self.rules = {'teacher':[(":",1),("(",1),(")",1)],
                      'date':[("/",2)],
                      'noteacher': [(":",1),("(",0),(")",0)],
                      'period' :[(":",2),("-",1)]}
        
    def test_teacher(self):
        self.inputstr = "ELA: Nathaniel (Amelia)"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.student.subject.teacher')
            
    def test_noteacher(self):
        self.inputstr = "Science: Oscar, Peter "
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.student.subject.noteacher')
        
    def test_noteacher2(self):
        self.inputstr = "Engineering: Oscar, Peter "
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.student.subject.noteacher')
        
    def test_date(self):
        self.inputstr =  "09/19/16"
        recordtype = self.ssloader.identify_record(self.inputstr)
        self.assertEquals(recordtype, 'date')
        
    def test_period(self):
        self.inputstr = "\"8:30- 9:10"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'period')
        
    def test_teacher_extra_quote(self):
        self.inputstr = "Science: Jake (Paraic) \""
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.student.subject.teacher')   
        
    def test_teacher_edgecase2(self):
        self.inputstr = "Movement: Shane, Simon B, Asher"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.student.subject.noteacher')
        
    def test_teacher_edgecase3(self):
        self.inputstr = "Students News: Orig, Stephen:"
       
        
        with self.assertRaises(SSLoaderNoRulesMatchException):
            recordtype = self.ssloader.identify_record(self.inputstr)
        
    def test_PERIOD_2(self):
        self.inputstr = "Period 1"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'ignore')

    def test_PERIOD_1(self):
        self.inputstr = "PERIOD 1"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'ignore')
    
    # with
    def test_With(self):
        self.inputstr = "Engineering with Paraic"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.nostudent.nosubject.noteacher.with')
        
    def test_teacher_Syno_Match(self):
        self.inputstr = "Humanities Work Period with Johnny"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.nostudent.subject.noteacher.with')
        
    def test_teacher_WP_With(self):
        self.inputstr = "Work Period with Alyssa"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.nostudent.nosubject.noteacher.with')
       
    def test_teacher_with_edge(self):
        self.inputstr = "Science with (Paraic)"
        
        
        with self.assertRaises(SSLoaderNoRulesMatchException):
            recordtype = self.ssloader.identify_record(self.inputstr)
     
    def test_nowith(self):
        self.inputstr = "History Samantha"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'student.student.subject.teacher.nowith')
        
    def test_nowith2(self):
        self.inputstr = "ELA Aaron"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'student.student.subject.teacher.nowith')
        
    def test_nowith_colon(self):
        self.inputstr = "ELA: Aaron"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'student.student.subject.teacher.nowith.colon')     
            
    # with and
    def test_teacher_WP_With_And(self):
        self.inputstr = "Work Period with Paraic and Rahul"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.nostudent.nosubject.noteacher.with.and')
    
    def test_With_And(self):
        self.inputstr = "Engineering with Paraic and Eric"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.nostudent.nosubject.noteacher.with.and')

    def test_and_no_with(self):
        self.inputstr = "Chess: NAthaniel and Jake"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.student.subject.noteacher.and')
        
    # Work Period
    def test_teacher_Start_Work_Period_Students(self):
        self.inputstr =  'Work Period: Shane, Asher'
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.student.nosubject.noteacher')
        
    def test_teacher_Start_Work_Period_Students_Syno(self):
        self.inputstr =  'WP: Shane, Asher'
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.student.nosubject.noteacher')

    def test_teacher_WP_Teacher(self):
        self.inputstr = "Work Period: Asher (Alyssa)"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.student.nosubject.teacher')
        
    def test_teacher_Work_Period(self):
        self.inputstr = "Work Period"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.nostudent.nosubject.noteacher')
        
    def test_teacher_WP(self):
        self.inputstr = "WP"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp.nostudent.nosubject.noteacher')
            
            
            
    # Subjects (not Work Period)
    def test_teacher_Subject_Italian(self):
        self.inputstr = "Italian"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'subject.nostudent.nosubject.noteacher')
        
    def test_teacher_Movement(self):
        self.inputstr = "Movement"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype,'subject.nostudent.nosubject.noteacher')   
            
            
    # Work Period Subjects
    def test_teacher_Subject_Work_Period(self):
        self.inputstr = "Humanities Work Period"
        recordtype = self.ssloader.identify_record(self.inputstr)
         
        self.assertEquals(recordtype, 'wp.nostudent.subject.noteacher')  
        
    def test_teacher_Subject_Work_Period(self):
        self.inputstr = "Math WP"
        recordtype = self.ssloader.identify_record(self.inputstr)
         
        self.assertEquals(recordtype, 'wp.nostudent.subject.noteacher')
        
    def test_teacher_Subject_Work_Period_Student(self):
        self.inputstr = "Math WP: Jack"
        recordtype = self.ssloader.identify_record(self.inputstr)
         
        self.assertEquals(recordtype, 'wp.student.subject.noteacher')
        
    def test_teacher_Subject_Work_Period_Student_Teacher(self):
        self.inputstr = "Math WP: Jack (Stan)"
        recordtype = self.ssloader.identify_record(self.inputstr)
         
        self.assertEquals(recordtype, 'wp.student.subject.teacher')
        
    # students
    def test_student(self):
        self.inputstr = "Jack"
        recordtype = self.ssloader.identify_record(self.inputstr)
         
        self.assertEquals(recordtype, 'student.student.nosubject.noteacher')
        
    # fails
    def test_wp_with_colon(self):
        self.inputstr = "Humanities WP: with alyssa"
        recordtype = self.ssloader.identify_record(self.inputstr)
         
        self.assertEquals(recordtype, 'wp.nostudent.subject.teacher.with')        
        
        

    
    
    
    
class Test_RecordIdentifcation_realsample(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        fileasstring = self.ssloader.file2string("prep5data_test.csv")
        self.records = self.ssloader.string2records(fileasstring)

    def test_(self):
        
        results = {'dow':0,'noteacher':0,'ignore':0,'teacher':0,'date':0,'period':0,'SSLoaderNoRulesMatchException':0,
                   'SSLoaderMultiRuleMatchException':0,'block':0,'eol':0,'blankrow':0,'_ENDCELL_':0,'_CRETURN_':0}
        
        for record in self.records:
            try:
                recordtype = self.ssloader.identify_record(record)
            except Exception, e:
                results[e.__class__.__name__]+=1
                continue
            
            if recordtype.startswith("dow"):
                recordtype="dow"
            results[recordtype] += 1


        self.assertEquals(results['noteacher'],5)
        self.assertEquals(results['teacher'],6)
        self.assertEquals(results['SSLoaderNoRulesMatchException'],0)
        self.assertEquals(results['period'],1)
        
class Test_RecordIdentifcation_realsample2(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        fileasstring = self.ssloader.file2string("prep5data_miss-day-terminator.csv")
        self.records = self.ssloader.string2records(fileasstring)

    def test_(self):
        
        results = {'dow':0,'noteacher':0,'teacher':0,'ignore':0,'date':0,'period':0,'SSLoaderNoRulesMatchException':0,
                   'SSLoaderMultiRuleMatchException':0,'block':0,'eol':0,'_ENDCELL_':0,'blankrow':0}
        
        for record in self.records:
            try:
                recordtype = self.ssloader.identify_record(record)
            except Exception, e:
                results[e.__class__.__name__]+=1
                continue
            
            if recordtype.startswith("dow"):
                recordtype="dow"
            results[recordtype] += 1
           

class Test_PreProcessRecordsWith(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','ELA with Amelia','^','Engineering with Paraic']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',[],'subject.nostudent.nosubject.noteacher.with'],
                          ['830-910','Tuesday','Engineering','Paraic',[],'subject.nostudent.nosubject.noteacher.with']]
        
        self.assertListEqual(clean_records,expected_results)


class Test_PreProcessRecordsWithAnd(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','ELA with Amelia and Paraic','^','Engineering with Paraic']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',[],'subject.nostudent.nosubject.noteacher.with.and'],
                            ['830-910','Monday','ELA','Paraic',[],'subject.nostudent.nosubject.noteacher.with.and'],
                          ['830-910','Tuesday','Engineering','Paraic',[],'subject.nostudent.nosubject.noteacher.with']]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsWorkPeriodWith(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','Work Period with Amelia','^','Work Period with Paraic']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',[],'wp.nostudent.nosubject.noteacher.with'],
                          ['830-910','Tuesday','Science','Paraic',[],'wp.nostudent.nosubject.noteacher.with']]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsWorkPeriodWithAnd(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','Work Period with Amelia and Paraic','^','Work Period with Paraic']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','??','Amelia',[],'wp.nostudent.nosubject.noteacher.with.and'],
                            ['830-910','Monday','??','Paraic',[],'wp.nostudent.nosubject.noteacher.with.and'],
                          ['830-910','Tuesday','??','Paraic',[],'wp.nostudent.nosubject.noteacher.with']]
        
        self.assertListEqual(clean_records,expected_results)
        
        
class Test_PreProcessRecordsSpaceAndCommaDelim(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['John++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Movement: shane asher, nick','^','^','Math WP: Simon A']

        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','Movement','John',['shane','asher','nick'],'subject.student.subject.noteacher'],
                            ['830-910','Thursday','Math','John',['Simon A'],'wp.student.subject.noteacher']]
        
        self.assertListEqual(clean_records,expected_results)        
        
        
class Test_PreProcessRecordsWorkPeriodWithSubject(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','Humanities Work Period with Amelia','^','Math Work Period with Paraic']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','Humanities','Amelia',[],'wp.nostudent.subject.noteacher.with'],
                          ['830-910','Tuesday','Math','Paraic',[],'wp.nostudent.subject.noteacher.with']]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecords(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','ELA: Nathaniel (Amelia)','^',
                        'Math: CLayton, (Stan)','^','Engineering: Orig, Stephen, Oscar (Paraic)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel'],'subject.student.subject.teacher'],
                          ['830-910','Tuesday','Math','Stan',['CLayton'],'subject.student.subject.teacher'],
                          ['830-910','Wednesday','Engineering','Paraic',['Orig','Stephen','Oscar'],'subject.student.subject.teacher']]
        
        self.assertListEqual(clean_records,expected_results)
        
    def test_withleadingdows(self):
        
        self.records = ['09/19/16','^','Monday','^','Tuesday','^','8:30- 9:10','^','ELA: Nathaniel (Amelia)','^',
                        'Math: CLayton, (Stan)','^','Engineering: Orig, Stephen, Oscar (Paraic)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel'],'subject.student.subject.teacher'],
                          ['830-910','Tuesday','Math','Stan',['CLayton'],'subject.student.subject.teacher'],
                          ['830-910','Wednesday','Engineering','Paraic',['Orig','Stephen','Oscar'],'subject.student.subject.teacher']]
        
        #@self.assertListEqual(clean_records,expected_results)
        
    def test_realexample(self):
    
        self.records = ['8:30- 9:10', '&', 'PERIOD 1', '^', 'ELA: Nathaniel (Amelia)', '^', 'Math: CLayton, (Stan)']
    
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel'],'subject.student.subject.teacher'],
                            ['830-910','Tuesday','Math','Stan',['CLayton'],'subject.student.subject.teacher']]

            
        self.assertListEqual(clean_records,expected_results)

class Test_PreProcessRecordStudent(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['Asher**', '^', 'Monday', '^', 'Tuesday', '^', 'Wednesday', '^', 'Thursday', '^', 'Friday', 
                        '8:30- 9:10', '^', 'Science with John', '^', 'Math with Galina', '^', 'Science with John', '^', 'Math with Galina', '^', 'STEM']

        self.expected_results = [['830-910', 'Monday', 'Science', 'John', ['Asher'], 'subject.nostudent.nosubject.noteacher.with'], 
                                  ['830-910', 'Tuesday', 'Math', 'Galina', ['Asher'], 'subject.nostudent.nosubject.noteacher.with'], 
                                  ['830-910', 'Wednesday', 'Science', 'John', ['Asher'], 'subject.nostudent.nosubject.noteacher.with'], 
                                  ['830-910', 'Thursday', 'Math', 'Galina', ['Asher'], 'subject.nostudent.nosubject.noteacher.with'],
                                  ['830-910', 'Friday', 'STEM', '??', ['Asher'], 'subject.nostudent.nosubject.noteacher']
                                  ]
        self.ssloader.inputfile = "test"
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        self.assertListEqual(clean_records,self.expected_results)

        
        
class Test_PreProcessRecordsSubjectWorkPeriod(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['Moira++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Math WP: Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','??','Moira',['MacKenzie'],'wp.student.nosubject.noteacher'],
                          ['830-910','Thursday','Math','Moira',['Nick'],'wp.student.subject.noteacher']]
        
        self.assertListEqual(clean_records,expected_results)
        
    def test_with_teacher(self):
    
        self.records = ['09/19/16','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie (Amelia)','^','^','Math WP: Nick (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','ELA','Amelia',['MacKenzie'],'wp.student.nosubject.teacher'],
                          ['830-910','Thursday','Math','Stan',['Nick'],'wp.student.subject.teacher']]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsWorkPeriodStudent(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','Work Period: Shane, Asher','^','Work P: Bruno','^','WP: Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','??','??',['Shane', 'Asher'],'wp.student.nosubject.noteacher'],
                            ['830-910','Tuesday','??','??',['Bruno'],'wp.student.nosubject.noteacher'],
                            ['830-910','Wednesday','??','??',['Nick'],'wp.student.nosubject.noteacher']]   
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsWorkPeriodSubject(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','Humanities Work Period','^','Math Work P','^','ELA WP']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','Humanities','??',[],'wp.nostudent.subject.noteacher'],
                            ['830-910','Tuesday','Math','??',[],'wp.nostudent.subject.noteacher'],
                            ['830-910','Wednesday','ELA','??',[],'wp.nostudent.subject.noteacher']]   
        
        self.assertListEqual(clean_records,expected_results)
              
              
class Test_PreProcessRecordsWorkPeriod2(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','Work Period','^','Work P','^','WP']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','??','??',[],'wp.nostudent.nosubject.noteacher'],
                            ['830-910','Tuesday','??','??',[],'wp.nostudent.nosubject.noteacher'],
                            ['830-910','Wednesday','??','??',[],'wp.nostudent.nosubject.noteacher']]   
        
        self.assertListEqual(clean_records,expected_results)              
              
              
class Test_PreProcessRecordsWorkPeriod2(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','Work Period','^','Work P','^','WP']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','??','??',[],'wp.nostudent.nosubject.noteacher'],
                            ['830-910','Tuesday','??','??',[],'wp.nostudent.nosubject.noteacher'],
                            ['830-910','Wednesday','??','??',[],'wp.nostudent.nosubject.noteacher']]   
        
        self.assertListEqual(clean_records,expected_results)                    
              
class Test_PreProcessRecordsWorkPeriodStudentTeacherSubject(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','Math WP: Jack (Stan)','^','Math Work Period: Jack,Nick (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','Math','Stan',['Jack'],'wp.student.subject.teacher'],
                            ['830-910','Tuesday','Math','Stan',['Jack','Nick'],'wp.student.subject.teacher']]   
        
        self.assertListEqual(clean_records,expected_results)
        
              
class Test_PreProcessRecordsWorkPeriodStudentSubject(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','Math WP: Jack','^','Math Work Period: Jack,Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','Math','??',['Jack'],'wp.student.subject.noteacher'],
                            ['830-910','Tuesday','Math','??',['Jack','Nick'],'wp.student.subject.noteacher']]   
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsWorkPeriodStudentTeacher(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_teacher(self):
    
        self.records = ['09/19/16','8:30- 9:10','^','WP: Jack (Stan)','^','Work Period: Jack,Nick (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','Math','Stan',['Jack'],'wp.student.nosubject.teacher'],
                            ['830-910','Tuesday','Math','Stan',['Jack','Nick'],'wp.student.nosubject.teacher']]   
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsStaff(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
    
        self.records = ['Moira++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Work PEriod: Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','??','Moira',['MacKenzie'],'wp.student.nosubject.noteacher'],
                          ['830-910','Thursday','??','Moira',['Nick'],'wp.student.nosubject.noteacher']]
        
        self.assertListEqual(clean_records,expected_results)
        
    def test_newstaffname(self):
    
        self.records = ['Moira++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Work PEriod: Nick',
                        'John++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Work PEriod: Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','??','Moira',['MacKenzie'],'wp.student.nosubject.noteacher'],
                          ['830-910','Thursday','??','Moira',['Nick'],'wp.student.nosubject.noteacher'],
                          ['830-910','Tuesday','??','John',['MacKenzie'],'wp.student.nosubject.noteacher'],
                           ['830-910','Thursday','??','John',['Nick'],'wp.student.nosubject.noteacher']]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsNewPeriod(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        # not a real world example as this implies a spreadsheet with 1 day column not 5 
        self.records = ['09/19/16','8:30- 9:10','^','ELA: Nathaniel (Amelia)','9:10- 9:50','^',
                        'Math: CLayton, (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel'],'subject.student.subject.teacher'],
                          ['910-950','Monday','Math','Stan',['CLayton'],'subject.student.subject.teacher']]

        self.assertListEqual(clean_records,expected_results)
        
        
    def test_preceding_newline(self):
        
        # real world example with multiple new lines before an end of cell
        self.records = ['09/19/16','8:30- 9:10','^','ELA: Nathaniel (Amelia)','9:10- 9:50','&','&','^',
                        'Math: CLayton, (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel'],'subject.student.subject.teacher'],
                          ['910-950','Monday','Math','Stan',['CLayton'],'subject.student.subject.teacher']]

        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsStudentSubject(Test_Base):
    
    # Luke**	Monday	Tuesday	Wednesday	 Thursday	Friday
    # 8:30- 9:10	CORE	CORE	OT	Art	Movement

    def setUp(self):
        
        files = [('prep5studentJackPeriod1.csv',4,True)]
                 
        Test_Base.setUp(self)
        self.ssloader.run(self.databasename,files)

    def test_(self):
        pass
        
     
     
class Test_PreProcessRecordsNotWith(Test_Base):
    
    # checking out an edge case where <subject> newline<adult> does not match to the notwith subject rule
    # and checking out an edge case where <subject>: newline<adult> does not match to the notwith subject rule
    # and checking out an edge case where <subject>newline<adult> does not match to the notwith subject rule
    
    def setUp(self):
        Test_Base.setUp(self)

        fileasstring = self.ssloader.file2string("Prep6_Omer_1period.csv")
        
        
        print fileasstring
        self.records = self.ssloader.string2records(fileasstring)
        self.ssloader.inputfile="Prep6_Omer_1period.csv"
        
        print  self.records
        self.clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
    def test_(self):

        expected_records = [['830-910', 'Monday', 'Engineering', 'Paraic', ['Omer'], 'student.student.subject.teacher.nowith'], 
                            ['830-910', 'Tuesday', 'ELA', 'Aaron', ['Omer'], 'student.student.subject.teacher.nowith'],
                            ['830-910', 'Wednesday', 'Engineering', 'Paraic', ['Omer'], 'student.student.subject.teacher.nowith.colon'], 
                            ['830-910', 'Thursday', 'ELA', 'Aaron', ['Omer'], 'subject.nostudent.nosubject.noteacher.with'], 
                            ['830-910', 'Friday', 'STEM', '??', ['Omer'], 'subject.nostudent.nosubject.noteacher']]

        self.assertListEqual(self.clean_records,expected_records)

    
class Test_PreProcessRecordsPrep4100(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        
        fileasstring = self.ssloader.file2string("prep5data_test100.csv")
        self.records = self.ssloader.string2records(fileasstring)
        self.ssloader.inputfile="prep5data_test100.csv"
        
        
        # 1 bad row that should show up in the log 
        # 'could not match record to a rule,skipping'), ('record', 'Students News: Orig, Stephen:')]
        # extra colon
        
    def test_(self):
        
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        self.assertEqual(len(clean_records),110)
        
class Test_PreProcessRecordsPrep4(Test_Base):
    
    def setUp(self):
        Test_Base.setUp(self)
        
        fileasstring = self.ssloader.file2string("prep5data.csv")
        self.records = self.ssloader.string2records(fileasstring)
        self.ssloader.inputfile="prep5data.csv"
        
        # 1 bad row that should show up in the log 
        # 'could not match record to a rule,skipping'), ('record', 'Students News: Orig, Stephen:')]
        # extra colon
        
    def test_(self):
                
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        for record in clean_records:
            print record
            
        self.assertEqual(len(clean_records),203)
        
class Test_PreProcessRecordsComputerTime(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        fileasstring = self.ssloader.file2string("prep5data_testcomputertime.csv")
        self.records = self.ssloader.string2records(fileasstring)
        
        self.students = ['Nathaniel','Clayton','Orig','Stephen','Oscar','Peter','Jack',
                         'Jake','Bruno']   
        
        self.students.sort()
        
    def test_(self):
                
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['1110-1210','Monday','Computer Time','??',self.students,'computertime'],
                            ['1110-1210','Tuesday','Computer Time','??',self.students,'computertime'],
                            ['1110-1210','Wednesday','Computer Time','??',self.students,'computertime'],
                            ['1110-1210','Thursday','Computer Time','??',self.students,'computertime'],
                            ['1110-1210','Friday','Computer Time','??',self.students,'computertime'],
                            ['230-300','Monday','Computer Time','??',self.students,'computertime'],
                            ['230-300','Tuesday','Computer Time','??',self.students,'computertime'],
                            ['230-300','Wednesday','Computer Time','??',self.students,'computertime'],
                            ['230-300','Thursday','Computer Time','??',self.students,'computertime']]    
        
        self.assertListEqual(clean_records,expected_results)
        
        
class Test_PreProcessRecordsFriday(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        fileasstring = self.ssloader.file2string("prep5data_test1period.csv")
        self.records = self.ssloader.string2records(fileasstring)
        
        self.students = ['Nathaniel','Clayton','Orig','Stephen','Oscar','Peter','Jack',
                         'Jake','Bruno']   
        
        self.students.sort()
        
    def test_(self):
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        friday_clean_records = [ record for record in clean_records if record[1] == "Friday"]
                
        expected_results = [['830-910','Friday','Humanities','A',['Orig', 'Jake', 'Nathaniel', 'Stephen'],'subject.student.subject.teacher'],
                            ['830-910','Friday','Music','D',['Coby', 'THomas', 'Yosef'],'subject.student.subject.teacher'],
                            ['830-910','Friday','STEM','C',['Tris', 'Ashley', 'Simon', 'Booker', 'Omer'],'subject.student.subject.teacher'],
                            ['830-910','Friday','ART','B', ['Clayton', 'Bruno', 'Oscar', 'Peter', 'Jack'],'subject.student.subject.teacher']]
        
        self.assertListEqual(friday_clean_records,expected_results)
        

class Test_ValidateTokens(Test_Base):


    def setUp(self):
        Test_Base.setUp(self)
        
    
        
    def test_(self):
        
        record = ['830-910','monday','ELA','amelia',['Nathoniel'],'teacher']
        
        expected_results = ['830-910','Monday','ELA','Amelia',['Nathaniel'],'teacher']
        results =  self.ssloader.validate_tokens(record)
        
        self.assertListEqual(results,expected_results)
        

'''class Test_DBLoader_Big(Test_Base):

    def setUp(self):
        Test_Base.setUp(self)
        
        database = Database(self.databasename)
        try:
            with database:
                tbl_remove(database,'lesson')
                tbl_remove(database,'session')
        except:
            pass
        
    def test_session(self):'''
        
        
class Test_DBLoader(Test_Base):

    def setUp(self):
        Test_Base.setUp(self)
        
        self.ssloader.inputfile = "test"
        database = Database(self.databasename)
        try:
            with database:
                tbl_remove(database,'lesson')
                tbl_remove(database,'session')
        except:
            pass
        
    def test_session(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', [u'Simon A'],'academic'], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', ['Liam'],'academic']]
            
        
        expected_results =  [['Thea.STEM.Tuesday.100-140', 'Tuesday',7,'Thea', 'STEM'], 
                             ['Jess.Humanities.Wednesday.1210-100', 'Wednesday',6, 'Jess','Humanities']]
            
        self.ssloader.sourcecode = "test" 
        
        self.ssloader.dbloader(records)
        
        database = Database(self.databasename)
        with database:
            _,rows,_ = tbl_rows_get(database,'session',['code','dow','period','teacher','subject'])
        
        self.assertListEqual(expected_results,rows)
        
    def test_lesson(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', [u'Simon A'],'academic'], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', ['Liam'],'academic']]
            
        
        expected_results =  [['Simon A', 'TU','100-140','Thea', 'STEM','Thea.STEM.Tuesday.100-140'], 
                             ['Liam', 'WE','1210-100', 'Jess','Humanities','Jess.Humanities.Wednesday.1210-100']]
            
        self.ssloader.sourcecode = "test" 
        self.ssloader.dbloader(records)
        
        database = Database(self.databasename)
        with database:
            _,rows,_ = tbl_rows_get(database,'lesson',['student','dow','period','teacher','subject','session'])
        
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")

class Test_DBLoader_Prep5Computertime(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_session(self):
        
        expected_results = [['test', 5, 9], [u'Monday', 1, 1], [u'Tuesday', 1, 1], [u'Wednesday', 1, 1], [u'Thursday', 1, 1], [u'Friday', 1, 0], ['test', 5, 4]]
        self.ssloader.ssloader([('prep5data_testcomputertime.csv',5,True)],self.databasename)
        results =  _pivotexecfunc(self.ssloader.database,'test','period','dow','session',distinct=True,master=False)
        self.assertListEqual(results,expected_results)
        

    def test_lesson(self):
        
        expected_results = [['test', u'Bruno', u'Clayton', u'Jack', u'Jake', u'Nathaniel', u'Orig', u'Oscar', u'Peter', u'Stephen'], [u'Computer Time', 9, 9, 9, 9, 9, 9, 9, 9, 9], ['test', 9, 9, 9, 9, 9, 9, 9, 9, 9]]
        self.ssloader.ssloader([('prep5data_testcomputertime.csv',5,True)],self.databasename)
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        
        self.assertListEqual(results,expected_results)
    
class Test_DBLoader_Prep5_1period(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson_num_rows(self):
        
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename) 
        
        with self.database:
            _,result,_ = _rowcount(self.database,'lesson')
            
        self.assertEqual(result[0][0],52)
        
        
    def test_session_num_rows(self):
        
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename) 
        
        with self.database:
            _,result,_ = _rowcount(self.database,'session')
            
        self.assertEqual(result[0][0],25)
            
            
    def test_lesson(self):

        expected_results = [['test', u'Nathaniel', u'Clayton', u'Orig', u'Stephen', u'Oscar', u'Peter', u'Jack', u'Jake', u'Bruno', u'Coby', u'Thomas', u'Yosef', u'Tris', u'Ashley', u'Simon A', u'Booker', u'OmerC'],
                            [u'ELA', 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Math', 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Engineering', 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'??', 0, 0, 0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Movement', 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Counseling', 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Student News', 0, 0, 2, 1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Science', 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Core', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Humanities', 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Music', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                            [u'STEM', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                            [u'Art', 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            ['test', 5, 5, 5, 5, 5, 5, 5, 5, 4, 1, 1, 1, 1, 1, 1, 1, 1]]


        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        
        self.assertListEqual(results,expected_results)
        
    def test_session(self):
        
        expected_results = [['test', 1], 
                            [u'Monday', 5], 
                            [u'Tuesday', 6], 
                            [u'Wednesday', 4], 
                            [u'Thursday', 6], 
                            [u'Friday', 4], 
                            ['test', 25]]


        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','period','dow','session',distinct=True,master=False)

        self.assertListEqual(results,expected_results)
        

class Test_DBLoader_Prep5Student_WP(Test_Base):
    
    # tests that subject specific work periods are parsed correctly
    
    def setUp(self):
        Test_Base.setUp(self)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):
        
        expected_results = [['test', u'Clayton'],
                            [u'Math', 1],
                            [u'Humanities', 2],
                            [u'??', 1],
                            [u'Student News', 1],
                            ['test', 5]]
                            
        self.ssloader.ssloader([('prep5studentClaytonPeriod1WP.csv',5,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        
        self.assertListEqual(results,expected_results)
        
class Test_DBLoader_Prep5(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):
        
        expected_results = [['test', u'Nathaniel', u'Clayton', u'Orig', u'Stephen', u'Oscar', u'Peter', u'Jack', u'Jake', u'Bruno', u'Coby', u'Thomas', u'Yosef', u'Tris', u'Ashley', u'Simon A', u'Booker', u'OmerC'],
                            [u'ELA', 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Math', 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Engineering', 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'??', 8, 6, 8, 8, 7, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Movement', 2, 7, 3, 3, 4, 5, 3, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Counseling', 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Student News', 2, 2, 3, 1, 4, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Science', 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Core', 2, 2, 3, 3, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Humanities', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [u'Music', 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [u'STEM', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [u'Art', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [u'Activity Period', 3, 5, 1, 2, 3, 2, 8, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Math Activity Period', 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'History', 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Speech', 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'OT', 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Chess', 4, 0, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Computer Time', 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Reading', 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Independent Reading', 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            ['test', 45, 45, 44, 43, 45, 47, 44, 46, 44, 4, 4, 4, 4, 4, 4, 4, 4]]



        self.ssloader.ssloader([('prep5data.csv',5,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)

        self.assertListEqual(results,expected_results)
        
    def test_session(self):
        
        expected_results = [['test', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                            [u'Monday', 5, 5, 5, 6, 1, 4, 6, 5, 5, 1], 
                            [u'Tuesday', 6, 8, 5, 6, 1, 5, 7, 5, 5, 1],
                            [u'Wednesday', 4, 6, 5, 5, 1, 5, 7, 5, 5, 1], 
                            [u'Thursday', 6, 8, 5, 7, 1, 4, 6, 5, 5, 1],
                            [u'Friday', 4, 5, 4, 4, 1, 0, 0, 0, 0, 0], 
                            ['test', 25, 32, 24, 28, 5, 18, 26, 20, 20, 4]]

        self.ssloader.ssloader([('prep5data.csv',5,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','period','dow','session',distinct=True,master=False)
        self.assertListEqual(results,expected_results)
             
     
class Test_DBLoader_Staff_Issey(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,prep=-1)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):

        expected_result = [['test', u'Nick', u'Peter', u'Jack', u'Jake', u'Orig', u'Stephen', u'Shane', u'Asher', u'Simon B', u'Liam', u'Luke', u'Bruno', u'Nathaniel', u'Clayton', u'Mackenzie', u'Lucy', u'Oscar', u'Simon A'],
                           [u'??', 2, 3, 1, 4, 2, 4, 1, 3, 3, 3, 3, 4, 3, 2, 1, 2, 3, 1],
                           [u'Student News', 0, 0, 0, 0, 2, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                           [u'Activity Period', 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 0],
                           [u'Independent Reading', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [u'Core', 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           ['test', 2, 4, 2, 5, 4, 6, 3, 4, 4, 4, 3, 5, 4, 4, 2, 3, 4, 1]]


        self.ssloader.ssloader([('staffdata_issey.csv',-1,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        
        self.assertListEqual(results,expected_result)

    def test_session(self):

        expected_results = [['test', 1, 2, 3, 4, 6, 7, 8, 9],
                            [u'Monday', 1, 1, 1, 1, 1, 1, 1, 2],
                            [u'Tuesday', 1, 1, 1, 1, 1, 1, 1, 1],
                            [u'Wednesday', 1, 1, 1, 1, 1, 1, 1, 1],
                            [u'Thursday', 1, 1, 1, 2, 1, 1, 1, 1],
                            ['test', 4, 4, 4, 5, 4, 4, 4, 5]]


        self.ssloader.ssloader([('staffdata_issey.csv',-1,True)],self.databasename)  
        results = _pivotexecfunc(self.ssloader.database,'test','period','dow','session',distinct=True,master=False)

        self.assertListEqual(results,expected_results)
     

class Test_DBLoader_Staff_Dylan(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,prep=-1)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):

        expected_result = [['test', u'Booker', u'Thomas', u'Ashley', u'Yosef', u'Coby', u'Nathaniel', u'Clayton', u'Stephen', u'Oscar', u'OmerC', u'Shane', u'Tristan', u'Bruno', u'Asher', u'Nick', u'Simon A', u'Prep 4'], 
                           [u'Movement', 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 3], 
                           [u'Activity Period', 0, 0, 0, 1, 2, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0], 
                           [u'Work Period', 0, 2, 4, 0, 1, 1, 0, 0, 0, 4, 0, 1, 0, 0, 0, 3, 0], 
                           [u'Core', 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                           [u'Psychology Reading', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                           [u'Psychology', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                           [u'Student News', 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                           ['test', 1, 6, 6, 1, 6, 2, 2, 1, 1, 5, 2, 4, 1, 1, 1, 4, 3]]



        self.ssloader.ssloader([('staffdata_dylan.csv',-1,True)],self.databasename)        
        print _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        #self.assertListEqual(results,expected_result)

    def test_session(self):

        expected_results =[['test', 1, 2, 3, 4, 6, 7, 8, 9], 
                           [u'Monday', 1, 1, 1, 1, 1, 1, 1, 1], 
                           [u'Tuesday', 1, 1, 2, 1, 1, 1, 1, 1], 
                           [u'Wednesday', 1, 1, 1, 1, 1, 1, 1, 1], 
                           [u'Thursday', 1, 1, 1, 1, 1, 1, 1, 2], 
                           ['test', 4, 4, 5, 4, 4, 4, 4, 5]]



        self.ssloader.ssloader([('staffdata_dylan.csv',-1,True)],self.databasename)  
        print _pivotexecfunc(self.ssloader.database,'test','period','dow','session',distinct=True,master=False)
        
        #self.assertListEqual(results,expected_results)
     
       
class Test_DBLoader_Student_1Student_1Period(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,prep=-1)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):

        self.ssloader.ssloader([('prep4student_1student_1period.csv',4,True)],self.databasename)        
        
        self.expected_results = [['test', u'Asher'], [u'Science', 2], [u'Math', 2], [u'STEM', 1],['test', 5]]
        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        
        self.assertListEqual(results,self.expected_results)

class Test_DBLoader_Student_3Student(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,prep=-1)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):

        self.ssloader.ssloader([('prep4student3students.csv',-1,True)],self.databasename)        
        
        self.expected_results = [['test', u'Asher', u'Nick'],
                                 [u'Science', 2, 0],
                                 [u'Math', 2, 2],
                                 [u'STEM', 1, 3],
                                 [u'??', 7, 5],
                                 [u'Counseling', 1, 1],
                                 [u'Movement', 7, 9],
                                 [u'Activity Period', 4, 3],
                                 [u'History', 1, 2],
                                 [u'Humanities', 5, 5],
                                 [u'Drama', 1, 1],
                                 [u'Computer Time', 9, 9],
                                 [u'Speech', 1, 0],
                                 [u'Core', 2, 2],
                                 [u'OT', 1, 1],
                                 [u'Music', 1, 0],
                                 [u'Student News', 0, 2],
                                 ['test', 45, 45]]


        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
            
        self.assertListEqual(results,self.expected_results)
 
class Test_DBLoader_Staff(Test_Base):
    def setUp(self):
        Test_Base.setUp(self,prep=-1)
        
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson(self):

        expected_results = [['test', u'OmerC', u'Ashley', u'Tristan', u'Yosef', u'Coby', u'Nathaniel', u'Clayton', u'Jake', u'Peter', u'Thomas', u'Simon A', u'Orig', u'Jack', u'Bruno', u'Nick', u'Stephen', u'Shane', u'Asher', u'Simon B', u'Liam', u'Luke', u'Mackenzie', u'Lucy', u'Oscar', u'Booker', u'Tris', u'Prep 4', u'Donovan'],
                            [u'ELA', 1, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Activity Period', 4, 5, 2, 7, 5, 3, 5, 5, 3, 5, 4, 1, 4, 3, 2, 3, 2, 3, 2, 1, 1, 1, 2, 4, 2, 0, 0, 1],
                            [u'Student News', 1, 3, 1, 2, 3, 0, 3, 1, 3, 2, 0, 5, 1, 3, 3, 2, 0, 0, 2, 3, 2, 4, 4, 3, 1, 0, 0, 2],
                            [u'Debate', 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'??', 7, 8, 4, 8, 9, 9, 6, 8, 7, 9, 7, 7, 5, 8, 6, 8, 6, 10, 7, 9, 7, 5, 5, 7, 6, 1, 0, 6],
                            [u'Independent Reading', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Core', 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'History', 0, 0, 2, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 2, 3, 3, 0, 0, 0, 0, 0],
                            [u'Chess', 0, 0, 0, 1, 2, 4, 1, 4, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Counseling', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                            [u'Movement', 0, 1, 0, 0, 0, 0, 5, 1, 3, 1, 0, 3, 1, 3, 3, 3, 4, 4, 0, 0, 0, 0, 0, 3, 1, 0, 3, 1],
                            [u'Psychology Reading', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Psychology', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                            [u'Independent Art', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            ['test', 13, 17, 10, 20, 21, 16, 22, 22, 17, 23, 14, 20, 11, 17, 15, 16, 16, 19, 11, 13, 12, 15, 14, 17, 11, 2, 3, 10]]

        self.ssloader.ssloader([('staffdata.csv',-1,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
            
        self.assertListEqual(results,expected_results)

    def test_session(self):
                
        expected_results = [['test', 1, 2, 3, 4, 6, 7, 8, 9],
                            [u'Tuesday', 9, 8, 10, 9, 10, 8, 9, 9],
                            [u'Thursday', 8, 8, 9, 9, 7, 9, 8, 9],
                            [u'Monday', 6, 8, 8, 8, 8, 8, 8, 8],
                            [u'Wednesday', 7, 8, 9, 7, 9, 8, 8, 9],
                            ['test', 30, 32, 36, 33, 34, 33, 33, 35]]

        

        self.ssloader.ssloader([('staffdata.csv',-1,True)],self.databasename)
        results = _pivotexecfunc(self.ssloader.database,'test','period','dow','session',distinct=True,master=False)

        self.assertListEqual(results,expected_results)

class Test_DBLoader_Staff_with_Prep5_Period1(Test_Base):
    def setUp(self):
        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass

    def test_lesson(self):

        self.ssloader = SSLoader("test_ssloader")        
        self.ssloader.ssloader([('staffdata_1period_Issey.csv',-1,True)],self.databasename)
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename) 
    
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
    
        cols = ['status','dow','period','session','teacher']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['student','==',"\"" + "Peter" + "\""]])

        expected_results = [['incomplete','WE','830-910','Issey.??.Wednesday.830-910','Issey'],
                            ['incomplete','MO','830-910','??.??.Monday.830-910','??'],
                            ['incomplete','TU','830-910','??.??.Tuesday.830-910','??'],
                            ['incomplete','WE','830-910','??.??.Wednesday.830-910','??'],
                            ['incomplete','TH','830-910','??.??.Thursday.830-910','??'],
                            ['complete','FR','830-910','B.Art.Friday.830-910','B']]
    
        self.assertListEqual(rows,expected_results)
        
class Test_DBLoader_Staff_with_Prep5_Period1_StudentPeter(Test_Base):
    def setUp(self):
        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass

    def test_lesson_pre_primary_set(self):

        self.ssloader = SSLoader("test_ssloader")        
        self.ssloader.ssloader([('staffdata_1period_Issey.csv',-1,True)],self.databasename)
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename)
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.ssloader([('prep5studentPeter1period.csv',5,True)],self.databasename) 
    
        cols = ['status','dow','period','session','teacher']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['student','==',"\"" + "Peter" + "\""]])
        
        expected_results = [[u'complete', u'FR', u'830-910', u'B.Art.Friday.830-910', u'B'],
                            [u'incomplete', u'FR', u'830-910', u'??.Art.Friday.830-910', u'??'],
                            [u'incomplete', u'MO', u'830-910', u'??.??.Monday.830-910', u'??'],
                            [u'complete', u'MO', u'830-910', u'Stan.Math.Monday.830-910', u'Stan'],
                            [u'incomplete', u'TH', u'830-910', u'??.??.Thursday.830-910', u'??'],
                            [u'incomplete', u'TH', u'830-910', u'John.??.Thursday.830-910', u'John'],
                            [u'incomplete', u'TU', u'830-910', u'??.??.Tuesday.830-910', u'??'],
                            [u'complete', u'TU', u'830-910', u'Amelia.ELA.Tuesday.830-910', u'Amelia'],
                            [u'incomplete', u'WE', u'830-910', u'??.??.Wednesday.830-910', u'??'],
                            [u'incomplete', u'WE', u'830-910', u'Issey.??.Wednesday.830-910', u'Issey'],
                            [u'incomplete', u'WE', u'830-910', u'Issey.??.Wednesday.830-910', u'Issey']]


    
        expected_results.sort()
        rows.sort()
        
        self.assertListEqual(rows,expected_results)

    def test_lesson_primary_set(self):


        files = [('staffdata_1period_Issey.csv',-1,True),('prep5data_test1period.csv',5,True),
                 ('prep5studentPeter1period.csv',5,True)]
        
        self.ssloader = SSLoader("test_ssloader")        
        self.ssloader.run("test_ssloader",files)
    
        cols = ['status','dow','period','session','teacher']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['student','==',"\"" + "Peter" + "\""],
                                                                 ['status','=',"\"master\""]])

        expected_results = [['master','WE','830-910','Issey.??.Wednesday.830-910','Issey'],
                            ['master','MO','830-910','Stan.Math.Monday.830-910','Stan'],
                            ['master','TU','830-910','Amelia.ELA.Tuesday.830-910','Amelia'],
                            ['master','TH','830-910','John.??.Thursday.830-910','John'],
                            ['master','FR','830-910','B.Art.Friday.830-910','B']]
    
        expected_results.sort()
        rows.sort()
                   
        self.assertListEqual(rows,expected_results)
        

class Test_DBLoader_New_Amelia(Test_Base):

    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
    
    def test_lesson_records(self):

        cols = ['status','dow','period','session','student']
        
        files = [('prep56new_Amelia.csv',-1,True)]
    
        self.ssloader = SSLoader("test_ssloader")        
        self.ssloader.run("test_ssloader",files)

        expected_results = [[u'complete', u'MO', u'830-910', u'Amelia.ELA.Monday.830-910', u'Peter'],
                            [u'complete', u'MO', u'830-910', u'Amelia.Work Period.Monday.830-910', u'Coby'],
                            [u'incomplete', u'TU', u'830-910', u'??.Work Period.Tuesday.830-910', u'Peter'],
                            [u'complete', u'WE', u'830-910', u'Amelia.ELA.Wednesday.830-910', u'Peter'],
                            [u'complete', u'WE', u'830-910', u'Amelia.Work Period.Wednesday.830-910', u'Coby'],
                            [u'complete', u'TH', u'830-910', u'Amelia.Work Period.Thursday.830-910', u'Jack'],
                            [u'complete', u'MO', u'910-950', u'Amelia.ELA.Monday.910-950', u'Bruno'],
                            [u'complete', u'TU', u'910-950', u'Amelia.ELA.Tuesday.910-950', u'Simon A'],
                            [u'complete', u'WE', u'910-950', u'Amelia.ELA.Wednesday.910-950', u'Bruno'],
                            [u'complete', u'TH', u'910-950', u'Amelia.ELA.Thursday.910-950', u'Simon A'],
                            [u'complete', u'MO', u'950-1030', u'Amelia.ELA.Monday.950-1030', u'Stephen'],
                            [u'complete', u'TU', u'950-1030', u'Amelia.ELA.Tuesday.950-1030', u'Booker'],
                            [u'complete', u'WE', u'950-1030', u'Amelia.ELA.Wednesday.950-1030', u'Stephen'],
                            [u'complete', u'WE', u'950-1030', u'Amelia.Work Period.Wednesday.950-1030', u'Bruno'],
                            [u'complete', u'MO', u'1030-1110', u'Amelia.ELA.Monday.1030-1110', u'Nathaniel'],
                            [u'complete', u'TU', u'1030-1110', u'Amelia.ELA.Tuesday.1030-1110', u'Tristan'],
                            [u'complete', u'WE', u'1030-1110', u'Amelia.ELA.Wednesday.1030-1110', u'Nathaniel'],
                            [u'complete', u'TH', u'1030-1110', u'Amelia.ELA.Thursday.1030-1110', u'Tristan'],
                            [u'complete', u'MO', u'1210-100', u'Amelia.ELA.Monday.1210-100', u'Jack'],
                            [u'incomplete', u'WE', u'1210-100', u'Amelia.??.Wednesday.1210-100', u'Jack'],
                            [u'complete', u'MO', u'100-140', u'Amelia.ELA.Monday.100-140', u'Clayton'],
                            [u'complete', u'MO', u'100-140', u'Amelia.Work Period.Monday.100-140', u'Peter'],
                            [u'complete', u'TU', u'100-140', u'Amelia.ELA.Tuesday.100-140', u'Thomas'],
                            [u'complete', u'WE', u'100-140', u'Amelia.ELA.Wednesday.100-140', u'Clayton'],
                            [u'complete', u'WE', u'100-140', u'Amelia.Work Period.Wednesday.100-140', u'Peter'],
                            [u'complete', u'TH', u'100-140', u'Amelia.ELA.Thursday.100-140', u'Thomas'],
                            [u'complete', u'MO', u'140-220', u'Amelia.ELA.Monday.140-220', u'Oscar'],
                            [u'complete', u'MO', u'140-220', u'Amelia.Work Period.Monday.140-220', u'Clayton'],
                            [u'complete', u'TU', u'140-220', u'Amelia.ELA.Tuesday.140-220', u'Ashley'],
                            [u'complete', u'WE', u'140-220', u'Amelia.ELA.Wednesday.140-220', u'Oscar'],
                            [u'complete', u'WE', u'140-220', u'Amelia.Work Period.Wednesday.140-220', u'Clayton'],
                            [u'complete', u'TH', u'140-220', u'Amelia.ELA.Thursday.140-220', u'Ashley'],
                            [u'complete', u'TU', u'220-300', u'Amelia.ELA.Tuesday.220-300', u'Coby'],
                            [u'complete', u'TU', u'220-300', u'Amelia.Work Period.Tuesday.220-300', u'Ashley'],
                            [u'complete', u'TH', u'220-300', u'Amelia.ELA.Thursday.220-300', u'Coby'],
                            [u'complete', u'TH', u'220-300', u'Amelia.Work Period.Thursday.220-300', u'Ashley']]
        
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['source','=',"\"" + "prep56new_Amelia.csv" + "\""]])

        self.assertListEqual(expected_results,rows)
        
    def test_lesson_summary(self):
        
        self.ssloader = SSLoader("test_ssloader")    
        self.ssloader.ssloader([('prep56new_Amelia.csv',-1,True)],self.databasename)
        
        expected_results = [['test', u'Peter', u'Coby', u'Jack', u'Bruno', u'Simon A', u'Stephen', u'Booker', u'Nathaniel', u'Tristan', u'Clayton', u'Thomas', u'Oscar', u'Ashley'],
                            [u'ELA', 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2],
                            [u'Work Period', 3, 2, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 2],
                            [u'??', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            ['test', 5, 4, 3, 3, 2, 2, 1, 2, 2, 4, 2, 2, 4]]
        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        

        self.assertListEqual(expected_results,results)
        
class Test_DBLoader_New(Test_Base):

    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def test_lesson_summary(self):
        
        self.ssloader = SSLoader("test_ssloader")    
        self.ssloader.ssloader([('prep56new.csv',-1,True)],self.databasename)
        
        expected_results = [['test', u'Peter', u'Coby', u'Clayton', u'Booker', u'Orig', u'Stephen', u'Oscar', u'OmerC', u'Yosef', u'Jack', u'Bruno', u'Simon A', u'Thomas', u'Tristan', u'Ashley', u'Jake', u'Nathaniel'],
                            [u'ELA', 4, 4, 4, 1, 3, 2, 2, 2, 1, 2, 3, 3, 2, 3, 4, 2, 3],
                            [u'Math', 4, 2, 2, 2, 4, 3, 4, 1, 4, 2, 1, 4, 4, 0, 4, 4, 4],
                            [u'History', 4, 4, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 2, 1, 3, 3, 4],
                            [u'Engineering', 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Science', 2, 2, 3, 1, 3, 3, 2, 2, 4, 3, 4, 2, 4, 4, 4, 2, 4],
                            [u'??', 2, 4, 2, 1, 1, 0, 0, 3, 1, 1, 0, 2, 1, 1, 0, 0, 0],
                            [u'Student News', 1, 0, 0, 0, 2, 0, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                            [u'Movement', 1, 2, 2, 0, 1, 0, 0, 1, 2, 0, 2, 2, 1, 2, 1, 1, 0],
                            [u'Activity Period', 0, 4, 1, 0, 0, 2, 0, 1, 1, 0, 0, 0, 1, 2, 0, 3, 0],
                            [u'Core', 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Biology', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Math Activity Period', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [u'Psychology', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                            [u'Chess', 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 2, 1],
                            [u'Italian', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0],
                            [u'Work Period', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [u'Debate', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                            [u'Music', 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            ['test', 19, 24, 19, 8, 23, 17, 17, 17, 19, 13, 17, 20, 17, 17, 16, 17, 16]]

        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        

        self.assertListEqual(expected_results,results)
        
    def test_lesson_records(self):

        
        expected_results = [[u'complete', u'MO', u'830-910', u'Amelia.ELA.Monday.830-910', u'Peter'],
                            [u'complete', u'MO', u'830-910', u'Amelia.ELA.Monday.830-910', u'Coby'],
                            [u'complete', u'MO', u'830-910', u'Stan.Math.Monday.830-910', u'Clayton'],
                            [u'complete', u'MO', u'830-910', u'Samantha.History.Monday.830-910', u'Peter'],
                            [u'complete', u'MO', u'830-910', u'Samantha.History.Monday.830-910', u'Booker'],
                            [u'complete', u'MO', u'830-910', u'Paraic.Engineering.Monday.830-910', u'Orig'],
                            [u'complete', u'MO', u'830-910', u'Paraic.Engineering.Monday.830-910', u'Stephen'],
                            [u'complete', u'MO', u'830-910', u'Paraic.Engineering.Monday.830-910', u'Oscar'],
                            [u'complete', u'MO', u'830-910', u'Paraic.Engineering.Monday.830-910', u'OmerC'],
                            [u'complete', u'MO', u'830-910', u'Paraic.Science.Monday.830-910', u'Yosef']]

        cols = ['status','dow','period','session','student']
        
        files = [('prep56new.csv',-1,True)]
    
        self.ssloader = SSLoader("test_ssloader")        
        self.ssloader.run("test_ssloader",files)
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['source','=',"\"" + "prep56new.csv" + "\""],['dow','=',"\"MO\""],['period','=',"\"830-910\""]])
            
        self.assertListEqual(expected_results,rows)
            
        
class Test_DBLoader_Academic_Stan(unittest.TestCase):
    
    # 2 sessions are not implied by the academic and need to be added
    
    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
    
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)])  
        self.ssloader.ssloader([('test_academic_1period_3teachers.csv',-1,True)])   

    def test_lesson_from_academic(self):

        expected_results = [[u'complete', u'MO', u'830-910', u'Stan.Math.Monday.830-910', u'Clayton'],
                            [u'complete', u'TU', u'830-910', u'Stan.Math.Tuesday.830-910', u'Nathaniel'],
                            [u'complete', u'WE', u'830-910', u'Stan.Math.Wednesday.830-910', u'Clayton'], 
                            [u'complete', u'TH', u'830-910', u'Stan.Math.Thursday.830-910', u'Nathaniel'],
                            [u'complete', u'MO', u'830-910', u'Amelia.ELA.Monday.830-910', u'Nathaniel'], 
                            [u'complete', u'TU', u'830-910', u'Amelia.ELA.Tuesday.830-910', u'Peter'], 
                            [u'complete', u'TU', u'830-910', u'Amelia.ELA.Tuesday.830-910', u'Jack'], 
                            [u'complete', u'WE', u'830-910', u'Amelia.ELA.Wednesday.830-910', u'Nathaniel'],
                            [u'complete', u'TH', u'830-910', u'Amelia.ELA.Thursday.830-910', u'Jack'], 
                            [u'complete', u'TU', u'830-910', u'Paraic.Science.Tuesday.830-910', u'Jake'], 
                            [u'complete', u'TH', u'830-910', u'Paraic.Science.Thursday.830-910', u'Jake']]
    
        cols = ['status','dow','period','session','student']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['source','=',"\"" + "test_academic_1period_3teachers.csv" + "\""]])

        self.assertListEqual(expected_results,rows)
        
    def test_session_from_academic(self):
    
        expected_results = [[u'childrenatinit', u'Monday', 1, u'Math', u'Stan.Math.Monday.830-910'],
                            [u'childrenatinit', u'Tuesday', 1, u'Math', u'Stan.Math.Tuesday.830-910'],
                            [u'childrenatinit', u'Wednesday', 1, u'Math', u'Stan.Math.Wednesday.830-910'],
                            [u'childrenatinit', u'Thursday', 1, u'Math', u'Stan.Math.Thursday.830-910'],
                            [u'childrenatinit', u'Monday', 1, u'ELA', u'Amelia.ELA.Monday.830-910'],
                            [u'childrenatinit', u'Tuesday', 1, u'ELA', u'Amelia.ELA.Tuesday.830-910'],
                            [u'childrenatinit', u'Wednesday', 1, u'ELA', u'Amelia.ELA.Wednesday.830-910'],
                            [u'childrenatinit', u'Thursday', 1, u'ELA', u'Amelia.ELA.Thursday.830-910'],
                            [u'nochildrenatinit', u'Monday', 1, u'Engineering', u'Paraic.Engineering.Monday.830-910'],
                            [u'childrenatinit', u'Tuesday', 1, u'Science', u'Paraic.Science.Tuesday.830-910'],
                            [u'nochildrenatinit', u'Wednesday', 1, u'Engineering', u'Paraic.Engineering.Wednesday.830-910'],
                            [u'childrenatinit', u'Thursday', 1, u'Science', u'Paraic.Science.Thursday.830-910']]


        cols = ['status','dow','period','subject','code']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',cols,[['source','=',"\"" + "test_academic_1period_3teachers.csv" + "\""]])

        self.assertListEqual(expected_results,rows)
        
class Test_DBLoader_Academic_Stan_Orphan(unittest.TestCase):
    
    # this finds a session in the academic file that has not previously been added so adds the session and adds the lesson
    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
    
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)])  
        self.ssloader.ssloader([('test_academic_1period_3teachers_orphansession.csv',-1,False)])   
        
    def test_session_from_academic(self):
    
        cols = ['status','dow','period','teacher']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',cols,[['source','=',"\"" + "test_academic_1period_3teachers.csv" + "\""]])

        for row in rows:
            print row
            
        #self.assertListEqual(expected_results,rows)    
        
class Test_DBLoader_Academic(unittest.TestCase):
    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
    
        self.ssloader = SSLoader("test_ssloader")
        self.results = self.ssloader.run("test_ssloader",[('prep5data.csv',5,True),
                                                          ('academic.csv',-1,True)],True)
            
    def test_(self):

        expected_results = [[u'complete', u'MO', u'830-910', u'Stan.Math.Monday.830-910', u'Clayton'],
                            [u'complete', u'MO', u'910-950', u'Stan.Math.Monday.910-950', u'Simon A'], 
                            [u'complete', u'MO', u'1030-1110', u'Stan.Math.Monday.1030-1110', u'Yosef'], 
                            [u'complete', u'MO', u'1210-100', u'Stan.Math.Monday.1210-100', u'Booker'],
                            [u'complete', u'MO', u'100-140', u'Stan.Math.Monday.100-140', u'Thomas'], 
                            [u'complete', u'MO', u'140-220', u'Stan.Math.Monday.140-220', u'Ashley'], 
                            [u'complete', u'MO', u'220-300', u'Stan.Math.Monday.220-300', u'Coby'], 
                            [u'complete', u'TU', u'830-910', u'Stan.Math.Tuesday.830-910', u'Nathaniel'], 
                            [u'complete', u'TU', u'910-950', u'Stan.Math Activity Period.Tuesday.910-950', u'Bruno'], 
                            [u'complete', u'TU', u'1030-1110', u'Stan.Math.Tuesday.1030-1110', u'Peter'], 
                            [u'complete', u'TU', u'1210-100', u'Stan.Math.Tuesday.1210-100', u'Jake'], 
                            [u'complete', u'TU', u'100-140', u'Stan.Math.Tuesday.100-140', u'Orig'], 
                            [u'complete', u'TU', u'140-220', u'Stan.Math.Tuesday.140-220', u'Oscar'], 
                            [u'complete', u'TU', u'220-300', u'Stan.Math.Tuesday.220-300', u'Jack'], 
                            [u'complete', u'WE', u'830-910', u'Stan.Math.Wednesday.830-910', u'Clayton'], 
                            [u'complete', u'WE', u'910-950', u'Stan.Math.Wednesday.910-950', u'Simon A'], 
                            [u'complete', u'WE', u'1030-1110', u'Stan.Math.Wednesday.1030-1110', u'Yosef'], 
                            [u'complete', u'WE', u'1210-100', u'Stan.Math.Wednesday.1210-100', u'Booker'], 
                            [u'complete', u'WE', u'100-140', u'Stan.Math.Wednesday.100-140', u'Thomas'], 
                            [u'complete', u'WE', u'140-220', u'Stan.Math.Wednesday.140-220', u'Ashley'],
                            [u'complete', u'WE', u'220-300', u'Stan.Math.Wednesday.220-300', u'Coby'], 
                            [u'complete', u'TH', u'830-910', u'Stan.Math.Thursday.830-910', u'Nathaniel'],
                            [u'complete', u'TH', u'910-950', u'Stan.Math Activity Period.Thursday.910-950', u'Bruno'], 
                            [u'complete', u'TH', u'1030-1110', u'Stan.Math.Thursday.1030-1110', u'Peter'], 
                            [u'complete', u'TH', u'1210-100', u'Stan.Math.Thursday.1210-100', u'Jake'], 
                            [u'complete', u'TH', u'100-140', u'Stan.Math.Thursday.100-140', u'Orig'], 
                            [u'complete', u'TH', u'140-220', u'Stan.Math.Thursday.140-220', u'Oscar'],
                            [u'complete', u'TH', u'220-300', u'Stan.Math.Thursday.220-300', u'Jack']]
    
        cols = ['status','dow','period','session','student']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['source','=',"\"" + "academic.csv" + "\""],
                                                                 ['teacher','=',"\"" + "Stan" + "\""]])
        self.assertListEqual(rows,expected_results)
            
        cols = ['code']
          
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',cols,[['teacher','=',"\"" + "Stan" + "\""],
                                                                  ['source','=',"\"" + "academic.csv" + "\""]])

        self.assertEqual(len(rows),28)
        
        cols = ['status','dow','period','session','student']
        
        self.expected_results = [[u'master', u'MO', u'220-300', u'Stan.Math.Monday.220-300', u'Coby'], 
                                 [u'master', u'MO', u'100-140', u'Stan.Math.Monday.100-140', u'Thomas'], 
                                 [u'master', u'WE', u'830-910', u'Stan.Math.Wednesday.830-910', u'Clayton'], 
                                 [u'master', u'TU', u'910-950', u'Stan.Math Activity Period.Tuesday.910-950', u'Bruno'], 
                                 [u'master', u'MO', u'1210-100', u'Stan.Math.Monday.1210-100', u'Booker'],
                                 [u'master', u'TH', u'1210-100', u'Stan.Math.Thursday.1210-100', u'Jake'], 
                                 [u'master', u'TU', u'100-140', u'Stan.Math.Tuesday.100-140', u'Orig'], 
                                 [u'master', u'WE', u'140-220', u'Stan.Math.Wednesday.140-220', u'Ashley'], 
                                 [u'master', u'MO', u'830-910', u'Stan.Math.Monday.830-910', u'Clayton'], 
                                 [u'master', u'WE', u'220-300', u'Stan.Math.Wednesday.220-300', u'Coby'], 
                                 [u'master', u'TH', u'1030-1110', u'Stan.Math.Thursday.1030-1110', u'Peter'], 
                                 [u'master', u'TH', u'910-950', u'Stan.Math Activity Period.Thursday.910-950', u'Bruno'], 
                                 [u'master', u'WE', u'1030-1110', u'Stan.Math.Wednesday.1030-1110', u'Yosef'],
                                 [u'master', u'TU', u'1030-1110', u'Stan.Math.Tuesday.1030-1110', u'Peter'], 
                                 [u'master', u'MO', u'1030-1110', u'Stan.Math.Monday.1030-1110', u'Yosef'],
                                 [u'master', u'TH', u'830-910', u'Stan.Math.Thursday.830-910', u'Nathaniel'], 
                                 [u'master', u'TU', u'830-910', u'Stan.Math.Tuesday.830-910', u'Nathaniel'], 
                                 [u'master', u'MO', u'910-950', u'Stan.Math.Monday.910-950', u'Simon A'], 
                                 [u'master', u'MO', u'140-220', u'Stan.Math.Monday.140-220', u'Ashley'], 
                                 [u'master', u'WE', u'910-950', u'Stan.Math.Wednesday.910-950', u'Simon A'], 
                                 [u'master', u'TH', u'140-220', u'Stan.Math.Thursday.140-220', u'Oscar'],
                                 [u'master', u'TH', u'100-140', u'Stan.Math.Thursday.100-140', u'Orig'], 
                                 [u'master', u'TU', u'140-220', u'Stan.Math.Tuesday.140-220', u'Oscar'],
                                 [u'master', u'WE', u'1210-100', u'Stan.Math.Wednesday.1210-100', u'Booker'], 
                                 [u'master', u'WE', u'100-140', u'Stan.Math.Wednesday.100-140', u'Thomas'], 
                                 [u'master', u'TU', u'1210-100', u'Stan.Math.Tuesday.1210-100', u'Jake']]
        

        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['status','=',"\"" + "master" + "\""],
                                                                 ['teacher','=',"\"" + "Stan" + "\""]])    
            
        self.assertListEqual(rows,self.expected_results)
        
class Test_DBLoader_All(unittest.TestCase):
    def setUp(self):  
        
        self.databasename = "test_ssloader"
        self.ssloader = SSLoader("test_ssloader")
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
    
        files = [('prep5data.csv',5,True),('prep4data.csv',4,True),('prep6data.csv',6,True),('staffdata.csv',-1,True),
                 ('academic.csv',-1,False)]
    
        ssloader = SSLoader(self.databasename)
        ssloader.run(self.databasename,files,insertprimary=True)
    
    def test_(self):

        pass

class Test_Primary_Record_Base(unittest.TestCase):
    
    def cleandb(self,database):

        try:
            with database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        
    def filter_results(self,idx,value):
        filtered_results=[]
        for result in self.results:
            if result[idx] == value:
                filtered_results.append(result)
    
        filtered_results.sort()
        
        return filtered_results    

class Test_DBLoader_Primary_Record_Set(Test_Primary_Record_Base):
    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        
        self.cleandb(self.database)
    
        self.ssloader = SSLoader("test_ssloader")
        self.results = self.ssloader.run("test_ssloader",[('prep5data_test1period.csv',5,True),
                                           ('test_academic_1period_3teachers.csv',-1,True)],False)
        
    def test_Nathaniel(self):

        expected_results = [[u'830-910', u'FR', u'Humanities', u'A', u'Nathaniel', u'subject'],
                            [u'830-910', u'MO', u'ELA', u'Amelia', u'Nathaniel', u'[subject,student]'],
                            [u'830-910', u'TH', u'Math', u'Stan', u'Nathaniel', u'[subject,student]'],
                            [u'830-910', u'TU', u'Math', u'Stan', u'Nathaniel', u'[subject,student]'],
                            [u'830-910', u'WE', u'ELA', u'Amelia', u'Nathaniel', u'[subject,student]']]


        expected_results.sort()
        
        self.assertListEqual(self.filter_results(4,'Nathaniel'),expected_results)
        
    def test_Friday(self):
                
        expected_results = [[u'830-910', u'FR', u'Art', u'B', u'Bruno', u'subject'],
                            [u'830-910', u'FR', u'Art', u'B', u'Clayton', u'subject'],
                            [u'830-910', u'FR', u'Art', u'B', u'Jack', u'subject'],
                            [u'830-910', u'FR', u'Art', u'B', u'Oscar', u'subject'],
                            [u'830-910', u'FR', u'Art', u'B', u'Peter', u'subject'],
                            [u'830-910', u'FR', u'Humanities', u'A', u'Jake', u'subject'],
                            [u'830-910', u'FR', u'Humanities', u'A', u'Nathaniel', u'subject'],
                            [u'830-910', u'FR', u'Humanities', u'A', u'Orig', u'subject'],
                            [u'830-910', u'FR', u'Humanities', u'A', u'Stephen', u'subject'],
                            [u'830-910', u'FR', u'Music', u'D', u'Coby', u'subject'],
                            [u'830-910', u'FR', u'Music', u'D', u'Thomas', u'subject'],
                            [u'830-910', u'FR', u'Music', u'D', u'Yosef', u'subject'],
                            [u'830-910', u'FR', u'STEM', u'C', u'Ashley', u'subject'],
                            [u'830-910', u'FR', u'STEM', u'C', u'Booker', u'subject'],
                            [u'830-910', u'FR', u'STEM', u'C', u'OmerC', u'subject'],
                            [u'830-910', u'FR', u'STEM', u'C', u'Simon A', u'subject'],
                            [u'830-910', u'FR', u'STEM', u'C', u'Tris', u'subject']]


            
        expected_results.sort()
            
        self.assertListEqual(self.filter_results(1,'FR'),expected_results)
    
    def test_FOrig(self):

        expected_results = [[u'830-910', u'FR', u'Humanities', u'A', u'Orig', u'subject'],
                            [u'830-910', u'MO', u'Engineering', u'Paraic', u'Orig', u'subject'],
                            [u'830-910', u'TH', u'Student News', '??', u'Orig', u'subject'],
                            [u'830-910', u'TU', u'Student News', '??', u'Orig', u'subject'],
                            [u'830-910', u'WE', u'Engineering', u'Paraic', u'Orig', u'subject']]
        
        
        expected_results.sort()

        self.assertListEqual(self.filter_results(4,'Orig'),expected_results)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")


class Test_DBLoader_Primary_Record_Set_With_Staff_Student(Test_Primary_Record_Base):
    
    # test that multiple values are stored when there is a conflict on subject and teacher
    
    def setUp(self):  
        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)

        self.ssloader = SSLoader("test_ssloader")
        self.results = self.ssloader.run("test_ssloader",[('prep5data_test1period1Monday.csv',5,True),
                                                          ('prep5studentNathanielPeriod1.csv',-1,True)],False)  

    def test_Nathaniel(self):
        
        expected_results = [[u'830-910', u'FR', u'Humanities', '??', u'Nathaniel', u'subject'],
                            [u'830-910', u'MO', u'[ELA,Student News]', u'Amelia', u'Nathaniel', u'subject'],
                            [u'830-910', u'TH', u'Movement', '??', u'Nathaniel', u'subject'],
                            [u'830-910', u'TU', u'Movement', '??', u'Nathaniel', u'subject'],
                            [u'830-910', u'WE', u'Movement', '??', u'Nathaniel', u'subject']]
            
        self.assertListEqual(self.filter_results(4,'Nathaniel'),expected_results)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")
        
class Test_DBLoader_Primary_Record_Set_With_Staff(Test_Primary_Record_Base):
    def setUp(self):  

        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        self.cleandb(self.database)
    
        files = [('prep5data_test1period.csv',5,True),('staffdata_830910.csv',-1,True),('test_academic_1period_3teachers.csv',-1,True)]
    
        ssloader = SSLoader(self.databasename)
        self.results = ssloader.run(self.databasename,files,False)
       
    def test_FOrig(self):

        expected_results = [[u'830-910', u'FR', u'Humanities', u'A', u'Orig', u'subject'],
                            [u'830-910', u'MO', u'Engineering', u'Paraic', u'Orig', u'subject'],
                            [u'830-910', u'TH', u'Student News', u'Issey', u'Orig', u'subject'],
                            [u'830-910', u'TU', u'Student News', u'Johnny', u'Orig', u'subject'],
                            [u'830-910', u'WE', u'Engineering', u'Paraic', u'Orig', u'subject']]


        expected_results.sort()

        self.assertListEqual(self.filter_results(4,'Orig'),expected_results)

    def test_Bruno(self):        
        
        expected_results = [[u'830-910', u'FR', u'Art', u'B', u'Bruno', u'subject'],
                            [u'830-910', u'MO', u'Movement', '??', u'Bruno', u'subject'],
                            [u'830-910', u'TH', u'Core', '??', u'Bruno', u'subject'],
                            [u'830-910', u'TU', u'Student News', u'Johnny', u'Bruno', u'subject']]  
        
        expected_results.sort()
        
        self.assertListEqual(self.filter_results(4,'Bruno'),expected_results)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")
        
class Test_DBLoader_Primary_Record_Set_Nathaniel(Test_Primary_Record_Base):
    def setUp(self):  
        
        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
    
        self.cleandb(self.database)
    
        self.ssloader = SSLoader("test_ssloader")
        self.results = self.ssloader.run("test_ssloader",[('prep5data.csv',5,True)],False) 

    def test_Nathaniel(self):
        
        # expected_results are hand generated from source production files and presented in Prep5_Nathaniel_expected_results.csv
        # the expected_results do not necessarilly match the individual student schedule source prod files as they are known to not always reconcile
        
        expected_results = [[u'100-140', u'MO', u'ELA', u'Aaron', u'Orig', u'subject'],
                            [u'100-140', u'TH', u'Math', u'Stan', u'Orig', u'subject'],
                            [u'100-140', u'TU', u'Math', u'Stan', u'Orig', u'subject'],
                            [u'100-140', u'WE', u'ELA', u'Aaron', u'Orig', u'subject'],
                            [u'1030-1110', u'FR', u'Art', '??', u'Orig', u'subject'],
                            [u'1030-1110', u'MO', u'Core', '??', u'Orig', u'subject'],
                            [u'1030-1110', u'TH', u'Chess', '??', u'Orig', u'subject'],
                            [u'1030-1110', u'TU', u'Chess', '??', u'Orig', u'subject'],
                            [u'1110-1210', u'FR', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'1110-1210', u'MO', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'1110-1210', u'TH', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'1110-1210', u'TU', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'1110-1210', u'WE', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'1210-100', u'MO', u'Student News', '??', u'Orig', u'subject'],
                            [u'1210-100', u'TH', '??', '??', u'Orig', u'wp'],
                            [u'1210-100', u'TU', u'Music', '??', u'Orig', u'subject'],
                            [u'1210-100', u'WE', u'OT', '??', u'Orig', u'subject'],
                            [u'140-220', u'MO', '??', '??', u'Orig', u'wp'],
                            [u'140-220', u'TH', '??', '??', u'Orig', u'wp'],
                            [u'140-220', u'TU', '??', '??', u'Orig', u'wp'],
                            [u'140-220', u'WE', '??', '??', u'Orig', u'wp'],
                            [u'220-300', u'MO', u'Movement', '??', u'Orig', u'subject'],
                            [u'220-300', u'TH', u'Activity Period', '??', u'Orig', u'ap'],
                            [u'220-300', u'TU', u'Movement', '??', u'Orig', u'subject'],
                            [u'220-300', u'WE', u'Movement', '??', u'Orig', u'subject'],
                            [u'300-330', u'MO', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'300-330', u'TH', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'300-330', u'TU', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'300-330', u'WE', u'Computer Time', '??', u'Orig', u'computertime'],
                            [u'830-910', u'FR', u'Humanities', u'A', u'Orig', u'subject'],
                            [u'830-910', u'MO', u'Engineering', u'Paraic', u'Orig', u'subject'],
                            [u'830-910', u'TH', u'Student News', '??', u'Orig', u'subject'],
                            [u'830-910', u'TU', u'Student News', '??', u'Orig', u'subject'],
                            [u'830-910', u'WE', u'Engineering', u'Paraic', u'Orig', u'subject'],
                            [u'910-950', u'FR', u'Core', '??', u'Orig', u'subject'],
                            [u'910-950', u'MO', u'Science', u'Paraic', u'Orig', u'subject'],
                            [u'910-950', u'TH', u'History', '??', u'Orig', u'subject'],
                            [u'910-950', u'TU', u'History', '??', u'Orig', u'subject'],
                            [u'910-950', u'WE', u'Science', u'Paraic', u'Orig', u'subject'],
                            [u'950-1030', u'FR', u'STEM', '??', u'Orig', u'subject'],
                            [u'950-1030', u'MO', '??', '??', u'Orig', u'wp'],
                            [u'950-1030', u'TH', u'Core', '??', u'Orig', u'subject'],
                            [u'950-1030', u'TU', '??', '??', u'Orig', u'wp'],
                            [u'950-1030', u'WE', '??', '??', u'Orig', u'wp']]


        expected_results.sort()
        
        #for row in self.filter_results(4,'Orig'):
        #    print row
        
        self.assertListEqual(self.filter_results(4,'Orig'),expected_results)


class Test_DBInsert_Direct_Nathaniel(Test_Primary_Record_Base):
    def setUp(self):  

        self.databasename = "test_ssloader"
        #self.databasename = "test_ssloader_insertdirect_nathaniel"
        self.database = Database(self.databasename)
        
        self.cleandb(self.database)
        
        files = [('prep5data.csv',5,True),('prep4data.csv',4,True),('prep6data.csv',6,True),('staffdata.csv',-1,True),
                 ('academic.csv',-1,True)]
    
        ssloader = SSLoader(self.databasename)
        ssloader.run(self.databasename,files)

    def test_(self):

        expected_results = [['Nathaniel', 'MO', 'TU', 'WE', 'TH', 'FR'],
                            [u'830-910', u'ELA,Amelia', u'Math,Stan', u'ELA,Amelia', u'Math,Stan', u'Humanities,A'],                                                                                                                                                                                                                           
                            [u'910-950', u'Core,??', u'??,Dylan', u'??,Moira', u'Core,??', u'Music,??'],                                                                                                                                                                                                                                                 
                            [u'950-1030', u'??,Karolina', u'Activity Period,Aaron', u'OT,??', u'??,Issey', u'STEM,??'],                                                                                                                                                                                                                                  
                            [u'1030-1110', u'Activity Period,Dylan', u'Chess,Rahul', u'Activity Period,Issey', u'Chess,Rahul', u'Art,??'],                                                                                                                                                                                                               
                            [u'1110-1210', u'Computer Time,??', u'Computer Time,??', u'Computer Time,??', u'Computer Time,??', u'Computer Time,??'],                                                                                                                                                                                                     
                            [u'1210-100', u'Science,Paraic', u'History,Samantha', u'Science,Paraic', u'History,Samantha', 0],                                                                                                                                                                                                                            
                            [u'100-140', u'Chess,Rahul', u'??,Karolina', u'Chess,Rahul', u'??,[Aaron,Issey]', 0],                                                                                                                                                                                                                                           
                            [u'140-220', u'??,Johnny', u'Movement,??', u'??,Issey', u'Movement,??', 0],                                                                                                                                                                                                                                                  
                            [u'220-300', u'Speech,??', u'Student News,??', u'Counseling,Alexa', u'Student News,??', 0],                                                                                                                                                                                                                                  
                            [u'300-330', u'Computer Time,??', u'Computer Time,??', u'Computer Time,??', u'Computer Time,??', 0]]
        
        results = _pivotexecfunc(self.database,'Nathaniel','dow','period','lesson',False,True,[['student','=','Nathaniel']],"subject,teacher")

        self.assertListEqual(expected_results, results[:-1])

    def tearDown(self):
        pass
            
class Test_Primary_Set_Session(Test_Primary_Record_Base):
    def setUp(self):  

        self.databasename = "test_ssloader"
        #self.databasename = "test_ssloader_insertdirect_nathaniel"
        self.database = Database(self.databasename)
        
        self.cleandb(self.database)
        
        files = [('prep5studentClaytonPeriod1.csv',-1,True),('prep5data_Clayton_1Period.csv',5,True),
                 ('staffdata_johnny_1period.csv',-1,True),('test_academic_1period_Stan.csv',-1,True)]
    
        ssloader = SSLoader(self.databasename)
        ssloader.run(self.databasename,files)

    def test_lesson(self):
        
        expected_results = [[u'master', u'FR', u'830-910', u'A', u'Clayton', u'Humanities'],
                            [u'master', u'MO', u'830-910', u'Stan', u'Clayton', u'Math'],
                            [u'master', u'TH', u'830-910', u'Johnny', u'Clayton', u'Student News'],
                            [u'master', u'TH', u'830-910', u'Stan', u'Nathaniel', u'Math'],
                            [u'master', u'TU', u'830-910', u'Stan', u'Nathaniel', u'Math'],
                            [u'master', u'TU', u'830-910', u'[Amelia,Johnny]', u'Clayton', u'Activity Period'],
                            [u'master', u'WE', u'830-910', u'[Paraic,Stan]', u'Clayton', u'[Math,Engineering]']]

        expected_results.sort()
        
        cols = ['status','dow','period','teacher','student','subject']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['status','=','\"master\"']])
        
        rows.sort()
        
        self.assertListEqual(rows,expected_results)

    def test_session(self):
        
        expected_results = [[u'master', u'Friday', 1, u'??', u'Humanities'],
                            [u'master', u'Friday', 1, u'A', u'Humanities'],
                            [u'master', u'Monday', 1, u'??', u'Math'],
                            [u'master', u'Monday', 1, u'Johnny', u'Movement'],
                            [u'master', u'Monday', 1, u'Stan', u'Math'],
                            [u'master', u'Thursday', 1, u'??', u'Student News'],
                            [u'master', u'Thursday', 1, u'Johnny', u'Student News'],
                            [u'master', u'Thursday', 1, u'Stan', u'Math'],
                            [u'master', u'Tuesday', 1, u'??', u'??'],
                            [u'master', u'Tuesday', 1, u'Amelia', u'Activity Period'],
                            [u'master', u'Tuesday', 1, u'Johnny', u'??'],
                            [u'master', u'Tuesday', 1, u'Rahul', u'Movement'],
                            [u'master', u'Tuesday', 1, u'Stan', u'Math'],
                            [u'master', u'Wednesday', 1, u'??', u'Math'],
                            [u'master', u'Wednesday', 1, u'Johnny', u'Movement'],
                            [u'master', u'Wednesday', 1, u'Paraic', u'Engineering'],
                            [u'master', u'Wednesday', 1, u'Rahul', u'Movement'],
                            [u'master', u'Wednesday', 1, u'Stan', u'Math']]        

        cols = ['status','dow','period','teacher','subject']
        
        expected_results.sort()
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',cols,[['status','=','\"master\"']])
            
        rows.sort()
        
        self.assertListEqual(rows,expected_results)    

    def tearDown(self):
        pass
            
            
            
if __name__ == "__main__":
    suite = unittest.TestSuite()

    
    # #####################################################################################################
    # unit tests=
    
    
    # pre_process_records
    
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5_1period))   
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Student_3Student_1period))    
    #unittest.TextTestRunner(verbosity=2).run(suite) 
    #exit()
    
    
    # loadrefobjects
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_LoadRefObjects)) 
    
    # loadsynonyms
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_LoadSynonyms))
    
    # string2records
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_String2Records))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_String2Records_Prep4100))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_String2Records_Prep41Period))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_String2Records_Prep4ComputerTime))
        
    # identify_record
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation_realsample))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation_realsample2))
    
    # applyrules
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ApplyRules))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ApplyRules_Fails))
    
    # extract staff
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_extract_staff))
    
    # extract_period
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_periodtype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_extractteacher_Fails))
    
    # extract_students
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_teachertype_edgecasestudent))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_teachertype_1student)) 
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_teachertype_multi_student))
    
    # extract subject
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_nonacademic_1_student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_nonacademic_multi_student))
    
    # validatetokens
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens_Multi))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens))
    
    # validatetoken2
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens_Subject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens_Student))
    
    # _match_num_chars_same
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_NumCharsSame))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_NumCharsSamelLocation))
    
    # _match_relsize
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RelSize))

    # pre_process_records
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecords))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsNewPeriod))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsPrep4100))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsComputerTime))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsPrep4))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsStaff))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsFriday))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWith))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordStudent))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsSubjectWorkPeriod))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodStudent))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodSubject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriod2))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodStudentTeacherSubject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodStudentSubject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodStudentTeacher))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodWith))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsWorkPeriodWithSubject))    
    
    
    # dbloader
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_All))

    
    # db primary record set
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set_With_Staff))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set_With_Staff_Student))  
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set_Nathaniel))
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Primary_Set_Session))
    
    
    # ######################################################################################################
    # functional tests
    
    # 1 period of 1 prep

    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5Student_WP))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5_1period))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5Computertime))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_Issey))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_with_Prep5_Period1))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Academic_Stan))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Student_3Student))  
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Academic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Student_1Student_1Period))  
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_with_Prep5_Period1_StudentPeter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBInsert_Direct_Nathaniel))

    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    