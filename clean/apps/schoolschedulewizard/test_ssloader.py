import sys
import os
from os import path as ospath

from ssloader import SSLoader, SSLoaderRuleException, SSLoaderRecordEndException, SSLoaderNoMatchException

from database_table_util import tbl_rows_get, tbl_query
from database_util import Database, tbl_remove
from sswizard_query_utils import _pivotexecfunc

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
        self.rules = [(":",1),("(",1),(")",1)]
        self.inputstr = "ELA: Nathaniel (Amelia)"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_teachertype_multi_student(self):
        self.rules = [(":",1),("(",1),(")",1)]
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
        self.rules = [(":",1),("(",0),(")",0)]
        self.inputstr = "ELA: Nathaniel"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_staff(self):
        self.rules = [("+",2)]
        self.inputstr = "Moira++"
        self.assertTrue(self.ssloader.appyrules(self.inputstr,self.rules))
        
        
class Test_ApplyRules_Fails(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        
    def test_no_colon(self):
        
        self.inputstr = "ELA Nathaniel (Amelia)"
        self.rules = [(":",1),("(",1),(")",1)]
    
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
            
    def test_more_than_one_colon(self):
        
        self.inputstr = "ELA :Nathaniel : (Amelia)"
        self.rules = [(":",1),("(",1),(")",1)]
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
            
    def test_no_open_bracket(self):
        
        self.inputstr = "ELA :Nathaniel : Amelia)"
        self.rules = [(":",1),("(",1),(")",1)]
        self.assertFalse(self.ssloader.appyrules(self.inputstr,self.rules))
        
    def test_no_close_bracket(self):
        
        self.inputstr = "ELA :Nathaniel : (Amelia"
        self.rules = [(":",1),("(",1),(")",1)]
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
        
        self.valid_students = self.ssloader.loadrefobjects('quadref','student')
        
    '''def test_exact_match(self):
        
        validated_token = self.ssloader.validate_token('Cleyton',self.valid_students)
        
        self.assertEqual(validated_token,'Clayton')'''
        
    def test_extra_letter(self):
        
        validated_token = self.ssloader.validate_token2('Simon A',self.valid_students)
        
        self.assertEqual(validated_token,'Simon A')
  
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
        
    def test_date(self):
        self.inputstr =  "09/19/16"
        recordtype = self.ssloader.identify_record(self.inputstr)
        self.assertEquals(recordtype, 'date')
        
    def test_period(self):
        self.inputstr = "\"8:30- 9:10"
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'period')
        
    def test_teacher_edgecase(self):
        self.inputstr = "Science: Jake (Paraic) \""
        recordtype = self.ssloader.identify_record(self.inputstr)
        
        self.assertEquals(recordtype, 'teacher')        
     
class Test_RecordIdentifcation_realsample(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        fileasstring = self.ssloader.file2string("prep5data_test.csv")
        self.records = self.ssloader.string2records(fileasstring)

    def test_(self):
        
        results = {'noteacher':0,'teacher':0,'date':0,'period':0,'SSLoaderNoRulesMatchException':0,
                   'SSLoaderMultiRuleMatchException':0,'block':0,'eol':0,'blankrow':0,'_ENDCELL_':0,'_CRETURN_':0}
        
        for record in self.records:
            try:
                recordtype = self.ssloader.identify_record(record)
            except Exception, e:
                results[e.__class__.__name__]+=1
                continue
            results[recordtype] += 1


        self.assertEquals(results['noteacher'],5)
        self.assertEquals(results['teacher'],5)
        self.assertEquals(results['SSLoaderNoRulesMatchException'],6)
        self.assertEquals(results['period'],1)
        
class Test_RecordIdentifcation_realsample2(Test_Base):
    def setUp(self):
        Test_Base.setUp(self)
        fileasstring = self.ssloader.file2string("prep5data_miss-day-terminator.csv")
        self.records = self.ssloader.string2records(fileasstring)

    def test_(self):
        
        results = {'noteacher':0,'teacher':0,'date':0,'period':0,'SSLoaderNoRulesMatchException':0,
                   'SSLoaderMultiRuleMatchException':0,'block':0,'eol':0,'_ENDCELL_':0,'blankrow':0}
        
        for record in self.records:
            try:
                recordtype = self.ssloader.identify_record(record)
            except Exception, e:
                results[e.__class__.__name__]+=1
                continue
            results[recordtype] += 1
        print results
           
        
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
        
    '''def test_prep4(self):
        
        expected_results = {'Bruno': 9,'Stephen' :9,'Nathaniel': 9,'Jake': 9,'Oscar': 9,
                            'Clayton': 9,'Jack': 9,'Peter': 9,'Orig': 9}      

        self.ssloader.ssloader(['prep5data_testcomputertime.csv'],self.databasename)
        
        students = [name for name,prep in self.ssloader.prepmap.iteritems() if prep == "5"] 

        result=OrderedDict()
        with self.ssloader.database:
            
            for student in students:
                exec_str = "select count(*) from lesson "
                exec_str += "where student = {0} ".format("\""+student+"\"")             
                
                _,queryresults,_ = tbl_query(self.ssloader.database,exec_str)
                try:
                    result[student] = int(queryresults[0][0])
                except:
                    result[student] =0
                    
        self.assertEqual(result,expected_results)'''
        
    def test_session(self):
        
        expected_results = [['', 5, 9], [u'Monday', 1, 1], [u'Tuesday', 1, 1], [u'Wednesday', 1, 1], [u'Thursday', 1, 1], [u'Friday', 1, 0], ['', 5, 4]]
        self.ssloader.ssloader(['prep5data_testcomputertime.csv'],self.databasename)
        results =  _pivotexecfunc(self.ssloader.database,'period','dow','session',5)
        self.assertListEqual(results,expected_results)
        

    def test_lesson(self):
        
        expected_results = [['', u'Bruno', u'Clayton', u'Jack', u'Jake', u'Nathaniel', u'Orig', u'Oscar', u'Peter', u'Stephen'], [u'Computer Time', 9, 9, 9, 9, 9, 9, 9, 9, 9], ['', 9, 9, 9, 9, 9, 9, 9, 9, 9]]
        self.ssloader.ssloader(['prep5data_testcomputertime.csv'],self.databasename)
        results =  _pivotexecfunc(self.ssloader.database,'student','subject','lesson',5)

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
        
        expected_results = [['', u'Nathaniel', u'Clayton', u'Orig', u'Stephen', u'Oscar', u'Peter', u'Jack', u'Jake', u'Bruno', u'Coby', u'Thomas', u'Yosef', u'Tris', u'Ashley', u'Simon A', u'Booker', u'OmerC'], 
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
                            ['', 5, 5, 5, 5, 5, 5, 5, 5, 4, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.ssloader.ssloader([('prep5data_test1period.csv',5)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'student','subject','lesson')

        self.assertListEqual(results,expected_results)
        
    def test_session(self):
        
        expected_results = [['', 1], 
                            [u'Monday', 5], 
                            [u'Tuesday', 6], 
                            [u'Wednesday', 4], 
                            [u'Thursday', 6], 
                            [u'Friday', 4], 
                            ['', 25]]


        self.ssloader.ssloader([('prep5data_test1period.csv',5)],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'period','dow','session')

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
        
        expected_results = [['', u'Nathaniel', u'Clayton', u'Orig', u'Stephen', u'Oscar', u'Peter', u'Jack', u'Jake', u'Bruno', u'Coby', u'Thomas', u'Yosef', u'Tris', u'Ashley', u'Simon A', u'Booker', u'OmerC'], 
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
                            ['', 44, 45, 44, 43, 45, 47, 45, 46, 44, 4, 4, 4, 4, 4, 4, 4, 4]]

        self.ssloader.ssloader(['prep5data.csv'],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'student','subject','lesson',5)
        
        self.assertListEqual(results,expected_results)
        
    def test_session(self):
        
        expected_results = [['', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                            [u'Monday', 5, 5, 6, 6, 1, 4, 6, 5, 5, 1], 
                            [u'Tuesday', 6, 8, 5, 6, 1, 5, 7, 5, 5, 1],
                            [u'Wednesday', 4, 6, 5, 5, 1, 5, 7, 5, 5, 1], 
                            [u'Thursday', 6, 8, 5, 7, 1, 4, 6, 5, 5, 1],
                            [u'Friday', 4, 5, 4, 4, 1, 0, 0, 0, 0, 0], 
                            ['', 25, 32, 25, 28, 5, 18, 26, 20, 20, 4]]

        self.ssloader.ssloader(['prep5data.csv'],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'period','dow','session',5)
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
        
        expected_results = [['', u'OmerC', u'Ashley', u'Tristan', u'Yosef', u'Coby', u'Nathaniel', u'Clayton', u'Jake', u'Peter', u'Thomas', u'Simon A', u'Orig', u'Jack', u'Bruno', u'Nick', u'Stephen', u'Shane', u'Asher', u'Simon B', u'Liam', u'Luke', u'Mackenzie', u'Lucy', u'Oscar', u'Booker', u'Tris', u'Donovan'], 
                            [u'ELA', 1, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Activity Period', 4, 5, 2, 7, 5, 3, 5, 5, 3, 5, 4, 1, 4, 3, 2, 3, 2, 3, 2, 1, 1, 1, 2, 4, 2, 0, 1], 
                            [u'Student News', 1, 3, 1, 2, 3, 0, 3, 1, 3, 2, 0, 5, 1, 3, 3, 2, 0, 0, 2, 3, 2, 3, 4, 3, 1, 0, 2], 
                            [u'Debate', 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Work Period', 7, 8, 4, 8, 9, 8, 5, 8, 7, 9, 7, 7, 5, 8, 6, 8, 8, 10, 7, 9, 9, 6, 7, 7, 6, 1, 6], 
                            [u'??', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Core', 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'History', 0, 0, 2, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Chess', 0, 0, 0, 1, 2, 4, 1, 3, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            [u'Counseling', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                            [u'Movement', 0, 1, 0, 0, 0, 0, 5, 0, 3, 1, 0, 3, 1, 3, 2, 3, 3, 3, 0, 0, 0, 0, 0, 3, 1, 0, 1], 
                            [u'Psychology Reading', 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [u'Psychology', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
                            [u'Independent Art', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                            ['', 13, 17, 10, 20, 21, 15, 21, 20, 17, 23, 14, 20, 11, 17, 13, 16, 15, 18, 11, 13, 12, 12, 13, 17, 11, 2, 10]]


        self.ssloader.ssloader(['staffdata.csv'],self.databasename)        
        results = _pivotexecfunc(self.ssloader.database,'student','subject','lesson',5)
        print results
        #self.assertListEqual(results,expected_results)

    '''def test_session(self):
        expected_results = [['', 2, 3, 6, 7, 8, 9, 1, 4], 
                            [u'Monday', 6, 4, 4, 7, 1, 5, 3, 6], 
                            [u'Tuesday', 6, 4, 2, 3, 5, 5, 4, 6], 
                            [u'Wednesday', 6, 7, 3, 4, 4, 3, 2, 4], 
                            [u'Thursday', 6, 7, 2, 6, 5, 6, 2, 4], 
                            ['', 24, 22, 11, 20, 15, 19, 11, 20]]


        self.ssloader.ssloader(['staffdata.csv'],self.databasename)
        results = _pivotexecfunc(self.ssloader.database,'period','dow','session',5)
        self.assertListEqual(results,expected_results)'''
        
            
class Test_DBLoader_Staff_with_Prep5(Test_Base):
    def setUp(self):
        self.databasename = "test_ssloader"
        self.database = Database(self.databasename)
        try:
            with self.database:
                tbl_remove(self.database,'lesson')
                tbl_remove(self.database,'session')
        except:
            pass

    def test_(self):

        self.ssloader = SSLoader("test_ssloader",-1)        
        self.ssloader.ssloader(['staffdata.csv'],self.databasename)
        self.ssloader = SSLoader("test_ssloader",5)
        self.ssloader.ssloader(['prep5data.csv'],self.databasename) 

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

    def test_(self):

        self.ssloader = SSLoader("test_ssloader",-1)        
        self.ssloader.ssloader(['staffdata_1period_Issey.csv'],self.databasename)
        self.ssloader = SSLoader("test_ssloader",5)
        self.ssloader.ssloader(['prep5data_test1period.csv'],self.databasename) 

class Test_DBLoader_Academic(unittest.TestCase):
    def setUp(self):    
    
        ssloader = SSLoader("test_ssloader")
        ssloader.inputfile = "academic.csv"
        fileasstring = ssloader.file2string("academic.csv")

        records = ssloader.string2records(fileasstring)

        self.clean_records,_,_ = ssloader.pre_process_records(records)
        
        self.validated_clean_records = []
        for clean_record in self.clean_records:
            self.validated_clean_records.append(ssloader.validate_tokens(clean_record))
            
        ssloader.dbupdater(self.validated_clean_records)

    def test_(self):
        
        expected_results = [[u'830-910', 'Monday', '??', u'Stan', ['Clayton']],
        [u'910-950', 'Monday', '??', u'Stan', ['Simon A']],
        [u'1030-1110', 'Monday', '??', u'Stan', ['Yosef']],
        [u'1210-100', 'Monday', '??', u'Stan', ['Booker']],
        [u'100-140', 'Monday', '??', u'Stan', ['Thomas']],
        [u'140-220', 'Monday', '??', u'Stan', ['Ashley']],
        [u'220-300', 'Monday', '??', u'Stan', [u'Coby']],
        [u'830-910', 'Tuesday', '??', u'Stan', ['Nathaniel']],
        [u'910-950', 'Tuesday', u'Activity Period', u'Stan', ['Bruno']],
        [u'1030-1110', 'Tuesday', '??', u'Stan', ['Peter']],
        [u'1210-100', 'Tuesday', '??', u'Stan', ['Jake']],
        [u'100-140', 'Tuesday', '??', u'Stan', ['Orig']],
        [u'140-220', 'Tuesday', '??', u'Stan', ['Oscar']],
        [u'220-300', 'Tuesday', '??', u'Stan', ['Jack']],
        [u'830-910', 'Wednesday', '??', u'Stan', ['Clayton']],
        [u'910-950', 'Wednesday', '??', u'Stan', ['Simon A']],
        [u'1030-1110', 'Wednesday', '??', u'Stan', ['Yosef']],
        [u'1210-100', 'Wednesday', '??', u'Stan', ['Booker']],
        [u'100-140', 'Wednesday', '??', u'Stan', ['Thomas']],
        [u'140-220', 'Wednesday', '??', u'Stan', ['Ashley']],
        [u'220-300', 'Wednesday', '??', u'Stan', ['Coby']],
        [u'830-910', 'Thursday', '??', u'Stan', ['Nathaniel']],
        [u'910-950', 'Thursday', u'Activity Period', u'Stan', ['Bruno']],
        [u'1030-1110', 'Thursday', '??', u'Stan', ['Peter']],
        [u'1210-100', 'Thursday', '??', u'Stan', ['Jake']],
        [u'100-140', 'Thursday', '??', u'Stan', ['Orig']],
        [u'140-220', 'Thursday', '??', u'Stan', ['Oscar']],
        [u'220-300', 'Thursday', '??', u'Stan', ['Jack']]]

        
        self.assertListEqual(expected_results,self.clean_records)
        
        
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    '''
    
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

    # dbloader
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader))
    
    '''
    
    # ######################################################################################################
    # functional tests
    
    # 1 period of 1 prep
    Test_DBLoader_Prep5_1period
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5_1period))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_with_Prep5_Period1))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5Computertime))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Staff_with_Prep5))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Prep5_withs))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_Academic))
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


