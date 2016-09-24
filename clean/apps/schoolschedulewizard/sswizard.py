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
from sswizard_query_utils import *
from sswizard_config_utils import *

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from Tkinter import *
from ttk import *

from collections import OrderedDict

import tkFont
import unittest


controlpanelconfig = dict(height=300,width=200,x=100,y=100)

class schoolschedgeneric(dbtblgeneric):

    def __init__(self,of,database,recursion=True,**kwargs):
        self.recursion = recursion
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
    
    #def __repr__(self):
    #    
    #    print "r=",self.recursion,"objid",self.objid,type(self.objid)
    #    return(self.objid)

class WizardUI(Tk):
    #def __init__(self,database,of):
    def __init__(self,dbname,of,refdbname,maxentrycols=3,maxentryrows=4,
                 maxnewrowcols=3,maxnewrowrows=3):
        
        log.log(thisfuncname(),3,msg="initialize",dbname=dbname,refdbname=refdbname)
        
        Tk.__init__(self)
        
        self.enums = sswizard_utils.setenums('All','5',refdbname)
        
        self.dbname = dbname
        
        self.database = Database(self.dbname)
        self.of = of

        self.refdatabase = Database('quadref')
        font = tkFont.Font(family="monospace", size=14) 
        
        self.lastsaveversion=0

        style = Style()
        
        bigfont = tkFont.Font(family="Helvetica",size=50)
        self.option_add("*TCombobox*Listbox*Font", bigfont)
      
        set_configs(style)
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

        geom = geometry_get(1000,1000,0,0)
        self.geometry(geom)
        
        self.bind("<Prior>",self.focus_next_widget)

        '''configpanel = Frame(self,style='ConfigPanel.TFrame')
        configpanel.grid(row=0,column=0,sticky=EW)
        
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
        self.dow_label.focus_get()'''
        
        # daygrids
        setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['dow'])
        widget_args=dict(background='white',width=9,font=font,values=self.enums['dow'])
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        widgetcfg = sswizard_utils.dropdown_build(self.refdatabase,widgetcfg,_dowexecfunc,5)
        #setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['period'])   

        # daygrid 1
        self.dowentrygrid = TkImageLabelGrid(self,'dowentrygrid',setmemberp,wmwidth,wmheight,0,0,1,self.maxcols,True,{},widgetcfg)
        #self.entrygrid['style'] = 'EntryGrid.TFrame'
        self.dowentrygrid.grid(row=0,column=0,sticky=EW)
        
        # daygrid 2
        #self.dowentrygrid = TkImageLabelGrid(self,'dowentrygrid',setmemberp,wmwidth,wmheight,0,0,1,self.maxcols,False,{},widgetcfg)
        #self.entrygrid['style'] = 'EntryGrid.TFrame'
        #self.dowentrygrid.grid(row=0,column=1,sticky=EW)

        # entrygrids
        setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['student'])
        widget_args=dict(background='white',width=9,font=font,values=self.enums['student'])
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        widgetcfg = sswizard_utils.dropdown_build(self.refdatabase,widgetcfg,_execfunc,5,"Monday",_columnheaderexecfunc,_rowheaderexecfunc)
        setmemberp = SetMemberPartial(name='x{mylist}',set=self.enums['period'])   
        
        # entrygrid 1
        self.entrygrid = TkImageLabelGrid(self,'entrygrid',setmemberp,wmwidth,wmheight,0,0,self.maxrows,self.maxcols,True,{},widgetcfg)
        self.entrygrid['style'] = 'EntryGrid.TFrame'
        self.entrygrid.grid(row=1,column=0,sticky=NSEW)

        # entrygrid 2
        #self.entrygrid2 = TkImageLabelGrid(self,'entrygrid2',setmemberp,wmwidth,wmheight,0,0,self.maxrows,self.maxcols,True,{},widgetcfg)
        #self.entrygrid2['style'] = 'EntryGrid.TFrame'
        #self.entrygrid2.grid(row=1,column=1,sticky=NSEW)
        
        controlpanel = Frame(self,style='ControlPanel.TFrame')
        controlpanel.grid(row=2,column=0,sticky=NSEW,columnspan=2)
        
        self.save_button = Button(controlpanel,command=self.save,text="save",name="svb")
        self.save_button.grid(row=0,column=0)
        self.save_button.focus_get()
        
        self.persist_button = Button(controlpanel,command=self.persist,text="persist",name="pb")
        self.persist_button.grid(row=0,column=1)
        self.persist_button.focus_get()
        
        self.spacer_label = Label(controlpanel,text="                      ")
        self.spacer_label.grid(row=0,column=2)
        
        self.dbload_entry_label = Label(controlpanel,text="version")
        self.dbload_entry_label.grid(row=0,column=3)
        self.dbload_entry_label.focus_get()
        self.dbload_entry_sv = StringVar()
        self.dbload_entry = Entry(controlpanel,textvariable=self.dbload_entry_sv)
        self.dbload_entry.grid(row=0,column=4)
        self.dbload_entry.focus_get()
        
        self.dbload_button = Button(controlpanel,command=lambda: self.load(self.dbload_entry_sv.get()),
                                    text="dbload",name="dbl")
        
        self.dbload_button.grid(row=0,column=5)
        self.dbload_button.focus_get()
        
        self.clear_button = Button(controlpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(row=0,column=6)
        self.clear_button.focus_get()
        
        self.dbname_entry_label = Label(controlpanel,text="dbname")
        self.dbname_entry_label.grid(row=0,column=7)
        self.dbname_entry_label.focus_get()
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(controlpanel,textvariable=self.dbname_entry_sv)
        self.dbname_entry.grid(row=0,column=8)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set('htmlparser')
        
        self.pagedown_button = Button(controlpanel,command=self.pagedown,text="pgdwn",name="pgdwn")
        self.pagedown_button.grid(row=0,column=9)
        self.pagedown_button.focus_get()
        
        self.dow_entry_label = Label(controlpanel,text="dow")
        self.dow_entry_label.grid(row=0,column=10)
        self.dow_entry_label.focus_get()
        
        self.dow_entry_sv = StringVar()
        self.dow_entry = Entry(controlpanel,textvariable=self.dow_entry_sv)
        self.dow_entry.grid(row=0,column=11)
        self.dow_entry.focus_get()
        self.dow_entry_sv.set('Monday')
        
        self.rebuilddropdown_button = Button(controlpanel,command=self.dropdowns_set,text="ddown",name="ddown")
        self.rebuilddropdown_button.grid(row=0,column=12)
        self.rebuilddropdown_button.focus_get()
        
        self.bgmaxrows=len(self.enums['period']['name'])+1
        self.bgmaxcols=len(self.enums['student']['name'])+1 
        
        widget_args=dict(background='white',width=2,font=font,values=self.enums['dow'])
        widgetcfg = nxnarraycreate(self.bgmaxrows,self.bgmaxcols,widget_args)
        
        self.balancepanel = Frame(self)
        self.balancepanel.grid(row=3,column=0,sticky=NSEW)
        
        mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
        self.studentschedgrid = TkImageLabelGrid(self.balancepanel,'studentschedgrid',
                                            mytextalphanum,wmwidth,wmheight,
                                            0,0,self.bgmaxrows,self.bgmaxcols,
                                            True,{},widgetcfg)
        
        self.studentschedgrid.grid(row=0,column=0,sticky=NSEW)
        
        mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
        self.teacherschedgrid = TkImageLabelGrid(self.balancepanel,'teacherschedgrid',
                                            mytextalphanum,wmwidth,wmheight,
                                            0,0,self.bgmaxrows,self.bgmaxcols,
                                            True,{},widgetcfg)
        
        self.teacherschedgrid.grid(row=0,column=1,sticky=NSEW)
        
        self.balancepanel.grid_columnconfigure(0, weight=1, uniform="foo")
        self.balancepanel.grid_columnconfigure(1, weight=1, uniform="foo")
        self.balancepanel.grid_rowconfigure(0, weight=1, uniform="foo")

        self.grid_rowconfigure(0, weight=1, uniform="foo")
        self.grid_rowconfigure(1, weight=10, uniform="foo")
        self.grid_rowconfigure(2, weight=1, uniform="foo")
        self.grid_rowconfigure(3, weight=10, uniform="foo")
        self.grid_columnconfigure(0, weight=1, uniform="foo")
        #self.grid_columnconfigure(1, weight=1, uniform="foo")
        

    def printme(self,event):
        print "print me",event.widget.sv.get()
        
    def pagedown(self):
        self.ui.canvas.yview()
        
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
        self.clear(1,1,'studentschedgrid')
        self.clear(1,1,'teacherschedgrid')
        
        if self.dbname <> self.dbname_entry_sv.get():
            log.log(thisfuncname(),3,msg="dbname changed",oldname=self.dbname,newname=self.dbname_entry_sv.get())
            self.database = Database(self.dbname_entry_sv.get())
            self.dbname = self.dbname_entry_sv.get()
        
        if saveversion==None or saveversion == "":
            
            if self.dbload_entry_sv.get()==None or self.dbload_entry_sv.get() == "":
                log.log(thisfuncname(),1,msg="no saveversion set for save; exception")
                raise Exception("attempting to save without a saveversion set")  
                
            else:
                saveversion = self.dbload_entry_sv.get()
        
        log.log(thisfuncname(),3,msg="saving save version=",saveversion=str(saveversion))
            
        #if saveversion == None:
        #    saveversion=str(self.lastsaveversion)
            
        for x in range(1,self.maxrows):
            for y in range(1,self.maxcols):
                period=self.entrygrid.widgets[0][y].sv.get()
                student=self.entrygrid.widgets[x][0].sv.get()
                session =  self.entrygrid.widgets[x][y].sv.get()
                
                if session <> "":
                    
                    period_enum = x
                    student_enum = y
                    session_enum = self.enums['session']['name2enum'][session]

                    obj_id = ",".join(map(str,[period_enum,student_enum,session_enum]))
                    
                    #obj_id = session

                    teacher_code,lessontype_code,subject_code,dow = session.split(".")
                    
                    # get the column and row headers associated with this cell
                    #student = self.entrygrid.widgets[0][y].sv.get()
                    #period = self.entrygrid.widgets[x][0].sv.get()

                    '''teacher = self.enums['adult']['code2enum'][teacher_code]
                    lessontype = self.enums['lessontype']['code2enum'][lessontype_code]
                    subject = self.enums['subject']['code2enum'][subject_code]'''
                    

                    teacher = self.enums['adult']['code2name'][teacher_code]
                    lessontype = self.enums['lessontype']['code2name'][lessontype_code]
                    subject = self.enums['subject']['code2name'][subject_code]
                                                               
                    datamembers = dict(schedule = '1',
                                       dow=dow, 
                                       subject=subject,
                                       lessontype=lessontype,
                                       objtype='lesson',
                                       userobjid=obj_id, # unique key to store obj in of
                                       period=period,
                                       student=student,
                                       teacher=teacher,
                                       saveversion=saveversion,
                                       session=session)
                    
                    lesson = self.of.new(schoolschedgeneric,
                                         'lesson',
                                         objid=obj_id,
                                         constructor='datamembers',
                                         database=self.database,
                                         of=self.of,
                                         modname=__name__,
                                         dm=datamembers)
                    
                    setattr(self.entrygrid.widgets[x][y],"lesson",lesson)
                
                    self.lesson_change(lesson)
        
        self.teacher_schedule_calc() 
        self.student_schedule_calc()
            
        #self.dbload_entry_sv.set(self.lastsaveversion)
            
        #self.lastsaveversion+=1

    def _lesson_change_event(self,event):
        
        olesson = event.widget.lesson
        #olesson = self.of.store['lesson'][lessonobjid]
        
        self.lesson_change(olesson)
        self.student_schedule_calc()
        self.teacher_schedule_calc()
        
    def lesson_change(self,lesson):

        period = lesson.period.objid
        student = lesson.student.objid
        
        # add the lesson to the teacher object
        teacher = lesson.teacher
        if hasattr(teacher,'lessons') == False:
            setattr(teacher,'lessons',{})
            
        if teacher.lessons.has_key(period) == False:
            teacher.lessons[period] = []
            
        teacher.lessons[period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to teacher",lesson=lesson)
        # add the lesson to the student object
        student = lesson.student
        if hasattr(student,'lessons') == False:
            setattr(student,'lessons',{})
            
        if student.lessons.has_key(period) == False:
            student.lessons[period] = []
            
        student.lessons[period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to student",lesson=lesson)
            

    def student_schedule_calc(self):
        
        students = self.enums['student']['name']
        periods = self.enums['period']['name']
        
        gridx=1
        gridy=1
        
        for p in range(len(periods)):
            self.studentschedgrid.widgets[gridx][0].sv.set(periods[p])
            gridy+=1

            for s in range(len(students)):
                
                try:
                    ostudent = self.of.object_get('student',students[s])
                except KeyError:
                    #print "student",students[s],"does not exist"
                    continue
    
                if ostudent.lessons.has_key(periods[p]):
                    self.studentschedgrid.widgets[0][gridy].sv.set(students[s])
    
                    lessons = ostudent.lessons[periods[p]]
                    for lesson in lessons:
                        try:
                            subject = lesson.subject.objid
                            self.studentschedgrid.widgets[gridx][gridy].sv.set(subject)
                        except KeyError:
                            pass
                            #print "lesson",lesson,"does not exist"
                    #print
                    
                gridy+=1

            gridy=1
            gridx+=1
            
    def teacher_schedule_calc(self,event=None):
        
        teachers = self.enums['adult']['name']
        periods = self.enums['period']['name']
        
        gridx=1
        gridy=1
        
        
        for p in range(len(periods)):
            self.teacherschedgrid.widgets[gridx][0].sv.set(periods[p])
            gridy+=1

            for t in range(len(teachers)):
                
                try:
                    oteacher = self.of.object_get('teacher',teachers[t])
                except KeyError:
                    #print "teacher",teachers[t],"does not exist"
                    continue
            
                '''for p in range(len(periods)):
                    self.teacherschedgrid.widgets[gridx][0].sv.set(periods[p])
                    gridy+=1'''
    
                if oteacher.lessons.has_key(periods[p]):
                    self.teacherschedgrid.widgets[0][gridy].sv.set(teachers[t])
                    
                        
                    lessons = oteacher.lessons[periods[p]]
                    for lesson in lessons:
                        try:
                            subject = lesson.subject.objid
                            #subject = self.of.object_get('lesson',str(lesson)).subject
                            self.teacherschedgrid.widgets[gridx][gridy].sv.set(subject)
                        except KeyError:
                            #print "lesson",lesson,"does not exist"
                            pass
                    #print
                    
                gridy+=1
                    
                
            gridy=1
            gridx+=1
    
    def dropdowns_set(self):
        
        widget_args=dict(background='red',width=9,values=self.enums['student'])
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        widgetcfg = sswizard_utils.dropdown_build(self.refdatabase,widgetcfg,
                                                  _execfunc,5,
                                                  self.dow_entry_sv.get())        
        for x in range(1,self.maxrows):
            for y in range(1,self.maxcols):
                
                self.entrygrid.widgets[x][y].config(**widgetcfg[x][y])   

        
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
        self.dropdowns_set()
                    
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
    def load(self,saveversion=None,values=None, dow=None):
        
        if self.dbname <> self.dbname_entry_sv.get():
            log.log(thisfuncname(),3,msg="dbname changed",oldname=self.dbname,newname=self.dbname_entry_sv.get())
            self.database = Database(self.dbname_entry_sv.get())
            self.dbname = self.dbname_entry_sv.get()
        
        whereclause = []
        
        if saveversion==None or saveversion== "":
            if self.dbload_entry_sv.get() <> None and self.dbload_entry_sv.get() <> "":
                saveversion = self.dbload_entry_sv.get()
            else:
                log.log(thisfuncname(),1,msg="no saveversion set for load; exception")
                raise Exception("attempting to load without a saveversion set")
        
        whereclause.append(['saveversion',"=",saveversion])
        log.log(thisfuncname(),3,msg="loading",saveversion=str(saveversion))
            
        if dow==None:
            if self.dow_entry_sv.get() == None:
                raise Exception("dow must be specified")
            else:
                dow = self.dow_entry_sv.get()
                dow = self.enums['dow']['name2code'][dow]
                
                whereclause.append( ['dow',"=","\""+dow+"\""])
        
                log.log(thisfuncname(),3,msg="loading",dow=str(dow))
        
        cols = ['period','student','session','dow']
        
        if values==None:
            with self.database:
                colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',cols,whereclause)
                
                log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
                
            for row in rows:
                
                z = session =  row[cols.index('session')]
                period =  row[cols.index('period')]
                student =  row[cols.index('student')]
                
                x = self.enums['student']['name2enum'][student]
                y = self.enums['period']['name2enum'][str(period)]

                self.entrygrid.widgets[x+1][y+1].sv.set(session)
                self.entrygrid.widgets[0][y+1].sv.set(period)
                self.entrygrid.widgets[x+1][0].sv.set(student)
                
                log.log(thisfuncname(),3,msg="loading row",period=period,student=str(student),sv=saveversion,
                        x=x,y=y,value=z)
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
                
                exec_str, result = obj.persist()
                log.log(thisfuncname(),9,msg="persisting of obj",objid=str(obj),exec_str=exec_str,
                        result=result)
                
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
    app = WizardUI('htmlparser',of,'quadref',maxentrycols=12,maxentryrows=20)
    app.mainloop()