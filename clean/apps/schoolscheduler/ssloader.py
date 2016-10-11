from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=5,pidlogname=True,proclogname=False)

from misc_utils import os_file_to_string, thisfuncname
from database_table_util import tbl_rows_get, tbl_rows_insert, _quotestrs, _gencoldefn, tbl_exists, \
     tbl_create, tbl_remove
from database_util import Database 
from sswizard_utils import getdbenum, session_code_gen, dbinsert, dbinsert_direct

from sswizard_query_utils import _sessionenum, _maxlessonenum, _maxsessionenum

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
        
        self.database = Database(databasename)
        self.prep = prep
        
        self.rules = {'computertime':[("Computer Time",1),(":",0)],
	              'Movement':[("Movement",1),(":",0)],
	              'Engineering':[("Engineering",1),(":",0)],
	              'Art':[("Art",1),(":",0)],
	              'Music':[("Music",1),(":",0)],
                      'teacher':[(":",1),("(",1),(")",1)],
                      'date':[("/",2)],
                      'noteacher': [(":",1),("(",0),(")",0)],
                      'period' :[(":",2),("-",1)],
	              'ignore' : [("Period",1),(":",0),("(",0),(")",0)],
	              'ignore2' : [("Lunch",1),(":",0),("(",0),(")",0)],
                      #_ENDCELL_' :[("_ENDCELL_",1)],
                      #'_CRETURN_' :[("_CRETURN_",1)]}
                      '_ENDCELL_' :[("^",1)],
                      '_CRETURN_' :[("&",1)],
                      'staffname':[('+',2)],
	              'staffwith':[('with',1),(":",0),("(",0),(")",0)],
	              'dow1':[('Monday',1)],
	              'dow2':[('Tuesday',1)],
	              'dow3':[('Wednesday',1)],
	              'dow4':[('Thursday',1)],
	              'dow5':[('Friday',1)],
	              'academicname':[('-',2)]}
        
        self.synonyms = {}
        self.valid_values = {}
        self.valid_values['students'] = self.loadrefobjects(databasename,'student',True)
        self.valid_values['period'] = self.loadrefobjects(databasename,'period',True)
        self.valid_values['dow'] =  ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        self.valid_values['teacher'] = self.loadrefobjects(databasename,'adult',True)
        self.valid_values['subject'] = self.loadrefobjects(databasename,'subject',True)
    
        self.fields = ['period','dow','subject','teacher','students']

        self.prepmap = self.loadprepmapper()
        
    def pre_process_records(self,records):

        dowidx=-1
	periodidx=-1
        _records=[]
        _errors=[]

        lastrecordtype = None
        staffrecordflag = False
	academicrecordflag = False
	
	enums = {'maps':{},'enums':{},'codes':{}}	
	getdbenum(enums,self.database,'name','period')

	
        for record in records:
            try:
                recordtype = self.identify_record(record)
            except Exception, e:
		
		if  academicrecordflag==True:
		    recordtype="academicstudent"
		else:
		    _errors.append((record,str(e)))
		    log.log(thisfuncname(),2,msg="could not match record to a rule,skipping",record=record,source=self.inputfile)
		    continue


	    if  recordtype == 'academicstudent':
		period = enums['period']['name'][periodidx]
		#dow = self.valid_values['dow'][dowidx]
		subject = "??"
		teacher = academicname
		students = [record.lstrip().strip()]
		_record = [locals()[field] for field in self.fields]
		_records.append(_record)
		log.log(thisfuncname(),10,msg="record added",record=_record)
	    elif recordtype[:6] == "ignore":
		pass
	    elif recordtype in ['teacher','noteacher']:
                #try:
		subject,_rest = self.extract_subject(record)
		teacher = "??"
		
		if recordtype == 'teacher' : 
		    teacher,_rest = self.extract_teacher(_rest)
		elif staffrecordflag == True:
		    teacher = staffname
		    
		students = self.extract_students(_rest)
		
		if academicrecordflag==False: # edge case where academic records is matched
		    dow = self.valid_values['dow'][dowidx]
		else:
		    teacher = academicname
		    period = enums['period']['name'][periodidx]
		    
		_record = [locals()[field] for field in self.fields]
		_records.append(_record)
		log.log(thisfuncname(),10,msg="record added",record=_record)
                #except Exception, e:
                #    _errors.append((record,str(e)))
		#   log.log(thisfuncname(),1,msg="failed while extracting subject, teacher etc",error=e,emsg=e.message,record=record)
		#   continue
            elif recordtype == 'staffname':
                staffname = self.extract_staff(record)
                log.log(thisfuncname(),10,msg="this is a staff file",staffname=staffname)
                staffrecordflag=True
	    elif recordtype in ['Movement','Art','Music','Engineering']:
		if staffrecordflag == True:
		    subject = recordtype
		    teacher = staffname
		    students = []
		    dow = self.valid_values['dow'][dowidx]
		    _record = [locals()[field] for field in self.fields]
		    _records.append(_record)
		    log.log(thisfuncname(),10,msg="record added",record=_record)
	    elif recordtype == "staffwith":
		if staffrecordflag == True:
		    subject,_,_ = record.split(" ")
		    teacher = staffname
		    students = []
		    dow = self.valid_values['dow'][dowidx]
		    _record = [locals()[field] for field in self.fields]
		    _records.append(_record)
		    log.log(thisfuncname(),10,msg="record added",record=_record)
            elif recordtype == 'computertime':
                if self.prep <> -1:
		    students = [name for name,prep in self.prepmap.iteritems() if prep == str(self.prep)]
		    students.sort()
		    teacher = "??"
		    subject = "Computer Time"
		    dow = self.valid_values['dow'][dowidx]
		    _record = [locals()[field] for field in self.fields]
		    _records.append(_record)
		    log.log(thisfuncname(),10,msg="record added",record=_record)
		else:
		    log.log(thisfuncname(),10,msg="skipping Computer Time as Staff File",record=_record)
	    elif recordtype[:3] == 'dow':
		periodidx=-1
		dow = record
		log.log(thisfuncname(),10,msg="setting dow",dow=dow)
		
	    elif recordtype == 'academicname':
                academicname = self.extract_staff(record)
                log.log(thisfuncname(),10,msg="this is an academic file",academicname=academicname)
                academicrecordflag=True
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
		    log.log(thisfuncname(),10,msg="dow reset on period",dow=self.valid_values['dow'][dowidx])
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
                log.log(thisfuncname(),0,msg="could not identify record",recordtype=recordtype,record=record)
                raise SSLoaderFatal
            
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
            raise SSLoaderMultiRuleMatchException
        elif len(match) == 0:
            raise SSLoaderNoRulesMatchException
        else:
            log.log(thisfuncname(),10,msg="rule matched",record=record,matches=match)
            return(match[0])
        
    def appyrules(self,record,rules):
        for char,count in rules:    
            if record.lower().count(char.lower()) <> count:
                return False
        return True
    
    def extract_subject(self,record):
        # works with teacher or no teacher on record
        subject,_rest = record.split(":")
        return(subject,_rest)
    
    def extract_staff(self,record):
        if record[-2:] <> "++" and record[-2:] <> "--":
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
            sizediff = round(float(len(matchee)-len(matcher))/len(matcher),2)
            if sizediff > tolerance:
                return False, sizediff
            return True,sizediff
        else:
            sizediff = round(float(len(matcher)-len(matchee))/len(matchee),2)
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
                    new_value = self.validate_token2(orig_value,self.valid_values[self.fields[i]])
		    
		    if self.synonyms.has_key(new_value):
			log.log(thisfuncname(),10,msg="synonym, swapping",new_value=self.synonyms[new_value],old_value=new_value)
			new_value = self.synonyms[new_value]
		    
            except SSLoaderNoMatchException:
                log.log(thisfuncname(),2,msg="failed to validate record",record=record,file=self.inputfile)

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


	
    @logger(log)
    def dbupdater(self,records):
        
        from misc_utils import IDGenerator
        from datetime import datetime
	from copy import deepcopy

        enums = {'maps':{},'enums':{},'codes':{}}
        
        getdbenum(enums,self.database,'name','period')
        getdbenum(enums,self.database,'name','student')
        getdbenum(enums,self.database,'name','dow')
        
        cols = ['period','dow','subject','teacher','students']
        
        session_count=0
        lesson_count=0
        
        dblessonrows = []
        dbsessionrows = []
        
	dbrecords = []
        for record in records:

            whereclause = []
            d = dict(zip(cols,record))

	    if len(d['students']) == 0:
		log.log(thisfuncname(),2,msg="0 students - check input file",record=record)
		continue
	    
	    #_dow = enums['dow']['name2code'][d['dow']]
	    _period = enums['period']['name2enum'][d['period']]
	    
	    #whereclause.append(['student',"=","\"" + d['students'][0] + "\""])
	    whereclause.append(['period',"=","\"" + str(_period) + "\""])
	    whereclause.append(['dow',"=","\"" + d['dow'] + "\""])                 
	    whereclause.append(['teacher',"=","\"" + d['teacher'] + "\""])   
	    
	    with self.database:
		#colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',['__id','teacher','session','subject'],whereclause)
		colndefn,rows,exec_str = tbl_rows_get(self.database,'session',['__id','teacher','code','subject','enum'],whereclause)
		
	    if len(rows) == 0:
		d['source'] = self.inputfile
		d['__id'] = IDGenerator().getid()
		d['__timestamp'] = datetime.now().strftime("%H:%M:%S")	
		d['prep'] = int(self.prepmap[d['students'][0]])
		#d['period'] = _period
		d['code'] = ".".join([d['teacher'],d['subject'],d['dow']])
		d['type'] = "1-on-1"
		if len(d['students']) > 1:d['type'] = "Group"
		_students = d.pop('students')
		with self.database:
		    _,_session_count,_ = _maxsessionenum(self.database)		    
	    
		session_count = int(_session_count[0][0])+1
		d['enum'] = int(session_count)
		dbinsert(self.database,'session',[d.values()],d.keys())
		
		log.log(thisfuncname(),10,msg="createing session",record=d)
		
		sessioncode = d['code']
		subject = "??"
		sessionenum = session_count		
		
	    else:
		sessioncode = rows[0][2]
		subject = rows[0][3]
		sessionenum = rows[0][4]
		
	    _record = deepcopy(record) # take a copy as sometimes inspect record for testing
	    _record.append(sessioncode) # add sessioncode for inserting into lesson
	    _record.pop(2) # remove old subject
	    _record.insert(2,subject) # add new subject
	    _record.append(sessionenum) # add session_enum
	    
	    dbrecords.append(_record)

	cols = ['period','dow','subject','teacher','students','session','sessionenum']
	
	with self.database:
	    _,_lesson_count,_ = _maxlessonenum(self.database)		    
    
	lesson_count = int(_lesson_count[0][0])+1

	for record in dbrecords:
	    
	    d = dict(zip(cols,record))

	    # set status
	    d['status'] = "complete"
		
	    # move students so we can insert to sessions
	    _students = d.pop('students')  
	    _dow = d['dow']
	    
	    # set who loaded the record
	    d['source'] = self.inputfile

	    _sessionenum = d['sessionenum']
	    d.pop('sessionenum')
	    
	    for student in _students:
	
		_period =  int(enums['period']['name2enum'][d['period']])
		_prep = int(self.prepmap[student])
		_code = "\"" + d['session'] + "\""
		
		#with self.database:
		#    _,session_enum,exec_str = _sessionenum(self.database,_code,_period,_prep)
		    
		#if len(session_enum) == 0:
		#    log.log(thisfuncname(),2,msg="no session exists;need to create",record=record)
		#    continue
		
		# student enum
		d['student'] = student
		student_enum = enums['student']['name2enum'][student]
		
		d['dow'] = enums['dow']['name2code'][_dow]
		
		# set prep per student as could be cross preps
		d['prep'] = int(self.prepmap[student])
		
		# lesson enum
		d['enum'] = lesson_count
		
		# code
		d['session'] = ".".join([d['teacher'],d['subject'],_dow]) 
		
		# create userobjid
		d['userobjid'] = ",".join(map(str,[d['period'],student_enum,_sessionenum,d['teacher']]))
		
		# set the saveversion
		d['saveversion'] = 1
		
		d['__id'] = IDGenerator().getid()
		d['__timestamp'] = datetime.now().strftime("%H:%M:%S")

		dbinsert(self.database,'lesson',[d.values()],d.keys())
		
		lesson_count += 1

	    
    @logger(log)
    def dbloader(self,records):
        
        from misc_utils import IDGenerator
        from datetime import datetime

        enums = {'maps':{},'enums':{},'codes':{}}
        
        getdbenum(enums,self.database,'name','period')
        getdbenum(enums,self.database,'name','student')
        getdbenum(enums,self.database,'name','dow')
        
        
        cols = ['period','dow','subject','teacher','students']
        
        session_count=0
        lesson_count=0
        
        dblessonrows = []
        dbsessionrows = []
        
        for record in records:
            
            d = dict(zip(cols,record))

            # get an id
            d['__id'] = IDGenerator().getid()
            d['__timestamp'] = datetime.now().strftime("%H:%M:%S")
            
            # lookup prep
            
            try:
                student = d['students'][0]
            except IndexError:
                log.log(thisfuncname(),10,msg="no student name found, creating session only",record=record)
                #continue
            
            d['prep'] = int(self.prepmap[student])

            # lookup period enum
            _period = d['period']
            d['period'] =  int(enums['period']['name2enum'][_period])
            
            # lookup session code
            d['code'] = ".".join([d['teacher'],d['subject'],d['dow']]) 
            
            # create session type
            d['type'] = "1-on-1"
            if len(d['students']) > 1:d['type'] = "Group"
            
            # move students so we can insert to sessions
            _students = d.pop('students')

	    # set who loaded the record
	    d['source'] = self.inputfile            

            # insert session record
            d['enum'] = int(session_count)
	    
            #dbinsert(self.database,'session',[d.values()],d.keys())
            dbsessionrows.append(d.values())
	    
	    # set the cols so we can do a bulk load to db later
	    if session_count ==0: dbsessioncols = d.keys()

            # change col name for session code
            d['session'] = d['code']
            d.pop('code')

            # get rid of remaining fields not needed for lesson record
            d.pop('type')
            d.pop('enum')

            # store the day code for the lesson record
            d['dow'] = enums['dow']['name2code'][d['dow']]
            
            # store the period name for the lesson record
            d['period'] = _period
	    
	    # set status
	    d['status'] = "complete"
	    if d['teacher'] == '??':
		d['status'] = "incomplete"
            
            for student in _students:

                # student enum
                d['student'] = student
                student_enum = enums['student']['name2enum'][student]
                
                # set prep per student as could be cross preps
                d['prep'] = int(self.prepmap[student])
		
                # lesson enum
                d['enum'] = int(lesson_count)
                
                # create userobjid
		
		'''
		periodenum dayenum studenenum
		load them all into a hash using userobjid; set a complete and incomplete attribute and store the asociated id
		then parse list setting the tags
		'''
		
                d['userobjid'] = ",".join(map(str,[d['period'],student_enum,session_count]))   
                
                # set the saveversion
                d['saveversion'] = 1
                
                # insert lesson record
		#if d['teacher'] <> "??":
		dblessonrows.append(d.values())
		#else:
		#    log.log(thisfuncname(),3,msg="no teacher provided; not creating lesson from session",record=d)

                # set the cols so we can do a bulk load to db later
                if lesson_count ==0: dblessoncols = d.keys()

                lesson_count += 1
                
            session_count+=1
            
        with self.database:
            
            dblessoncoldefn = _gencoldefn(dblessonrows[0],dblessoncols)
	    dbsessioncoldefn = _gencoldefn(dbsessionrows[0],dbsessioncols)
	    
	    if not tbl_exists(self.database,'lesson') ==True:
		tbl_create(self.database,'lesson',dblessoncoldefn)    
		
	    if not tbl_exists(self.database,'session') ==True:
		tbl_create(self.database,'session',dbsessioncoldefn)    

	    maxrowsize = 300
            dblessonrows = _quotestrs(dblessonrows)
	    dbsessionrows = _quotestrs(dbsessionrows)
	    for starti in range(0,len(dblessonrows),maxrowsize):
		if starti+maxrowsize > len(dblessonrows):
		    endi = len(dblessonrows)
		else:
		    endi = starti + (maxrowsize-1)
		
		tbl_rows_insert(self.database,'lesson',dblessoncols,dblessonrows[starti:endi])
		log.log(thisfuncname(),10,msg="loaded rows to lesson",numrow=endi-starti)
		    
	    tbl_rows_insert(self.database,'session',dbsessioncols,dbsessionrows)               
	    log.log(thisfuncname(),10,msg="loaded row to session",numrows=len(dbsessionrows))

    def _sessionhashmapget(self):
	
	enums = {'maps':{},'enums':{},'codes':{}}
	
	getdbenum(enums,self.database,'name','period')
	getdbenum(enums,self.database,'name','dow')

	cols = ['period','dow','teacher','subject']
	
	with self.database:
	    _,rows,_ = tbl_rows_get(self.database,'session',cols)

	hashmap={}
	for row in rows:

	    d = dict(zip(cols,row))
	    
	    try:
		_dow = enums['dow']['name2code'][d['dow']]
		_period = enums['period']['enum2name'][d['period']]
	    except:
		continue
	    
	    hashkey = ".".join([_dow,str(_period),d['subject']])
	    
	    if hashmap.has_key(hashkey) == False:		
		hashmap[hashkey] = []
		
	    if d['teacher'] <> '??':
		hashmap[hashkey].append(d['teacher'])

	return hashmap
	    
	
    def primary_record_set(self):
	
	def _additem(items,newitem):
	    # if newitem is not 'notset/??' then add item to the list of items if its not already present.
	    
	    if newitem <> "??":
		# if items is unset then set it
		if len(items) == 1:
		    if items[0] == "??":
			items[0] = newitem
		
	def _itemset(items):
	    # return True if list still equals initial value ["??"]
	    if items <> ["??"]: return True
	    return False
	    
	cols = ['period','dow','student','teacher','subject','status','source']
	
	# order by makes sure any completed records get 
	with self.database:
	    _,rows,_ = tbl_rows_get(self.database,'lesson',cols)

	sessionhashmap = self._sessionhashmapget()
	
	hashmap={}
	for row in rows:

	    d = dict(zip(cols,row))
	    
	    hashkey = ".".join([d['dow'],d['period'],d['student']])
	    
	    if hashmap.has_key(hashkey) == False:		
		hashmap[hashkey] = dict(subject=["??"],teacher=["??"], \
		                        student=d['student'],status="unset",period=d['period'],\
		                        dow=d['dow'],source="")

	    _additem(hashmap[hashkey]['teacher'],d['teacher'])
	    _additem(hashmap[hashkey]['subject'],d['subject'])

	for row in rows:

	    d = dict(zip(cols,row))
	     
	    try:
		sessions = sessionhashmap[".".join([d['dow'],str(d['period']),d['subject']])]
		
		for newteacher in sessions:
		    _additem(hashmap[hashkey]['teacher'],newteacher)	
	    except KeyError:
		pass    


	for row in rows:
	    
	    d = dict(zip(cols,row))
	
	    hashkey = ".".join([d['dow'],d['period'],d['student']])    
	    
	    if _itemset(hashmap[hashkey]['subject']) and _itemset(hashmap[hashkey]['teacher']):
		hashmap[hashkey]['status'] = "primary"
	    elif hashmap[hashkey]['subject'] == "Computer Time":
		hashmap[hashkey]['status'] = "primary"

	    
	return (hashmap)
    	
    def ssloader(self,files,databasename="htmlparser"):
        
        for file,prep in files:
            
            self.inputfile = file
	    self.prep = prep
            fileasstring = self.file2string(file)
    
            records = self.string2records(fileasstring)
    
            clean_records,_,_ = self.pre_process_records(records)
    
            validated_clean_records = []
            for clean_record in clean_records:
                validated_clean_records.append(self.validate_tokens(clean_record))
                
	    self.dbloader(validated_clean_records)

    def run(self,dbname):

	def _getprimarykeyhash(pred=None,predval=None):
    
	    cols = ['dow','period','student']
	    hashmap = self.ssloader.primary_record_set()
	    
	    # add the key components to the flat output record
	    results = []      
	    for hashkey in hashmap:
		hashmap[hashkey].pop('source')
		d = dict(zip(cols,hashkey.split(".")))
		results.append(hashmap[hashkey].values())
	    results.sort()
	    return results   

	self.databasename = dbname
	self.database = Database(self.databasename)
	try:
	    with self.database:
		tbl_remove(self.database,'lesson')
		tbl_remove(self.database,'session')
	except:
	    pass
    
	# load in prep 5 via dbinsert
	print "loading prep5"
	self.ssloader = SSLoader(self.databasename)
	self.ssloader.ssloader([('prep5data.csv',5)],self.databasename)
    
	# load in prep 4 via dbinsert
	print "loading prep4"
	self.ssloader = SSLoader(self.databasename)
	self.ssloader.ssloader([('prep4data.csv',4)],self.databasename)  

	# load in prep 6 via dbinsert
	print "loading prep6"
	self.ssloader = SSLoader(self.databasename)
	self.ssloader.ssloader([('prep6data.csv',6)],self.databasename)  

	# load in staff via dbinsert
	print "loading staff"
	self.ssloader = SSLoader(self.databasename)
	self.ssloader.ssloader([('staff.csv',-1)],self.databasename)  

	# load in academic via dbupdater
	print "loading academic"
	self.ssloader = SSLoader(self.databasename)
	self.ssloader.inputfile = "academic.csv"
	fileasstring = self.ssloader.file2string("academic.csv")
	records = self.ssloader.string2records(fileasstring)
	self.clean_records,_,_ = self.ssloader.pre_process_records(records)

	self.validated_clean_records = []
	for clean_record in self.clean_records:
	    self.validated_clean_records.append(self.ssloader.validate_tokens(clean_record))

	self.ssloader.dbupdater(self.validated_clean_records)
	
	# create master record set in _new
	print "creating master record"
	self.databasename = dbname + "_new"
	self.database = Database(self.databasename)
    
	cols = ['status','teachers','student','subject','period','dow']
	rows = _getprimarykeyhash()
	
	# strip out required columns from the primarykeyhash
	newrows = []
	for row in rows:    
	    d = dict(zip(cols,row))
	    newrows.append([d['period'],d['dow'],d['subject'][0],d['teachers'][0],d['student'],'1-on-1'])
    
	print "loading master record"
	dbinsert_direct(self.database,newrows,'session','test')
	dbinsert_direct(self.database,newrows,'lesson','test')

if __name__ == "__main__":
    databasename = "quad"
    
    ssloader = SSLoader(databasename)
    ssloader.run(databasename)
