from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,pidlogname=True,proclogname=False)

from misc_utils import os_file_to_string, thisfuncname, IDGenerator
from database_table_util import tbl_rows_get, tbl_rows_insert, _quotestrs, _gencoldefn, tbl_exists, \
     tbl_create, tbl_remove
from database_util import Database 
from sswizard_utils import getdbenum, session_code_gen, dbinsert, dbinsert_direct, _updaterecordval

from collections import OrderedDict

from sswizard_query_utils import _sessionenum, _maxlessonenum, _maxsessionenum, _findsessions

from datetime import datetime
from copy import deepcopy
import re
import os
import shutil

PRODDIR="clean/apps/schoolscheduler"
DEVDIR="clean/apps/schoolschedulewizard"

class SSLoaderRuleException(Exception):
    def __repr__(self):
        return(self.__class.__name__)

class SSLoaderRecordEndException(Exception):
    def __repr__(self):
        return(self.__class.__name__)
    
class SSLoaderBadTokenException(Exception):
    def __repr__(self):
        return(self.__class.__name__)
    
class SSLoaderRecordDelimException(Exception):
    def __repr__(self):
        return(self.__class.__name__)

class SSLoaderNoMatchException(Exception):
    def __repr__(self):
        return(self.__class.__name__)

class SSLoaderNoRulesMatchException(Exception):
    def __repr__(self):
        return(self.__class.__name__)

class SSLoaderMultiRuleMatchException(Exception):
    def __repr__(self):
        return(self.__class.__name__)
    
class SSLoaderFatal(Exception):
    def __repr__(self):
        return(self.__class.__name__)

class SSLoader(object):
    
    def __init__(self,databasename,prep=-1):
	
	self.keepversion = False
	self.database = Database(databasename)
	_rules = [('computertime',[("Computer Time",1),(":",0),("with",0)]),
	          ('pp.nostudent.subject.teacher',[('Prep Period',1),("\(",1),("\)",1),(":",1),('Computer Time',0),('with',0)]),
	          ('wp.student.nosubject.noteacher', [("Subject=^Work Period",1),("\(",0),("\)",0),(":",1),('Computer Time',0),('with',0)]),
	          ('wp.student.nosubject.teacher', [("Subject=^Work Period",1),("\(",1),("\)",1),(":",1),('Computer Time',0),('with',0)]),
	          ('wp.nostudent.nosubject.noteacher', [("Subject=^Work Period$",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',0)]),
	          ('wp.nostudent.subject.noteacher', [("subject=^**",1),("Subject=Work Period",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',0)]),
	          ('wp.student.subject.noteacher', [("subject=^**",1),("Subject=Work Period",1),("\(",0),("\)",0),(":",1),('Computer Time',0),('with',0)]),
	          ('wp.student.subject.teacher', [("subject=^**",1),("Subject=Work Period",1),("\(",1),("\)",1),(":",1),('Computer Time',0),('with',0)]), 
	          ('wp.nostudent.nosubject.noteacher.with.and', [("Subject=^Work Period",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',1),('and',1)]),
	          ('wp.nostudent.subject.teacher.with', [("subject=^**",1),("Subject=Work Period",1),("\(",0),("\)",0),(":",1),('Computer Time',0),('with',1)]), 
	          ('wp.nostudent.nosubject.noteacher.with', [("Subject=^Work Period",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',1)]),
	          ('wp.nostudent.subject.noteacher.with', [("subject=^**",1),("Subject=Work Period",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',1)]),
	
	          ('seminar.nostudent.subject.teacher.with', [("subject=^**",1),("Seminar",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',1)]),


	          ('seminar.student.subject.teacher',[("Seminar",1),(":",1),("\(",1),("\)",1)]),

	          
	          
	          ('ap.student.subject.teacher',[("Subject=^Activity Period",1),(":",1),("\(",1),("\)",1)]),
	          ('ap.student.subject.noteacher',[("Subject=^Activity Period",1),(":",1),("\(",0),("\)",0)]),
	          ('ap.nostudent.nosubject.noteacher', [("Subject=^Activity Period$",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',0)]),
	          
	          
	          ('subject.nostudent.nosubject.noteacher', [("subject=^**$",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',0)]),	          
	          ('subject.nostudent.nosubject.noteacher.with.and', [("subject=^**",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',1),('and',1)]),	   
	          ('subject.nostudent.nosubject.noteacher.with', [("subject=^**",1),("\(",0),("\)",0),(":",0),('Computer Time',0),('with',1)]),	          	          
	          ('subject.student.subject.teacher',[(":",1),("\(",1),("\)",1)]),
	          ('subject.student.subject.noteacher.and',[(":",1),("\(",0),("\)",0),("and",1)]),
	          ('subject.student.subject.noteacher',[(":",1),("\(",0),("\)",0)]),
	          ('student.student.nosubject.noteacher',[("students=^**$",1),(":",0),("\(",0),("\)",0)]),
	           
	          ('date',[("/",2)]),
	          ('period' ,[(":",2),("-",1)]),
	          ('ignore' , [("^Period",1),(":",0),("\(",0),("\)",0)]),
	          ('ignore2' , [("Lunch",1),(":",0),("\(",0),("\)",0)]),
	          ('_ENDCELL_' ,[("\^",1)]),
	          ('_CRETURN_' ,[("\&",1)]),
	          ('staffname',[('\+',2)]),
	          ('dow1',[('Monday',1)]),
	          ('dow2',[('Tuesday',1)]),
	          ('dow3',[('Wednesday',1)]),
	          ('dow4',[('Thursday',1)]),
	          ('dow5',[('Friday',1)]),
	          ('academicname',[('-',2)]),
	          ('studentname',[('\*',2)]),
	          
	          ]
	
	
        self.rules = OrderedDict()
	
	for name,rule in _rules:
	    self.rules[name] = rule
	    
        
        self.synonyms = {}
        self.valid_values = {}
        self.valid_values['students'] = self.loadrefobjects(databasename,'student',True)
        self.valid_values['period'] = self.loadrefobjects(databasename,'period',True)
        self.valid_values['dow'] =  ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.valid_values['teacher'] = self.loadrefobjects(databasename,'adult',True)
        self.valid_values['subject'] = self.loadrefobjects(databasename,'subject',True)
    
	self.enums = {'maps':{},'enums':{},'codes':{}}
	
        getdbenum(self.enums,self.database,'name','period')
        getdbenum(self.enums,self.database,'name','student')
        getdbenum(self.enums,self.database,'name','dow')
	
        self.fields = ['period','dow','subject','teacher','students',"recordtype"]

        self.prepmap = self.loadprepmapper()
	self.subjectmap = self.loadsubjectmapper()
        
    def pre_process_records(self,records):

        dowidx=-1
	periodidx=-1
        _records=[]
        _errors=[]

        lastrecordtype = None
        staffrecordflag = False
	academicrecordflag = False
	studentfile=False
	
	enums = {'maps':{},'enums':{},'codes':{}}	
	getdbenum(enums,self.database,'name','period')

        for record in records:
	    
	    subject = ""
	    
            try:
                recordtype = self.identify_record(record)
            except Exception, e:
		log.log(thisfuncname(),2,msg="could not match record to a rule,skipping",record=record,source=self.inputfile)
		continue		

	    def _addrecord(_locals):
		
		_record = [_locals[field] for field in self.fields]
		_records.append(_record)
		log.log(thisfuncname(),10,msg="record added",record=_record)
		
	    def _setteacher():
		teacher = "??"
		
		# if staff or academic file then teacher is provided from the top left cell of the input grid
		# not from the record/cell being processed
		if staffrecordflag == True:
		    teacher = staffname
		elif academicrecordflag==True:
		    teacher = academicname
		return(teacher)
	    
	    def _setdow():
		if academicrecordflag==False: # edge case where academic records is matched
		    return(self.valid_values['dow'][dowidx])
		return dow

	    def _setstudent():
		if studentfile == True:
		    return([studentname])
		return([])
	    
	    def _setsubject():
		if self.subjectmap.has_key(teacher.lower()) and subject == "":
		    log.log(thisfuncname(),10,msg="overiding subject",teacher=teacher,subject=str(self.subjectmap[teacher.lower()]))
		    return self.subjectmap[teacher.lower()]
		elif subject == "" or subject == None:
		    return "??"
		return subject
	    
	    def _period():
		#if academicrecordflag == True or staffrecordflag == True or studentfile == True:
		#if academicrecordflag == True or  studentfile == True:
		if academicrecordflag == True:
		    return(enums['period']['name'][periodidx])
		return period

	    try:
		
		if  recordtype == 'wp.student.nosubject.noteacher':
		    # WP: Shane, Asher
		    #subject = "??"
		    teacher = _setteacher()
		    students = self.extract_students(record.split(":")[1])
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif  recordtype == 'wp.student.nosubject.teacher':
		    # WP: Shane, Asher (Amelia)
		    #subject = "??"
		    location,_rest = self.extract_location(record)
		    teacher,_rest = self.extract_teacher(_rest.split(":")[1])
		    students = self.extract_students(_rest)
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif  recordtype == 'wp.nostudent.nosubject.noteacher':
		    # Work Period
		    #subject = "??"		    
		    teacher = _setteacher()
		    students = _setstudent()
		    if studentfile == True:
			students = [studentname]
		    dow = _setdow()	
		    subject = _setsubject()
		    _addrecord(locals())
		elif recordtype == 'wp.nostudent.subject.noteacher':
		    # Humanities Work Period
		    subject = record.split(" ")[0]
		    teacher = _setteacher()
		    students = _setstudent()
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif recordtype == 'wp.student.subject.noteacher':
		    # Math WP: Jack
		    subject = record.split(" ")[0]
		    teacher = _setteacher()
		    students = self.extract_students(record.split(":")[1])
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif recordtype == 'wp.student.subject.teacher':
		    # Math WP: Jack (Stan)
		    location,_rest = self.extract_location(record)
		    subject = _rest.split(" ")[0]
		    teacher,_rest = self.extract_teacher(_rest.split(":")[1])
		    students = self.extract_students(_rest)
		    subject = _setsubject()
		    dow = _setdow()	
		    _addrecord(locals())

		elif recordtype == 'seminar.student.subject.teacher':
		    # Math Seminar G2: Jack (Stan)
		    location,_rest = self.extract_location(record)
		    subject = _rest.split(" ")[0]
		    teacher,_rest = self.extract_teacher(_rest.split(":")[1])
		    students = self.extract_students(_rest)
		    subject = _setsubject()
		    dow = _setdow()	
		    _addrecord(locals())
		    
		elif recordtype == 'wp.nostudent.nosubject.noteacher.with.and':
		    # Work Period with Alyssa and Paraic
		    
		    location,record = self.extract_location(record)
		    
		    _teachers = record.split("with")[1]
		    teachers = _teachers.split("and")
		    
		    #subject = "??"
		    students = _setstudent()
		    dow = _setdow()	    
		    subject = _setsubject()
		    
		    for teacher in teachers:
			teacher = teacher.lstrip()
			teacher = teacher.strip()
			_addrecord(locals())
			
		elif recordtype == 'wp.nostudent.nosubject.noteacher.with':
		    # Work Period with Alyssa
		    
		    location,record = self.extract_location(record)
		    
		    teacher = record.split("with")[1]
		    teacher = teacher.lstrip()
		    #subject = "??"
		    subject = _setsubject()
		    students = _setstudent()
		    dow = _setdow()	
		    _addrecord(locals())
		    
		    
		elif recordtype == 'wp.nostudent.subject.teacher.with':
		    # Humanities WP: with alyssa
		    
		    location,record = self.extract_location(record)
		    
		    teacher = record.split("with")[1]
		    teacher = teacher.lstrip()
		    subject = record.split(" ")[0]
		    students = _setstudent()
		    dow = _setdow()	
		    _addrecord(locals())
		    	    
		elif recordtype == 'seminar.nostudent.subject.teacher.with':
		    # "Math Seminar G2 with Stan"
		    subject = record.lower().split(" ")[0]
		    teacher = record.lower().split("with")[1]
		    teacher = teacher.lstrip()
		    students = _setstudent()
		    dow = _setdow()
		    subject = _setsubject()
		    #fullrecord = record
		    _addrecord(locals())
		    
		elif recordtype == 'wp.nostudent.subject.noteacher.with':
		    # Humanities Work Period with Johnny

		    location,record = self.extract_location(record)
		    
		    
		    subject = record.lower().split(" ")[0]
		    teacher = record.lower().split("with")[1]
		    teacher = teacher.lstrip()
		    students = _setstudent()
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif recordtype == 'subject.nostudent.nosubject.noteacher':
		    # Humanities
		    
		    location,record = self.extract_location(record)
		    
		    
		    subject = record
		    teacher = _setteacher()
		    students = _setstudent()
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif recordtype == 'subject.nostudent.nosubject.noteacher.with':
		    # ELA with Amelia
		    
		    location,record = self.extract_location(record)
		    
		    
		    subject,teacher = record.lower().split("with")
		    teacher = teacher.lstrip()
		    subject = subject.strip()
		    students = _setstudent()
		    dow = _setdow()
		    subject = _setsubject()
		    _addrecord(locals())
		elif recordtype == 'subject.nostudent.nosubject.noteacher.with.and':
		    # ELA with Amelia and Paraic
		    
		    location,record = self.extract_location(record)
		    
		    
		    subject,_teachers = record.split("with")
		    teachers = _teachers.split("and")
		    subject = subject.strip()
		    students = _setstudent()
		    dow = _setdow()	
		    subject = _setsubject()
    
		    for teacher in teachers:
			teacher = teacher.lstrip()
			teacher = teacher.strip()
    
			_addrecord(locals())
		    
		elif recordtype == 'student.student.nosubject.noteacher':
		    teacher = _setteacher()
		    dow = _setdow()
		    #subject = "??"
		    period = _period()
		    students = [record.lstrip().strip()]
		    subject = _setsubject()
		    _addrecord(locals())
				    
		elif recordtype[:6] == "ignore":
		    pass
		    
		elif recordtype == 'pp.nostudent.subject.teacher':
		    # Prep Period: ?? (Amelia)"
		    location,_rest = self.extract_location(record)
		    subject,_rest = self.extract_subject(_rest)
		    teacher,_rest = self.extract_teacher(_rest)
		    students = ["Dummy"]
		    dow = _setdow()
		    period = _period()
		    subject = "Prep Period"
		    _addrecord(locals())		    
		    
		elif recordtype == 'subject.student.subject.teacher':
		    # ELA: Nathaniel (Amelia)"
		    location,_rest = self.extract_location(record)
		    subject,_rest = self.extract_subject(_rest)
		    teacher,_rest = self.extract_teacher(_rest)
		    students = self.extract_students(_rest)
		    dow = _setdow()
		    period = _period()
		    subject = _setsubject()
		    _addrecord(locals())
		    
		elif recordtype == 'subject.student.subject.noteacher':
		    # Science: Oscar, Peter"
		    
		    subject,_rest = self.extract_subject(record)
		    teacher = _setteacher()
		    students = self.extract_students(_rest)
		    dow = _setdow()
		    period = _period()
		    subject = _setsubject()
		    _addrecord(locals())
		    
		elif recordtype == 'subject.student.subject.noteacher.and':
		    # Chess: NAthaniel and Jake"
		    
		    subject,_rest = self.extract_subject(record)
		    teacher = _setteacher()
		    _rest = _rest.replace("and",",")
		    students = self.extract_students(_rest)
		    dow = _setdow()
		    period = _period()
		    subject = _setsubject()
		    _addrecord(locals())
		    
		elif  recordtype == 'ap.nostudent.nosubject.noteacher':
		    # Activity Period
		    subject = "Activity Period"
		    teacher = _setteacher()
		    students = _setstudent()
		    if studentfile == True:
			students = [studentname]		
		    dow = _setdow()
		    _addrecord(locals())
		    
		elif recordtype == 'ap.student.subject.teacher':
		    # Activity Period: Nathaniel (Amelia)"
		    location,_rest = self.extract_location(record)
		    subject,_rest = self.extract_subject(_rest)
		    teacher,_rest = self.extract_teacher(_rest)
		    students = self.extract_students(_rest)
		    dow = _setdow()
		    period = _period()
		    subject = _setsubject()
		    _addrecord(locals())
		    
		elif recordtype == 'ap.student.subject.noteacher':
		    # Activity Period: Oscar, Peter"
		    
		    subject,_rest = self.extract_subject(record)
		    teacher = _setteacher()
		    students = self.extract_students(_rest)
		    dow = _setdow()
		    period = _period()
		    subject = _setsubject()
		    _addrecord(locals())
    
		# mode determination options
		# is it a student file, staff file or an academic file
		elif recordtype == 'studentname':
		    # this function actually extrats staff and students
		    studentname = self.extract_staff(record)
		    log.log(thisfuncname(),10,msg="this is a student file",studentname=studentname)
		    studentfile=True
		elif recordtype == 'staffname':
		    staffname = self.extract_staff(record)
		    log.log(thisfuncname(),10,msg="this is a staff file",staffname=staffname)
		    staffrecordflag=True	
		elif recordtype == 'academicname':
		    academicname = self.extract_staff(record)
		    log.log(thisfuncname(),10,msg="this is an academic file",academicname=academicname)
		    academicrecordflag=True
		    
		# special use cases
		    
		elif recordtype == 'computertime':
		    if studentfile == True:
			#studentname = self.extract_staff(record)
			students = [studentname]
			teacher = "??"
			subject = "Computer Time"
			dow = self.valid_values['dow'][dowidx]
			_record = [locals()[field] for field in self.fields]
			_records.append(_record)
			log.log(thisfuncname(),10,msg="record addede",record=_record)

		    
		    elif self.prep <> -1:
			
			students = [name for name,prep in self.prepmap.iteritems() if prep == str(self.prep)]
			#students = [studentname]
			students.sort()
			teacher = "??"
			subject = "Computer Time"
			dow = self.valid_values['dow'][dowidx]
			_record = [locals()[field] for field in self.fields]
			_records.append(_record)
			log.log(thisfuncname(),10,msg="record added",record=_record)
		    else:
			subject = "Computer Time"
    
		    
    
		# file markers used to increment axes (period, dow, etc)
		elif recordtype[:3] == 'dow':
		    periodidx=-1
		    dow = record
		    log.log(thisfuncname(),10,msg="setting dow",dow=dow)
		elif recordtype == 'date':
		    pass
		elif recordtype == '_CRETURN_':
		    pass
		elif recordtype == 'blankrow':
		    pass
		elif recordtype == 'period':
		    if academicrecordflag==False:
			period = self.extract_period(record)
			dowidx=-1
			log.log(thisfuncname(),10,msg="period set reset on period",period=period)
		elif recordtype == '_ENDCELL_':
		    
		    if academicrecordflag==False:
			old_dowidx = dowidx
			# increment day each time we hit an end of cell marker; set to -1 at 4 so that
			# period cell is missed on the next line.
			if dowidx==4:dowidx=-1
			dowidx+=1
		    
			log.log(thisfuncname(),10,msg="dow increment",old_dowidx=old_dowidx,dowidx=dowidx,lastrecordtype=lastrecordtype)
		    else:
			old_periodidx =periodidx
			if periodidx==8:
			    periodidx=-1
			elif periodidx==3:
			    periodidx=4
			periodidx+=1
			log.log(thisfuncname(),10,msg="period increment",old_periodidx=old_periodidx,periodidx=periodidx,lastrecordtype=lastrecordtype)
		else:
		    log.log(thisfuncname(),2,msg="could not identify record",recordtype=recordtype,record=record)
		    #raise SSLoaderFatal
		    continue
	    except SSLoaderRecordDelimException,SSLoaderRecordEndException:
		log.log(thisfuncname(),2,msg="exception thrown while identify record",recordtype=recordtype,record=record)
		continue	    
		
            lastrecordtype = recordtype
        
            log.log(thisfuncname(),10,msg="processed",recordtype=recordtype,record=record)
        return _records, _errors, self.fields
            
    def loadrefobjects(self,databasename,objtype,synonyms=False):
        # objtype = db table name
        
        cols = ['name']
        database = Database(databasename)
        
        with database:
            _,rows,_ = tbl_rows_get(database,objtype,cols)
        
        rows = [row[0] for row in rows]
        log.log(thisfuncname(),10,msg="loading refdata",objtype=objtype,rows=rows)
        
        if synonyms == True:
            synonyms = self.addsynonyms(databasename,objtype)
            rows = rows + synonyms
            log.log(thisfuncname(),10,msg="adding synonyms",objtype=objtype,synonyms=synonyms)
            
        rows.sort()
        return rows
    
    def addsynonyms(self,databasename,objtype):
        cols = ['name','synonym']
        database = Database(databasename)
        
        with database:
            _,rows,_ = tbl_rows_get(database,'synonyms',cols,[['objtype','=',"\""+objtype+"\""]])
        
        for name,syno in rows:
	    self.synonyms[syno]=name
	    log.log(thisfuncname(),10,msg="adding synonym to lookup",name=name,syno=syno)
	
	rows = [row[1] for row in rows]

	
        return rows
    
    def loadsubjectmapper(self):
        cols = ['name','subject']
	
	with self.database:
	    _,rows,_ = tbl_rows_get(self.database,'adult',cols,[['subject','<>','\"None\"']])
	
	d = dict((row[0].lower(),row[1]) for row in rows)
	
	log.log(thisfuncname(),10,msg="loaded subject map",map=d)
	return d
	
    def loadprepmapper(self):
        cols = ['name','prep']
        
        with self.database:
            _,rows,_ = tbl_rows_get(self.database,'student',cols)
        
        d = dict((row[0],row[1]) for row in rows)
        return d
        
    def file2string(self,filename):
        str=""
        fh = open(filename, 'r+')
        
        linecount=0
        for line in fh:
            if line <> "":
                #line = line.replace("\n","_CRETURN_").replace("\"","")
                #line = line.replace("^","_ENDCELL_")
                
                line = line.replace("\n","&")
                line = line.replace("\"","")
                str+=line
            
            linecount+=1
            
        fh.close()
        return(str)
    
    def string2records(self,fileasstring):
        ''' take the input file as a single string input; & represents a newline and
        ^ is the logical end of a spreadsheet cell '''
        records = []
        record=""
        
        lastchar = ""
        for i in range(len(fileasstring)-1):
            #if fileasstring[i] in ["_CRETURN_","_ENDCELL_"]:
            
            if fileasstring[i] == "&" and lastchar == "&": # ignore all but one consecutive newlin3
                # lastchar already set to & so no need to change
                continue
            
            elif fileasstring[i] == "&" and fileasstring[i+1] == "^": # newline before end of cell; ignore newline
                #lastchar = fileasstring[i]
                # ignore this &; do not change last char
                continue
            elif fileasstring[i] == "&":
		
		if fileasstring[i-4:i] == "with":
		    record += " "
		    lastchar = " "
		    continue
		
		elif fileasstring[i+1:i+5] == "with":
		    lastchar = " "
		    continue
		elif fileasstring[i-5:i] == "with ":
		    continue
		elif fileasstring[i-1:i] == ":":
		    continue
		elif fileasstring[i-1:i] == "/":
		    continue
                
                records.append(record.strip())
                record=""
                lastchar = fileasstring[i]
                
            elif fileasstring[i] == "^":
                if record <> "": records.append(record.strip()) # incase preceded by a &
                records.append("^") # add a record for end of cell as we drive dow increment from this
                record=""
                lastchar = fileasstring[i]
            else:
                lastchar = fileasstring[i]
                record += fileasstring[i]
            
        # catch the last char and any other chars that remain
        if fileasstring[i+1] <> "&":
            record += fileasstring[i+1]
        
        if record <> "": records.append(record.strip())
        return records

    def identify_record(self,record):
        match=[]
        for name,rule in self.rules.iteritems():
            try:
                if self.appyrules(record,rule) == True:
                    match.append(name)
            except SSLoaderRuleException:
                pass
	
        if record=='':
            log.log(thisfuncname(),10,msg="skipoing as blank row",record=record,matches=match)
            return('blankrow')
        elif len(match) > 1:
            log.log(thisfuncname(),3,msg="multiple rules matched picking on priority",mathes=match)
	    return(match[0])
	    #raise SSLoaderMultiRuleMatchException
        elif len(match) == 0:
            raise SSLoaderNoRulesMatchException
        else:
            log.log(thisfuncname(),10,msg="rule matched",record=record,matches=match)
            return(match[0])
        
    def appyrules(self,record,rules):
	
        for char,count in rules:
	    if char.count("=") == 1:
		
		objtype,value = char.split("=")
		#if char[-1] == "=":
		if value.count("**") == 1:
		    value = value.replace("**","")
		    
		    # match any of objtype to whole record
		    #objtype = char[:-1]
		    objtypematch=False
		    for validvalue in self.valid_values[objtype]:
		    
			if validvalue <> "??":
			    
			    if len(value) > 0:
				
				for _v in value:
				    if _v == "^":
					validvalue = "^" + validvalue
				    if _v == "$":
					validvalue = validvalue + "$"

			    p = re.compile(validvalue.lower())
			    if len(p.findall(record.lower())) == count:
				objtypematch=True
				
		    if objtypematch==False:
			return False
		else:
		    # match if record contains synonym
		    #objtype,value = char.split("=")

		    synomatch=False
		    for syno,master_value in self.synonyms.iteritems():

			try:
			    if value[0] == "^":
				syno = "^" + syno
				_value = value[1:]
			    else:
				_value = value
			except:
			    _value = value
			    
			try:
			    if _value[-1] == "$":
				syno = syno + "$"
				_value = _value[:-1]
			except:
			    pass

			p = re.compile(syno.lower())
			#if master_value==value and record.count(syno) == count:
			    
			if master_value==_value and len(p.findall(record.lower())) == count:
			    synomatch=True
    
		    if synomatch==False:
			return False
	    
	    #elif record.lower().count(char.lower()) <> count:
            else:
		p = re.compile(char.lower())
		if len(p.findall(record.lower())) <> count:
		    return False
        return True
    
    def extract_subject(self,record):
        # works with teacher or no teacher on record
        subject,_rest = record.split(":")
        return(subject,_rest)
    
    def extract_location(self,record):
    
        try:
	    _rest,location = record.split("[")
	    return(location[:-1],_rest)
	except:
	    return("",record)
    
    def extract_staff(self,record):
        if record[-2:] <> "++" and record[-2:] <> "--" and record[-2:] <> "**":
            raise SSLoaderBadTokenException

        return(record[:-2])

    
    def extract_period(self,record):
        return (record.replace("\"","").replace(" ","").replace("\n","").replace(":",""))

    def extract_teacher(self,record):
        # works with subject or no subject on record
        _rest,teacher = record.split("(")
        teacher = teacher.strip() # lose any trailing spaces
        
        if teacher[-1] == ")":
            teacher = teacher[:-1] # lose trailing bracket
        else:
            log.log(thisfuncname(),2,msg="not ending with bracket then spaces",record=record)
            raise SSLoaderRecordEndException
        return(teacher,_rest)
        
    def extract_students(self,record):
        # assumes the teacher has been removed from end of record if one existed

        record = record.lstrip() # lose any leading spaces
        record = record.strip() # lose any trailing spaces

        if record.count(",") == 0:
            students = record.split(" ")
	    if len(students) > 1:
		if len(students[1]) == 1:
		    students = [record]
		    log.log(thisfuncname(),10,msg="no commas detected <= 2 names, 2nd 1 char; assuming 1 name",students=students)
	    else:
		log.log(thisfuncname(),10,msg="no commas detected; 2nd > 1 char; assuming space delim",students=students)

		#raise SSLoaderRecordDelimException 
        else:
            students = record.split(",")
	    newstudents = []
	    for student in students:
		student = student.lstrip()
		student = student.strip()
		
		if len(student.split(" ")) >= 2 and student.split(" ")[1] not in ["A","B","a","b"]:
		    
		    newstudents = newstudents + student.split(" ")
		else:
		    newstudents.append(student)
	
	    students=newstudents    
	    
		       
            
        _students = []
        for student in students:
            student = student.lstrip() # lose any leading spaces
            student = student.strip() # lose any trailing spaces
            if student <> "":
                _students.append(student)
            else:
                log.log(thisfuncname(),10,msg="trailing comma detected and corrected",record=record)
        return(_students)
    
    def _match_num_chars_same(self,matchee,matcher,tolerance=0.8):
        ''' determine if the number of chars that appear in each string are within a certain tolerance, 
        Currently always ignores case'''        
        matches=0
            
        for i in range(len(matchee)):
            try:
                matcher.lower().index(matchee.lower()[i])
                matches+=1
            except ValueError:
                pass

        percent_match = float(matches) / len(matchee)
        if  percent_match >= tolerance:
            return True, percent_match
        return False, percent_match

    def _match_rel_size(self,matchee,matcher,tolerance=0.5):
        ''' determine if the 2 strings are within a certain percentage size of each other '''
        
        # compare how much the bigger one is bigger than the smaller one
        
	if len(matchee)> len(matcher):
	    try:
		sizediff = round(float(len(matchee)-len(matcher))/len(matcher),2)
	    except ZeroDivisionError:
		log.log(thisfuncname(),2,msg="div by zero",matchee=str(matchee),matcher=str(matcher))
		return False,-1
	    if sizediff > tolerance:
		return False, sizediff
	    return True,sizediff
	else:
	    try:
		sizediff = round(float(len(matcher)-len(matchee))/len(matchee),2)
	    except ZeroDivisionError:
		log.log(thisfuncname(),2,msg="div by zero",matchee=str(matchee),matcher=str(matcher))
		return False,-1
	    
	    if  sizediff > tolerance:
		return False, sizediff
	    return True,sizediff

        
    def _match_num_chars_same_location(self,matchee,matcher,tolerance=0.8):
        ''' when comparing 2 strings, determine if the num of chars in the same location
        are withing a certain percentage tolerance, Currently always ignores case'''

        num_matches=0
        
        # first start at the left most char of the matchee and work char by char comparing
        # and quit when hit a difference
        i=0
        while i < len(matchee) and i < len(matcher):
            if matchee[i].lower() == matcher[i].lower():
                num_matches+=1
                i+=1
            else:
                i=len(matchee)
        
        # if we didnt match 100%; start at the right most char of the matcher and work backwards
        # and quit when hit a difference
        if num_matches < len(matchee)-1:
            i=-1
            while i >= (len(matchee)*-1) and i >= (len(matcher)*-1):
                if matchee[i].lower() == matcher[i].lower():
                    num_matches += 1
                    i-=1
                else:
                    i = (len(matchee)*-1)-1
        
        percent_match = round(float(num_matches) / len(matcher),2)
        
        if  percent_match >= tolerance:
            return True, percent_match
        return False, percent_match
        
    
    def _ascii_value(self,token):
        value=0
        for char in token.lower():
            value+=ord(char)
            
        value = value / len(token)
        return value
        

    def validate_tokens(self,record):

        for i in range(len(self.fields)):
            orig_value = record[i]
            new_value = "??"
            try:
                if isinstance(orig_value,list) == True: # probably students
                    new_value = []
                    for _value in orig_value:
                        new_value.append(self.validate_token2(_value,self.valid_values[self.fields[i]]))
                else:
                    try:
			new_value = self.validate_token2(orig_value,self.valid_values[self.fields[i]])
		    
			if self.synonyms.has_key(new_value):
			    log.log(thisfuncname(),10,msg="synonym, swapping",new_value=self.synonyms[new_value],old_value=new_value)
			    new_value = self.synonyms[new_value]
		    except KeyError:
			# not all fields have (or need) valid values to compare against
			# one example would be recordtype; where values are generated by the program
			# not from the user / file input
			log.log(thisfuncname(),10,msg="no valid values available",objtype=self.fields[i])
			new_value = orig_value
		    
            except SSLoaderNoMatchException:
                log.log(thisfuncname(),2,msg="failed to validate field, skipping record",value=str(record[i]),field=self.fields[i],
		        record=record,file=self.inputfile)
		raise SSLoaderBadTokenException

            if orig_value <> new_value:
                record.remove(orig_value)
                record.insert(i,new_value)
        return record
    
    def validate_token2(self,token,valid_values,tolerance=0.7):
        
        for value in valid_values:
            if value == token:
                log.log(thisfuncname(),10,msg="straight match",token=token,validvalue=str(value))
                return token
            elif value.lower() == token.lower():
                log.log(thisfuncname(),10,msg="match if case ignored",token=token,validvalue=value)
                return value
            elif value.lower().lstrip().strip() == token.lower().lstrip().strip():
                log.log(thisfuncname(),10,msg="match if case ignored and lead/trail space stripped",token=token,validvalue=value)
                return value
            
        for value in valid_values:
            #else:
                
            result,similarity=self._match_rel_size(token,value)
            
            if result == True:
                
                result,similarity = self._match_num_chars_same_location(token,value,tolerance)
                if result == True:
                    log.log(thisfuncname(),3,msg="fuzzy match",token=token,validvalue=str(value),similarity=similarity)                        
                    return value
		else:
		    log.log(thisfuncname(),10,msg="failed to fuzzy match",token=token,validvalue=str(value),similarity=similarity)          
		    
	    else:
		log.log(thisfuncname(),10,msg="size difference too big to fuzzy match",result=result)
                    
        log.log(thisfuncname(),10,msg="failed to validate token",token=token,file=self.inputfile)
        raise SSLoaderNoMatchException

    def dbloader(self,records):
        
        dblessonrows = []
        dbsessionrows = []

        #cols = ['period','dow','subject','teacher','students',"recordtype","record"]
	_idx = self.fields.index('students')
	
        for record in records:
	    d = dict(zip(self.fields,record))
	    
	    # switch the last item for a count of number of students
	    # this is so we can determine which session was created with no students and so
	    # can be matched up with lessons at the same time/dow later on
	    #_record = deepcopy(record)[:-1]
	    _record = deepcopy(record)
	    _record.append(len(d['students']))
	    
            dbsessionrows.append(_record)
	    
	    if len(d['students']) > 1:
		pass
	    
            for student in d['students']:
		_record = deepcopy(record)
		_record.pop(_idx)
		_record.insert(_idx,student)
		
		dblessonrows.append(_record)
		
	dbinsert_direct(self.database,dbsessionrows,'session',self.sourcecode,
	                ['period','dow','subject','adult','student','recordtype','numstudents'],
	                masterstatus=False,keepversion=self.keepversion)
	dbinsert_direct(self.database,dblessonrows,'lesson',
	                self.sourcecode,list(self.fields),masterstatus=False,keepversion=self.keepversion)    

    def primary_record_set_session(self):
	
	def _additem(items,newitem):
	    # if newitem is not 'notset/??' then add item to the list of items if its not already present.
	    
	    if newitem <> "??":
		# if items is unset then set it
		if len(items) == 1:
		    if items[0] == "??":
			items[0] = newitem
		    else:
			try:
			    items.index(newitem)
			except:
			    log.log(thisfuncname(),3,msg="conflicting item",newitem=str(newitem),items=items)
			    items.append(newitem)
		else:
		    try:
			items.index(newitem)
		    except:
			log.log(thisfuncname(),3,msg="conflicting item",newitem=str(newitem),items=items)
			items.append(newitem)
		
	def _itemset(items):
	    # return True if list still equals initial value ["??"]
	    if items <> ["??"]: return True
	    return False
	    
	cols = ['period','dow','teacher','subject','status','source','recordtype','numstudents']
	
	with self.database:
	    _,rows,_ = tbl_rows_get(self.database,'session',cols)
	    
	hashmap={}
	for row in rows:

	    d = dict(zip(cols,row))
	    
	    hashkey = ".".join([d['dow'],str(d['period']),d['subject'],d['teacher']])
	    
	    if hashmap.has_key(hashkey) == False:
		hashmap[hashkey] = dict(teacher=d['teacher'],subject=d['subject'],
			                status="unset",period=d['period'],
		                        recordtype=d['recordtype'],
			                dow=d['dow'],source="",numstudents=0)	
		
	    if hashmap[hashkey]['teacher'] <> "??" and hashmap[hashkey]['subject'] <> "??":
		hashmap[hashkey]['status'] = "completed"
	    elif hashmap[hashkey]['teacher'] <> "??" or hashmap[hashkey]['subject'] <> "??":
		hashmap[hashkey]['status'] = "incomplete"

	    hashmap[hashkey]['numstudents'] += int(d['numstudents'])
	    
	return (hashmap)
    
    def primary_record_set(self):
	
	def _additem(items,newitem):
	    # if newitem is not 'notset/??' then add item to the list of items if its not already present.
	    
	    if newitem <> "??":
		# if items is unset then set it
		if len(items) == 1:
		    if items[0] == "??":
			items[0] = newitem
		    else:
			try:
			    items.index(newitem)
			except:
			    log.log(thisfuncname(),3,msg="conflicting item",newitem=str(newitem),items=items)
			    items.append(newitem)
		else:
		    try:
			items.index(newitem)
		    except:
			log.log(thisfuncname(),3,msg="conflicting item",newitem=str(newitem),items=items)
			items.append(newitem)
		
	def _itemset(items):
	    # return True if list still equals initial value ["??"]
	    if items <> ["??"]: return True
	    return False
	    
	cols = ['period','dow','student','teacher','subject','status','source','recordtype']
	
	try:
	    _idx = self.fields.index('students')
	    self.fields.pop(_idx)
	    self.fields.insert(_idx,'student')
	except:
	    pass
	
	# order by makes sure any completed records get 
	with self.database:
	    _,rows,_ = tbl_rows_get(self.database,'lesson',self.fields)

	hashmap={}
	for row in rows:

	    d = dict(zip(self.fields,row))
	    
	    hashkey = ".".join([d['dow'],d['period'],d['student']])
	    
	    if hashmap.has_key(hashkey) == False:		
		hashmap[hashkey] = dict(subject=["??"],teacher=["??"], \
		                        student=d['student'],status="unset",period=d['period'],\
		                        dow=d['dow'],source="",recordtype=['??'])

	    _additem(hashmap[hashkey]['teacher'],d['teacher'])
	    _additem(hashmap[hashkey]['subject'],d['subject'])
	    
	    _recordtype = d['recordtype'].split(".")[0]
	    #_additem(hashmap[hashkey]['recordtype'],d['recordtype'])
	    _additem(hashmap[hashkey]['recordtype'],_recordtype)
	    #_additem(hashmap[hashkey]['record'],d['record'])

	for row in rows:
	    
	    d = dict(zip(self.fields,row))
	
	    hashkey = ".".join([d['dow'],d['period'],d['student']])    
	    
	    if _itemset(hashmap[hashkey]['subject']) and _itemset(hashmap[hashkey]['teacher']):
		hashmap[hashkey]['status'] = "primary"
	    elif hashmap[hashkey]['subject'] == "Computer Time":
		hashmap[hashkey]['status'] = "primary"
	    elif hashmap[hashkey]['status'] <> "unset":
		hashmap[hashkey]['status'] = "conflict"
	    else:
		hashmap[hashkey]['status'] <> "unset"

	return (hashmap)
    	
    def ssloader(self,files,databasename="htmlparser",fields=None):
        
        if fields <> None:
	    self.fields = fields
	    
        for file in files:
	    
	    if len(file) == 4:
		_file,prep,dbloader,_source = file
	    elif len(file) == 3:
		_file,prep,dbloader = file
		_source = _file
	    else:
		log.log(thisfuncname(),0,msg="only 3 or 4 args accepted in file tuple descriptor")
            
            log.log(thisfuncname(),3,msg="loading",file=_file,prep=prep,dbloaderflag=dbloader)
	    
            self.inputfile = _file
	    self.prep = prep
	    self.sourcecode = _source # shortname for source file
	    
            fileasstring = self.file2string(_file)
	    log.log(thisfuncname(),15,fileasstring=fileasstring)
	    
            records = self.string2records(fileasstring)
	    log.log(thisfuncname(),15,records=records)
	    
            clean_records,_,_ = self.pre_process_records(records)
	    log.log(thisfuncname(),15,clean_records=clean_records)
	    
            self.validated_clean_records = []

            for clean_record in clean_records:
                try:
		    self.validated_clean_records.append(self.validate_tokens(clean_record))
		except SSLoaderBadTokenException:
		    pass # logged in validate_tokens
		    
	    log.log(thisfuncname(),15,validated_clean_records=self.validated_clean_records)
	    
	    if dbloader == True:
		self.dbloader(self.validated_clean_records)
	    else:
		self.dbupdater(self.validated_clean_records)
		

    def run(self,dbname,files,insertprimary=True):    
	def _formatval(objtype,d):
	    if len(d[objtype]) > 1:
		return( "["+",".join(d[objtype])+"]")
	    return(",".join(d[objtype]))
	    
	self.databasename = dbname
	self.database = Database(self.databasename)
	try:
	    with self.database:
		tbl_remove(self.database,'lesson')
		tbl_remove(self.database,'session')
	except:
	    pass

	# pass in self.fields here in case its been updated since
	# object constructed
	self.ssloader = SSLoader(self.databasename)
	self.ssloader.fields = self.fields
	
	self.ssloader.keepversion=self.keepversion
	self.ssloader.ssloader(files,self.databasename)

	# for now only  create primary record in certain cases - as it has no meaning when we have adde extra
	# fields like record etc
	if hasattr(self,"primary_record"):
	    if self.primary_record == False:
		log.log(thisfuncname(),3,msg="primary_record flag set to false, skipping") 
		return

	log.log(thisfuncname(),3,msg="creating master record set")    

	hashmap = self.primary_record_set()
	newrows = []
	for key,d in hashmap.iteritems():
	    newrows.append([d['period'],d['dow'],_formatval('subject',d),_formatval('teacher',d),d['student'],
	                    _formatval('recordtype',d)])
    
	hashmap = self.primary_record_set_session()
	newsessionrows = []
	for key,d in hashmap.iteritems():
	    newsessionrows.append([d['period'],d['dow'],d['subject'],d['teacher'],[],d['recordtype'],d['numstudents']])    

	if insertprimary==True:
	    log.log(thisfuncname(),10,msg="loading master record set")    
	    dbinsert_direct(self.database,newsessionrows,'session','dbinsert',
	                     ['period','dow','subject','adult','student','recordtype','numstudents'],
	                     keepversion=self.keepversion)
	    dbinsert_direct(self.database,newrows,'lesson','dbinsert',self.fields,keepversion=self.keepversion)
	else:
	    return newrows

if __name__ == "__main__":
    
    if os.environ.has_key("APPROOT") == False:
	raise Exception("env variable APPROOT is not set")
    
    APPROOT = os.environ["APPROOT"]
    
    '''if os.getcwd() == os.path.join(APPROOT,DEVDIR):
	env = "DEV"
	databasename = "test_ssloader"
	
	files = [('prep5data.csv',5,True),('prep4data.csv',4,True),('prep6data.csv',6,True),('staffdata.csv',-1,True),
	         ('academic.csv',-1,True),('prep56new.csv',-1,True)]
	#files = [('prep56new_Amelia.csv',5,True)]	
	
    elif os.getcwd() == os.path.join(APPROOT,PRODDIR):'''
    
    env = "PROD"
    databasename = "quad"
    shutil.copyfile(databasename+".sqlite.backup",databasename+".sqlite")

    '''files = [("prep4student.csv",4,True),
	     ("prep5student.csv",5,True),
	     ("prep6student.csv",6,True),
	     ("prep4data.csv",4,True),
	     ("prep5data.csv",5,True),
	     ("prep6data.csv",6,True),
	     ("staff.csv",-1,True),
	     ("academic.csv",-1,True),
	     ('prep56new.csv',-1,True)]'''
    
    '''files = [("/mnt/bumblebee-burtnolej/googledrive/current/Prep6IndividualSchedules_new.csv",6,True,"6s"),
             ("/mnt/bumblebee-burtnolej/googledrive/current/Prep4IndividualSchedules_new.csv",4,True,"4s"),
             ("/mnt/bumblebee-burtnolej/googledrive/current/Prep5IndividualSchedules_new.csv",5,True,"5s"),
             ("/mnt/bumblebee-burtnolej/googledrive/current/Prep5and6schedulenewworkperiod.csv",-1,True,"56n"),
             ("/mnt/bumblebee-burtnolej/googledrive/current/Prep4schedulenewworkperiod.csv",5,True,"4n")]'''
    
    '''files = [("/mnt/bumblebee-burtnolej/googledrive/current/Prep6IndividualSchedules_new.csv",6,True,"6s"),
             ("/mnt/bumblebee-burtnolej/googledrive/current/Prep5IndividualSchedules_new.csv",5,True,"5s")]'''
    
    '''files = [("/Users/burtnolej/Development/pythonapps/clean/scripts/googledrive/googledrive/current/Prep6IndividualSchedules-2ndSemester_new.csv",6,True,"6s2"),
             ("/Users/burtnolej/Development/pythonapps/clean/scripts/googledrive/googledrive/current/Prep5IndividualSchedules-2ndSemester_new.csv",5,True,"5s2")]'''
    	                                          
    files = [("/Users/burtnolej/Development/pythonapps/clean/scripts/googledrive/googledrive/current/MasterSchedulePrep5&6.csv",6,True,"56m")]
    	
    '''else:
	raise Exception("do not know how to run in this working dir",dir=os.getcwd())'''
    
    print "".join(["env=",env,"db=",databasename])
        
    ssloader = SSLoader(databasename)
    ssloader.keepversion = True
    ssloader.fields =  ['period','dow','subject','teacher','students',"recordtype","record"] 
    ssloader.primary_record = False
    ssloader.run(databasename,files)
