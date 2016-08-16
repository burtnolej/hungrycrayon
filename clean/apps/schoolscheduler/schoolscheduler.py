import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log
from misc_utils_objectfactory import ObjFactory
from database_util import Database, tbl_create
#from schoolscheduler_defn import *
from schoolscheduler_htmlparser import *
from schoolscheduler_utils import *

def _validate_token(token,item=None,objtype=None,throwex=True):
    
    for _type in types_enum:
        _type_enum = globals()[_type + "_enum"]
        if token in _type_enum:
            return True
    #return False
    if throwex==True:
        raise Exception("bad "+str(objtype)+" token "+str(token)+" in item "+str(item))
    
def _token_type_get(token,item=None):
    
    for _type in types_enum:
        _type_enum = globals()[_type + "_enum"]
        if token in _type_enum:
            return _type
        
    raise Exception("bad token "+str(token)+" in item "+str(item))
    
def match_isa_rule_work_lesson(item,datafields):

    if item.find('Work Period') <> -1 or item.find('WP') <> -1 or item.find('W lesson') <> -1 or item.find('Work period') <> -1:
        prefix = item.split(" ")[0]
        if  prefix not in ['Work']: # its a non work period           
            _subject = prefix.replace(":","").upper()
            if _validate_token(_subject,item,'subject',throwex=False) == True:
                datafields['subject'] = _subject
            else:
                twowordprefix = item.split(" ")[0].upper() + " " + item.split(" ")[1].upper()
                if _validate_token(twowordprefix,item,'subject') == True:
                    datafields['subject'] = twowordprefix    
             
            datafields['lessontype'] ="wp"
        else:
            datafields['lessontype'] ="nwp"

        suffix=item.split(" ")[-1].upper()
        
        if item.split(" ")[-2] in ['With:','with:','W/']:
            if _validate_token(suffix,item,'teacher') == True:
                datafields['teacher'] = suffix
        
        elif len(item.split(" ")) == 3:
            if _validate_token(suffix,item,'teacher',throwex=False) == True:
                datafields['teacher'] = suffix
            else:
                # there is a scenario where first 2 words are 'work period'
                # and last word is a teacher or a scenario where last 2 words
                # are 'work period' and first word is subject so dont
                # throw an exception here
                pass

        else:
            token = item.split(" ")[-1].split(":")[0]
            
            if token == 'with':
                teacher = item.split(" ")[-1].split(":")[1].upper()
                if _validate_token(teacher,item,'teacher') == True:    
                    datafields['teacher'] = teacher

        return(True)
    elif(len(item.split(" ")) == 1):
        
        item = item.upper()
        _token_type =_token_type_get(item,item)
        
        if _token_type == 'teacher':
            datafields['teacher'] = item
            datafields['lessontype'] =teacher_lesson_type[item]
            return(True)
        else:
            datafields['subject'] = item
            datafields['lessontype'] = _token_type
            
            return(True)
    return(False)

def _find(item,tokens,inverse=False):
    item = item.upper()
    hits=[]
    for t in tokens:
        if item.find(t) <> -1 and inverse == False:
            hits.append(t)
    
    if len(hits) == 1:
        return(hits[0])
    elif len(hits) > 1:
        raise Exception('multiple hits for',item,'in',tokens)
    return(None)

def match_isa_rule(item, datafields,enum,lessontype):
    _subject = _find(item,enum)
    if _subject == None: return(False)
    if _validate_token(_subject.upper(),item,'subject') == True:
        datafields['subject'] = _subject
         
    datafields['lessontype'] = lessontype
    
    if len(item.split(" ")) > 2:
                   
        suffix=item.split(" ")[-1].upper()
        
        if item.split(" ")[-2] in ['With:','with:','W/']:
            if _validate_token(suffix,item,'teacher') == True:    
                datafields['teacher'] = suffix

        else:
            token = item.split(" ")[-1].split(":")[0]
            if token == 'with':
                teacher =  item.split(" ")[-1].split(":")[1].upper()
                if _validate_token(teacher) == True:    
                    datafields['teacher'] = teacher
     
    return(True)
    
def _enrich(item,datafields):
    if item <> "":
        if match_isa_rule_work_lesson(item,datafields) == True:
            pass
        elif match_isa_rule(item,datafields,edu_enum,'edu') == True:
            pass
        elif match_isa_rule(item,datafields,break_enum,'break') == True:
            pass
        elif match_isa_rule(item,datafields,other_enum,'other') == True:
            pass
        elif match_isa_rule(item,datafields,psych_enum,'psych') == True:
            pass
        else:
            raise Exception('no rules matched for:',item)

def schedule_persist(of,database):
    with database:
        for obj in of.object_iter():
            obj.persist()
        
def schedule_load(schedule,of=None,database=None):
    for schedule_num in range(len(schedule)):
        for period_num in range(1,len(schedule[schedule_num])):
            for day_num in range(2,len(schedule[schedule_num][period_num])):

                datamembers = _initdatamembers('lesson',
                                               schedule_num = schedule_num,
                                               day_num=day_num, 
                                               period_num=period_num,
                                               student_num=schedule_num)
                
                _enrich(schedule[schedule_num][period_num][day_num],
                        datamembers)
                
                _lesson_create(datamembers,database,of)

if __name__ == '__main__':
    database = Database('htmlparser')
    of = ObjFactory(True)
    schedule, students = htmlschedule_parse('schedule.html')
    schedule_load(schedule,of,database)
    schedule_persist(of,database)