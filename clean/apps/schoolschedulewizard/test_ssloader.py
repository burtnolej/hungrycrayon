import sys
import os
from os import path as ospath

from ssloader import SSLoader, SSLoaderRuleException, SSLoaderRecordEndException, SSLoaderNoMatchException

from database_table_util import tbl_rows_get, tbl_query
from database_util import Database, tbl_remove
from sswizard_query_utils import _pivotexecfunc
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
        
        self.record = ['830-910','Monday','WP','Amelia',['Nathaniel']]
        
    def test_(self):
        new_record = self.ssloader.validate_tokens(self.record)
        expected_results = ['830-910','Monday','Work Period','Amelia',['Nathaniel']]
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
        
        self.assertEquals(recordtype, 'teacher')
            
    def test_noteacher(self):
        self.inputstr = "Science: Oscar, Peter "
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'noteacher')
        
    def test_noteacher2(self):
        self.inputstr = "Work Period: Oscar, Peter "
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'noteacher')
        
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
        
        self.assertEquals(recordtype, 'teacher')   
        
    def test_teacher_edgecase2(self):
        self.inputstr = "Movement: Shane, Asher, Simon B"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'noteacher')
        
    def test_PERIOD_2(self):
        self.inputstr = "Period 1"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'ignore')

    def test_PERIOD_1(self):
        self.inputstr = "PERIOD 1"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'ignore')
        
    def test_With(self):
        self.inputstr = "Engineering with Paraic"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'staffwith')
        
    def test_teacher_Syno_Match(self):
        self.inputstr = "Humanities Work Period with Johnny"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'wp')  
     
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
        
        expected_results = [['830-910','Monday','ELA','Amelia',[]],
                          ['830-910','Tuesday','Engineering','Paraic',[]]]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecords(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        self.records = ['09/19/16','8:30- 9:10','^','ELA: Nathaniel (Amelia)','^',
                        'Math: CLayton, (Stan)','^','Engineering: Orig, Stephen, Oscar (Paraic)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel']],
                          ['830-910','Tuesday','Math','Stan',['CLayton']],
                          ['830-910','Wednesday','Engineering','Paraic',['Orig','Stephen','Oscar']]]
        
        self.assertListEqual(clean_records,expected_results)
        
    def test_withleadingdows(self):
        
        self.records = ['09/19/16','^','Monday','^','Tuesday','^','8:30- 9:10','^','ELA: Nathaniel (Amelia)','^',
                        'Math: CLayton, (Stan)','^','Engineering: Orig, Stephen, Oscar (Paraic)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel']],
                          ['830-910','Tuesday','Math','Stan',['CLayton']],
                          ['830-910','Wednesday','Engineering','Paraic',['Orig','Stephen','Oscar']]]
        
        #@self.assertListEqual(clean_records,expected_results)
        
    def test_realexample(self):
    
        self.records = ['8:30- 9:10', '&', 'PERIOD 1', '^', 'ELA: Nathaniel (Amelia)', '^', 'Math: CLayton, (Stan)']
    
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel']],
                            ['830-910','Tuesday','Math','Stan',['CLayton']]]

            
        self.assertListEqual(clean_records,expected_results)

class Test_PreProcessRecordsStaff(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
    
        self.records = ['Moira++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Work PEriod: Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','Work Period','Moira',['MacKenzie']],
                          ['830-910','Thursday','Work PEriod','Moira',['Nick']]]
        
        self.assertListEqual(clean_records,expected_results)
        
    def test_newstaffname(self):
    
        self.records = ['Moira++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Work PEriod: Nick',
                        'John++','^','Monday','^','Tuesday','^','Wednesday','^','Thursday','^','Friday','^',
                        '8:30- 9:10','^','^','Work Period: MacKenzie','^','^','Work PEriod: Nick']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Tuesday','Work Period','Moira',['MacKenzie']],
                          ['830-910','Thursday','Work PEriod','Moira',['Nick']],
                          ['830-910','Tuesday','Work Period','John',['MacKenzie']],
                           ['830-910','Thursday','Work PEriod','John',['Nick']]]
        
        self.assertListEqual(clean_records,expected_results)
        
class Test_PreProcessRecordsNewPeriod(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_(self):
        
        # not a real world example as this implies a spreadsheet with 1 day column not 5 
        self.records = ['09/19/16','8:30- 9:10','^','ELA: Nathaniel (Amelia)','9:10- 9:50','^',
                        'Math: CLayton, (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel']],
                          ['910-950','Monday','Math','Stan',['CLayton']]]

        self.assertListEqual(clean_records,expected_results)
        
        
    def test_preceding_newline(self):
        
        # real world example with multiple new lines before an end of cell
        self.records = ['09/19/16','8:30- 9:10','^','ELA: Nathaniel (Amelia)','9:10- 9:50','&','&','^',
                        'Math: CLayton, (Stan)']
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['830-910','Monday','ELA','Amelia',['Nathaniel']],
                          ['910-950','Monday','Math','Stan',['CLayton']]]

        self.assertListEqual(clean_records,expected_results)
        
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
                
        print self.records
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        expected_results = [['1110-1210','Monday','Computer Time','??',self.students],
                            ['1110-1210','Tuesday','Computer Time','??',self.students],
                            ['1110-1210','Wednesday','Computer Time','??',self.students],
                            ['1110-1210','Thursday','Computer Time','??',self.students],
                            ['1110-1210','Friday','Computer Time','??',self.students],
                            ['230-300','Monday','Computer Time','??',self.students],
                            ['230-300','Tuesday','Computer Time','??',self.students],
                            ['230-300','Wednesday','Computer Time','??',self.students],
                            ['230-300','Thursday','Computer Time','??',self.students]]    
        
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
                
        print self.records
        
        clean_records,_,_ = self.ssloader.pre_process_records(self.records)
        
        friday_clean_records = [ record for record in clean_records if record[1] == "Friday"]
                
        expected_results = [['830-910','Friday','Humanities','A',['Orig', 'Jake', 'Nathaniel', 'Stephen']],
                            ['830-910','Friday','Music','D',['Coby', 'THomas', 'Yosef']],
                            ['830-910','Friday','STEM','C',['Tris', 'Ashley', 'Simon', 'Booker', 'Omer']],
                            ['830-910','Friday','ART','B', ['Clayton', 'Bruno', 'Oscar', 'Peter', 'Jack']]]
        
        self.assertListEqual(friday_clean_records,expected_results)

class Test_ValidateTokens(Test_Base):


    def setUp(self):
        Test_Base.setUp(self)
        
    
        
    def test_(self):
        
        record = ['830-910','monday','ELA','amelia',['Nathoniel']]
        
        expected_results = ['830-910','Monday','ELA','Amelia',['Nathaniel']]
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
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', [u'Simon A']], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', ['Liam']]]
            
        
        expected_results =  [['Thea.STEM.Tuesday', 'Tuesday',7,'Thea', 'STEM'], 
                             ['Jess.Humanities.Wednesday', 'Wednesday',6, 'Jess','Humanities']]
            
            
        self.ssloader.dbloader(records)
        
        database = Database(self.databasename)
        with database:
            _,rows,_ = tbl_rows_get(database,'session',['code','dow','period','teacher','subject'])
        
        self.assertListEqual(expected_results,rows)
        
    def test_lesson(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', [u'Simon A']], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', ['Liam']]]
            
        
        expected_results =  [['Simon A', 'TU','100-140','Thea', 'STEM','Thea.STEM.Tuesday'], 
                             ['Liam', 'WE','1210-100', 'Jess','Humanities','Jess.Humanities.Wednesday']]
            
            
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
        
    def test_lesson(self):
        
        expected_results = [['test', u'Nathaniel', u'Clayton', u'Orig', u'Stephen', u'Oscar', u'Peter', u'Jack', u'Jake', u'Bruno', u'Coby', u'Thomas', u'Yosef', u'Tris', u'Ashley', u'Simon A', u'Booker', u'OmerC'], 
                            [u'ELA', 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Math', 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Engineering', 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Work Period', 0, 0, 0, 0, 0, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
                            [u'Work Period', 7, 6, 8, 8, 7, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0], 
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
                            [u'??', 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'OT', 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Chess', 4, 0, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Computer Time', 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Reading', 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Independent Reading', 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            ['test', 44, 45, 44, 43, 45, 47, 45, 46, 44, 4, 4, 4, 4, 4, 4, 4, 4]]

        self.ssloader.ssloader([('prep5data.csv',5,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        
        self.assertListEqual(results,expected_results)
        
    def test_session(self):
        
        expected_results = [['test', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                            [u'Monday', 5, 5, 6, 6, 1, 4, 6, 5, 5, 1], 
                            [u'Tuesday', 6, 8, 5, 6, 1, 5, 7, 5, 5, 1],
                            [u'Wednesday', 4, 6, 5, 5, 1, 5, 7, 5, 5, 1], 
                            [u'Thursday', 6, 8, 5, 7, 1, 4, 6, 5, 5, 1],
                            [u'Friday', 4, 5, 4, 4, 1, 0, 0, 0, 0, 0], 
                            ['test', 25, 32, 25, 28, 5, 18, 26, 20, 20, 4]]

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
                           [u'Work Period', 2, 3, 1, 4, 2, 4, 1, 3, 3, 3, 3, 4, 3, 2, 1, 2, 3, 1], 
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
                            [u'Work Period', 7, 8, 4, 8, 9, 9, 6, 8, 7, 9, 7, 7, 5, 8, 7, 8, 8, 10, 7, 9, 9, 8, 8, 7, 6, 1, 0, 6], 
                            [u'Independent Reading', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Core', 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'History', 0, 0, 2, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Chess', 0, 0, 0, 1, 2, 4, 1, 3, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Counseling', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], 
                            [u'Movement', 0, 1, 0, 0, 0, 0, 5, 1, 2, 1, 0, 3, 1, 3, 2, 3, 3, 3, 0, 0, 0, 0, 0, 3, 1, 0, 3, 1], 
                            [u'Psychology Reading', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Psychology', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                            [u'Independent Art', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
                            ['test', 13, 17, 10, 20, 21, 16, 22, 21, 16, 23, 14, 20, 11, 17, 14, 16, 15, 18, 11, 13, 12, 15, 14, 17, 11, 2, 3, 10]]


        self.ssloader.ssloader([('staffdata.csv',-1,True)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'test','student','subject','lesson',distinct=True,master=False)
        self.assertListEqual(results,expected_results)

    def test_session(self):
        expected_results = [['test', 1, 2, 3, 4, 6, 7, 8, 9], 
                            [u'Thursday', 8, 8, 9, 9, 6, 9, 8, 9], 
                            [u'Monday', 6, 8, 8, 8, 8, 8, 8, 8], 
                            [u'Tuesday', 7, 8, 10, 9, 9, 8, 9, 9], 
                            [u'Wednesday', 7, 8, 9, 8, 9, 8, 8, 9], 
                            ['test', 28, 32, 36, 34, 32, 33, 33, 35]]

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

        expected_results = [['complete','WE','830-910','Issey.Work Period.Wednesday','Issey'],
                            ['incomplete','MO','830-910','??.Work Period.Monday','??'],
                            ['incomplete','TU','830-910','??.Work Period.Tuesday','??'],
                            ['incomplete','WE','830-910','??.Work Period.Wednesday','??'],
                            ['incomplete','TH','830-910','??.Work Period.Thursday','??'],
                            ['complete','FR','830-910','B.Art.Friday','B']]
    
        self.assertListEqual(rows,expected_results)

class Test_DBLoader_Academic_Stan(unittest.TestCase):
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
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename)  
        
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.inputfile = "test_academic_1period_3teachers.csv"
        fileasstring = self.ssloader.file2string("test_academic_1period_3teachers.csv")

        records = self.ssloader.string2records(fileasstring)

        self.clean_records,_,_ = self.ssloader.pre_process_records(records)
        
        self.validated_clean_records = []
        for clean_record in self.clean_records:
            self.validated_clean_records.append(self.ssloader.validate_tokens(clean_record))

    '''def test_clean_records(self):
        
        expected_results = [[u'830-910', 'Monday', '??', u'Stan', ['Clayton']],
                            [u'830-910', 'Tuesday', '??', u'Stan', ['Nathaniel']],          
                            [u'830-910', 'Wednesday', '??', u'Stan', ['Clayton']],                
                            [u'830-910', 'Thursday', '??', u'Stan', ['Nathaniel']],               
                            [u'830-910', 'Monday', '??', u'Amelia', ['Nathaniel']],                                      
                            [u'830-910', 'Tuesday', 'Work Period', u'Amelia', ['Peter','Jack']],                                        
                            [u'830-910', 'Wednesday', '??', u'Amelia', ['Nathaniel']],                                                 
                            [u'830-910', 'Thursday', 'Work Period', u'Amelia', ['Jack']],
                            [u'830-910', 'Monday', '??', u'Paraic', []],    
                            [u'830-910', 'Tuesday', '??', u'Paraic', ['Jake']],      
                            [u'830-910', 'Wednesday', '??', u'Paraic', []],    
                            [u'830-910', 'Thursday', '??', u'Paraic', ['Jake']]]
        
        self.assertListEqual(expected_results,self.clean_records)'''
        

    def test_lesson(self):

        expected_results = [[u'complete', u'MO', u'830-910', u'Stan.Math.Monday', u'Clayton'],
                            [u'complete', u'TU', u'830-910', u'Stan.Math.Tuesday', u'Nathaniel'],
                            [u'complete', u'WE', u'830-910', u'Stan.Math.Wednesday', u'Clayton'], 
                            [u'complete', u'TH', u'830-910', u'Stan.Math.Thursday', u'Nathaniel'],
                            [u'complete', u'MO', u'830-910', u'Amelia.ELA.Monday', u'Nathaniel'], 
                            [u'complete', u'TU', u'830-910', u'Amelia.??.Tuesday', u'Peter'], 
                            [u'complete', u'TU', u'830-910', u'Amelia.??.Tuesday', u'Jack'], 
                            [u'complete', u'WE', u'830-910', u'Amelia.ELA.Wednesday', u'Nathaniel'],
                            [u'complete', u'TH', u'830-910', u'Amelia.??.Thursday', u'Jack'], 
                            [u'complete', u'TU', u'830-910', u'Paraic.Science.Tuesday', u'Jake'], 
                            [u'complete', u'TH', u'830-910', u'Paraic.Science.Thursday', u'Jake']]
        
        
        self.ssloader.dbupdater(self.validated_clean_records)   
    
        cols = ['status','dow','period','session','student']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['source','=',"\"" + "test_academic_1period_3teachers.csv" + "\""]])
            
        #results = _pivotexecfunc(self.ssloader.database,'student','subject','lesson')
        
        self.assertListEqual(expected_results,rows)
        
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
        self.ssloader.ssloader([('prep5data.csv',5,True)],self.databasename)  
        
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.inputfile = "academic.csv"
        fileasstring = self.ssloader.file2string("academic.csv")

        records = self.ssloader.string2records(fileasstring)

        self.clean_records,_,_ = self.ssloader.pre_process_records(records)
        
        self.validated_clean_records = []
        for clean_record in self.clean_records:
            self.validated_clean_records.append(self.ssloader.validate_tokens(clean_record))
            
    def test_(self):
        
        # rest are missing because session not created from a previous load
        expected_results = [[u'complete', u'MO', u'830-910', u'Stan.Math.Monday', u'Clayton'], 
                            [u'complete', u'MO', u'910-950', u'Stan.??.Monday', u'Simon A'], 
                            [u'complete', u'MO', u'1030-1110', u'Stan.??.Monday', u'Yosef'], 
                            [u'complete', u'MO', u'1210-100', u'Stan.??.Monday', u'Booker'], 
                            [u'complete', u'MO', u'100-140', u'Stan.??.Monday', u'Thomas'], 
                            [u'complete', u'MO', u'140-220', u'Stan.??.Monday', u'Ashley'],
                            [u'complete', u'MO', u'220-300', u'Stan.??.Monday', u'Coby'], 
                            [u'complete', u'TU', u'830-910', u'Stan.Math.Tuesday', u'Nathaniel'], 
                            [u'complete', u'TU', u'910-950', u'Stan.??.Tuesday', u'Bruno'], 
                            [u'complete', u'TU', u'1030-1110', u'Stan.Math.Tuesday', u'Peter'],
                            [u'complete', u'TU', u'1210-100', u'Stan.??.Tuesday', u'Jake'], 
                            [u'complete', u'TU', u'100-140', u'Stan.Math.Tuesday', u'Orig'], 
                            [u'complete', u'TU', u'140-220', u'Stan.Math.Tuesday', u'Oscar'], 
                            [u'complete', u'TU', u'220-300', u'Stan.??.Tuesday', u'Jack'], 
                            [u'complete', u'WE', u'830-910', u'Stan.Math.Wednesday', u'Clayton'], 
                            [u'complete', u'WE', u'910-950', u'Stan.??.Wednesday', u'Simon A'], 
                            [u'complete', u'WE', u'1030-1110', u'Stan.??.Wednesday', u'Yosef'], 
                            [u'complete', u'WE', u'1210-100', u'Stan.??.Wednesday', u'Booker'], 
                            [u'complete', u'WE', u'100-140', u'Stan.??.Wednesday', u'Thomas'], 
                            [u'complete', u'WE', u'140-220', u'Stan.??.Wednesday', u'Ashley'], 
                            [u'complete', u'WE', u'220-300', u'Stan.??.Wednesday', u'Coby'], 
                            [u'complete', u'TH', u'830-910', u'Stan.Math.Thursday', u'Nathaniel'], 
                            [u'complete', u'TH', u'910-950', u'Stan.Math Activity Period.Thursday', u'Bruno'], 
                            [u'complete', u'TH', u'1030-1110', u'Stan.??.Thursday', u'Peter'],
                            [u'complete', u'TH', u'1210-100', u'Stan.??.Thursday', u'Jake'], 
                            [u'complete', u'TH', u'100-140', u'Stan.Math.Thursday', u'Orig'], 
                            [u'complete', u'TH', u'140-220', u'Stan.Math.Thursday', u'Oscar'], 
                            [u'complete', u'TH', u'220-300', u'Stan.??.Thursday', u'Jack']]


        self.ssloader.dbupdater(self.validated_clean_records)   
    
        cols = ['status','dow','period','session','student']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',cols,[['source','=',"\"" + "academic.csv" + "\""],
                                                                 ['teacher','=',"\"" + "Stan" + "\""]])

        self.assertListEqual(rows,expected_results)
            
        cols = ['code']
          
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',cols,[['teacher','=',"\"" + "Stan" + "\""],
                                                                  ['source','=',"\"" + "academic.csv" + "\""]])

        self.assertEqual(len(rows),18)
        
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

class Test_DBLoader_Primary_Record_Set(unittest.TestCase):
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
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename)  
        
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.inputfile = "test_academic_1period_3teachers.csv"
        fileasstring = self.ssloader.file2string("test_academic_1period_3teachers.csv")

        records = self.ssloader.string2records(fileasstring)

        self.clean_records,_,_ = self.ssloader.pre_process_records(records)
        
        self.validated_clean_records = []
        for clean_record in self.clean_records:
            self.validated_clean_records.append(self.ssloader.validate_tokens(clean_record))
            
        self.ssloader.dbupdater(self.validated_clean_records)

    
    def _getprimarykeyhash(self,pred,predval):
        
        cols = ['dow','period','student']
        hashmap = self.ssloader.primary_record_set()
        results = []      
        for hashkey in hashmap:
            
            hashmap[hashkey].pop('source')

            d = dict(zip(cols,hashkey.split(".")))

            if d[pred] == predval:
                hashmap[hashkey].pop('student')
                results.append(hashmap[hashkey].values())
           
        results.sort()
          
        return results
        
    def test_Nathaniel(self):

        expected_results = [['primary',['Amelia'],['ELA'],'830-910','MO'],
                            ['primary',['Stan'],['Math'],'830-910','TU'],
                            ['primary',['Amelia'],['ELA'],'830-910','WE'],
                            ['primary',['Stan'],['Math'],'830-910','TH'],
                            ['primary',['A'],['Humanities'],'830-910','FR']]

        expected_results.sort()
        
        self.assertListEqual(self._getprimarykeyhash('student','Nathaniel'),expected_results)
        
    def test_Friday(self):
        
        expected_results =[['primary',['A'],['Humanities'],'830-910','FR'],
                           ['primary',['B'],['Art'],'830-910','FR'],
                           ['primary',['A'],['Humanities'],'830-910','FR'],
                           ['primary',['A'],['Humanities'],'830-910','FR'],
                           ['primary',['B'],['Art'],'830-910','FR'],
                           ['primary',['B'],['Art'],'830-910','FR'],
                           ['primary',['B'],['Art'],'830-910','FR'],
                           ['primary',['A'],['Humanities'],'830-910','FR'],
                           ['primary',['B'],['Art'],'830-910','FR'],
                           ['primary',['D'],['Music'],'830-910','FR'],
                           ['primary',['D'],['Music'],'830-910','FR'],
                           ['primary',['D'],['Music'],'830-910','FR'],
                           ['primary',['C'],['STEM'],'830-910','FR'],
                           ['primary',['C'],['STEM'],'830-910','FR'],
                           ['primary',['C'],['STEM'],'830-910','FR'],
                           ['primary',['C'],['STEM'],'830-910','FR'],
                           ['primary',['C'],['STEM'],'830-910','FR']]
        
        expected_results.sort()
        
        self.assertListEqual(self._getprimarykeyhash('dow','FR'),expected_results)
    
    def test_FOrig(self):
         
        expected_results =[['primary',['Paraic'],['Engineering'],'830-910','MO'],
                           ['unset',['??'],['Student News'],'830-910','TU'],
                           ['primary',['Paraic'],['Engineering'],'830-910','WE'],
                           ['unset',['??'],['Student News'],'830-910','TH'],
                           ['primary',['A'],['Humanities'],'830-910','FR']]
        
        expected_results.sort()
        
        self.assertListEqual(self._getprimarykeyhash('student','Orig'),expected_results)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")

    
class Test_DBLoader_Primary_Record_Set_With_Staff(unittest.TestCase):
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
        self.ssloader.ssloader([('prep5data_test1period.csv',5,True)],self.databasename)  
        
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.ssloader([('staffdata_830910.csv',-1,True)],self.databasename)  
     
        self.ssloader = SSLoader("test_ssloader")
        self.ssloader.inputfile = "test_academic_1period_3teachers.csv"
        fileasstring = self.ssloader.file2string("test_academic_1period_3teachers.csv")

        records = self.ssloader.string2records(fileasstring)

        self.clean_records,_,_ = self.ssloader.pre_process_records(records)
        
        self.validated_clean_records = []
        for clean_record in self.clean_records:
            self.validated_clean_records.append(self.ssloader.validate_tokens(clean_record))
            
        self.ssloader.dbupdater(self.validated_clean_records)

    
    def _getprimarykeyhash(self,pred,predval):
        
        cols = ['dow','period','student']
        hashmap = self.ssloader.primary_record_set()
        results = []      
        for hashkey in hashmap:
            
            hashmap[hashkey].pop('source')

            d = dict(zip(cols,hashkey.split(".")))

            if d[pred] == predval:
                hashmap[hashkey].pop('student')
                results.append(hashmap[hashkey].values())
           
        results.sort()
          
        return results            

    def test_FOrig(self):

        expected_results = [['primary', [u'A'], [u'Humanities'], u'830-910', u'FR'],
                            ['primary', [u'Issey'], [u'Student News'], u'830-910', u'TH'],
                            ['primary', [u'Johnny'], [u'Student News'], u'830-910', u'TU'],
                            ['primary', [u'Paraic'], [u'Engineering'], u'830-910', u'MO'],
                            ['primary', [u'Paraic'], [u'Engineering'], u'830-910', u'WE']]


        
        expected_results.sort()
        
        self.assertListEqual(self._getprimarykeyhash('student','Orig'),expected_results)


    def test_Bruno(self):        

        expected_results = [['unset', [u'??'], [u'Movement'], u'830-910', u'MO'],
                            ['primary', [u'Johnny'], [u'Student News'], u'830-910', u'TU'],
                            ['unset', ['??'], [u'Core'], u'830-910', u'TH'],
                            ['primary', [u'B'], [u'Art'], u'830-910', u'FR']]
        
        expected_results.sort()
        
        self.assertListEqual(self._getprimarykeyhash('student','Bruno'),expected_results)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")
        
class Test_DBLoader_Primary_Record_Set_Nathaniel(unittest.TestCase):
    def setUp(self):  

        self.databasename = "test_ssloader_prset_nathaniel"
        self.database = Database(self.databasename)
        self.ssloader = SSLoader("test_ssloader_prset_nathaniel")
    
    def _getprimarykeyhash(self,pred,predval):
        
        cols = ['dow','period','student']
        hashmap = self.ssloader.primary_record_set()
        results = []      
        for hashkey in hashmap:
            
            hashmap[hashkey].pop('source')

            d = dict(zip(cols,hashkey.split(".")))

            if d[pred] == predval:
                hashmap[hashkey].pop('student')
                results.append(hashmap[hashkey].values())
           
        results.sort()
          
        return results            

    def test_Nathaniel(self):
        
        # expected_results are hand generated from source production files and presented in Prep5_Nathaniel_expected_results.csv
        # the expected_results do not necessarilly match the individual student schedule source prod files as they are known to not always reconcile
        
        expected_results = [['primary',["Amelia"],["ELA"],"830-910","MO"],
                            ['unset',["??"],["Core"],"910-950","MO"],
                            ['primary',["Karolina"],["Work Period"],"950-1030","MO"],
                            ['primary',[u"Dylan"],[u"Activity Period"],u"1030-1110",u"MO"],
                            ['unset',["??"],["Computer Time"],"1110-1210","MO"],
                            ['primary',["Paraic"],["Science"],"1210-100","MO"],
                            ['primary',["Rahul"],["Chess"],"100-140","MO"],
                            ['primary',["Johnny"],["Work Period"],"140-220","MO"],
                            ['unset',["??"],["Speech"],"220-300","MO"],
                            ['unset',["??"],["Computer Time"],"300-330","MO"],
                            ['primary',["Stan"],["Math"],"830-910","TU"],
                            ['primary',["Dylan"],["Work Period"],"910-950","TU"],
                            ['primary',["Aaron"],["Activity Period"],"950-1030","TU"],
                            ['primary',["Rahul"],["Chess"],"1030-1110","TU"],
                            ['unset',["??"],["Computer Time"],"1110-1210","TU"],
                            ['primary',["Samantha"],["History"],"1210-100","TU"],
                            ['primary',["Karolina"],["Work Period"],"100-140","TU"],
                            ['unset',["??"],["Movement"],"140-220","TU"],
                            ['unset',["??"],["Student News"],"220-300","TU"],
                            ['unset',["??"],["Computer Time"],"300-330","TU"],
                            ['primary',["Amelia"],["ELA"],"830-910","WE"],
                            ['primary',["Moira"],["Work Period"],"910-950","WE"],
                            ['unset',["??"],["OT"],"950-1030","WE"],
                            ['primary',["Issey"],["Activity Period"],"1030-1110","WE"],
                            ['unset',["??"],["Computer Time"],"1110-1210","WE"],
                            ['primary',["Paraic"],["Science"],"1210-100","WE"],
                            ['primary',["Rahul"],["Chess"],"100-140","WE"],
                            ['primary',["Issey"],["Work Period"],"140-220","WE"],
                            ['primary',["Alexa"],["Counseling"],"220-300","WE"],
                            ['unset',["??"],["Computer Time"],"300-330","WE"],
                            ['primary',["Stan"],["Math"],"830-910","TH"],
                            ['unset',["??"],["Core"],"910-950","TH"],
                            ['primary',["Issey"],["Work Period"],"950-1030","TH"],
                            ['primary',["Rahul"],["Chess"],"1030-1110","TH"],
                            ['unset',["??"],["Computer Time"],"1110-1210","TH"],
                            ['primary',["Samantha"],["History"],"1210-100","TH"],
                            ['primary',["Aaron"],["Work Period"],"100-140","TH"],
                            ['unset',["??"],["Movement"],"140-220","TH"],
                            ['unset',["??"],["Student News"],"220-300","TH"],
                            ['unset',["??"],["Computer Time"],"300-330","TH"],
                            ['primary',["A"],["Humanities"],"830-910","FR"],
                            ['unset',["??"],["Music"],"910-950","FR"],
                            ['unset',["??"],["STEM"],"950-1030","FR"],
                            ['unset',["??"],["Art"],"1030-1110","FR"],
                            ['unset',["??"],["Computer Time"],"1110-1210","FR"]]
                              
        expected_results.sort()
            
        results = self._getprimarykeyhash('student','Nathaniel') 
        
        self.assertListEqual(expected_results,results)



class Test_DBInsert_Direct(unittest.TestCase):
    def setUp(self):  

        #Test_Base.setUp(self)
        
        self.databasename = "test_ssloader"

        self.database = Database(self.databasename)
        
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass
        

    def test_session(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', u'Simon A','1-on-1'], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', 'Liam','1-on-1']]
            
        
        expected_results =  [['Thea.STEM.Tuesday', 'Tuesday',7,'Thea', 'STEM'], 
                             ['Jess.Humanities.Wednesday', 'Wednesday',6, 'Jess','Humanities']]
            
        expected_results.sort()
        
        dbinsert_direct(self.database,records,'session','test')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'session',['code','dow','period','teacher','subject'])
        
        rows.sort()
         
        self.assertListEqual(expected_results,rows)
        
    def test_lesson(self):
        
        records = [['100-140', 'TU', 'STEM', 'Thea', u'Simon A','1-on-1'], 
                  ['1210-100', 'WE', 'Humanities', 'Jess', 'Liam','1-on-1']]
            
        
        expected_results =  [['Simon A', 'TU','100-140','Thea', 'STEM','Thea.STEM.Tuesday'], 
                             ['Liam', 'WE','1210-100', 'Jess','Humanities','Jess.Humanities.Wednesday']]
        

        expected_results.sort()
        
        dbinsert_direct(self.database,records,'lesson','test')
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'lesson',['student','dow','period','teacher','subject','session'])
        
        rows.sort()
        
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")


class Test_DBInsert_Direct_Nathaniel(unittest.TestCase):
    def setUp(self):  

        #self.databasename = "test_ssloader"
        self.databasename = "test_ssloader_insertdirect_nathaniel"
        self.database = Database(self.databasename)
        
        #files = [('prep5data.csv',5,True),('prep4data.csv',4,True),('prep6data.csv',6,True),('staffdata.csv',-1,True),
        #         ('academic.csv',-1,False)]
    
        #ssloader = SSLoader(self.databasename)
        #ssloader.run(self.databasename,files)

                   
    def test_(self):

        expected_results = [["Nathaniel","MO","TU","WE","TH","FR"],                                                                                                                                                                                                                
                            ["830-910","ELA,Amelia","Math,Stan","ELA,Amelia","Math,Stan","Humanities,A"],                                                                                                                                                                                                     
                            ["910-950","Core,??","Work Period,Dylan","Work Period,Moira","Core,??","Music,??"],                                                                                                                                                                                               
                            ["950-1030","Work Period,Karolina","Activity Period,Aaron","OT,??","Work Period,Issey","STEM,??"],                                                                                                                                                                                
                            ["1030-1110","Activity Period,Dylan","Chess,Rahul","Activity Period,Issey","Chess,Rahul","Art,??"],                                                                                                                                                                               
                            ["1110-1210","Computer Time,??","Computer Time,??","Computer Time,??","Computer Time,??","Computer Time,??"],                                                                                                                                                                     
                            ["1210-100","Science,Paraic","History,Samantha","Science,Paraic","History,Samantha",0],                                                                                                                                                                                         
                            ["100-140","Chess,Rahul","Work Period,Karolina","Chess,Rahul","Work Period,Aaron",0],                                                                                                                                                                                            
                            ["140-220","Work Period,Johnny","Movement,??","Work Period,Issey","Movement,??",0],                                                                                                                                                                                            
                            ["220-300","Speech,??","Student News,??","Counseling,Alexa","Student News,??",0],                                                                                                                                                                                           
                            ["300-330","Computer Time,??","Computer Time,??","Computer Time,??","Computer Time,??",0]]
        
        results = _pivotexecfunc(self.database,'Nathaniel','dow','period','lesson',False,True,[['student','=','Nathaniel']],"subject,teacher")
        
        self.assertListEqual(expected_results, results[:-1])
        
    def tearDown(self):
        pass
            
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation))    
    
    #unittest.TextTestRunner(verbosity=2).run(suite) 
    #exit()
    
    # #####################################################################################################
    # unit tests=
    
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
    
    
    # dbloader
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_All))
    
    # dbinsert_direct
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBInsert_Direct))
    
    # db primary record set
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set_With_Staff))

    
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Primary_Record_Set_Nathaniel))
    
    
    # ######################################################################################################
    # functional tests
    
    # 1 period of 1 prep
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5_1period))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5Computertime))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_Issey))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_with_Prep5_Period1))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Academic_Stan))
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Academic))
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBInsert_Direct_Nathaniel))

    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


