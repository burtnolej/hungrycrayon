import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import Log
from misc_utils_objectfactory import ObjFactory
from misc_utils_enum import enum
from database_table_util import dbtblgeneric
from database_util import Database, tbl_create
from htmlparser_defn import *

__all__ = ["period_enum","day_enum","other_enum","teacher","lesson","period","dow",
           "objtype","student","subject","lessontype","userdefid","edu_enum","psych_enum",
           "break_enum","lesson_type"]

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
            if not hasattr(self,k):
                self.attr_set('none',k)
            else:
                self.attr_set(v,k)

    def __repr__(self):
        return(self.objid)

    def attr_set(self,name,clsname):
        setattr(self,clsname,str(self.of.new(clsname,
                                         objid=name,
                                         of=self.of,
                                         constructor='datamembers',
                                         database=self.database,
                                         modname=__name__,
                                         dm={'objtype':"\""+clsname+"\"",
                                             'userdefid':"\""+name+"\""})))

        return(getattr(self,clsname))
