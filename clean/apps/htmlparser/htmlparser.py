import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log
from misc_utils_objectfactory import ObjFactory
from misc_utils_enum import enum
from database_table_util import dbtblgeneric
from database_util import Database, tbl_create
from htmlparser_defn import *

from lxml import etree
data = open('schedule.html','r').read()
htmldoc = etree.HTML(data)
database = Database('htmlparser')
of = ObjFactory(True)

def students_get_from_html(htmldoc):
    students=[]
    for _s in htmldoc.xpath('//body')[0].getchildren():
        
        if _s.tag == "p":
            for item in _s.iter():
                if len(item)==0:
                    if item.text <> None:
                        students.append(item.text.replace("\n",""))
    return(students)

students = students_get_from_html(htmldoc)
table = [table for table in htmldoc.xpath('//table')]

schedule=[]
for _table in table:
    row = [row for row in _table.xpath('.//tr')]
    rw=[]
    for _row in row:
        item = [item for item in _row.xpath('.//td')]   
        i =[]
        for _item in item:
            _str=""
            for part in _item.iter():
                try:
                    _str = _str + part.text.replace("\n","").replace("\t"," ")
                except AttributeError:
                    pass
                
            _i = _str.split(" ")

            __str=""
            for __i in _i:
                if __i <> "":
                    if _str == "":
                        _str = __i
                    else:
                        __str = __str + " " + __i

            i.append(__str.strip())
        rw.append(i)
    schedule.append(rw)

def work_lesson_isa(lesson, item):

    if item.find('Work Period') <> -1 or item.find('WP') <> -1 or item.find('W lesson') <> -1:
        prefix = item.split(" ")[0]
        if  prefix not in ['Work']:
            lesson.attr_set(prefix.replace(":",""),'subject')

        suffix=item.split(" ")[-1]
        
        if item.split(" ")[-2] in ['With:','with:']:
            lesson.attr_set(suffix,'teacher')

        lesson.type="wp"
        return(True)
    return(False)

def non_work_lesson_isa(lesson, item):
    if item.find('Work Period') == -1 and item.find('WP') == -1 and item.find('W lesson') == -1:
        
        suffix=item.split(" ")[-1]
        try:
            if item.split(" ")[-2] in ['With:','with:']:
                lesson.attr_set(suffix,'teacher')
                lesson.attr_set(subject,'subject')
                lesson.attr_set("nwp",'lessontype')
                return(True)            
        except:
            pass

    return(False)

def _find(item,tokens,inverse=False):
    
    item = item.upper()
    for t in tokens:
        if item.find(t) <> -1 and inverse == False:
            return(t)
    
    return(None)

def break_lesson_isa(lesson,item):
    _subject = _find(item,break_enum)
    if _subject == None: return(False)
    lesson.attr_set(_subject,'subject')
    lesson.attr_set("break",'lessontype')
    return(True)

def edu_lesson_isa(lesson, item):
    _subject = _find(item,edu_enum)
    if _subject == None: return(False)
    lesson.attr_set(_subject,'subject')
    lesson.attr_set("edu",'lessontype')
    return(True)

def other_lesson_isa(lesson, item):
    _subject = _find(item,other_enum)
    if _subject == None: return(False)
    lesson.attr_set(_subject,'subject')
    lesson.attr_set("other",'lessontype')
    return(True)

def psych_lesson_isa(lesson, item):
    _subject = _find(item,psych_enum)
    if _subject == None: return(False)
    lesson.attr_set(_subject,'subject')
    lesson.attr_set("psych",'lessontype')
    return(True)
    
for schedule_num in range(len(schedule)):
    for period_num in range(1,len(schedule[schedule_num])):
        for day_num in range(2,len(schedule[schedule_num][period_num])):
            _period = period_enum[period_num-1]
            _dow =day_enum[day_num-2]
            objid = str(schedule_num)+"."+str(day_num-2)+"."+str(period_num-1)

            _lesson=of.new('lesson',
                               objid="\""+objid+"\"",
                               constructor='datamembers',
                               database=database,
                               of=of,
                               modname=__name__,
                               dm={'objtype':"\"lesson\"",
                                   'student':"\""+students[schedule_num]+"\"",
                                   'period':"\""+_period+"\"",
                                   'dow':"\""+_dow+"\"",
                                   'lessontype':"\"notset\"",
                                   'subject':"\"notset\"",
                                   'userdefid':"\""+objid+"\""})

            _lesson.attr_set(students[schedule_num],'student')
            
            _i = schedule[schedule_num][period_num][day_num]
            
            if _i <> "":
                if work_lesson_isa(_lesson,_i) == True:
                    pass
                elif non_work_lesson_isa(_lesson,_i) == True:
                    pass
                elif edu_lesson_isa(_lesson,_i) == True:
                    pass
                elif break_lesson_isa(_lesson,_i) == True:
                    pass
                elif other_lesson_isa(_lesson,_i) == True:
                    pass
                elif psych_lesson_isa(_lesson,_i) == True:
                    pass
                else:
                    print _i

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
