import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log, ObjFactory
from misc_utils_enum import enum

from lxml import etree
data = open('schedule.html','r').read()
htmldoc = etree.HTML(data)

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
            lesson.subject=prefix.replace(":","")

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
                lesson.subject = item.split(" ")[0]
                lesson.type = "nwp"
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
    
    lesson.subject = _find(item,break_enum)
    if lesson.subject == None: return(False)
    lesson.type="break"
    return(True)

def edu_lesson_isa(lesson, item):

    lesson.subject = _find(item,edu_enum)
    if lesson.subject == None: return(False)
    lesson.type="edu"
    return(True)

def other_lesson_isa(lesson, item):

    lesson.subject = _find(item,other_enum)
    if lesson.subject == None: return(False)
    lesson.type="other"
    return(True)

def psych_lesson_isa(lesson, item):

    lesson.subject = _find(item,psych_enum)
    if lesson.subject == None: return(False)
    lesson.type="psych"
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


of = ObjFactory(True)

class Teacher(generic):
    def __init__(self,name):
        super(Teacher,self).__init__()
        self.name = name

    def __repr__(self):
        return(self.name)

class Lesson(generic):
    def __init__(self,objid,**kwargs):

        super(Lesson,self).__init__(**kwargs)
        self.objid = objid

        if not hasattr(self,'subject'):
            setattr(self,'subject',None)

        if not hasattr(self,'teacher'):
            setattr(self,'teacher',None)

        if not hasattr(self,'type'):
            setattr(self,'type',None)

    def __repr__(self):
        return(self.objid)

    def attr_set(self,name,clsname):
        self.teacher = of.new(clsname,name,modname=__name__)

for schedule_num in range(len(schedule)):
    for period_num in range(1,len(schedule[schedule_num])):
        for day_num in range(2,len(schedule[schedule_num][period_num])):
            period = period_enum[period_num-1]
            dow =day_enum[day_num-2]
            objid = str(schedule_num)+"."+str(day_num-2)+"."+str(period_num-1)

            lesson= of.new('Lesson',objid,
                                     modname=__name__,
                                     student = students[schedule_num],
                                     period=period,
                                     dow=dow)
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

for obj in of.query('Lesson'):
    print obj.dump()
