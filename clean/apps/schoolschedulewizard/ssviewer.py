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
import ssviewer_utils

from sswizard_query_utils import *
from sswizard_config_utils import *
from ssviewer_utils_palette import dbformats_get, dbcolors_get

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from Tkinter import *
from ttk import *

from Tkinter import Checkbutton as _checkbutton

from collections import OrderedDict

import tkFont
import unittest

controlpanelconfig = dict(height=300,width=200,x=100,y=100)

dbname,_ = sswizard_utils.getdatabase()

colorpalette = dbformats_get(dbname,'bgcolor')
fontpalette = dbformats_get(dbname,'fgcolor')
colors = dbcolors_get(dbname)

class WizardUI(Tk):
    #def __init__(self,database,of):
    
    
    def __init__(self,dbname,of,refdbname,maxentrycols=3,maxentryrows=4,
                 maxnewrowcols=3,maxnewrowrows=3):
        
        log.log(thisfuncname(),3,msg="initialize",dbname=dbname,refdbname=refdbname)
        
        #sys.platform == "darwin":
        #self.clipboard=[]
        #self.clipboard_selection=-1
        Tk.__init__(self)
        
        globals()['colors'] = dbcolors_get(dbname)
        self.colorpalette = dbformats_get(dbname,'bgcolor')
        self.fontpalette = dbformats_get(dbname,'fgcolor')
        
        #self.colorpalette = colorpalette
        #self.fontpalette = fontpalette
        
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
        
        self.unknown_checkbutton_sv = StringVar()
        self.unknown_checkbutton = _checkbutton(controlpanel, text="unknowns", variable=self.unknown_checkbutton_sv,
                                                onvalue="Y", offvalue="N",width=wx*2,font=font)
        self.unknown_checkbutton.grid(row=0,column=17,pady=5)
        
        buttonpanel = Frame(controlpanel,style='ControlPanel.TFrame')
        buttonpanel.grid(row=0,column=18,sticky=NSEW)
    
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
        
        self.wheight_label = Label(self.viewcontrolpanel,text="wheight",width=wx,font=font,anchor=E)
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
        
        self.wratio_label = Label(self.viewcontrolpanel,text="wratio",width=wx,font=font,anchor=E)
        self.wratio_label.grid(row=0,column=15,pady=5)
        self.wratio_label.focus_get()
        self.wratio_label_sv = StringVar()
        self.wratio_label = Entry(self.viewcontrolpanel,textvariable=self.wratio_label_sv,width=wx,font=font)
        self.wratio_label.grid(row=0,column=16,pady=5)
        self.wratio_label.focus_get()
        self.wratio_label_sv.set("1,1,1")

        self.grid_columnconfigure(0, weight=1, uniform="foo")
        
    def viewer(self,ui=True,source_type=None,source_value=None,
               ztypes=None,yaxis_type=None,xaxis_type=None,
               conflicts_only=None,constraints=None,wratio=None,formatson=False,
               valuetype=False):
        
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
        
        if wratio == None:
            wratio = self.wratio_label_sv.get().split(",")
        
        # what attributes of an object do we want to display
        # if * is passed that means show the count of the number of records returned
        if ztypes == None:
            ztypes = self.viewdata_label_sv.get().split(",")
            
        values = ssviewer_utils.dataset_pivot(self.of,self.enums,yaxis_type,xaxis_type,ztypes, source_type,source_value,
                                            conflicts_only,constraints,wratio,formatson)
        
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
                        if _value <> []:
                            #if len(_value) == 1 and conflicts_only <> "Y": # replace with line below if want to switch on conflicts
                            if len(_value) == 1:
                                                            
                                if isinstance(_value[0],tuple) == True:
                                    # 1 item, multi attributes
                                    bgs,fgs = _color_get_multi(_value[0])
                                    _widgets = widget.addlabel(len(_value[0]),True,_value[0],bgs,fgs,wratio)
                                elif isinstance(_value[0],list) == False:
                                    # 1 item, single value
                                    bg,fg = color_get(_value[0])
                                    _widgets = widget.addlabel(1,True,_value[0],bg,fg)
                                    
                            # multiple items
                            #if len(_value) > 1 and conflicts_only == "Y": # replace with line below if want to switch on conflicts
                            if len(_value) > 1:
                                for __value in _value:
                                    bgs,fgs = _color_get_multi(__value)
                                    _widgets = widget.addlabel(len(__value),True,__value,bgs,fgs,wratio)

                    else:
                        expand=False
                        if x == 0 or y == 0:
                            expand=True
                            
                        _widgets = widget.addlabel(expand)
                        _widgets[0].sv.set(_value)                                       
        else:
            schema=None
            if valuetype == True:
                schema = dict(xaxis=xaxis_type,yaxis=yaxis_type,ztypes=ztypes)
            values = ssviewer_utils.dataset_serialize(values,formatson,schema=schema)
                                   
            return values
            
            
        self.viewergrid.reset_framewidth()
        self.viewergrid.resize_canvasframe()
        
    def _dumpviewergrid(self):
        
        w = self.viewergrid.widgets
        _grid = []
        for x in range(len(w)):
            _row = []
            for y in range(len(w[0])):
                if hasattr(w[x][y],"widgets"):
                    _row.append(w[x][y].dumpcontents())
                else:
                    _row.append("")
            _grid.append(_row)
        return(_grid)

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
    def load(self,saveversion=None, dow=None, prep=None, period=None, teacher=None, student=None, source=None,
             unknown=None):
        
        self.of.reset()
        
        # database name
        if self.dbname_entry_sv.get() <> self.dbname:
            newdb = self.dbname_entry_sv.get()
            log.log(thisfuncname(),3,msg="switching databases",olddb=self.dbname,newdb=newdb)
            self.database = Database(newdb)
            self.dbname = newdb
            
        # saveversion
        if saveversion==None or saveversion== "":
            saveversion = self.dbload_entry_sv.get()
        if saveversion == "":
            log.log(thisfuncname(),1,msg="no saveversion set for load; exception")
            raise Exception("attempting to load without a saveversion set")
        
        # unknown
        if unknown==None:
            unknown = self.unknown_checkbutton_sv.get()
            
        # prep
        if prep==None: prep=self.prep_entry_sv.get()
        if  prep == "":
            prep = -1
        
        # period
        if period==None: period=self.period_entry_sv.get()
        if period == "":
            period = "all"

        # dow
        if dow==None: dow = self.dow_entry_sv.get()
        if dow == "":
            dow = "all"
        
        # teacher
        if teacher==None: teacher = self.teacher_label_sv.get()
        if teacher == "":
            teacher = "all"    
        
        # student
        if student==None: student = self.student_label_sv.get()
        if student == "":
            student = "all"
        
        # source
        if source==None: source = self.source_label_sv.get()
        if source == "":
            source = "dbinsert"       

        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)

        ssviewer_utils.dataset_load(self.database,self.refdatabase,self.of,self.enums,saveversion,unknown,prep,period,
                                    dow,teacher,student,source)
        
        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)

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

    outputstr = ""
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
        
        outputstr += "^".join(output_row) + "\n"
    return outputstr
        
if __name__ == "__main__":
    
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
    
    conflicts_only="Y"
    unknowns="N"
    
    if enableui == True:
        app.mainloop()       
    else:
        app.load(saveversion=1,student="",source="56n,4n,4s,5s,6s",unknown=unknowns)

        for dow in ['MO','TU','WE','TH','FR']:
            app.viewer(ui=True,source_type="adult",ztypes=['adult','subject'],
                       source_value="",yaxis_type="student",constraints=[('dow',dow)],
                       conflicts_only=conflicts_only)
            
            results = app._dumpviewergrid()
        
            print dump2csv(results,conflicts_only)
    