import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from database_table_util import dbtblgeneric

__all__ = ["period_enum","day_enum","other_enum","teacher","lesson","period","dow",
           "objtype","student","subject","lessontype","userdefid","edu_enum","psych_enum",
           "break_enum","lesson_type"]

period_enum = ['8:30-9:10','9:11-9:51','9:52-10:32','10:33-11:13',
               '11:13-11:45','11:45-12:25','12:26-1:06','1:07-1:47',
               '1:48-2:28','2:30-3:00']
day_enum = ['Monday','Tuesday','Wednesday','Thursday','Friday']
other_enum = ['MOVEMENT','CORE','YOGA','MUSIC','CODING/TED TALKS']
psych_enum = ['COUNSELING','SPEECH','READING','EMILY']
edu_enum = ['SCIENCE','STEM','MATH','HUMANITIES','SS','PSYCHOLOGY',
            'ELA','ITALIAN','ART','SOCIAL STUDIES','LITERACY','OT',
            'SOCIAL S']
break_enum = ['LUNCH','COMPUTER TIME','QUAD CAFE','QUADCAFE',
              'GAME STAR MECHANIC','BOARD GAMES','SEWING',
              'GS MECHANIC','STUDENT NEWS']
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
            self.attr_set(v,k)

    def __repr__(self):
        return(self.objid)

    def attr_set(self,name,clsname):
        # this can be factored out using _obj_creater
        setattr(self,clsname,str(self.of.new(clsname,
                                             objid=name,
                                             of=self.of,
                                             constructor='datamembers',
                                             database=self.database,
                                             modname=__name__,
                                             dm={'objtype':clsname,
                                                 'userdefid':name})))

        return(getattr(self,clsname))
