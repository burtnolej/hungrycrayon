import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from misc_utils import Log
from misc_utils_objectfactory import ObjFactory

import sswizard_utils

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from Tkinter import *
from ttk import *

from collections import OrderedDict

import tkFont
import unittest



log = Log()

controlpanelconfig = dict(height=300,width=200,x=100,y=100)

def _execfunc(database,value):
    exec_str = "select tag from session where period = {0} and subject <> \"None\"".format(value)
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
    def __init__(self,database,of):
        
        Tk.__init__(self)
        
        self.enums = sswizard_utils.setenums('All','3','quadref')
        
        self.database = database
        self.of = of

        self.refdatabase = Database('quadref')
        
        self.lastsaveversion=0

        # any children that change update this 
        # key is the name and value is the new val
        # the name is likely to be the tkwidgetid.x,y
        self.updates = OrderedDict()    

        self.maxrows=14 # rows in the grid
        self.maxcols=20 # cols in the grid
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
        setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['students'])
        widget_args=dict(background='white',width=7,values=self.enums['students'])
        
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
        

        self.bgmaxrows=len(self.enums['period'])+1
        self.bgmaxcols=len(self.enums['students'])+1 
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
         
    '''def update_callback(self,widget,new_value):        
        #via BaseTk class; all entry widgets assign a callback to the change event
        #to call this function if it exists
        widget.current_value = new_value

        if str(widget.current_value) <> str(widget.init_value):
                        
            widget.config(foreground='red')
        else:
            widget.config(foreground='black')
            
        self.updates[str(widget.winfo_name())] = new_value'''
            
    def _draw_balancegrid_labels(self):
        
        for x in range(len(self.enums['period'])+1):
            self.balancegrid.widgets[x][0].sv.set(self.enums['period'][x-1])
            
        for y in range(1,len(self.enums['students'])+1):
            self.balancegrid.widgets[0][y].sv.set(self.enums['students'][y-1])
        
    def save(self,saveversion=None):

        self.of.reset()
        self.clear(1,1,'balancegrid')
        
        if saveversion==None:
            saveversion = str(self._lastsaveversion_get()+1)
            log.log(self,3,"saving save version=",str(saveversion))
            
        #if saveversion == None:
        #    saveversion=str(self.lastsaveversion)
            
        for x in range(1,self.maxrows):
            ylabel=self.entrygrid.widgets[x][0].sv.get()
            
            for y in range(1,self.maxcols):
                xlabel=self.entrygrid.widgets[0][y].sv.get()
                
                value =  self.entrygrid.widgets[x][y].sv.get()
                
                if value <> "":

                    # get the actual row and column number from the enum_maps
                    # add one to account for the origin
                    '''x = period_enum = period_map[ylabel]+1
                    y = student_enum = student_map[value]+1
                    z = teacher_enum = teacher_map[xlabel]+1'''
                    
                    x = period_enum = self.enums['enums'][ylabel]+1
                    y = student_enum = self.maps['students'][xlabel]+1
                    z = session_enum = self.maps['session'][value]+1
                    
                    obj_id = ",".join(map(str,[x,y,z]))

                    teacher_code,lessontype_code,subject_code = value.split(".")
                    
                    datamembers = dict(schedule = '1',
                                       dow='Tuesday', 
                                       subject=subject,
                                       lessontype="wp",
                                       objtype='lesson',
                                       userobjid=obj_id, # unique key to store obj in of
                                       period=ylabel,
                                       student=xlabel,
                                       teacher=teacher,
                                       saveversion=saveversion,
                                       tag=value)
                    
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
        
        for student in range(1,len(self.enums['students'])+1):
            student_full = True
            for x in range(len(self.enums['period'])+1):
                current_value = self.balancegrid.widgets[x][student].cget("text")
                if current_value == "":
                    student_full=False
                    
                # for now force foreground back to black as default
                # in TkBase makes in 'red' on change
                self.balancegrid.widgets[x][student].config(foreground='black')
                
            if student_full == True:
                self.balancegrid.widgets[0][student].config(background='green')
            
    def focus_next_widget(self,event):
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
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
                

    def clear(self,firstrow=0,firstcol=0,gridname=None):
        if gridname == None:
            self._clear_grid('entrygrid',firstrow,firstcol)
            self._clear_grid('balancegrid',firstrow,firstcol)
        else:
            self._clear_grid(gridname,firstrow,firstcol)
        
        self.updates={}
        
    '''def clear(self):
        
        for x in range(self.maxrows):
            for y in range(self.maxcols):
                self.entrygrid.widgets[x][y].sv.set("")
        
        for x in range(self.bgmaxrows):
            for y in range(self.bgmaxcols):
                self.balancegrid.widgets[x][y].config(text="")    
                self.balancegrid.widgets[x][y].config(background="white") '''

    def load_save(self,saveversion=None):
        self.load()
        #self.load(saveversion)
        self.save()
        
    def load(self,saveversion=None,values=None):
        
        if saveversion==None:
            saveversion = self._lastsaveversion_get()
            log.log(self,3,"loading last save version=",str(saveversion))
        
        cols = ['period','student','tag','dow']
        
        if values==None:
            with self.database:
                colndefn,rows = tbl_rows_get(self.database,'lesson',cols,
                                    ('saveversion',saveversion))
            
            for row in rows:
                x = period_enum = self.maps['period'][row[cols.index('period')]]+1
                y = student_enum = self.maps['students'][row[cols.index('student')]]+1
                z = class_enum = self.maps['session'][row[cols.index('tag')]]+1
    
                '''x = period_map[]
                y = teacher_map[row[cols.index('teacher')]]
                v = student_map[row[cols.index('student')]]'''

                self.entrygrid.widgets[x+1][y+1].sv.set(row[cols.index('tag')])
                
                self.entrygrid.widgets[0][y+1].sv.set(row[cols.index('student')])
                self.entrygrid.widgets[x+1][0].sv.set(row[cols.index('period')])
        else:
                
            for x in range(len(values)):
                for y in range(len(values[0])):
                    self.entrygrid.widgets[x][y].sv.set(values[x][y])

    def updates_get(self,gridname,ignoreaxes=False):
        
        return(sswizard_utils.updates_get(self,gridname,ignoreaxes))
        
    def persist(self):
        with self.database:
            for obj in self.of.object_iter():
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
    
    database = Database('htmlparser')
    of = ObjFactory(True)
    app = WizardUI(database,of)
    app.mainloop()