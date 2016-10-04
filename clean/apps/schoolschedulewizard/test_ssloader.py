import sys
import os
from os import path as ospath

from database_table_util import tbl_rows_get
from database_util import Database

from Tkinter import *
from ttk import *
from shutil import copyfile

import unittest
from ssloader import SSLoader, SSLoaderRuleException, SSLoaderRecordEndException, SSLoaderNoMatchException

# "ELA: Nathaniel (Amelia)$$Math: CLayton, (Stan)$$Engineering: Orig, Stephen, Oscar (Paraic)"

class Test_String2Records(unittest.TestCase):
    
    def setUp(self):
        self.ssloader = SSLoader()
        
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
        
class Test_ApplyRules(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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
        
        
class Test_ApplyRules_Fails(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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
    
class Test_teachertype_1student(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
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
        
class Test_teachertype_edgecasestudent(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        self.inputstr = "Science: Oscar, Peter, (Paraic)"

    def test_subject(self):
    
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
        teacher,_rest = self.ssloader.extract_teacher(_rest)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,["Oscar","Peter"])
        
class Test_teachertype_edgecase_quotes(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
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
        
class Test_teachertype_multi_student(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
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

class Test_periodtype(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        self.inputstr = "8:30 \n-9:10"
        
    def test_(self):
        
        period = self.ssloader.extract_period(self.inputstr)
        self.assertEqual(period,"830-910")

class Test_extract_staff(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        self.inputstr = "Moira++"

    def test_subject(self):
    
        subject = self.ssloader.extract_staff(self.inputstr)
        
        self.assertEqual(subject,"Moira")
        
class Test_nonacademic_1_student(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        self.inputstr = "History: Oscar"

    def test_subject(self):
    
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"History")

    def test_students(self):
        
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,['Oscar'])
        
class Test_nonacademic_multi_student(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        self.inputstr = "Student News: Peter, Jack "

    def test_subject(self):
    
        subject,_ = self.ssloader.extract_subject(self.inputstr)
        
        self.assertEqual(subject,"Student News")

    def test_students(self):
        
        subject,_rest = self.ssloader.extract_subject(self.inputstr)
    
        students = self.ssloader.extract_students(_rest)
        
        self.assertListEqual(students,['Peter','Jack'])
        
class Test_extractteacher_Fails(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        self.rules = [(":",1),("(",1),(")",1)]
        self.ruletype = "teacher"

    def test_wrong_record_end(self):
        
        self.inputstr = "ELA :Nathaniel (Amelia) foobar"
    
        with self.assertRaises(SSLoaderRecordEndException):
            teacher,_ = self.ssloader.extract_teacher(self.inputstr)
        
class Test_LoadRefObjects(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
    def test_(self):
        
        rows = self.ssloader.loadrefobjects("quadref","subject")
        
        expected_results = ['Math Activity Period',u'ELA', 'Psychology','Psychology Reading','Biology','Spanish','Italian','Debate',u'Drama', 'Reading',u'Engineering', u'Math', u'Student News', u'Counseling', u'Science', u'Movement', u'Activity Period', u'Speech', u'History', u'OT', u'Core', u'Chess', u'Lunch Computer Time', u'Music', u'??', u'Independent Reading', 'Independent Art',u'Piano', u'Art', u'STEM', u'Humanities', u'Work Period']

        expected_results.sort()
        
        self.assertListEqual(expected_results,rows)
        
    def test_synonyms(self):
        
        rows = self.ssloader.loadrefobjects("quadref","subject",True)
        
        expected_results = [u'WP', u'Work P', u'AP', u'APeriod', u'SN', u'SNews', u'Activity P', u'Student N', 'Independent Art',u'Movement / Chess', u'Movement/chess', u'Debate Elective','Math Activity Period',u'ELA', 'Psychology','Psychology Reading','Biology','Spanish','Italian','Debate',u'Drama', 'Reading',u'Engineering', u'Math', u'Student News', u'Counseling', u'Science', u'Movement', u'Activity Period', u'Speech', u'History', u'OT', u'Core', u'Chess', u'Lunch Computer Time', u'Music', u'??', u'Independent Reading', u'Piano', u'Art', u'STEM', u'Humanities', u'Work Period']

        expected_results.sort()
        
        self.assertListEqual(expected_results,rows)
        
class Test_LoadSynonyms(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
    def test_(self):
        
        rows = self.ssloader.addsynonyms("quadref","subject")
        rows.sort()
        
        expected_results = [u'WP', u'Work P', u'AP', u'APeriod', u'SN', u'SNews', u'Activity P', u'Student N', u'Movement / Chess', u'Movement/chess', u'Debate Elective']
        
        expected_results.sort()

        self.assertListEqual(expected_results,rows)
        
        
class Test_ValidateTokens_Subject(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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
        
class Test_ValidateTokens_Student(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
        self.valid_students = self.ssloader.loadrefobjects('quadref','student')
        
    '''def test_exact_match(self):
        
        validated_token = self.ssloader.validate_token('Cleyton',self.valid_students)
        
        self.assertEqual(validated_token,'Clayton')'''
        
    def test_extra_letter(self):
        
        validated_token = self.ssloader.validate_token2('Simon A',self.valid_students)
        
        self.assertEqual(validated_token,'SimonA')
  
class Test_RelSize(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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

class Test_NumCharsSamelLocation(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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
        
class Test_NumCharsSame(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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

class Test_NumCharsLocationSame(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
    def test_identical(self):
        
        result,value = self.ssloader._match_num_chars_same_location("foobar","foobar")
        self.assertEquals(result,True)
        self.assertEquals(value,1)
        
class Test_RecordIdentifcation(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
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
     
class Test_RecordIdentifcation_realsample(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
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
        
class Test_RecordIdentifcation_realsample2(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
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
           
        
class Test_PreProcessRecords(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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

class Test_PreProcessRecordsStaff(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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
        
class Test_PreProcessRecordsNewPeriod(unittest.TestCase):
    def setUp(self):
        self.ssloader = SSLoader()
        
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
        
        
class Test_ValidateTokens(unittest.TestCase):


    def setUp(self):
        self.ssloader = SSLoader()
        
    def test_(self):
        
        record = ['830-910','monday','ELA','amelia',['Nathoniel']]
        
        expected_results = ['830-910','Monday','ELA','Amelia',['Nathaniel']]
        results =  self.ssloader.validate_tokens(record)
        
        self.assertListEqual(results,expected_results)
        
class Test_DBLoader(unittest.TestCase):

    def setUp(self):
        
        self.databasename = "test_ssloader"
        self.ssloader = SSLoader(self.databasename)
        
    def test_session(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', [u'SimonA']], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', ['Liam']]]
            
        
        expected_results =  [['Thea.STEM.Tuesday', 'Tuesday',7,'Thea', 'STEM'], 
                             ['Jess.Humanities.Wednesday', 'Wednesday',6, 'Jess','Humanities']]
            
            
        self.ssloader.dbloader(records)
        
        database = Database(self.databasename)
        with database:
            _,rows,_ = tbl_rows_get(database,'session',['code','dow','period','teacher','subject'])
        
        self.assertListEqual(expected_results,rows)
        
    def test_lesson(self):
        
        records = [['100-140', 'Tuesday', 'STEM', 'Thea', [u'SimonA']], 
                  ['1210-100', 'Wednesday', 'Humanities', 'Jess', ['Liam']]]
            
        
        expected_results =  [['SimonA', 'Tuesday',7,'Thea', 'STEM','Thea.STEM.Tuesday'], 
                             ['Liam', 'Wednesday',6, 'Jess','Humanities','Jess.Humanities.Wednesday']]
            
            
        self.ssloader.dbloader(records)
        
        database = Database(self.databasename)
        with database:
            _,rows,_ = tbl_rows_get(database,'lesson',['student','dow','period','teacher','subject','session'])
        
        self.assertListEqual(expdatabasenameected_results,rows)
        
    def tearDown(self):
        copyfile(self.databasename+".sqlite.backup",self.databasename+".sqlite")
    
class Test_DBLoader_RealFile(unittest.TestCase):
    def setUp(self):
        
        self.databasename = "test_ssloader"
        self.ssloader = SSLoader(self.databasename)
        
    def test_prep4(self):
        
        self.ssloader.ssloader(['prep4data.csv'],self.databasename)
    
    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    '''suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_String2Records))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ApplyRules))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ApplyRules_Fails))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_teachertype_1student)) 
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_teachertype_multi_student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_extractteacher_Fails))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_extract_staff))
    
      
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_nonacademic_1_student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_nonacademic_multi_student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens_Subject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens_Student))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation_realsample))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RecordIdentifcation_realsample2))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_periodtype))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_teachertype_edgecasestudent))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecords))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsNewPeriod))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_ValidateTokens))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_NumCharsSame))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_NumCharsSamelLocation))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_RelSize))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_PreProcessRecordsStaff))
    suite.addTeTest_DBLoader_RealFilest(unittest.TestLoader().loadTestsFromTestCase(Test_LoadRefObjects)) 
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_LoadSynonyms))'''
    
    
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_DBLoader_RealFile))
    
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
    
    


