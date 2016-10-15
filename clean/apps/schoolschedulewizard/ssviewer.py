import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate, thisfuncname

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get, TkGridCombobox, \
     TkCombobox

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
        
        #self.clipboard=[]
        #self.clipboard_selection=-1
        Tk.__init__(self)
        self.geometry("2000x500+0+0")
        
        self.refdatabase = Database(refdbname)
        
        #self.enums = sswizard_utils.setenums('All','5',self.refdatabase)
        
        self.dbname = dbname
        
        self.database = Database(self.dbname)
        self.of = of

        
        font = tkFont.Font(family="monospace", size=10) 
        
        self.lastsaveversion=0

        style = Style()
        
        #bigfont = tkFont.Font(family="Helvetica",size=50)
        #self.option_add("*TCombobox*Listbox*Font", bigfont)
        
        self.current_inputmode = "Normal"
        
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
                
        buttonpanel = Frame(self,style='ControlPanel.TFrame')
        buttonpanel.grid(row=0,column=0,sticky=NSEW)
                
        self.dbload_button = Button(buttonpanel,command=lambda: self.load(self.dbload_entry_sv.get()),
                                    text="dbload",name="dbl")
    
        self.dbload_button.grid(row=0,column=0)
        self.dbload_button.focus_get()
    
        self.clear_button = Button(buttonpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(row=0,column=1)
        self.clear_button.focus_get()

        self.viewer_button = Button(buttonpanel,command=self.viewer,text="viewer",name="view")
        self.viewer_button.grid(row=0,column=2)
        self.viewer_button.focus_get()

        controlpanel = Frame(self,style='ControlPanel.TFrame')
        controlpanel.grid(row=1,column=0,sticky=NSEW,columnspan=2)
        
        self.dbload_entry_label = Label(controlpanel,text="version",font=font)
        self.dbload_entry_label.grid(row=0,column=1)
        self.dbload_entry_label.focus_get()
        self.dbload_entry_sv = StringVar()
        self.dbload_entry = Entry(controlpanel,textvariable=self.dbload_entry_sv,font=font)
        self.dbload_entry.grid(row=0,column=2)
        self.dbload_entry_sv.set('1')
        self.dbload_entry.focus_get()
        
        self.dbname_entry_label = Label(controlpanel,text="dbname",font=font)
        self.dbname_entry_label.grid(row=0,column=3)
        self.dbname_entry_label.focus_get()
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(controlpanel,textvariable=self.dbname_entry_sv,font=font)
        self.dbname_entry.grid(row=0,column=4)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set(self.dbname)
        
        self.dow_entry_label = Label(controlpanel,text="dow",width=10,font=font)
        self.dow_entry_label.grid(row=0,column=5)
        self.dow_entry_label.focus_get()
        
        self.dow_entry_sv = StringVar()
        self.dow_entry = Entry(controlpanel,textvariable=self.dow_entry_sv,width=10,font=font)
        self.dow_entry.grid(row=0,column=6)
        self.dow_entry.focus_get()
        #self.dow_entry_sv.set('MO')
        
        self.prep_label = Label(controlpanel,text="prep",width=10,font=font)
        self.prep_label.grid(row=0,column=7)
        self.prep_label.focus_get()
        
        self.prep_entry_sv = StringVar()        
        self.prep_entry = Entry(controlpanel,textvariable=self.prep_entry_sv,width=10,font=font)
        self.prep_entry.grid(row=0,column=8)
        self.prep_entry.focus_get()
        #self.prep_entry_sv.set(5)
        
        self.period_label = Label(controlpanel,text="period",width=10,font=font)
        self.period_label.grid(row=0,column=9)
        self.period_label.focus_get()
        
        self.period_entry_sv = StringVar()        
        self.period_entry = Entry(controlpanel,textvariable=self.period_entry_sv,width=10,font=font)
        self.period_entry.grid(row=0,column=10)
        self.period_entry.focus_get()
        #self.period_entry_sv.set('830-910')
        
        self.teacher_label = Label(controlpanel,text="teacher",width=10,font=font)
        self.teacher_label.grid(row=0,column=11)
        self.teacher_label.focus_get()
        
        self.teacher_label_sv = StringVar()        
        self.teacher_label = Entry(controlpanel,textvariable=self.teacher_label_sv,width=10,font=font)
        self.teacher_label.grid(row=0,column=12)
        self.teacher_label.focus_get()
        #self.teacher_label_sv.set('Stan')
        
        self.student_label = Label(controlpanel,text="student",width=10,font=font)
        self.student_label.grid(row=0,column=13)
        self.student_label.focus_get()
        
        self.student_label_sv = StringVar()        
        self.student_label = Entry(controlpanel,textvariable=self.student_label_sv,width=10,font=font)
        self.student_label.grid(row=0,column=14)
        self.student_label.focus_get()
        #self.student_label_sv.set('Nathaniel')
        
        
        self.viewcontrolpanel = Frame(self.master)
        self.viewcontrolpanel.grid(row=2,column=0,sticky=NSEW)
        
        self.viewxaxis_label = Label(self.viewcontrolpanel,text="xaxis",font=font)
        self.viewxaxis_label.grid(row=0,column=0)
        self.viewxaxis_label.focus_get()
        self.viewxaxis_label_sv = StringVar()
        self.viewxaxis_label = Entry(self.viewcontrolpanel,textvariable=self.viewxaxis_label_sv,font=font)
        self.viewxaxis_label.grid(row=0,column=1)
        self.viewxaxis_label.focus_get()
        self.viewxaxis_label_sv.set("period")
        
        self.viewyaxis_label = Label(self.viewcontrolpanel,text="yaxis",font=font)
        self.viewyaxis_label.grid(row=0,column=2)
        self.viewyaxis_label.focus_get()
        self.viewyaxis_label_sv = StringVar()
        self.viewyaxis_label = Entry(self.viewcontrolpanel,textvariable=self.viewyaxis_label_sv,font=font)
        self.viewyaxis_label.grid(row=0,column=3)
        self.viewyaxis_label.focus_get()
        self.viewyaxis_label_sv.set("dow")
        
        self.viewfocus_label = Label(self.viewcontrolpanel,text="focus",font=font)
        self.viewfocus_label.grid(row=0,column=4)
        self.viewfocus_label.focus_get()
        self.viewfocus_label_sv = StringVar()
        self.viewfocus_label = Entry(self.viewcontrolpanel,textvariable=self.viewfocus_label_sv,font=font)
        self.viewfocus_label.grid(row=0,column=5)
        self.viewfocus_label.focus_get()
        self.viewfocus_label_sv.set("student=Nathaniel")
        
        self.viewstudent_label = Label(self.viewcontrolpanel,text="student",font=font)
        self.viewstudent_label.grid(row=0,column=6)
        self.viewstudent_label.focus_get()
        self.viewstudent_label_sv = StringVar()
        self.viewstudent_label = Entry(self.viewcontrolpanel,textvariable=self.viewstudent_label_sv,font=font)
        self.viewstudent_label.grid(row=0,column=7)
        self.viewstudent_label.focus_get()
        self.viewstudent_label_sv.set("Nathaniel")
        
        self.viewteacher_label = Label(self.viewcontrolpanel,text="dow",font=font)
        self.viewteacher_label.grid(row=0,column=8)
        self.viewteacher_label.focus_get()
        self.viewteacher_label_sv = StringVar()
        self.viewteacher_label = Entry(self.viewcontrolpanel,textvariable=self.viewteacher_label_sv,font=font)
        self.viewteacher_label.grid(row=0,column=9)
        self.viewteacher_label.focus_get()
        
        self.viewdata_label = Label(self.viewcontrolpanel,text="data",font=font)
        self.viewdata_label.grid(row=0,column=8)
        self.viewdata_label.focus_get()
        self.viewdata_label_sv = StringVar()
        self.viewdata_label = Entry(self.viewcontrolpanel,textvariable=self.viewdata_label_sv,font=font)
        self.viewdata_label.grid(row=0,column=9)
        self.viewdata_label.focus_get()
        self.viewdata_label_sv.set("subject,teacher")

        self.recalc_button = Button(self.viewcontrolpanel,command=self.viewer,text="calc",name="vc")
        self.recalc_button.grid(row=0,column=10)
        self.recalc_button.focus_get()
        
        #self.grid_rowconfigure(0, weight=1, uniform="foo")
        #self.grid_rowconfigure(1, weight=1, uniform="foo")
        #self.grid_rowconfigure(2, weight=1, uniform="foo")
        self.grid_columnconfigure(0, weight=1, uniform="foo")
    
    def dump(self,value):
        
        with self.database:
            cols,rows,_ = _versions(self.database,*value)
            
        value = [self.enums['period']['name2enum'][value[0]],self.enums['dow']['code2name'][value[1]]]
        
        #with self.database:           
        #    cols,rows,_ = _sessionversions(self.database,*value)
        #    
        #    print rows

        if len(rows) <> 0:
            self.bgmaxrows=len(rows)
            self.bgmaxcols=len(rows[0])
        
        
            widget_args=dict(background='white',width=1,height=1,highlightbackground='black',highlightthickness=1,values=self.enums['dow'])
            widgetcfg = nxnarraycreate(self.bgmaxrows,self.bgmaxcols,widget_args)
            mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
            try:
                self.versionsgrid.destroy()
            except:
                pass
        
            self.versionsgrid = TkImageLabelGrid(self,'versionsgrid',mytextalphanum,10,10,0,0,self.bgmaxrows,self.bgmaxcols,True,False,{},widgetcfg)
        
            self.versionsgrid.grid(row=4,column=0,sticky=NSEW)
            self.grid_rowconfigure(4, weight=3, uniform="foo")
            
            for x in range(len(rows)):
                for y in range(len(rows[x])):
                    widget = self.versionsgrid.widgets[x][y]
                    widget.sv.set(rows[x][y])
        else:
            self.versionsgrid.destroy()

    def viewer(self,ui=True,source_type=None,source_value=None,ztypes=None):

        xaxis_type = self.viewxaxis_label_sv.get() # period
        yaxis_type = self.viewyaxis_label_sv.get() # dow

        if source_type == None or source_value == None:
            source_type,source_value = self.viewfocus_label_sv.get().split("=")
        
        if ztypes == None:
            ztypes = self.viewdata_label_sv.get().split(",")
        
        source_obj = self.of.object_get(source_type,source_value)
        
        xaxis_obj = self.of.query(xaxis_type)
        yaxis_obj = self.of.query(yaxis_type)
        
        xaxis_enum = self.enums[xaxis_type]['name2enum']
        yaxis_enum = self.enums[yaxis_type]['code2enum']
        
        values = [] # contains the values displayed on the grid
        row=[''] # 

        values = [['']]    
        for yval in yaxis_enum.keys():
            values[0].append(yval)
            
        for xval in xaxis_enum.keys():
            values.append([xval])

        ymax = len(values[0])
        xmax = len(values)-1

        for yval,y in yaxis_enum.iteritems():

            for xval,x in xaxis_enum.iteritems():
                celltext=[]
                
                for ztype in ztypes:
                    try:
                        _vals = source_obj.lessons[yval][xval]
                        for _val in _vals:
                            zval = getattr(_val,ztype)
                            celltext.append(zval.name)

                    except Exception, e:
                        log.log(thisfuncname(),2,msg="attr not found on object",error=e,
                                attr=ztype,xval=str(xval),yval=str(yval))
                        celltext.append("??")
                values[x].append(",".join(celltext))
                

        if ui==True:
            self.bgmaxrows=len(values)
            self.bgmaxcols=len(values[0])
        
            widget_args=dict(background='white',width=1,height=4,wraplength=180,highlightbackground='black',highlightthickness=1,values=self.enums['dow'])
            widgetcfg = nxnarraycreate(self.bgmaxrows,self.bgmaxcols,widget_args)
            mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
            try:
                self.viewergrid.destroy()
            except:
                pass
        
            self.viewergrid = TkImageLabelGrid(self,'viewergrid',mytextalphanum,10,10,0,0,self.bgmaxrows,self.bgmaxcols,True,False,{},widgetcfg)
        
            self.viewergrid.grid(row=3,column=0,sticky=NSEW)
            self.grid_rowconfigure(3, weight=10, uniform="foo")
            
            for x in range(len(values)):
                for y in range(len(values[x])):
                    widget = self.viewergrid.widgets[x][y]
                    widget.sv.set(values[x][y])
                    if x > 0 and y > 0:
                        key = [self.enums[xaxis_type]['enum2name'][x],self.enums[yaxis_type]['code'][y-1],source_value]                           
                        widget.bind("<Button-1>",lambda e,key=key:self.dump(key))
                    
        else:
            results = []
            for x in range(len(values)):
                row=[]
                for y in range(len(values[x])):
                    row.append(values[x][y])
                results.append(row)
            return results
            
        
    @logger(log)    
    def save(self,saveversion=None):

        self.of.reset()
        
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
        
        #$self.teacher_schedule_calc() 
        #self.student_schedule_calc()
            
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
        dow = lesson.dow.objid
        
        # add the lesson to the teacher object
        teacher = lesson.teacher
        if hasattr(teacher,'lessons') == False:
            setattr(teacher,'lessons',{})
          
        if teacher.lessons.has_key(dow) == False:
            teacher.lessons[dow] = {} 

        if teacher.lessons[dow].has_key(period) == False:
            teacher.lessons[dow][period] = []
            
        teacher.lessons[dow][period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to teacher",dow=str(dow),period=str(period),
                 session=str(lesson.session.name),teacher=str(lesson.teacher.name))
        
        # add the lesson to the student object
        student = lesson.student
        if hasattr(student,'lessons') == False:
            setattr(student,'lessons',{})
            
        if student.lessons.has_key(dow) == False:
            student.lessons[dow] = {}
            
        if student.lessons[dow].has_key(period) == False:
            student.lessons[dow][period] = []
            
        student.lessons[dow][period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to student",dow=str(dow),period=str(period),
                session=str(lesson.session.name),student=str(lesson.student.name))
            
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
        
        self.of.store={}

    @logger(log)       
    def load(self,saveversion=None,values=None, dow=None, prep=None, period=None, teacher=None, student=None):
        
        # database name
        if self.dbname_entry_sv.get() <> self.dbname:
            newdb = self.dbname_entry_sv.get()
            log.log(thisfuncname(),3,msg="switching databases",olddb=self.dbname,newdb=newdb)
            self.database = Database(newdb)
            self.dbname = newdb
            
        whereclause = []
    
        # saveversion
        if saveversion==None or saveversion== "":
            saveversion = self.dbload_entry_sv.get()
        if saveversion == "":
            log.log(thisfuncname(),1,msg="no saveversion set for load; exception")
            raise Exception("attempting to load without a saveversion set")
        else:
            log.log(thisfuncname(),3,msg="loading",saveversion=str(saveversion))
            whereclause.append(['saveversion',"=",saveversion])
        
        # prep
        if prep==None: prep=self.prep_entry_sv.get()
        if  prep == "":
            prep = -1
        else:
            whereclause.append(['prep',"=",prep])
        log.log(thisfuncname(),3,msg="loading",prep=str(prep))
        
        # period
        if period==None: period=self.period_entry_sv.get()
        if period == "":
            prep = -1
        else:
            whereclause.append(['period',"=","\""+period+"\""])            
        log.log(thisfuncname(),3,msg="loading",prep=str(prep))

        # dow
        if dow==None: dow = self.dow_entry_sv.get()
        if dow == "":
            dow = "all"
        else:
            whereclause.append( ['dow',"=","\""+dow+"\""])
        log.log(thisfuncname(),3,msg="loading",dow=str(dow))
        
        
        # teacher
        if teacher==None: teacher = self.teacher_label_sv.get()
        if teacher == "":
            teacher = "all"
        else:
            whereclause.append( ['teacher',"=","\""+teacher+"\""])
        log.log(thisfuncname(),3,msg="loading",teacher=str(teacher))      
        
        
        # student
        if student==None: student = self.student_label_sv.get()
        if student == "":
            student = "all"
        else:
            whereclause.append( ['student',"=","\""+student+"\""])
        log.log(thisfuncname(),3,msg="loading",student=str(student))
        
        whereclause.append( ['status',"=","\"" + "master" + "\""])
        
        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)

        # load from database
        cols = ['period','student','session','dow','teacher','subject','userobjid','status','substatus']        
        with self.database:
            colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',cols,whereclause)
            log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
        
        # parse rows
        for row in rows:
            datamembers = {}
            for i in range(len(cols)):
                datamembers[cols[i]] = row[i]
            
            _,lessontype_code,_ = datamembers['session'].split(".")
            #lessontype = self.enums['lessontype']['code2name'][lessontype_code]      
            datamembers['objtype'] = 'lesson'                               
            
            lesson = self.of.new(schoolschedgeneric,'lesson',objid=datamembers['userobjid'],
                                 constructor='datamembers',database=self.database,
                                 of=self.of,modname=__name__,dm=datamembers)
            
            self.lesson_change(lesson)
                            
            log.log(thisfuncname(),3,msg="loading row",dm=datamembers)

        # post log with results
        log.log(thisfuncname(),3,msg="db rows loaded",num=len(rows))        
        for i in range(len(cols)):
            log.log(thisfuncname(),3,msg="lesson obj created",num=len(self.of.store[cols[i]]))

    def updates_get(self,gridname,ignoreaxes=False):
        
        return(sswizard_utils.updates_get(self,gridname,ignoreaxes))
        
    def _lastsaveversion_get(self):
        
        try:
            with self.database:
            
                colndefn,rows = tbl_query(self.database,"select max(saveversion) from lesson")                   
            return(rows[0][0])
        except Exception:
            return(-1)

if __name__ == "__main__":
    #master = Tk()
    
    enableui = True
    
    if len(sys.argv) <= 1:
        raise Exception("provide a database name; no extension")
    else:
        log.log(thisfuncname(),3,msg="using database",database=sys.argv[1])
        
        try:
            if sys.argv[2] == "True":
                enableui = True
        except:
            pass
        
    of = ObjFactory(True)
    app = WizardUI(sys.argv[1],of,sys.argv[1],maxentrycols=12,maxentryrows=20)
        
    if enableui == True:
        app.mainloop()       
    else:
        app.load()
        app.viewer(False)
        
    
    