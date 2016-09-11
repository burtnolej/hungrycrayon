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

teachers = ["Stan","Galina","Samantha","Amelia","Paraic"]

students = ['NATHANIEL','TRISTAN','SIMON A.','ORIG','COBY','BOOKER',
            'ASHLEY','YOSEF','LUCY','JAKE','ASHER','DONOVAN','LIAM','SIMON B','NICK']

def _get_enums(values):
    type = OrderedDict()
    map = OrderedDict()
    enum = []
    
    for i in range(len(values)):
        type[values[i]] = ""
        map[values[i]] = i
        enum.append(values[i])
    
    return(type,map,enum)

teacher_lesson_type,teacher_map,teacher_enum = _get_enums(teachers)

_,student_map,student_enum = _get_enums(students)

log = Log()

controlpanelconfig = dict(height=300,width=200,x=100,y=100)

class schoolschedgeneric(dbtblgeneric):

    def __init__(self,of,database,recursion=True,**kwargs):
        super(schoolschedgeneric,self).__init__(database=database,
                                                **kwargs)
        
        self.of = of
        self.database = database
        
        for k,v in kwargs['dm'].iteritems():
            if v <> 'None':
                if recursion == True:
                    # create objects for all member attributes
                    self.attr_set(v,k)
                                   
    def attr_set(self,name,clsname):        
        datamembers = dict(objtype=clsname,
                           userobjid=name,
                           name=name)
        
        setattr(self,clsname,self.of.new(schoolschedgeneric,
                                         clsname,
                                         objid=name, # unique key to store obj in of
                                         constructor='datamembers',
                                         database=self.database,
                                         of=self.of,
                                         modname=__name__,
                                         recursion=False,
                                         dm=datamembers))

            
        return(getattr(self,clsname))
    
    def __repr__(self):
        return(self.objid)

class WizardUI(Frame):
    def __init__(self,master,database,of):
        
        self.database = database
        self.of = of

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
        
        master.geometry(geom)
        
        Frame.__init__(self,master)
        self.bind("<Prior>",self.focus_next_widget)
        self.grid()


        '''
        # default combolist values is student
        setmemberp = SetMemberPartial(name='x{mylist}',set=student_enum)
        widget_args=dict(background='white',var=setmemberp)
        
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        # column headers are teacher
        setmemberp = SetMemberPartial(name='x{mylist}',set=teacher_enum)
        _widget_args=dict(background='white',var=setmemberp)      
        for y in range(1,self.maxcols):
            widgetcfg[0][y] = _widget_args  

        # row headers are teacher
        setmemberp = SetMemberPartial(name='x{mylist}',set=period_enum)
        _widget_args=dict(background='white',values=setmemberp)    
        for x in range(1,self.maxrows):
            widgetcfg[x][0] = _widget_args

        self.entrygrid = TkImageLabelGrid(self,wmwidth,wmheight,    
                             0,0,self.maxrows,self.maxcols,
                             {},widgetcfg)
        '''
        
        # default combolist values is student
        
        setmemberp = SetMemberPartial(name='x{mylist}',set=student_enum)
        widget_args=dict(background='white',values=student_enum)
        
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        # column headers are teacher
        setmemberp = SetMemberPartial(name='x{mylist}',set=teacher_enum)
        _widget_args=dict(background='white',values=teacher_enum)     
        for y in range(1,self.maxcols):
            widgetcfg[0][y] = _widget_args  

        # row headers are teacher
        setmemberp = SetMemberPartial(name='x{mylist}',set=period_enum)
        _widget_args=dict(background='white',values=period_enum)     
        for x in range(1,self.maxrows):
            widgetcfg[x][0] = _widget_args

        setmemberp = SetMemberPartial(name='x{mylist}',set=period_enum)

        self.entrygrid = TkImageLabelGrid(self,setmemberp,wmwidth,wmheight,    
                             0,0,self.maxrows,self.maxcols,
                             {},widgetcfg)

        self.entrygrid.grid(row=0,column=0,sticky=NSEW)
        
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
        
        self.dbload_button = Button(controlpanel,
                                    command=lambda: self.load(self.dbload_entry_sv.get()),
                                    text="dbload",name="dbl")
        
        self.dbload_button.grid(row=2,column=5)
        self.dbload_button.focus_get()
        
        self.clear_button = Button(controlpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(row=2,column=6)
        self.clear_button.focus_get()    

        self.bgmaxrows=len(period_enum)+1
        self.bgmaxcols=len(student_enum)+1 
        mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
        self.balancegrid = TkImageLabelGrid(self.master,mytextalphanum,wmwidth,wmheight,
                             0,0,self.bgmaxrows,self.bgmaxcols,
                             {},widgetcfg)
        
        self.balancegrid.grid(row=1,column=0,sticky=NSEW)
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

        self.of.reset()
        
        for x in range(1,self.maxrows):
            ylabel=self.entrygrid.widgets[x][0].sv.get()
            
            for y in range(1,self.maxcols):
                xlabel=self.entrygrid.widgets[0][y].sv.get()
                
                value =  self.entrygrid.widgets[x][y].sv.get()
                
                if value <> "":

                    # get the actual row and column number from the enum_maps
                    # add one to account for the origin
                    x = period_enum = period_map[ylabel]+1
                    y = student_enum = student_map[value]+1
                    z = teacher_enum = teacher_map[xlabel]+1
                    
                    obj_id = ",".join(map(str,[x,y,z]))

                    datamembers = dict(schedule = '1',
                                       dow='Tuesday', 
                                       subject="MATH",
                                       lessontype="wp",
                                       objtype='lesson',
                                       userobjid=obj_id, # unique key to store obj in of
                                       period=ylabel,
                                       student=value,
                                       saveversion=str(self.lastsaveversion),
                                       teacher=xlabel)
                    
                    self.of.new(schoolschedgeneric,
                                'lesson',
                                objid=obj_id,
                                constructor='datamembers',
                                database=self.database,
                                of=self.of,
                                modname=__name__,
                                dm=datamembers)

                    current_value = self.balancegrid.widgets[x][y].cget("text")
                    if current_value == xlabel:
                        pass
                    elif current_value == "":
                        
                        self.balancegrid.widgets[x][y].config(background='lightgreen')
                        self.balancegrid.widgets[x][y].config(text=xlabel)
                    else:
                        self.balancegrid.widgets[x][y].config(text=current_value+","+xlabel)
                        self.balancegrid.widgets[x][y].config(background='red')
                    
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
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
    def clear(self):
        
        for x in range(self.maxrows):
            for y in range(self.maxcols):
                self.entrygrid.widgets[x][y].sv.set("")
        
        for x in range(self.bgmaxrows):
            for y in range(self.bgmaxcols):
                self.balancegrid.widgets[x][y].config(text="")    
                self.balancegrid.widgets[x][y].config(background="white") 

    def load_save(self,saveversion):
        self.load(saveversion)
        self.save()
        
    def load(self,saveversion,values=None):
        
        cols = ['period','student','teacher','dow']
        
        if values==None:
            with self.database:
                colndefn,rows = tbl_rows_get(self.database,'lesson',cols,
                                    ('saveversion',saveversion))
            
            for row in rows:
                x = period_map[row[cols.index('period')]]
                y = teacher_map[row[cols.index('teacher')]]
                v = student_map[row[cols.index('student')]]

                self.entrygrid.widgets[x+1][y+1].sv.set(row[cols.index('student')])
                
                self.entrygrid.widgets[0][y+1].sv.set(row[cols.index('teacher')])
                self.entrygrid.widgets[x+1][0].sv.set(row[cols.index('period')])
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
    ui = WizardUI(master,database,of)
    master.mainloop()