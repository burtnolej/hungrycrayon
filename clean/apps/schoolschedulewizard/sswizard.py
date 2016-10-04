import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
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
        
        self.refdatabase = Database('quadref')
        
        #self.enums = sswizard_utils.setenums('All','5',self.refdatabase)
        
        self.dbname = dbname
        
        self.database = Database(self.dbname)
        self.of = of

        
        font = tkFont.Font(family="monospace", size=12) 
        
        self.lastsaveversion=0

        style = Style()
        
        bigfont = tkFont.Font(family="Helvetica",size=50)
        self.option_add("*TCombobox*Listbox*Font", bigfont)
        
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

        #geom = geometry_get(1000,1000,0,0)
        #self.geometry(geom)
        
        self.bind("<Prior>",self.focus_next_widget)
        
        # daygrids
        setmemberp = SetMemberPartial(name='x{mylist}',set=['Monday'])
        widget_args=dict(background='white',width=9,font=font,values=['Monday'])
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)

        # daygrid 1
        self.dowentrygrid = TkImageLabelGrid(self,'dowentrygrid',setmemberp,wmwidth,wmheight,0,0,1,self.maxcols,True,{},widgetcfg)
        self.dowentrygrid.grid(row=0,column=0,sticky=EW)
        
        # entrygrids
        setmemberp = SetMemberPartial(name='x{mylist}',set=[])
        widget_args=dict(background='white',width=9,font=font,values=[])
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        # entrygrid 1
        setmemberp.widgettype = TkGridCombobox
        self.entrygrid = TkImageLabelGrid(self,'entrygrid',setmemberp,wmwidth,wmheight,0,0,self.maxrows,self.maxcols,True,True,{},widgetcfg)
        self.entrygrid['style'] = 'EntryGrid.TFrame'
        self.entrygrid.grid(row=1,column=0,sticky=NSEW)

        buttonpanel = Frame(self,style='ControlPanel.TFrame')
        buttonpanel.grid(row=2,column=0,sticky=NSEW,columnspan=2)
        
        self.save_button = Button(buttonpanel,command=self.save,text="save",name="svb")
        self.save_button.grid(row=0,column=0)
        self.save_button.focus_get()
    
        self.persist_button = Button(buttonpanel,command=self.persist,text="persist",name="pb")
        self.persist_button.grid(row=0,column=1)
        self.persist_button.focus_get()
        
        
        self.dbload_button = Button(buttonpanel,command=self.load,text="dbload",name="dbl")
    
        self.dbload_button.grid(row=0,column=2)
        self.dbload_button.focus_get()
    
        self.clear_button = Button(buttonpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(row=0,column=3)
        self.clear_button.focus_get()

        self.viewer_button = Button(buttonpanel,command=self.viewer,text="viewer",name="view")
        self.viewer_button.grid(row=0,column=4)
        self.viewer_button.focus_get()

        self.rebuilddropdown_button = Button(buttonpanel,command=self.dropdowns_set,text="ddown",name="ddown")
        self.rebuilddropdown_button.grid(row=0,column=5)
        self.rebuilddropdown_button.focus_get()

        controlpanel = Frame(self,style='ControlPanel.TFrame')
        controlpanel.grid(row=3,column=0,sticky=NSEW,columnspan=2)

        self.dbload_entry_label = Label(controlpanel,text="version")
        self.dbload_entry_label.grid(row=0,column=0)
        self.dbload_entry_label.focus_get()
        self.dbload_entry_sv = StringVar()
        self.dbload_entry = Entry(controlpanel,textvariable=self.dbload_entry_sv)
        self.dbload_entry.grid(row=0,column=1)
        self.dbload_entry.focus_get()
        
        self.dbname_entry_label = Label(controlpanel,text="dbname")
        self.dbname_entry_label.grid(row=0,column=2)
        self.dbname_entry_label.focus_get()
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(controlpanel,textvariable=self.dbname_entry_sv)
        self.dbname_entry.grid(row=0,column=3)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set('htmlparser')
        
        self.dow_entry_label = Label(controlpanel,text="dow",width=10)
        self.dow_entry_label.grid(row=0,column=4)
        self.dow_entry_label.focus_get()
        
        self.dow_entry_sv = StringVar()
        self.dow_entry = Entry(controlpanel,textvariable=self.dow_entry_sv,width=10)
        self.dow_entry.grid(row=0,column=5)
        self.dow_entry.focus_get()
        self.dow_entry_sv.set('MO')
        
        self.prep_label = Label(controlpanel,text="prep",width=10)
        self.prep_label.grid(row=0,column=6)
        self.prep_label.focus_get()
        
        self.prep_entry_sv = StringVar()        
        self.prep_entry = Entry(controlpanel,textvariable=self.prep_entry_sv,width=10)
        self.prep_entry.grid(row=0,column=7)
        self.prep_entry.focus_get()
        self.prep_entry_sv.set(5)
                
        self.grid_rowconfigure(0, weight=1, uniform="foo")
        self.grid_rowconfigure(1, weight=10, uniform="foo")
        self.grid_rowconfigure(2, weight=1, uniform="foo")
        self.grid_rowconfigure(3, weight=1, uniform="foo")
        self.grid_columnconfigure(0, weight=1, uniform="foo")
    
    def viewer(self):
        
        font = tkFont.Font(family="monospace", size=18) 
        
        self.viewerui = Toplevel(self.master)
        self.viewerui.transient(self.master)
        self.viewerui.geometry("2000x1000+0+0")

        
        controlpanel = Frame(self.viewerui)
        controlpanel.grid(row=0,column=0,sticky=NSEW)
        
    
        self.viewerui.xaxis_label = Label(controlpanel,text="xaxis",font=font)
        self.viewerui.xaxis_label.grid(row=0,column=0)
        self.viewerui.xaxis_label.focus_get()
        self.viewerui.xaxis_label_sv = StringVar()
        self.viewerui.xaxis_label = Entry(controlpanel,textvariable=self.viewerui.xaxis_label_sv,font=font)
        self.viewerui.xaxis_label.grid(row=0,column=1)
        self.viewerui.xaxis_label.focus_get()
        self.viewerui.xaxis_label_sv.set("period")
        
        self.viewerui.yaxis_label = Label(controlpanel,text="yaxis",font=font)
        self.viewerui.yaxis_label.grid(row=0,column=2)
        self.viewerui.yaxis_label.focus_get()
        self.viewerui.yaxis_label_sv = StringVar()
        self.viewerui.yaxis_label = Entry(controlpanel,textvariable=self.viewerui.yaxis_label_sv,font=font)
        self.viewerui.yaxis_label.grid(row=0,column=3)
        self.viewerui.yaxis_label.focus_get()
        self.viewerui.yaxis_label_sv.set("dow")
        
        self.viewerui.prep_label = Label(controlpanel,text="prep",font=font)
        self.viewerui.prep_label.grid(row=0,column=4)
        self.viewerui.prep_label.focus_get()
        self.viewerui.prep_label_sv = StringVar()
        self.viewerui.prep_label = Entry(controlpanel,textvariable=self.viewerui.prep_label_sv,font=font)
        self.viewerui.prep_label.grid(row=0,column=5)
        self.viewerui.prep_label.focus_get()
        
        self.viewerui.student_label = Label(controlpanel,text="student",font=font)
        self.viewerui.student_label.grid(row=0,column=6)
        self.viewerui.student_label.focus_get()
        self.viewerui.student_label_sv = StringVar()
        self.viewerui.student_label = Entry(controlpanel,textvariable=self.viewerui.student_label_sv,font=font)
        self.viewerui.student_label.grid(row=0,column=7)
        self.viewerui.student_label.focus_get()
        self.viewerui.student_label_sv.set("Nathaniel")
        
        self.viewerui.teacher_label = Label(controlpanel,text="dow",font=font)
        self.viewerui.teacher_label.grid(row=0,column=8)
        self.viewerui.teacher_label.focus_get()
        self.viewerui.teacher_label_sv = StringVar()
        self.viewerui.teacher_label = Entry(controlpanel,textvariable=self.viewerui.teacher_label_sv,font=font)
        self.viewerui.teacher_label.grid(row=0,column=9)
        self.viewerui.teacher_label.focus_get()

        self.recalc_button = Button(controlpanel,command=self.viewer_calc,text="calc",
                                    name="vc")
        self.recalc_button.grid(row=0,column=0)
        self.recalc_button.focus_get()
        
        
        values = self.viewer_calc()
        

        #self.bgmaxrows=len(self.enums['period']['name'])+1
        #self.bgmaxcols=len(self.of.query('student'))+1
        
        
        self.bgmaxrows=len(values)
        self.bgmaxcols=len(values[0])

        widget_args=dict(background='white',width=2,height=3,wraplength=180,
                         highlightbackground='black',highlightthickness=4,
                         font=font,values=self.enums['dow'])
        widgetcfg = nxnarraycreate(self.bgmaxrows,self.bgmaxcols,widget_args)

        mytextalphanum = TextAlphaNumRO(name='textalphanum')

        try:
            self.viewergrid.destroy()
        except:
            pass
        
        self.viewergrid = TkImageLabelGrid(self.viewerui,'viewergrid',
                                                 mytextalphanum,10,10,
                                                 0,0,self.bgmaxrows,self.bgmaxcols,
                                                 True,False,{},widgetcfg)

        self.viewergrid.grid(row=1,column=0,sticky=NSEW)
        self.viewerui.grid_rowconfigure(1, weight=1, uniform="foo")
        self.viewerui.grid_columnconfigure(0, weight=1, uniform="foo")
        
        for x in range(len(values)):
            for y in range(len(values[x])):
                self.viewergrid.widgets[x][y].sv.set(values[x][y])
                
    def viewer_calc(self):
        
        values = []
    
        xaxis_type = self.viewerui.xaxis_label_sv.get() # period
        yaxis_type = self.viewerui.yaxis_label_sv.get() # dow
        
        source = "student"
        ztype = "teacher"
        
        source_obj = self.of.object_get(source,self.viewerui.student_label_sv.get())
        
        xaxis_obj = self.of.query(xaxis_type)
        yaxis_obj = self.of.query(yaxis_type)
        
        # get yaxis value
        row=['']
        for y in range(1,len(yaxis_obj)+1):
            row.append(yaxis_obj[y-1].name)
        values.append(row)
            
        # get xaxis value
        for x in range(len(xaxis_obj)):
            row = [xaxis_obj[x].name]
            values.append(row)
        
        for y in range(1,len(values[0])):

            for x in range(1,len(values)):
                
                xval = xaxis_obj[x-1].name     
                zval = getattr(source_obj.lessons[xval][y-1],ztype)
                values[x].append(zval.name)

        return(values)
   
        
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
        # prep
        prep=self.prep_entry_sv.get()
        if  prep == "":prep = -1
        
        # dow
        dow = self.dow_entry_sv.get()
        if dow == "": dow = "all"

        log.log(thisfuncname(),3,msg="saving save version=",saveversion=str(saveversion),prep=prep,dow=dow)

        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)

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
                    
                    try:
                        teacher = self.enums['adult']['code2name'][teacher_code]
                    except KeyError:
                        log.log(thisfuncname(),5,msg="could not find in enum; using **",teacher_code=teacher_code)
                        teacher = "**"
                        
                    try:
                        lessontype = self.enums['lessontype']['code2name'][lessontype_code]
                    except KeyError:
                        log.log(thisfuncname(),5,msg="could not find in enum; using **",lessontype_code=lessontype_code)
            
                        lessontype = "**"
                        
                    try:    
                        subject = self.enums['subject']['code2name'][subject_code]
                    except KeyError:
                        log.log(thisfuncname(),5,msg="could not find in enum; using **",subject_code=subject_code)
                             
                        subject = "**"
                    
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
            
    
    def dropdowns_set(self):
        
        #widget_args=dict(background='red',width=9,values=self.enums['student'])
        widget_args=dict(background='red',width=9,values=self.enums['student'])
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        widgetcfg = sswizard_utils.dropdown_build(self.refdatabase,widgetcfg,
                                                  _execfunc,self.prep_entry_sv.get(),
                                                  self.dow_entry_sv.get(),
                                                  _columnheaderexecfunc,_rowheaderexecfunc)    

        for x in range(self.maxrows):
            for y in range(self.maxcols):
                
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
    def load(self,saveversion=None,values=None, dow=None, prep=None):
        
        whereclause = []
        
        # dbname
        if self.dbname <> self.dbname_entry_sv.get():
            log.log(thisfuncname(),3,msg="dbname changed",oldname=self.dbname,newname=self.dbname_entry_sv.get())
            self.database = Database(self.dbname_entry_sv.get())
            self.dbname = self.dbname_entry_sv.get()
        
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
        
        # dow
        if dow==None: dow = self.dow_entry_sv.get()
        if dow == "":
            dow = "all"
        else:
            whereclause.append( ['dow',"=","\""+dow+"\""])
        log.log(thisfuncname(),3,msg="loading",dow=str(dow))
        
        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)
        
        whereclause.append(['saveversion',"=",saveversion])
        log.log(thisfuncname(),3,msg="loading",saveversion=str(saveversion))
        
        cols = ['period','student','session','dow']
        
        if values==None:
            with self.database:
                colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',cols,whereclause)
                
                log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
                
            if len(rows) == 0:
                log.log(thisfuncname(),2,msg="no rows detected",whereclause=whereclause)
                
            for row in rows:
                
                print row
                
                z = session =  row[cols.index('session')]
                period =  row[cols.index('period')]
                student =  row[cols.index('student')]
                
                x = self.enums['student']['name2enum'][student]
                y = self.enums['period']['name2enum'][str(period)]
                
                self.entrygrid.widgets[x][y].sv.set(session)
                self.entrygrid.widgets[0][y].sv.set(period)
                self.entrygrid.widgets[x][0].sv.set(student)
                
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