import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from database_table_util import dbtblgeneric
from schoolscheduler_utils import *
from misc_utils import Log

__all__ = ["period_enum","day_enum","other_enum","teacher","lesson","period","dow",
           "objtype","student","subject","lessontype","userdefid","edu_enum","psych_enum",
           "break_enum","lesson_enum","_initdatamembers","_lesson_create", \
           "_obj_create","teacher_enum","types_enum","student_enum", \
           "teacher_lesson_type"]

types_enum = ['period','day','other','psych','edu',
             'break','lesson','student','teacher']

period_enum = ['8:30-9:10','9:11-9:51','9:52-10:32','10:33-11:13',
               '11:13-11:45','11:45-12:25','12:26-1:06','1:07-1:47',
               '1:48-2:28','2:30-3:00']
day_enum = ['Monday','Tuesday','Wednesday','Thursday','Friday']
other_enum = ['MOVEMENT','CORE','YOGA','MUSIC','CODING/TED TALKS',
              'REGENTS PREP','REGIONS PREP','READING PERIOD',
              'INDEPENDENT READING','MENTORING','READING','CAR BLOG',
              'INDEPENDENT STUDY','SUBWAY BLOG','VIDEO GAME BLOG']

psych_enum = ['COUNSELING','SPEECH']
edu_enum = ['SCIENCE','STEM','MATH','HUMANITIES','PSYCHOLOGY',
            'ELA','ITALIAN','ART','SOCIAL STUDIES','LITERACY','OT',
            'ANIMAL RESEARCH','ESPANOL']
break_enum = ['END COMPUTER TIME','LUNCH COMPUTER TIME','QUAD CAFE','QUADCAFE',
              'GAME STAR MECHANIC','BOARD GAMES','SEWING',
              'GS MECHANIC','STUDENT NEWS','CHESS']
lesson_enum = 'wp','nwp','break','edu','other','psych'

student_enum = ['NATHANIEL','TRISTAN','SIMON A.','ORIG','COBY',
                'BOOKER',
                'ASHLEY','YOSEF','LUCY','JAKE','ASHER',
                'DONOVAN','LIAM','SIMON B','NICK']

teacher_lesson_type = {'MELISSA':'psych','EMILY':'psych','ALEXA':'other','ASHLEY':'other',
                       'DYLAN':'other','FRAN':'other','ISAAC':'other','KAYLA':'other',
                       'MOIRA':'other','NATHANIEL':'other','RACHEL':'other','RAHUL':'other',
                       'RICKY':'other','TRISTAN':'other','YOSEF':'other','CHRIS':'other'}

teacher_enum = teacher_lesson_type.keys()

log = Log()
#['ALEXA','ASHLEY','DYLAN','EMILY','FRAN','ISAAC','KAYLA','MOIRA',\
#                'NATHANIEL','RACHEL','RAHUL','RICKY','TRISTAN','YOSEF', \
#                'EMILY','MELISSA']

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

class userdefid(dbtblgeneric):
    def __repr__(self):
        return(self.objid)

class objtype(dbtblgeneric):
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
            if v <> 'None':
                self.attr_set(v,k)

    def __repr__(self):
        return(self.objid)

    def attr_set(self,name,clsname):
        datamembers = _initdatamembers(clsname,name=name)
        
        setattr(self,clsname,_obj_create(datamembers,
                                         self.database,
                                         self.of,
                                         clsname))

        return(getattr(self,clsname))

def _initdatamembers(clsname,**kw):
    
    if clsname == 'lesson':       
        try:
            userdefid = str(kw['schedule_num'])+"."+ \
                str(kw['day_num'])+"."+\
                str(kw['period_num'])
            
            '''userdefid = str(kw['schedule_num'])+"."+ \
                str(kw['day_num']-2)+"."+\
                str(kw['period_num']-1)'''
            
            student = student_enum[kw['student_num']]
        except KeyError:
            raise KeyError("lesson init requires args: schedule_num, day_num, period_num, student_num")
        
        dm = {'teacher':'None',
              'subject':'None',
              'lessontype':'None',
              'period':period_enum[kw['period_num']],
              'dow':day_enum[kw['day_num']],
              'student':student}
    else:
        try:
            userdefid = str(kw['name'])
        except KeyError:
            print 
            raise KeyError(clsname,"init requires args: schedule_num, day_num, period_num")

        dm = {}
        
    dm['objtype'] = clsname
    dm['userdefid'] = userdefid
    return(dm)
        
def _lesson_create(datamembers,database,of):
    _lesson = _obj_create(datamembers,database,of,'lesson')
    return(_lesson)
    
def _obj_create(datamembers,database,of,clsname):
    return(of.new(clsname,
                  objid=datamembers['userdefid'],
                  constructor='datamembers',
                  database=database,
                  of=of,
                  modname=__name__,
                  dm=datamembers))
    