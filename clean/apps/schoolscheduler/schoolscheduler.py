import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log
from misc_utils_objectfactory import ObjFactory
from database_util import Database, tbl_create
from schoolscheduler_defn import *
from schoolscheduler_htmlparser import *

def match_isa_rule_work_lesson(item,datafields):

    if item.find('Work Period') <> -1 or item.find('WP') <> -1 or item.find('W lesson') <> -1 or item.find('Work period') <> -1:
        prefix = item.split(" ")[0]
        if  prefix not in ['Work']: # its a non work period
            datafields['subject'] = prefix.replace(":","")
            datafields['lessontype'] ="wp"
        else:
            datafields['lessontype'] ="nwp"

        suffix=item.split(" ")[-1]
        
        if item.split(" ")[-2] in ['With:','with:','W/']:
            datafields['teacher'] = suffix
        elif len(item.split(" ")) == 3:
            datafields['teacher'] = suffix

        return(True)
    return(False)

def _find(item,tokens,inverse=False):
    item = item.upper()
    for t in tokens:
        if item.find(t) <> -1 and inverse == False:
            return(t)
    return(None)

def match_isa_rule(item, datafields,enum,lessontype):
    _subject = _find(item,enum)
    if _subject == None: return(False)
    datafields['subject'] = _subject
    datafields['lessontype'] = lessontype
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
            raise Exception('no rules matched')

def _initdatamembers(schedule_num,day_num, period_num):
    
    objid = str(schedule_num)+"."+str(day_num-2)+"."+str(period_num-1)
    
    return({'teacher':None,
            'subject':None,
            'lessontype':None,
            'period':period_enum[period_num-1],
            'dow':day_enum[day_num-2],
            'objid':objid})  

def _lesson_create(datamembers,database,of):
    _lesson = _obj_create(datamembers,database,of,'lesson')
    
    return(_lesson)
    
def _teacher_create(datamembers,database,of):
    return(_obj_create(datamembers,database,of,'teacher'))
    
def _obj_create(datamembers,database,of,clsname):
    return(of.new(clsname,
                  objid=datamembers['userdefid'],
                  constructor='datamembers',
                  database=database,
                  of=of,
                  modname=__name__,
                  dm=datamembers))
    

def schedule_load(schedule,of=None,database=None):
    for schedule_num in range(len(schedule)):
        for period_num in range(1,len(schedule[schedule_num])):
            for day_num in range(2,len(schedule[schedule_num][period_num])):
                
                datamembers = _initdatamembers(schedule_num,day_num, 
                                               period_num)
                _enrich(schedule[schedule_num][period_num][day_num],
                        datamembers)
                
                '''_lesson=of.new('lesson',
                                   objid=objid,
                                   constructor='datamembers',
                                   database=database,
                                   of=of,
                                   modname=__name__,
                                   dm={'objtype':"lesson",
                                       'student':students[schedule_num],
                                       'period':_period,
                                       'dow':_dow,
                                       'lessontype':"notset",
                                       'subject':"notset",
                                       'userdefid':objid})'''
                
                
    
                #_lesson.attr_set(students[schedule_num],'student')
                

if __name__ == '__main__':
    database = Database('htmlparser')
    of = ObjFactory(True)
    schedule, students = htmlschedule_parse('schedule.html')
    
    import pprint
    pprint.pprint(schedule)
    exit()
    schedule_load(schedule,of,database)
    
    with database:
        tbl_create(database,'lesson',[('objtype','text'),
                                      ('student','text'),
                                      ('period','integer'),
                                      ('dow','integer'),
                                      ('userdefid','text'),
                                      ('lessontype','integer'),
                                      ('subject','integer'),
                                      ('__timestamp','text'),
                                      ('__id','text')])
        
        tbl_create(database,'teacher',[('objtype','text'),
                                       ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'lessontype',[('objtype','text'),
                                          ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'subject',[('objtype','text'),
                                       ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'student',[('objtype','text'),
                                       ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'objid',[('objtype','text'),
                                     ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'dow',[('objtype','text'),
                                   ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'period',[('objtype','text'),
                                      ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'userdefid',[('objtype','text'),
                                         ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
        
        tbl_create(database,'objtype',[('objtype','text'),
                                         ('userdefid','text'),
                                           ('__timestamp','text'),
                                           ('__id','text')])
    
    
        for obj in of.object_iter():
            print of.object_serialize(obj)
            obj.persist(False)
