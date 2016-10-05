from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,pidlogname=True,proclogname=False)

from misc_utils import os_file_to_string, thisfuncname
from database_table_util import tbl_rows_get, tbl_rows_insert, _quotestrs, _gencoldefn, tbl_exists, tbl_create
from database_util import Database 
from sswizard_utils import getdbenum, session_code_gen, dbinsert


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
    
    def __init__(self,databasename,prep):
        
        self.database = Database(databasename)
        self.prep = prep
        
        self.rules = {'computertime':[("Computer Time",1)],
                      'teacher':[(":",1),("(",1),(")",1)],
                      'date':[("/",2)],
                      'noteacher': [(":",1),("(",0),(")",0)],
                      'period' :[(":",2),("-",1)],
                      #_ENDCELL_' :[("_ENDCELL_",1)],
                      #'_CRETURN_' :[("_CRETURN_",1)]}
                      '_ENDCELL_' :[("^",1)],
                      '_CRETURN_' :[("&",1)],
                      'staffname':[('+',2)]}
        
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
        _records=[]
        _errors=[]

        lastrecordtype = None
        staffrecordflag = False
        for record in records:
            try:
                recordtype = self.identify_record(record)
            except Exception, e:
                _errors.append((record,str(e)))
                log.log(thisfuncname(),1,msg="could not match record to a rule,skipping",record=record)
                continue
            
            if recordtype in ['teacher','noteacher']:
                #try:
		subject,_rest = self.extract_subject(record)
		teacher = "??"
		
		if recordtype == 'teacher' : 
		    teacher,_rest = self.extract_teacher(_rest)
		elif staffrecordflag == True:
		    teacher = staffname
		    
		students = self.extract_students(_rest)
		
		dow = self.valid_values['dow'][dowidx]
		_record = [locals()[field] for field in self.fields]
		_records.append(_record)
		log.log(thisfuncname(),10,msg="record added",record=_record)
                #except Exception, e:
                #    _errors.append((record,str(e)))
		#   log.log(thisfuncname(),1,msg="failed while extracting subject, teacher etc",error=e,emsg=e.message,record=record)
		#   continue
            elif recordtype == 'staffname':
                staffname = self.extract_staff(record)
                log.log(thisfuncname(),3,msg="this is a staff file",staffname=staffname)
                staffrecordflag=True
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
                
            elif recordtype == 'date':
                pass
            elif recordtype == '_CRETURN_':
                pass
            elif recordtype == 'blankrow':
                pass
            elif recordtype == 'period':
                period = self.extract_period(record)
                dowidx=-1
                log.log(thisfuncname(),10,msg="dow reset on period",dow=self.valid_values['dow'][dowidx])
            elif recordtype == '_ENDCELL_':
                old_dowidx = dowidx
                # increment day each time we hit an end of cell marker; set to -1 at 4 so that
                # period cell is missed on the next line.
                if dowidx==4:dowidx=-1
                dowidx+=1
                
                log.log(thisfuncname(),10,msg="dow increment",old_dowidx=old_dowidx,dowidx=dowidx,lastrecordtype=lastrecordtype)
                
            else:
                log.log(thisfuncname(),0,msg="could not identify record",record=record)
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
        cols = ['synonym']
        database = Database(databasename)
        
        with database:
            _,rows,_ = tbl_rows_get(database,'synonyms',cols,[['objtype','=',"\""+objtype+"\""]])
        
        rows = [row[0] for row in rows]
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
            if record.count(char) <> count:
                return False
        return True
    
    def extract_subject(self,record):
        # works with teacher or no teacher on record
        subject,_rest = record.split(":")
        return(subject,_rest)
    
    def extract_staff(self,record):
        if record[-2:] <> "++":
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
            log.log(thisfuncname(),1,msg="not ending with bracket then spaces",record=record)
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
                if matchee[i] == matcher[i]:
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
            except SSLoaderNoMatchException:
                log.log(thisfuncname(),2,msg="failed to validate record",record=record,file=self.inputfile)

            if orig_value <> new_value:
                record.remove(orig_value)
                record.insert(i,new_value)
        return record
    
    def validate_token2(self,token,valid_values,tolerance=0.8):
        
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
                    
        log.log(thisfuncname(),2,msg="failed to validate token",token=token,file=self.inputfile)
        raise SSLoaderNoMatchException
    
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
                log.log(thisfuncname(),1,msg="no student name found, skipping",record=record)
                continue
            
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
            
            for student in _students:

                # student enum
                d['student'] = student
                student_enum = enums['student']['name2enum'][student]
                
                # set prep per student as could be cross preps
                d['prep'] = int(self.prepmap[student])
		
                # lesson enum
                d['enum'] = int(lesson_count)
                
                # create userobjid
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
		
		print starti,endi
		tbl_rows_insert(self.database,'lesson',dblessoncols,dblessonrows[starti:endi])
		log.log(thisfuncname(),10,msg="loaded rows to lesson",numrow=endi-starti)
		    
	    tbl_rows_insert(self.database,'session',dbsessioncols,dbsessionrows)               
	    log.log(thisfuncname(),10,msg="loaded row to session",numrows=len(dbsessionrows))

        
    def ssloader(self,files,databasename):
        
        for file in files:
            
            self.inputfile = file
            fileasstring = self.file2string(file)
    
            records = self.string2records(fileasstring)
    
            clean_records,_,_ = self.pre_process_records(records)
    
            validated_clean_records = []
            for clean_record in clean_records:
                validated_clean_records.append(self.validate_tokens(clean_record))
                
            
        self.dbloader(validated_clean_records)
 
if __name__ == "__main__":
    ssloader = SSLoader(databasename,prep)
 
    files = ["prep4data.csv"]
    #files = ["prep4data.csv","prep5data.csv","prep6data.csv","staffdata.csv"]
    
    ssloader.ssloader(files)
    
