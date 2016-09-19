import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate, thisfuncname

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from misc_utils_objectfactory import ObjFactory

import sswizard_utils

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from Tkinter import *
from ttk import *

from collections import OrderedDict

import tkFont
import unittest


controlpanelconfig = dict(height=300,width=200,x=100,y=100)

def _execfunc(database,value):
    exec_str = "select code from session where period = {0} and subject <> \"None\"".format(value)
    return(tbl_query(database,exec_str))

def _rowheaderexecfunc(database):
    exec_str = "select name from period"
    return(tbl_query(database,exec_str))

def _columnheaderexecfunc(database,pred=None,predvalue=None):
    exec_str = "select name from student"
    if pred <> None:
        exec_str = exec_str + " where {0} = {1}".format(pred,predval)
    return(tbl_query(database,exec_str))

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

class WizardUI(Tk):
    #def __init__(self,database,of):
    def __init__(self,dbname,of,maxentrycols=3,maxentryrows=4,
                 maxnewrowcols=3,maxnewrowrows=3):
        
        Tk.__init__(self)
        
        self.enums = sswizard_utils.setenums('All','5','quadref')
        
        self.dbname = dbname
        
        self.database = Database(self.dbname)
        self.of = of

        self.refdatabase = Database('quadref')
        
        self.lastsaveversion=0

        # any children that change update this 
        # key is the name and value is the new val
        # the name is likely to be the tkwidgetid.x,y
        self.updates = OrderedDict()    

        self.maxrows=maxentryrows # rows in the grid
        self.maxcols=maxentrycols # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*self.maxrows # master height
        wmwidth=wwidth*self.maxcols # master width 

        geom = geometry_get(wmheight,wmwidth,0,0)
        
        self.geometry(geom)

        self.bind("<Prior>",self.focus_next_widget)

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
        
        configpanel = Frame(self)
        configpanel.grid(row=0,sticky=NSEW)
        
        self.prep_label = Label(configpanel,text="prep")
        self.prep_label.grid(row=0,column=0)
        self.prep_label.focus_get()
        
        self.prep_entry_sv = StringVar()
        self.prep_entry = Entry(configpanel,textvariable=self.prep_entry_sv)
        self.prep_entry.grid(row=0,column=1)
        self.prep_entry.focus_get()
        
        self.dow_label = Label(configpanel,text="dow")
        self.dow_label.grid(row=0,column=2)
        self.dow_label.focus_get()
        
        self.dow_label_sv = StringVar()
        self.dow_label = Entry(configpanel,textvariable=self.dow_label_sv)
        self.dow_label.grid(row=0,column=3)
        self.dow_label.focus_get()
        
        
        # default combolist values is student

        #dbsetmember = DBSetMember('quadref','classes','
        setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['student'])
        widget_args=dict(background='white',width=7,values=self.enums['student'])
        
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,
                                   widget_args)
        
        widgetcfg = sswizard_utils.dropdown_build(self.refdatabase,
                                                  widgetcfg,
                                                  _execfunc,
                                                  _rowheaderexecfunc,
                                                  _columnheaderexecfunc)

        '''# column headers are teacher
        setmemberp = SetMemberPartial(name='x{mylist}',set=teacher_enum)
        _widget_args=dict(background='white',values=teacher_enum)     
        for y in range(1,self.maxcols):
            widgetcfg[0][y] = _widget_args  

        # row headers are teacher
        setmemberp = SetMemberPartial(name='x{mylist}',set=period_enum)
        _widget_args=dict(background='white',values=period_enum)     
        for x in range(1,self.maxrows):
            widgetcfg[x][0] = _widget_args'''

        setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['period'])

        self.entrygrid = TkImageLabelGrid(self,'entrygrid',setmemberp,
                                          wmwidth,wmheight,    
                                          0,0,self.maxrows,self.maxcols,
                                          {},widgetcfg)

        self.entrygrid.grid(row=1,column=0,sticky=NSEW)
        
        controlpanel = Frame(self)
        controlpanel.grid(row=2,sticky=NSEW)
        
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
        
        self.dbname_entry_label = Label(controlpanel,text="dbname")
        self.dbname_entry_label.grid(row=2,column=7)
        self.dbname_entry_label.focus_get()
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(controlpanel,textvariable=self.dbname_entry_sv)
        self.dbname_entry.grid(row=2,column=8)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set('htmlparser')
        

        self.bgmaxrows=len(self.enums['period']['name'])+1
        self.bgmaxcols=len(self.enums['student']['name'])+1 
        
        widgetcfg = nxnarraycreate(self.bgmaxrows,self.bgmaxcols,
                                   widget_args)
        
        mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
        self.balancegrid = TkImageLabelGrid(self,'balancegrid',
                                            mytextalphanum,wmwidth,wmheight,
                                            0,0,self.bgmaxrows,self.bgmaxcols,
                                            {},widgetcfg)
        
        
        self.balancegrid.grid(row=3,column=0,sticky=S)
        self._draw_balancegrid_labels()
        
        #self.grid_rowconfigure(0, weight=1, uniform="foo")
        self.grid_rowconfigure(1, weight=1, uniform="foo")
        self.grid_columnconfigure(0, weight=1, uniform="foo")
         
         
    def update_callback(self,widget,new_value):
        sswizard_utils.update_callback(self,widget,new_value)

            
    def _draw_balancegrid_labels(self):
        for name,enum in self.enums['period']['name2enum'].iteritems():
            self.balancegrid.widgets[enum][0].sv.set(str(name))
            
        for name,enum in self.enums['student']['name2enum'].iteritems():
            self.balancegrid.widgets[0][enum].sv.set(str(name))
       
    @logger(log)    
    def save(self,saveversion=None):

        self.of.reset()
        self.clear(1,1,'balancegrid')
        
        if self.dbname <> self.dbname_entry_sv.get():
            log.log(thisfuncname(),3,msg="dbname changed",oldname=self.dbname,newname=self.dbname_entry_sv.get())
            self.database = Database(self.dbname_entry_sv.get())
            self.dbname = self.dbname_entry_sv.get()
        
        if saveversion==None:
            saveversion = str(self._lastsaveversion_get()+1)
            #log.log(self,3,"saving save version=",str(saveversion))
            log.log(thisfuncname(),3,msg="saving save version=",saveversion=str(saveversion))
            
        #if saveversion == None:
        #    saveversion=str(self.lastsaveversion)
            
        for x in range(1,self.maxrows):
            ylabel=self.entrygrid.widgets[x][0].sv.get()
            
            for y in range(1,self.maxcols):
                xlabel=self.entrygrid.widgets[0][y].sv.get()
                
                session =  self.entrygrid.widgets[x][y].sv.get()
                
                if session <> "":
                    
                    period_enum = x
                    student_enum = y
                    session_enum = self.enums['session']['name2enum'][session]

                    obj_id = ",".join(map(str,[period_enum,student_enum,session_enum]))

                    teacher_code,lessontype_code,subject_code = session.split(".")
                    
                    # get the column and row headers associated with this cell
                    student = self.entrygrid.widgets[0][y].sv.get()
                    student = self.entrygrid.widgets[x][0].sv.get()

                    teacher = self.enums['adult']['code2enum'][teacher_code]
                    lessontype = self.enums['lessontype']['code2enum'][lessontype_code]
                    subject = self.enums['subject']['code2enum'][subject_code]
                                                               
                    datamembers = dict(schedule = '1',
                                       dow='Tuesday', 
                                       subject=subject,
                                       lessontype=lessontype,
                                       objtype='lesson',
                                       userobjid=obj_id, # unique key to store obj in of
                                       period=ylabel,
                                       student=xlabel,
                                       teacher=teacher,
                                       saveversion=saveversion,
                                       session=session)
                    
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
                        self.balancegrid.widgets[x][y].sv.set(xlabel)
                    else:
                        self.balancegrid.widgets[x][y].sv.set(current_value+","+xlabel)
                        self.balancegrid.widgets[x][y].config(background='red')
                    
        self.student_totals_calc()        
            
        self.dbload_entry_sv.set(self.lastsaveversion)
            
        self.lastsaveversion+=1

    def student_totals_calc(self):
        
        
        for sname,y in self.enums['student']['name2enum'].iteritems():
            student_full = True
            for pname,x in self.enums['period']['name2enum'].iteritems():
                current_value = self.balancegrid.widgets[x][y].cget("text")
                if current_value == "":
                    student_full=False
                    
                self.balancegrid.widgets[x][y].config(foreground='black')
                
            if student_full == True:
                self.balancegrid.widgets[0][y].config(background='green')

    
    @logger(log)   
    def focus_next_widget(self,event):
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
    @logger(log)
    def _clear_grid(self,gridname,firstrow,firstcol):
        grid = getattr(self,gridname)
        
        for x in range(firstrow,grid.maxrows):
            for y in range(firstcol,grid.maxcols):
                grid.widgets[x][y].sv.set("")
                grid.widgets[x][y].config(background='white')
                grid.widgets[x][y].config(foreground='black')
                grid.widgets[x][y].init_value = ""
                grid.widgets[x][y].current_value = ""
                grid.widgets[x][y].version = 0
                    
    @logger(log)     
    def clear(self,firstrow=0,firstcol=0,gridname=None):
        if gridname == None:
            self._clear_grid('entrygrid',firstrow,firstcol)
            self._clear_grid('balancegrid',firstrow,firstcol)
        else:
            self._clear_grid(gridname,firstrow,firstcol)
        
        self.updates={}

    def load_save(self,saveversion=None):
        self.load()
        #self.load(saveversion)
        self.save()
        
    @logger(log)       
    def load(self,saveversion=None,values=None):
        
        if self.dbname <> self.dbname_entry_sv.get():
            log.log(thisfuncname(),3,msg="dbname changed",oldname=self.dbname,newname=self.dbname_entry_sv.get())
            self.database = Database(self.dbname_entry_sv.get())
            self.dbname = self.dbname_entry_sv.get()
        
        if saveversion==None:
            saveversion = self._lastsaveversion_get()
            log.log(thisfuncname(),3,msg="loading last save version",saveversion=str(saveversion))
        
        cols = ['period','student','session','dow']
        
        if values==None:
            with self.database:
                colndefn,rows = tbl_rows_get(self.database,'lesson',cols,
                                    ('saveversion',saveversion))
            
            for row in rows:
                
                z = session =  row[cols.index('session')]
                period =  row[cols.index('period')]
                student =  row[cols.index('student')]
                
                x = self.enums['period']['name2enum'][str(period)]
                y = self.enums['student']['name2enum'][student]

                self.entrygrid.widgets[x+1][y+1].sv.set(session)
                self.entrygrid.widgets[0][y+1].sv.set(student)
                self.entrygrid.widgets[x+1][0].sv.set(period)
        else:
                
            for x in range(len(values)):
                for y in range(len(values[0])):
                    self.entrygrid.widgets[x][y].sv.set(values[x][y])

    def updates_get(self,gridname,ignoreaxes=False):
        
        return(sswizard_utils.updates_get(self,gridname,ignoreaxes))
        
    @logger(log)
    def persist(self):
        with self.database:
            for obj in self.of.object_iter():
                log.log(thisfuncname(),9,msg="persisting of obj",objid=obj.userobjid)
                obj.persist()
                
    def _lastsaveversion_get(self):
        
        try:
            with self.database:
            
                colndefn,rows = tbl_query(self.database,"select max(saveversion) from lesson")                   
            return(rows[0][0])
        except Exception:
            return(-1)

if __name__ == "__main__":
    #master = Tk()
    
    
    of = ObjFactory(True)
    app = WizardUI('htmlparser',of,maxentrycols=10,maxentryrows=10)
    app.mainloop()