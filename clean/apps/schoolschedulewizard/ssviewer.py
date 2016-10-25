import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate, thisfuncname

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get, TkGridCombobox, \
     TkCombobox, Tk3Label, _tklabel, TkNLabel, _tkbutton

from misc_utils_objectfactory import ObjFactory

import sswizard_utils
from sswizard_query_utils import *
from sswizard_config_utils import *

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from Tkinter import *
from ttk import *

from Tkinter import Checkbutton as _checkbutton

from collections import OrderedDict

import tkFont
import unittest

pink = '#%02x%02x%02x' % (255, 153, 153)
salmon = '#%02x%02x%02x' % (255, 204, 153)
lightyellow = '#%02x%02x%02x' % (255, 255, 153)
lightgreen = '#%02x%02x%02x' % (204, 255, 153)
lightturquoise = '#%02x%02x%02x' % (153, 255, 204)
lightblue = '#%02x%02x%02x' % (153, 255, 255)
lavender = '#%02x%02x%02x' % (153, 153, 255)
purple = '#%02x%02x%02x' % (204, 153, 255)
pink = '#%02x%02x%02x' % (255, 153, 204)
darkgreen = '#%02x%02x%02x' % (0, 102, 0)
burgundy = '#%02x%02x%02x' % (102, 0, 51)
karky = '#%02x%02x%02x' % (102, 102, 0)
darkburgundy = '#%02x%02x%02x' % (102, 0, 51)
darkgrey = '#%02x%02x%02x' % (0, 51, 51)
brown = '#%02x%02x%02x' % (102, 51, 0)
mauve = '#%02x%02x%02x' % (204, 204, 0)
navyblue = '#%02x%02x%02x' % (0, 0, 51)
darkyellow = '#%02x%02x%02x' % (155,140,6)
paleblue = '#%02x%02x%02x' %(173,217,222)
palegreen = '#%02x%02x%02x' %(183,229,183)
cerise = '#%02x%02x%02x' %(212, 7, 253)

verydarkgrey = '#%02x%02x%02x' %(54, 46, 55)
dirtyyellow = '#%02x%02x%02x' %(242, 232, 19)


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
    

class WizardUI(Tk):
    #def __init__(self,database,of):
    def __init__(self,dbname,of,refdbname,maxentrycols=3,maxentryrows=4,
                 maxnewrowcols=3,maxnewrowrows=3):
        
        log.log(thisfuncname(),3,msg="initialize",dbname=dbname,refdbname=refdbname)
        
        #sys.platform == "darwin":
        #self.clipboard=[]
        #self.clipboard_selection=-1
        Tk.__init__(self)
        
        #self.colorpalette = dict(recordtype=dict(wp='green',subject='blue',ap='yellow'))
        self.colorpalette = dict(wp='green',subject=lightblue,ap='yellow',
                                 Movement=pink,ELA=salmon,Humanities=lightyellow,
                                 Counseling=lightgreen,Math=lightturquoise, 
                                 Music=lightblue,STEM=lavender,Art=purple,History=pink,
                                 Science=darkgreen,Core=karky,Chess=burgundy,
                                 computertime='darkgrey',Speech=darkburgundy,
                                 Student_News=darkgrey,Computer_Time=brown,
                                 Activity_Period=mauve,Melissa=navyblue,Amelia=darkgreen,
                                 Samantha=darkyellow, Alexa=paleblue, Paraic=palegreen, 
                                 Francisco=cerise,Rahul=verydarkgrey,Dylan=verydarkgrey,
                                 Moira=verydarkgrey,Issey=verydarkgrey, Daryl=verydarkgrey, 
                                 Karolina=verydarkgrey)
        

        self.fontpalette = dict(Amelia='green',Paraic=darkgreen,Stan=lavender,
                                Samantha=lightgreen,Alexa='blue',Francisco=purple,
                                Melissa=lightblue,Rahul=dirtyyellow,Dylan=dirtyyellow, 
                                Moira=dirtyyellow,Issey=dirtyyellow, Daryl=dirtyyellow, 
                                Karolina=dirtyyellow,Chess=pink,Student_News=lightyellow,
                                subject='blue')
        
        
        screenwidth = self.winfo_vrootwidth()
        screenheight = self.winfo_vrootheight()
        
        self.geometry(str(screenwidth) + "x" + str(screenheight) +"+0+0")
        
        wx = 8
        
        self.refdatabase = Database(refdbname)
        
        #self.enums = sswizard_utils.setenums('All','5',self.refdatabase)
        
        self.dbname = dbname
        
        self.database = Database(self.dbname)
        self.of = of

        
        font = tkFont.Font(family="monospace", size=12) 
        self.font = font
        
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
                
        style.configure('ControlPanel.TFrame',background='lightgrey')

        controlpanel = Frame(self,style='ControlPanel.TFrame')
        controlpanel.grid(row=1,column=0,sticky=NSEW,columnspan=2)
        
        self.dbload_entry_label = Label(controlpanel,text="version",width=wx,font=font,anchor=E)
        self.dbload_entry_label.grid(row=0,column=1,pady=5)
        self.dbload_entry_label.focus_get()
        self.dbload_entry_sv = StringVar()
        self.dbload_entry = Entry(controlpanel,textvariable=self.dbload_entry_sv,width=wx,font=font)
        self.dbload_entry.grid(row=0,column=2,pady=5)
        self.dbload_entry_sv.set('1')
        self.dbload_entry.focus_get()
        
        self.dbname_entry_label = Label(controlpanel,text="dbname",width=wx,font=font,anchor=E)
        self.dbname_entry_label.grid(row=0,column=3,pady=5)
        self.dbname_entry_label.focus_get()
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(controlpanel,textvariable=self.dbname_entry_sv,width=wx,font=font)
        self.dbname_entry.grid(row=0,column=4,pady=5)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set(self.dbname)
        
        self.dow_entry_label = Label(controlpanel,text="dow",width=wx,font=font,anchor=E)
        self.dow_entry_label.grid(row=0,column=5,pady=5)
        self.dow_entry_label.focus_get()
        
        self.dow_entry_sv = StringVar()
        self.dow_entry = Entry(controlpanel,textvariable=self.dow_entry_sv,width=wx,font=font)
        self.dow_entry.grid(row=0,column=6,pady=5)
        self.dow_entry.focus_get()
        #self.dow_entry_sv.set('MO')
        
        self.prep_label = Label(controlpanel,text="prep",width=wx,font=font,anchor=E)
        self.prep_label.grid(row=0,column=7,pady=5)
        self.prep_label.focus_get()
        
        self.prep_entry_sv = StringVar()        
        self.prep_entry = Entry(controlpanel,textvariable=self.prep_entry_sv,width=wx,font=font)
        self.prep_entry.grid(row=0,column=8,pady=5)
        self.prep_entry.focus_get()
        #self.prep_entry_sv.set(5)
        
        self.period_label = Label(controlpanel,text="period",width=wx,font=font,anchor=E)
        self.period_label.grid(row=0,column=9,pady=5)
        self.period_label.focus_get()
        
        self.period_entry_sv = StringVar()        
        self.period_entry = Entry(controlpanel,textvariable=self.period_entry_sv,width=wx,font=font)
        self.period_entry.grid(row=0,column=10,pady=5)
        self.period_entry.focus_get()
        #self.period_entry_sv.set('830-910')
        
        self.teacher_label = Label(controlpanel,text="teacher",width=wx,font=font,anchor=E)
        self.teacher_label.grid(row=0,column=11,pady=5)
        self.teacher_label.focus_get()
        
        self.teacher_label_sv = StringVar()        
        self.teacher_label = Entry(controlpanel,textvariable=self.teacher_label_sv,width=wx,font=font)
        self.teacher_label.grid(row=0,column=12,pady=5)
        self.teacher_label.focus_get()
        #self.teacher_label_sv.set('Stan')
        
        self.student_label = Label(controlpanel,text="student",width=wx,font=font,anchor=E)
        self.student_label.grid(row=0,column=13,pady=5)
        self.student_label.focus_get()
        
        self.student_label_sv = StringVar()        
        self.student_label = Entry(controlpanel,textvariable=self.student_label_sv,width=wx,font=font)
        self.student_label.grid(row=0,column=14,pady=5)
        self.student_label.focus_get()
        self.student_label_sv.set('Nathaniel')
        
    
        self.source_label = Label(controlpanel,text="source",width=wx,font=font,anchor=E)
        self.source_label.grid(row=0,column=15,pady=5)
        self.source_label.focus_get()
    
        self.source_label_sv = StringVar()        
        self.source_label = Entry(controlpanel,textvariable=self.source_label_sv,width=wx,font=font)
        self.source_label.grid(row=0,column=16,pady=5)
        self.source_label.focus_get()
        self.source_label_sv.set('dbinsert')
        
        buttonpanel = Frame(controlpanel,style='ControlPanel.TFrame')
        buttonpanel.grid(row=0,column=17,sticky=NSEW)
    
        self.dbload_button = _tkbutton(buttonpanel,font=font,command=lambda: self.load(self.dbload_entry_sv.get()),
                                    text="dbload",name="dbl")
    
        self.dbload_button.grid(row=0,column=0,pady=5)
        self.dbload_button.focus_get()
    
        self.clear_button = _tkbutton(buttonpanel,font=font,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(row=0,column=1,pady=5)
        self.clear_button.focus_get()
    
        self.viewer_button = _tkbutton(buttonpanel,font=font,command=self.viewer,text="viewer",name="view")
        self.viewer_button.grid(row=0,column=2,pady=5)
        self.viewer_button.focus_get()

        
        
        self.viewcontrolpanel = Frame(self.master)
        self.viewcontrolpanel.grid(row=2,column=0,sticky=NSEW)
        
        self.viewxaxis_label = Label(self.viewcontrolpanel,text="xaxis",width=wx,font=font,anchor=E)
        self.viewxaxis_label.grid(row=0,column=0,pady=5)
        self.viewxaxis_label.focus_get()
        self.viewxaxis_label_sv = StringVar()
        self.viewxaxis_label = Entry(self.viewcontrolpanel,textvariable=self.viewxaxis_label_sv,width=wx,font=font)
        self.viewxaxis_label.grid(row=0,column=1,pady=5)
        self.viewxaxis_label.focus_get()
        self.viewxaxis_label_sv.set("period")
        
        self.viewyaxis_label = Label(self.viewcontrolpanel,text="yaxis",width=wx,font=font,anchor=E)
        self.viewyaxis_label.grid(row=0,column=2,pady=5)
        self.viewyaxis_label.focus_get()
        self.viewyaxis_label_sv = StringVar()
        self.viewyaxis_label = Entry(self.viewcontrolpanel,textvariable=self.viewyaxis_label_sv,width=wx,font=font)
        self.viewyaxis_label.grid(row=0,column=3,pady=5)
        self.viewyaxis_label.focus_get()
        self.viewyaxis_label_sv.set("dow")
        
        self.viewfocus_label = Label(self.viewcontrolpanel,text="focus",width=wx,font=font,anchor=E)
        self.viewfocus_label.grid(row=0,column=4,pady=5)
        self.viewfocus_label.focus_get()
        self.viewfocus_label_sv = StringVar()
        self.viewfocus_label = Entry(self.viewcontrolpanel,textvariable=self.viewfocus_label_sv,width=wx*2,font=font)
        self.viewfocus_label.grid(row=0,column=5,pady=5)
        self.viewfocus_label.focus_get()
        self.viewfocus_label_sv.set("student=Nathaniel")
        
        self.viewstudent_label = Label(self.viewcontrolpanel,text="student",width=wx,font=font,anchor=E)
        self.viewstudent_label.grid(row=0,column=6,pady=5)
        self.viewstudent_label.focus_get()
        self.viewstudent_label_sv = StringVar()
        self.viewstudent_label = Entry(self.viewcontrolpanel,textvariable=self.viewstudent_label_sv,width=wx,font=font)
        self.viewstudent_label.grid(row=0,column=7,pady=5)
        self.viewstudent_label.focus_get()
        self.viewstudent_label_sv.set("Nathaniel")
        
        self.viewteacher_label = Label(self.viewcontrolpanel,text="dow",width=wx,font=font,anchor=E)
        self.viewteacher_label.grid(row=0,column=8,pady=5)
        self.viewteacher_label.focus_get()
        self.viewteacher_label_sv = StringVar()
        self.viewteacher_label = Entry(self.viewcontrolpanel,textvariable=self.viewteacher_label_sv,width=wx,font=font)
        self.viewteacher_label.grid(row=0,column=9,pady=5)
        self.viewteacher_label.focus_get()
        
        self.viewdata_label = Label(self.viewcontrolpanel,text="data",width=wx,font=font,anchor=E)
        self.viewdata_label.grid(row=0,column=10,pady=5)
        self.viewdata_label.focus_get()
        self.viewdata_label_sv = StringVar()
        self.viewdata_label = Entry(self.viewcontrolpanel,textvariable=self.viewdata_label_sv,width=wx*3,font=font)
        self.viewdata_label.grid(row=0,column=11,pady=5)
        self.viewdata_label.focus_get()
        self.viewdata_label_sv.set("subject,teacher,recordtype")
        
        self.wheight_label = Label(self.viewcontrolpanel,text="data",width=wx,font=font,anchor=E)
        self.wheight_label.grid(row=0,column=12,pady=5)
        self.wheight_label.focus_get()
        self.wheight_label_sv = StringVar()
        self.wheight_label = Entry(self.viewcontrolpanel,textvariable=self.wheight_label_sv,width=wx,font=font)
        self.wheight_label.grid(row=0,column=13,pady=5)
        self.wheight_label.focus_get()
        self.wheight_label_sv.set(1)
                                  
        self.conflict_checkbutton_sv = StringVar()
        self.conflict_checkbutton = _checkbutton(self.viewcontrolpanel, text="conflicts only", variable=self.conflict_checkbutton_sv,
                                                onvalue="Y", offvalue="N",width=wx*2,font=font)
        self.conflict_checkbutton.grid(row=0,column=14,pady=5)

        
        self.grid_columnconfigure(0, weight=1, uniform="foo")
            
    def dump(self,value):
        
        with self.database:
            cols,rows,_ = _versions(self.database,*value)
            _,subjects,_ = _versions_subjects(self.database,*value)
        
        for subject in subjects:
            
            if subject[0] <> "??":
                _period = sswizard_utils._isenum(self.enums,'period',value[0])
                _dow = sswizard_utils._isname(self.enums,'dow',value[1])
                
                value = [_period,_dow,subject[0]]
            
                with self.database: 
                    cols,sessionrows,_ = _sessionversions(self.database,*value)
        
        rows = rows + sessionrows
        
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
            try:
                self.versionsgrid.destroy()
            except AttributeError:
                pass
        
        rows.sort()
        return rows

    def color_get(self,value):
        
        bg = 'lightgrey'
        fg = 'black'
             
        if value.count(" ") > 0:
            value= value.replace(" ","_")
            
        if value.count("[") == 1 and value.count("]") == 1:
            bg = 'red'
        
        if value.count(".") > 0:
            value = value.split(".")[0]
            
        if self.colorpalette.has_key(value):
            bg = self.colorpalette[value]
            
        if self.fontpalette.has_key(value):
            fg = self.fontpalette[value]
            
            
        return(bg,fg)


        
        
    def viewer(self,ui=True,source_type=None,source_value=None,
               ztypes=None,yaxis_type=None,xaxis_type=None,
               conflicts_only=None,constraints=None):
        
        # constraint will be a list of tuples of the form
        # objtype,objvalue i.e. ('dow','MO')
        
        if conflicts_only == None:
            conflicts_only = self.conflict_checkbutton_sv.get() 
            
        if yaxis_type == None:
            yaxis_type = self.viewyaxis_label_sv.get() # dow
            
        if xaxis_type == None:
            xaxis_type = self.viewxaxis_label_sv.get() # period
        
        if source_type == None or source_value == None:
            source_type,source_value = self.viewfocus_label_sv.get().split("=")
        
        if ztypes == None:
            ztypes = self.viewdata_label_sv.get().split(",")
            
        if source_value == "":
            source_objs = self.of.query(source_type)
        else:
            source_objs = [self.of.object_get(source_type,source_value)]
            
        xaxis_obj = self.of.query(xaxis_type)
        yaxis_obj = self.of.query(yaxis_type)
        
        count=0
        yaxis_enum = {}
        for _yaxis_obj in yaxis_obj:
            yaxis_enum[_yaxis_obj.name] = count
            count+=1
        
        xaxis_enum = self.enums[xaxis_type]['name2enum']
        #yaxis_enum = self.enums[yaxis_type]['code2enum']
        
        values = [] # contains the values displayed on the grid
        row=[''] # 

        values = [['']]    
        for yval in yaxis_enum.keys():
            values[0].append(yval)
            
        for xval in xaxis_enum.keys():
            values.append([xval])

        ymax = len(values[0])
        xmax = len(values)-1
        
        def _additem(celltext,item):
            
            if len(celltext) == 0:
                celltext.append(item)
            else:
                try:
                    celltext.index(item)
                except:
                    celltext.append(item)
            return(celltext)
                
            
        for yval,y in yaxis_enum.iteritems():

            for xval,x in xaxis_enum.iteritems():
                celltext=[]
                
                for source_obj in source_objs:
                    if source_obj.lessons.has_key(yval):
                        if source_obj.lessons[yval].has_key(xval):
                            _vals = source_obj.lessons[yval][xval]
                            _valcount=0
                            for _val in _vals:
                                
                                if constraints <> None:
                                    flag=False
                                    for objtype,objval in constraints:
                                        
                                        if getattr(_val,objtype).name <> objval:
                                            flag=True
                                    if flag == True:
                                        continue
                                            
                                if _valcount >= 1:
                                    celltext.append('spacer')
                                for ztype in ztypes:
                                    if hasattr(_val,ztype) == True:
                                        zval = getattr(_val,ztype)
                                        
                                        celltext = _additem(celltext,zval.name)
                                        #celltext.append(zval.name)
                                    #else:
                                        #print "lesson",_val,"does not have attr",ztype
                                
                                _valcount+=1
                        #else:
                            #print "source",source_obj.name,"yval=",yval," does not have key",xval
                    #else:
                        #print "source",source_obj.name," does not have key",yval
                
                if celltext == []:
                    celltext.append("")
                    
                values[x].append(celltext)
                
        #for row in values:
        #    print row
        
        if ui==True:
            self.bgmaxrows=len(values)
            self.bgmaxcols=len(values[0])
        
            #,wraplength=240
            widget_args=dict(background='white',width=1,height=4,highlightbackground='black',highlightthickness=1,values=self.enums['dow'])
            widgetcfg = nxnarraycreate(self.bgmaxrows,self.bgmaxcols,widget_args)
            mytextalphanum = TextAlphaNumRO(name='textalphanum')
        
            try:
                self.viewergrid.destroy()
            except:
                pass
            
            mytextalphanum.widgettype = TkNLabel
            
            self.viewergrid = TkImageLabelGrid(self,'viewergrid',mytextalphanum,10,10,0,0,self.bgmaxrows,self.bgmaxcols,True,False,{},widgetcfg,1)
        
            self.viewergrid.grid(row=3,column=0,sticky=NSEW)
            self.grid_rowconfigure(3, weight=10, uniform="foo")
            
            for x in range(len(values)):
                for y in range(len(values[x])):
                    widget = self.viewergrid.widgets[x][y]
                    _value = values[x][y]

                    if isinstance(_value,list) == True:

                        for i in range(len(_value)):
                            if _value[i] == "spacer":
                                widget.addspacer()
                            elif _value[i] <> "":
                                _bg,_fg = self.color_get(_value[i])
                                
                                if conflicts_only == "Y":
                                    if _bg <> 'red':
                                        continue
                                
                                _widget,_widget_sv = widget.addlabel()
                                _widget_sv.set(_value[i])
                                
                                _widget.config(background=_bg,foreground=_fg,height=self.wheight_label_sv.get())
                                
                    else:
                        expand=False
                        if x == 0 or y == 0:
                            expand=True
                            
                        _widget,_widget_sv = widget.addlabel(expand)
                        _widget_sv.set(_value)                                       
        else:
            return values
            
        self.viewergrid.reset_framewidth()
        self.viewergrid.resize_canvasframe()
        
        
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
        
        
        # add the lesson to the adult object
        adult = lesson.adult
        if hasattr(adult,'lessons') == False:
            setattr(adult,'lessons',{})
          
        if adult.lessons.has_key(dow) == False:
            adult.lessons[dow] = {} 

        if adult.lessons[dow].has_key(period) == False:
            adult.lessons[dow][period] = []
            
        adult.lessons[dow][period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to adult",dow=str(dow),period=str(period),
                 session=str(lesson.session.name),adult=str(lesson.adult.name))
        
        # add the lesson to the student object (indexed by dow/period)
        student = lesson.student
        if hasattr(student,'lessons') == False:
            setattr(student,'lessons',{})
            
        if student.lessons.has_key(dow) == False:
            student.lessons[dow] = {}
            
        if student.lessons[dow].has_key(period) == False:
            student.lessons[dow][period] = []
            
        student.lessons[dow][period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to student (dow/period index)",dow=str(dow),period=str(period),
                session=str(lesson.session.name),student=str(lesson.student.name))
        
        #adult = self.enums['adult']['name2code'][lesson.adult.objid]
        
        adult = lesson.adult.objid
        
        # add the lesson to the student object (indexed by adult/period)
        if student.lessons.has_key(adult) == False:
            student.lessons[adult] = {}
            
        if student.lessons[adult].has_key(period) == False:
            student.lessons[adult][period] = []
            
        student.lessons[adult][period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to student (adult/period index)",adult=str(adult),period=str(period),
                session=str(lesson.session.name),student=str(lesson.student.name))
        
        adult = lesson.adult
        student = lesson.student.objid
        # add the lesson to the adult object (indexed by student)
        if adult.lessons.has_key(student) == False:
            adult.lessons[student] = {}
            
        if adult.lessons[student].has_key(period) == False:
            adult.lessons[student][period] = []
            
        adult.lessons[student][period].append(lesson)
        log.log(thisfuncname(),9,msg="lesson added to student (student/period index)",student=str(student),period=str(period),
                session=str(lesson.session.name),adult=str(lesson.student.name))
        
        
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
    def load(self,saveversion=None, dow=None, prep=None, period=None, teacher=None, student=None, source=None):
        
        self.of.reset()
        
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
        
        # source
        if source==None: source = self.source_label_sv.get()
        if source == "":
            source = "dbinsert"
        else:
            _sources = ["\"" + _source + "\"" for _source in source.split(",")]
            whereclause.append( ['source',"in","("+",".join(_sources)+")"])
        log.log(thisfuncname(),3,msg="loading",source=str(source))
        
        #whereclause.append( ['status',"=","\"" + "master" + "\""])
        #whereclause.append( ['source',"=","\"" + "prep56new.csv" + "\""])
        
        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)

        # load from database
        cols = ['period','student','session','dow','teacher','subject','userobjid','status','substatus','recordtype','source']        
        with self.database:
            colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',cols,whereclause)
            
            log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
        
        cols = ['period','student','session','dow','adult','subject','userobjid','status','substatus','recordtype','source']
        
        # parse rows
        for row in rows:
            datamembers = {}
            for i in range(len(cols)):
                datamembers[cols[i]] = row[i]
            
            _,lessontype_code,_,_ = datamembers['session'].split(".")
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

def dump2csv(results,conflicts_only):

    for row in results:
        output_row = []
        for item in row:
            
            if isinstance(item,list) == True:
                output_cell = []
                for _item in item:
                    if conflicts_only == "Y":
                        if _item.count("[") <> 1 or _item.count("]") <> 1:
                            continue
                    output_cell.append(_item.replace(",","/"))    
                output_row.append(" ".join(output_cell))
            else:
                output_row.append(str(item))
        print ",".join(output_row)
        
if __name__ == "__main__":
    #master = Tk()
    
    enableui = False
    
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
    
    conflicts_only="Y"
    
    if enableui == True:
        app.mainloop()       
    else:
        app.load(saveversion=1,student="")
        
        
        for dow in ['MO','TU','WE','TH','FR']:
            results = app.viewer(ui=False,source_type="adult",ztypes=['adult','subject'],
                                 source_value="",yaxis_type="student",constraints=[('dow',dow)])
        
            dump2csv(results,"Y")
    