import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log
from misc_utils_objectfactory import ObjFactory
from misc_utils_enum import enum
from database_table_util import dbtblgeneric
from database_util import Database, tbl_create

from lxml import etree
data = open('schedule.html','r').read()
htmldoc = etree.HTML(data)
database = Database('htmlparser')

def students_get_from_html(htmldoc):
    students=[]
    for _s in htmldoc.xpath('//body')[0].getchildren():
        
        if _s.tag == "p":
            for item in _s.iter():
                if len(item)==0:
                    if item.text <> None:
                        students.append(item.text.replace("\n",""))
    return(students)

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
            #lesson.subject=prefix.replace(":","")
            lesson.attr_set(prefix.replace(":",""),'Subject')
            

        suffix=item.split(" ")[-1]
        
        if item.split(" ")[-2] in ['With:','with:']:
            lesson.attr_set(suffix,'Teacher')

        lesson.type="wp"
        return(True)
    return(False)

def non_work_lesson_isa(lesson, item):
    if item.find('Work Period') == -1 and item.find('WP') == -1 and item.find('W lesson') == -1:
        
        suffix=item.split(" ")[-1]
        try:
            if item.split(" ")[-2] in ['With:','with:']:
                lesson.attr_set(suffix,'Teacher')
                lesson.attr_set(subject,'Subject')
                lesson.attr_set("nwp",'LessonType')
                
                #lesson.subject = item.split(" ")[0]
                #lesson.type = "nwp"
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
    
    lesson.attr_set(_subject,'subject')
    
    #lesson.subject = _find(item,break_enum)
    if _subject == None: return(False)
    lesson.attr_set("break",'lessontype')
    #lesson.type="break"
    return(True)

def edu_lesson_isa(lesson, item):
    _subject = _find(item,edu_enum)
    #lesson.subject = _find(item,edu_enum)
    if _subject == None: return(False)
    lesson.attr_set("edu",'lessontype')
    #lesson.type="edu"
    return(True)

def other_lesson_isa(lesson, item):
    _subject = _find(item,other_enum)
    #lesson.subject = _find(item,other_enum)
    if _subject == None: return(False)
    lesson.attr_set("other",'lessontype')
    #lesson.type="other"
    return(True)

def psych_lesson_isa(lesson, item):
    _subject = _find(item,psych_enum)
    #lesson.subject = _find(item,psych_enum)
    if _subject == None: return(False)
    lesson.attr_set("psych",'lessontype')
    #lesson.type="psych"
    return(True)
    
students = students_get_from_html(htmldoc)

period_enum = ['8:30-9:10','9:11-9:51','9:52-10:32','10:33-11:13',
               '11:13-11:45','11:45-12:25','12:26-1:06','1:07-1:47',
               '1:48-2:28','2:30-3:00']

day_enum = ['Monday','Tuesday','Wednesday','Thursday','Friday']

other_enum = ['MOVEMENT','CORE','YOGA','MUSIC','STUDENT NEWS',
              'GS MECHANIC','CODING/TED TALKS',
              'GAME STAR MECHANIC','BOARD GAMES','SEWING']
psych_enum = ['COUNSELING','SPEECH','READING','EMILY']
edu_enum = ['SCIENCE','STEM','MATH','HUMANITIES','SS','PSYCHOLOGY',
            'ELA','ITALIAN','ART','SOCIAL STUDIES','LITERACY','OT',
            'SOCIAL S']
break_enum = ['LUNCH','COMPUTER TIME','QUAD CAFE','QUADCAFE']

lesson_type = 'wp','nwp','break','edu','other','psych'
of = ObjFactory(True)

class teacher(dbtblgeneric):
    def __repr__(self):
        return(self.objid)
    
class lessontype(dbtblgeneric):
    def __repr__(self):
        return(self.objid)
    
class subject(dbtblgeneric):
    def __repr__(self):
        return(self.objid)
    
class student(dbtblgeneric):
    def __repr__(self):
        return(self.objid)
    
class objid(dbtblgeneric):
    def __repr__(self):
        return(self.objid)
    
class dow(dbtblgeneric):
    def __repr__(self):
        return(self.objid)
    
class period(dbtblgeneric):
    def __repr__(self):
        return(self.objid)

class lesson(dbtblgeneric):
    def __init__(self,objid,**kwargs):

        super(lesson,self).__init__(**kwargs)
        self.objid = objid

        for k,v in kwargs['dm'].iteritems():
            if not hasattr(self,k):
                self.attr_set('none',k)
            else:
                self.attr_set(v,k)
            
        #if not hasattr(self,'subject'):
        #    setattr(self,'subject',None)

        #if not hasattr(self,'teacher'):
        #    setattr(self,'teacher',None)

        #if not hasattr(self,'type'):
        #    setattr(self,'type',None)

    def __repr__(self):
        return(self.objid)

    def attr_set(self,name,clsname):
        setattr(self,clsname,of.new(clsname,
                              objid=name,
                              #constructor='datamembers',
                              database=database,
                              modname=__name__))
                              #dm={objid:"\""+name+"\""}))
    
        return(getattr(self,clsname))
                   

for schedule_num in range(len(schedule)):
    for period_num in range(1,len(schedule[schedule_num])):
        for day_num in range(2,len(schedule[schedule_num][period_num])):
            _period = period_enum[period_num-1]
            _dow =day_enum[day_num-2]
            objid = str(schedule_num)+"."+str(day_num-2)+"."+str(period_num-1)

            lesson=of.new('lesson',
                               objid="\""+objid+"\"",
                               constructor='datamembers',
                               database=database,
                               modname=__name__,
                               dm={'student':"\""+students[schedule_num]+"\"",
                                   'period':"\""+_period+"\"",
                                   'dow':"\""+_dow+"\""})
                                   #'objid':"\""+objid+"\""})


            lesson.attr_set(students[schedule_num],'student')
            
            _i = schedule[schedule_num][period_num][day_num]
            
            if _i <> "":
                if work_lesson_isa(lesson,_i) == True:
                    pass
                elif non_work_lesson_isa(lesson,_i) == True:
                    pass
                elif edu_lesson_isa(lesson,_i) == True:
                    pass
                elif break_lesson_isa(lesson,_i) == True:
                    pass
                elif other_lesson_isa(lesson,_i) == True:
                    pass
                elif psych_lesson_isa(lesson,_i) == True:
                    pass
                else:
                    print _i

with database:
    tbl_create(database,'lesson',[('student','text'),
                                       ('period','integer'),
                                       ('dow','integer'),
                                       ('_objid','text'),
                                       ('__timestamp','text'),
                                       ('__id','text')])
    
    tbl_create(database,'leacher',[('name','text'),
                                       ('__timestamp','text'),
                                       ('__id','text')])

    for obj in of.object_iter():
        obj.persist(False)
