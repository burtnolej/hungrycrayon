import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from misc_utils import Log
from misc_utils_objectfactory import ObjFactory

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get

#from schoolscheduler_utils import *

from Tkinter import *
from ttk import *

from collections import OrderedDict

import tkFont
import unittest

types_enum = ['period','day','other','psych','edu',
              'break','lesson','student','teacher']

period_enum = ['8:30-9:10','9:11-9:51','9:52-10:32','10:33-11:13',
               '11:13-11:45','11:45-12:25','12:26-1:06','1:07-1:47',
               '1:48-2:28','2:30-3:00']
period_map = dict((pe,period_enum.index(pe)) for pe in period_enum)

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

teacher_lesson_type = {"Stan":"","Galina":"","Samantha":"","Amelia":"","Paraic":""}

#teacher_lesson_type = {'MELISSA':'psych','EMILY':'psych','ALEXA':'other','ASHLEY':'other',
#                       'DYLAN':'other','FRAN':'other','ISAAC':'other','KAYLA':'other',
#                       'MOIRA':'other','NATHANIEL':'other','RACHEL':'other','RAHUL':'other',
#                       'RICKY':'other','TRISTAN':'other','YOSEF':'other','CHRIS':'other'}

teacher_enum = teacher_lesson_type.keys()

teacher_map = dict((te,teacher_enum.index(te)) for te in teacher_enum)

log = Log()

controlpanelconfig = dict(height=300,width=200,x=100,y=100)

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

class schoolschedgeneric(dbtblgeneric):

    def __init__(self,objid,**kwargs):

        super(schoolschedgeneric,self).__init__(**kwargs)
        self.objid = objid

        
        for k,v in kwargs['dm'].iteritems():
            if v <> 'None':
                self.attr_set(v,k)
                
    def attr_set(self,name,clsname):
        
        datamembers = _initdatamembers(clsname,name=name)
        setattr(self,clsname,_obj_create(datamembers,self.database,self.of,clsname))
            
        return(getattr(self,clsname))
    
    def __repr__(self):
        return(self.objid)
    
class teacher(schoolschedgeneric):
    pass

class saveversion(schoolschedgeneric):
    pass

class lessontype(schoolschedgeneric):
    pass

class subject(schoolschedgeneric):
    pass

class student(schoolschedgeneric):
    pass

class dow(schoolschedgeneric):
    pass

class period(schoolschedgeneric):
    pass

class userdefid(dbtblgeneric):
    
    def __init__(self,objid,**kwargs):
        
        super(userdefid,self).__init__(**kwargs)
        self.objid = objid
        
    def __repr__(self):
        return(self.objid)

class objtype(dbtblgeneric):
    def __repr__(self):
        return(self.objid)

class lesson(schoolschedgeneric):
    pass


def _initdatamembers(clsname,**kw):
    
    if clsname == 'lesson':       
        try:
            userdefid = str(kw['teacher'])+"."+ \
                str(kw['day_num'])+"."+\
                str(kw['period_num'])
            
            student = student_enum[kw['student_num']]
        except KeyError:
            raise KeyError("lesson init requires args: schedule_num, day_num, period_num, student_num")
        
        dm = {'teacher':kw['teacher'],
              'saveversion':kw['saveversion'],
              'subject':'None',
              'lessontype':'None',
              'period':kw['period_num'],
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

class WizardUI(object):
    def __init__(self,master):

        self.lastsaveversion=0
        
        self.master = master
        self.maxrows=14 # rows in the grid
        self.maxcols=20 # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*self.maxrows # master height
        wmwidth=wwidth*self.maxcols # master width 

        geom = geometry_get(wmheight,wmwidth,0,0)
        #self.master.geometry(self.geom)
        
        master.geometry(geom)
        master.bind("<Prior>",self.focus_next_widget)


        widget_args=dict(background='white')
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        #rowcfg = dict(height=2,width=2,text="x")
        #colcfg = dict(height=2,width=2,text="y")

        setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                            'peach','pomegranate','passionfruit',
                                                            'pear','grape','strawberry','raspberry',
                                                            'rhubarb','mango','guava','apple',
                                                            'Orange'])

        self.entrygridframe = Frame(self.master)
        self.entrygrid = TkImageLabelGrid(self.entrygridframe,setmemberp,wmwidth,wmheight,
                             0,0,self.maxrows,self.maxcols,
                             {},widgetcfg)
                             #{},widgetcfg,1,1,rowcfg,colcfg)
        self.entrygridframe.grid(row=0,column=0,sticky=NSEW)

        controlpanel = Frame(master)
        controlpanel.grid(row=2)
        
        self.save_button = Button(controlpanel,command=self.save,text="save",name="svb")
        self.save_button.grid(row=2,column=0)
        self.save_button.focus_get()
        
        self.persist_button = Button(controlpanel,command=self.persist,text="persist",name="pb")
        self.persist_button.grid(row=2,column=1)
        self.persist_button.focus_get()
        
        self.spacer_label = Label(controlpanel,text="                      ")
        self.spacer_label.grid(row=2,column=2)
        
        self.dbload_entry_label = Label(controlpanel,text="version")
        self.dbload_entry_label.grid(row=2,column=3)
        self.dbload_entry_label.focus_get()
        self.dbload_entry_sv = StringVar()
        self.dbload_entry = Entry(controlpanel,textvariable=self.dbload_entry_sv)
        self.dbload_entry.grid(row=2,column=4)
        self.dbload_entry.focus_get()
        
        self.dbload_button = Button(controlpanel,command=self.load,text="dbload",name="dbl")
        self.dbload_button.grid(row=2,column=5)
        self.dbload_button.focus_get()
        
        
        
        self.bgmaxrows=len(period_enum)+1
        self.bgmaxcols=len(student_enum)+1 
        mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
        self.balancegridframe = Frame(self.master)
        self.balancegrid = TkImageLabelGrid(self.balancegridframe,mytextalphanum,wmwidth,wmheight,
                             0,0,self.bgmaxrows,self.bgmaxcols,
                             {},widgetcfg)
                             #{},widgetcfg,1,1,rowcfg,colcfg)
        self.balancegridframe.grid(row=1,column=0,sticky=NSEW)
        self._draw_balancegrid_labels()
        
        self.master.grid_columnconfigure(0, weight=1, uniform="foo")
        self.master.grid_rowconfigure(0, weight=1, uniform="foo")
        self.master.grid_rowconfigure(1, weight=1, uniform="foo")
            
        
    def _draw_balancegrid_labels(self):
        
        for x in range(len(period_enum)+1):
            self.balancegrid.widgets[x][0].config(text=period_enum[x-1])
            
        for y in range(1,len(student_enum)+1):
            self.balancegrid.widgets[0][y].config(text=student_enum[y-1])
        
        
    def save(self):

        of.reset()
        
        for x in range(1,self.maxrows):
            ylabel=self.entrygrid.widgets[x][0].sv.get()
            
            for y in range(1,self.maxcols):
                xlabel=self.entrygrid.widgets[0][y].sv.get()
                
                value =  self.entrygrid.widgets[x][y].sv.get()
                
                try:
                    value = int(value)
                except:
                    pass
                
                if value <> "":
                    
                    print "record"
                    datamembers = _initdatamembers('lesson',
                                                   schedule_num = '1',
                                                   day_num=1, 
                                                   period_num=ylabel,
                                                   student_num=value,
                                                   saveversion=self.lastsaveversion,
                                                   teacher=xlabel)
                    
                    _lesson_create(datamembers,database,of)
                    
                    # get the actual row number from the period string
                    # add one to account for the origin
                    x = period_map[ylabel]+1
                    
                    current_value = self.balancegrid.widgets[x][value].cget("text")
                    if current_value == xlabel:
                        pass
                    elif current_value == "":
                        
                        self.balancegrid.widgets[x][value].config(background='lightgreen')
                        self.balancegrid.widgets[x][value].config(text=xlabel)
                    else:
                        self.balancegrid.widgets[x][value].config(text=current_value+","+xlabel)
                        self.balancegrid.widgets[x][value].config(background='red')
                    
        self.student_totals_calc()        
            
        self.dbload_entry_sv.set(self.lastsaveversion)
            
        self.lastsaveversion+=1

    def student_totals_calc(self):
        
        for student in range(1,len(student_enum)+1):
            student_full = True
            for x in range(len(period_enum)+1):
                current_value = self.balancegrid.widgets[x][student].cget("text")
                if current_value == "":
                    student_full=False
            if student_full == True:
                self.balancegrid.widgets[0][student].config(background='green')
            
    def focus_next_widget(self,event):
        print "focuschange"
        #nextwidget = self.master.tk_focusNext()
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
    def load(self,values=None):
        
        
        if values==None:
            #load from database
            with database:
                colndefn,rows = tbl_rows_get(database,'lesson',['period','student','teacher','dow'],
                                    ('saveversion',str(self.lastsaveversion)))
            print rows
        else:
                
            for x in range(len(values)):
                for y in range(len(values[0])):
                    self.entrygrid.widgets[x][y].sv.set(values[x][y])

    def persist(self):
        with database:
            for obj in of.object_iter():
                obj.persist()

    
if __name__ == "__main__":
    master = Tk()
    
    
    database = Database('htmlparser')
    of = ObjFactory(True)
    
    ui = WizardUI(master)
    values=[["","Stan","Galina","Samantha","Amelia","Paraic"],
            ['8:30-9:10',1,9,3,5,7],
            ['9:11-9:51',2,1,4,6,8]]
    ui.load(values)
    master.mainloop()