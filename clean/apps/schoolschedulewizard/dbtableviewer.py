import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNum, \
     TextAlphaNumRO, TrueFalse
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get, TkGridEntry
from misc_utils import nxnarraycreate, thisfuncname


import sswizard_utils

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, \
     tbl_rows_update, dbtblfactory, tbl_col_update, tbl_col_add,tbl_row_delete

from collections import OrderedDict
from Tkinter import *
from ttk import *
import tkFont

class DBTableUI(Tk):
    def __init__(self,maxentrycols=18,maxentryrows=12,
                 maxnewrowcols=16,maxnewrowrows=3):
        
        Tk.__init__(self)

        self.lastsaveversion=0
        
        # any children that change update this 
        # key is the name and value is the new val
        # the name is likely to be the tkwidgetid.x,y
        self.updates = OrderedDict()
        
        
        # clipboard stuff
        self.clipboard=[]
        self.clipboard_selection=-1        

        # dbm columns are added here as they are loaded
        # .index+1 will give the col # on the grid that corresponds
        # useful for looking up pk values for updates
        self.dbcol_defn = []
        
        self.maxrows=maxentryrows # rows in the grid
        self.maxcols=maxentrycols # cols in the grid        

        #self.maxrows=57 # rows in the grid
        #self.maxcols=15 # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*20 # master height
        wmwidth=wwidth*20 # master width 

        geom = geometry_get(1500,2000,0,0)
        self.geometry(geom)
               
        #master.bind("<Prior>",self.focus_next_widget)
        self.bind("<Prior>",self.focus_next_widget)
        self.grid()

        font = tkFont.Font(family="monospace", size=10)  

        # entry grid origin label
        xlbl_widget_args=dict(width=10,font=font)
        xlbl_widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,xlbl_widget_args)
        
        mytruefalse = TrueFalse(name='truefalse')
        self.entrygridolbl = TkImageLabelGrid(self,'entrygridolbl',mytruefalse,2,wmheight,
                                                0,0,1,1,False,{},xlbl_widgetcfg)
        self.entrygridolbl.grid(row=0,column=0,rowspan=2,sticky=NS)
        
        # entry grid y label
        ylbl_widget_args=dict(width=10,font=font)
        ylbl_widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,ylbl_widget_args)
        
        mytextalphanumro = TextAlphaNum(name='textalphanum')
        self.entrygridylabel = TkImageLabelGrid(self,'entrygridylbl',mytextalphanumro,2,wmheight,
                                                0,0,1,self.maxcols,False,False,{},ylbl_widgetcfg)
        self.entrygridylabel.grid(row=0,column=1,sticky=EW)
        
        for i in range(self.maxcols):
            self.entrygridylabel.widgets[0][i].sv.set(i+1)
            self.entrygridylabel.widgets[0][i]['style'] = 'InFocus.Label.TEntry'
            
        # entry grid x label
        xlbl_widget_args=dict(width=10,font=font)
        xlbl_widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,xlbl_widget_args)
        
        mytruefalse = TrueFalse(name='truefalse')
        self.entrygridxlabel = TkImageLabelGrid(self,'entrygridxlbl',mytruefalse,2,wmheight,
                                                0,0,self.maxrows,1,False,False,{},xlbl_widgetcfg)
        self.entrygridxlabel.grid(row=1,column=0,rowspan=1,sticky=NS)
        
        for i in range(self.maxrows):
            self.entrygridxlabel.widgets[i][0].sv.set(i+1)
            self.entrygridxlabel.widgets[i][0]['style'] = 'InFocus.Label.TEntry'
         
   
        # entry grid
        widget_args=dict(background='white',width=20,font=font)
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)

        mytextalphanum = TextAlphaNum(name='textalphanum')
        
        mytextalphanum.widgettype = TkGridEntry
        
        self.entrygrid = TkImageLabelGrid(self,'entrygrid',mytextalphanum,wmwidth,wmheight,
                             0,0,self.maxrows,self.maxcols,
                             False,True,{},widgetcfg)
        self.entrygrid.grid(row=1,column=1,sticky=NSEW)
        
        
        # dbcontrolpanel
        dbcontrolpanel = Frame(self)
        dbcontrolpanel.grid(row=2,column=1,sticky=NSEW,padx=10,pady=10)
                
        self.dbname_label = Label(dbcontrolpanel,text="database",width=10)
        self.dbname_label.grid(column=0,row=1,sticky=NSEW)
        self.dbname_label.focus_get()
        
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(dbcontrolpanel,textvariable=self.dbname_entry_sv)
        self.dbname_entry.grid(column=1,row=1,sticky=NSEW)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set("htmlparser")

        self.tblname_label = Label(dbcontrolpanel,text="table",width=10)
        self.tblname_label.grid(column=0,row=2,sticky=NSEW)
        self.tblname_label.focus_get()
        
        self.tblname_entry_sv = StringVar()
        self.tblname_entry = Entry(dbcontrolpanel,textvariable=self.tblname_entry_sv)
        self.tblname_entry.grid(column=1,row=2,sticky=NSEW)
        self.tblname_entry.focus_get()
        self.tblname_entry_sv.set("lesson")

        # query predicate 1
        self.pred1_label = Label(dbcontrolpanel,text="pred1",width=10)
        self.pred1_label.grid(column=7,row=1,sticky=NSEW)
        self.pred1_label.focus_get()
    
        self.pred1_entry_sv = StringVar()
        self.pred1_entry = Entry(dbcontrolpanel,textvariable=self.pred1_entry_sv)
        self.pred1_entry.grid(column=8,row=1,sticky=NSEW)
        self.pred1_entry.focus_get()
    
        # query predicate value 1
        self.pred1_op_entry_sv = StringVar()
        self.pred1_op_entry = Entry(dbcontrolpanel,textvariable=self.pred1_op_entry_sv)
        self.pred1_op_entry.grid(column=9,row=1,sticky=NSEW)
        self.pred1_op_entry.focus_get()
        self.pred1_op_entry_sv.set("=")
    
        self.predval1_entry_sv = StringVar()
        self.predval1_entry = Entry(dbcontrolpanel,textvariable=self.predval1_entry_sv)
        self.predval1_entry.grid(column=10,row=1,sticky=NSEW)
        self.predval1_entry.focus_get()
    
        # query predicate 2
        self.pred2_label = Label(dbcontrolpanel,text="pred2",width=10)
        self.pred2_label.grid(column=7,row=2,sticky=NSEW)
        self.pred2_label.focus_get()
    
        self.pred2_entry_sv = StringVar()
        self.pred2_entry = Entry(dbcontrolpanel,textvariable=self.pred2_entry_sv)
        self.pred2_entry.grid(column=8,row=2,sticky=NSEW)
        self.pred2_entry.focus_get()
    
        # query predicate value 2
        self.pred2_op_entry_sv = StringVar()
        self.pred2_op_entry = Entry(dbcontrolpanel,textvariable=self.pred2_op_entry_sv)
        self.pred2_op_entry.grid(column=9,row=2,sticky=NSEW)
        self.pred2_op_entry.focus_get()
        self.pred2_op_entry_sv.set("=")
    
        self.predval2_entry_sv = StringVar()
        self.predval2_entry = Entry(dbcontrolpanel,textvariable=self.predval2_entry_sv)
        self.predval2_entry.grid(column=10,row=2,sticky=NSEW)
        self.predval2_entry.focus_get()
        
        # query predicate 3
        self.pred3_label = Label(dbcontrolpanel,text="pred3",width=10)
        self.pred3_label.grid(column=7,row=3,sticky=NSEW)
        self.pred3_label.focus_get()
    
        self.pred3_entry_sv = StringVar()
        self.pred3_entry = Entry(dbcontrolpanel,textvariable=self.pred3_entry_sv)
        self.pred3_entry.grid(column=8,row=3,sticky=NSEW)
        self.pred3_entry.focus_get()
    
        # query predicate value 3
        self.pred3_op_entry_sv = StringVar()
        self.pred3_op_entry = Entry(dbcontrolpanel,textvariable=self.pred3_op_entry_sv)
        self.pred3_op_entry.grid(column=9,row=3,sticky=NSEW)
        self.pred3_op_entry.focus_get()
        self.pred3_op_entry_sv.set("=")
    
        self.predval3_entry_sv = StringVar()
        self.predval3_entry = Entry(dbcontrolpanel,textvariable=self.predval3_entry_sv)
        self.predval3_entry.grid(column=10,row=3,sticky=NSEW)
        self.predval3_entry.focus_get()
        
        # primary key specifier
        self.pkentry_label = Label(dbcontrolpanel,text="pk",width=10)
        self.pkentry_label.grid(column=11,row=1,sticky=NSEW)
        self.pkentry_label.focus_get()
    
        self.pk_entry_sv = StringVar()
        self.pk_entry = Entry(dbcontrolpanel,textvariable=self.pk_entry_sv)
        self.pk_entry.grid(column=12,row=1,sticky=NSEW)
        self.pk_entry.focus_get()
        self.pk_entry_sv.set("__id")
        
        # last query row count
        self.lastquery_rowcount_label = Label(dbcontrolpanel,text="last row#",width=10)
        self.lastquery_rowcount_label.grid(column=13,row=1,sticky=NSEW)
        self.lastquery_rowcount_label.focus_get()
    
        self.lastquery_rowcount_text_sv = StringVar()
        self.lastquery_rowcount_text = Entry(dbcontrolpanel,text=self.lastquery_rowcount_text_sv)
        self.lastquery_rowcount_text.grid(column=14,row=1,sticky=NSEW)
        self.lastquery_rowcount_text.focus_get()

        
        # last query viewer
        self.lastquery_label = Label(dbcontrolpanel,text="last query",width=10)
        self.lastquery_label.grid(column=11,row=2,sticky=NSEW)
        self.lastquery_label.focus_get()
    
        self.lastquery_text_sv = StringVar()
        self.lastquery_text = Entry(dbcontrolpanel,textvariable=self.lastquery_text_sv)
        self.lastquery_text.grid(column=12,row=2,sticky=NSEW,columnspan=3)
        self.lastquery_text.focus_get()

        # controlpanel
        controlpanel = Frame(self)
        controlpanel.grid(row=3,column=1,sticky=NSEW,pady=10,padx=10)
  
        self.scrolldelta_label = Label(controlpanel,text="sdelta",width=10)
        self.scrolldelta_label.grid(column=0,row=0,sticky=NSEW)
        self.scrolldelta_label.focus_get()
        
        self.scrolldelta_label_entry_sv = StringVar()
        self.scrolldelta_label_entry = Entry(controlpanel,textvariable=self.scrolldelta_label_entry_sv)
        self.scrolldelta_label_entry.grid(column=1,row=0,sticky=NSEW)
        self.scrolldelta_label_entry.focus_get()
        self.scrolldelta_label_entry_sv.set(10)
        
        self.hlightpk_label = Label(controlpanel,text="hlight pk",width=10)
        self.hlightpk_label.grid(column=2,row=0,sticky=NSEW)
        self.hlightpk_label.focus_get()
        
        self.hlightpk_text_sv = StringVar()
        self.hlightpk_text = Entry(controlpanel,text=self.hlightpk_text_sv)
        self.hlightpk_text.grid(column=3,row=0,sticky=NSEW)
        self.hlightpk_text.focus_get()
        
        self.inputmode_label = Label(controlpanel,text="hlight pk",width=10)
        self.inputmode_label.grid(column=4,row=0,sticky=NSEW)
        self.inputmode_label.focus_get()

        self.inputmode_value_sv = StringVar()        
        self.inputmode_value = Entry(controlpanel,width=10,textvariable=self.inputmode_value_sv)
        self.inputmode_value.grid(row=0,column=5)
        self.inputmode_value.focus_get()
        self.inputmode_value_sv.set("NORMAL")
    
        self.clipboard_size_label = Label(controlpanel,text="hlight pk",width=10)
        self.clipboard_size_label.grid(column=6,row=0,sticky=NSEW)
        self.clipboard_size_label.focus_get()
        
        self.clipboard_size_value_sv = StringVar()        
        self.clipboard_size_value= Entry(controlpanel,width=10,textvariable=self.clipboard_size_value_sv)
        self.clipboard_size_value.grid(row=0,column=7)
        self.clipboard_size_value.focus_get()
        self.clipboard_size_value_sv.set(0)
        
        self.clipboard_selected_label = Label(controlpanel,text="hlight pk",width=10)
        self.clipboard_selected_label.grid(column=8,row=0,sticky=NSEW)
        self.clipboard_selected_label.focus_get()
    
        self.clipboard_selected_value_sv = StringVar()        
        self.clipboard_selected_value= Entry(controlpanel,width=10,textvariable=self.clipboard_selected_value_sv)
        self.clipboard_selected_value.grid(row=0,column=9)
        self.clipboard_selected_value.focus_get()        
        self.clipboard_selected_value_sv.set(self.clipboard_selection)

        # buttoncontrolpanel
        buttoncontrolpanel = Frame(self)
        buttoncontrolpanel.grid(row=4,column=1,sticky=NSEW,pady=10,padx=10)
    
        self.dbload_button = Button(buttoncontrolpanel,command=self.load,text="dbload",name="dbl")
        self.dbload_button.grid(column=0,row=1,sticky=NSEW)
        self.dbload_button.focus_get()
    
        self.clear_button = Button(buttoncontrolpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(column=1,row=1,sticky=NSEW)
        self.clear_button.focus_get()
    
        self.dbinsert_button = Button(buttoncontrolpanel,command=self.insert,text="dbinsert",name="dbi")
        self.dbinsert_button.grid(column=2,row=1,sticky=NSEW)
        self.dbinsert_button.focus_get()
    
        self.dbsavechanges_button = Button(buttoncontrolpanel,command=self.process_updates,text="dbsavechgs",name="dbc")
        self.dbsavechanges_button.grid(column=3,row=1,sticky=NSEW)
        self.dbsavechanges_button.focus_get()
    
        self.clone_button = Button(buttoncontrolpanel,command=self.clone,text="clone",name="cln")
        self.clone_button.grid(column=4,row=1,sticky=NSEW)
        self.clone_button.focus_get()
    
        self.delrow_button = Button(buttoncontrolpanel,command=self.delrow,text="delrow",name="drw")
        self.delrow_button.grid(column=5,row=1,sticky=NSEW)
        self.delrow_button.focus_get()
    
        self.pagedown_button = Button(buttoncontrolpanel,
                                      command=lambda: self.pagescroll('down'),
                                      text="DOWN",name="pgd")
        self.pagedown_button.grid(row=1,column=6,sticky=NSEW)
        self.pagedown_button.focus_get()
    
        self.pageup_button = Button(buttoncontrolpanel,
                                    command=lambda: self.pagescroll('up'),
                                    text="UP",name="pgu")
    
        self.pageup_button.grid(row=1,column=7,sticky=NSEW)
        self.pageup_button.focus_get()
    
        self.pageleft_button = Button(buttoncontrolpanel,
                                      command=lambda: self.pagescroll('left'),
                                      text="LEFT",name="pgl")
        self.pageleft_button.grid(row=1,column=8,sticky=NSEW)
        self.pageleft_button.focus_get()
    
        self.pageright_button = Button(buttoncontrolpanel,
                                       command=lambda: self.pagescroll('right'),
                                       text="RIGHT",name="pgr")
        self.pageright_button.grid(row=1,column=9,sticky=NSEW)
        self.pageright_button.focus_get()
        
        self.hlightpk_button = Button(buttoncontrolpanel,width=1,command=self.delrow_show,
                                      text="PK",name="hlpk")
        self.hlightpk_button.grid(row=1,column=10,sticky=NSEW)
        self.hlightpk_button.focus_get()


        # new row  grid x label
        xlbl_widget_args=dict(width=10,font=font)
        xlbl_widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,xlbl_widget_args)
        
        mytruefalse = TrueFalse(name='truefalse')
        self.newrowgridxlabel = TkImageLabelGrid(self,'entrygridxlbl',mytruefalse,2,wmheight,
                                                0,0,self.maxrows,1,False,False,{},xlbl_widgetcfg)
        self.newrowgridxlabel.grid(row=5,column=0,rowspan=1,sticky=NS)
        
        for i in range(self.maxrows):
            self.newrowgridxlabel.widgets[i][0].sv.set(i+1)
            self.newrowgridxlabel.widgets[i][0]['style'] = 'InFocus.Label.TEntry'
            
        # new row grid
        self.maxnewrows=maxnewrowrows
        self.newrowgrid = TkImageLabelGrid(self,'newrowgrid',mytextalphanum,wmwidth,wmheight,
                             0,0,self.maxnewrows,self.maxcols,
                             False,False,{},widgetcfg)
        self.newrowgrid.grid(row=5,column=1,sticky=NSEW)
                
        self.grid_columnconfigure(0, weight=1, uniform="foo")
        self.grid_columnconfigure(1, weight=25, uniform="foo")
        self.grid_rowconfigure(0, weight=1, uniform="foo")
        self.grid_rowconfigure(1, weight=15,uniform="foo")
        self.grid_rowconfigure(5, weight=10, uniform="foo")
        
        
        buttoncontrolpanel.grid_rowconfigure(0, weight=1, uniform="foo")
        for i in range(10):
            buttoncontrolpanel.grid_columnconfigure(i, weight=1, uniform="foo")

        #controlpanel.grid_rowconfigure(0, weight=1, uniform="foo")
        #for i in range(7):
        #    controlpanel.grid_columnconfigure(i, weight=1, uniform="foo")          
          
    def delrow_show(self):
        
        l=[]
        for i in range(self.maxrows):
            if i <> 0:
                widget = self.entrygridxlabel.widgets[i][0]
                
                if widget['style'] == widget.style_on:
                    pk_id = self.pk_entry_sv.get()
                    pk_id_index = self.colnames.index(pk_id)
                    pkval = self.entrygrid.widgets[i-1][pk_id_index].sv.get()
                    l.append(pkval)
                
          
        self.hlightpk_text_sv.set(",".join(l))
        return(l)
                    
    
    def delrow(self):
        database = Database(self.dbname_entry_sv.get())
        
        for i in range(self.maxrows):
            if i <> 0:
                widget = self.entrygridxlabel.widgets[i][0]
                
                if widget['style'] == widget.style_on:
                    pk_id = self.pk_entry_sv.get()
                    pk_id_index = self.colnames.index(pk_id)
                    pkval = self.entrygrid.widgets[i-1][pk_id_index].sv.get()
                    
                    with database:
                        exec_str = tbl_row_delete(database,self.tblname_entry_sv.get(),
                                                                [[pk_id,"=","\""+pkval+"\""]])
    
                        self.lastquery_text_sv.set(exec_str)
                        
        self.clear()
        self.load()
        
    
    def deleteflagset(self,event=None):
        print self.focus_get()
        #print event.widget
        
    def pagescroll(self,direction):
        delta = int(self.scrolldelta_label_entry_sv.get())
        invdelta = int(delta*-1)
        
        if direction == "down":
            self.entrygrid.canvas.yview("scroll",delta,"units")
            self.entrygridxlabel.canvas.yview("scroll",delta,"units")
        elif direction == "up":
            self.entrygrid.canvas.yview("scroll",invdelta,"units")
            self.entrygridxlabel.canvas.yview("scroll",invdelta,"units")
        elif direction == "left":
            self.entrygrid.canvas.xview("scroll",invdelta,"units")
            self.entrygridylabel.canvas.xview("scroll",invdelta,"units")
        elif direction == "right":
            self.entrygrid.canvas.xview("scroll",delta,"units")
            self.entrygridylabel.canvas.xview("scroll",delta,"units")
            
        #self.entrygridxlabel.canvas.yview("scroll",10,"units")
        #self.entrygridxlabel.canvas.xview("scroll",10,"units")

        
    def pagedown(self):
        self.entrygrid.canvas.yview("scroll",10,"units")

        
    @logger(log)            
    def widget_current_values_get(self,gridname,rownum):
        return sswizard_utils.widget_current_values_get(self,gridname,rownum)
                 
    def update_callback(self,widget,new_value):
        
        sswizard_utils.update_callback(self,widget,new_value)
        
    @logger(log)        
    def clone(self):
        for y in range(self.maxcols):
            colname = self.entrygrid.widgets[0][y].sv.get()
            value = self.entrygrid.widgets[int(self.clone_entry_sv.get())][y].sv.get()
            
            if colname <> "" and colname.startswith("_") == False:
                self.newrowgrid.widgets[1][y].sv.set(value)
    
    '''def _clear_entrygrid(self):
        for x in range(self.maxrows):
            for y in range(self.maxcols):
                self.entrygrid.widgets[x][y].sv.set("")
                self.entrygrid.widgets[x][y].config(background='white')

    def _clear_newrowgrid(self,preserveheader=False):
        firstrow=0
        if preserveheader == True:
            firstrow=1
        for x in range(firstrow,self.maxnewrows):
            for y in range(self.maxcols):
                self.newrowgrid.widgets[x][y].sv.set("")
                self.newrowgrid.widgets[x][y].config(background='white')'''
    @logger(log)                    
    def _clear_grid(self,gridname,firstrow):
        grid = getattr(self,gridname)
        
        for key in self.updates.keys():
            row=[]
            _gridname,x,y = key.split(",")
            x = int(x)
            y = int(y)
            if gridname == _gridname:
                grid.widgets[x][y].sv.set("")
                grid.widgets[x][y].config(background='white')
                grid.widgets[x][y].init_value = ""
                grid.widgets[x][y].current_value = ""
                grid.widgets[x][y].version = 0    
            
        #for x in range(firstrow,grid.maxrows):
        #    for y in range(grid.maxcols):
        #        grid.widgets[x][y].sv.set("")
        #        grid.widgets[x][y].config(background='white')
        #        grid.widgets[x][y].init_value = ""
        #        grid.widgets[x][y].current_value = ""
        #        grid.widgets[x][y].version = 0
                
    @logger(log)        
    def clear(self,firstrow=0,gridname=None):
        if gridname == None:
            self._clear_grid('entrygrid',firstrow)
            self._clear_grid('newrowgrid',firstrow)
        else:
            self._clear_grid(gridname,firstrow)
        
        self.updates={}
            
    @logger(log)                    
    def focus_next_widget(self,event):
        #nextwidget = self.master.tk_focusNext()
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
    @logger(log)        
    def process_updates(self,database=None):

        if database == None:
            database = Database(self.dbname_entry_sv.get())
        
        pkcolnum = self.dbcol_defn.index(self.pk_entry_sv.get())
                  
        rows=[]
        
        if len(self.updates.keys()) == 0:
            log.log(thisfuncname(),3,"wierd","len(updates)=0")
            
        for key in self.updates.keys():
            row=[]
            gridname,x,y = key.split(",")
            
            # newrowgrid updates processed by insert; at some point
            # add a flag to grid constructor as to whether or not it
            # needs to put updates on the update queue
            if gridname == "entrygrid":
                colname = self.entrygrid.widgets[0][int(y)].sv.get()
                new_value,version = self.updates[key]
                
                # ignore any updates that are initial version (version=1)
                if int(x)==0:
                    init_value = getattr(self,gridname).widgets[0][int(y)].init_value
                    current_value = getattr(self,gridname).widgets[0][int(y)].current_value
                    #new_value = getattr(self,gridname).widgets[0][int(y)].sv.get()
    
                    if new_value <> current_value:
                        log.log(thisfuncname(),3,msg="update_required",y=y,x=x,colname=colname,key=key)
                        if init_value == "":
                            with database:
                                
                                try:
                                    tbl_col_add(database,
                                                self.tblname_entry_sv.get(),
                                                new_value)
                                    log.log(thisfuncname(),4,func=tbl_col_add,current_value=current_value,new_value=new_value)
                                    
                                    getattr(self,gridname).widgets[0][int(y)].version += 1 
                                except Exception,e:                            
                                    log.log(thisfuncname(),1,func=tbl_col_add,error=str(e))
                        else:
                            #try:
                                with database:
                                    tbl_col_update(database,
                                                   self.tblname_entry_sv.get(),
                                                   current_value,
                                                   new_value)
                                
                                    log.log(thisfuncname(),4,func=tbl_col_update,current_value=current_value,new_value=new_value)
                            #except Exception,e:               
                                #log.log(thisfuncname(),1,func=tbl_col_update,error=str(e))
                                
                        getattr(self,gridname).widgets[0][int(y)].current_value = new_value
                    else:
                        log.log(thisfuncname(),3,msg="ignoring as values have not changed",current_value=current_value,new_value=new_value)
                else:
                    pkval = self.entrygrid.widgets[int(x)][pkcolnum].sv.get()
                    
                    # ignore updates that are not different from init_value
                    # could be changed and then changed back or could be just inital load
                    
                    if str(new_value) <> str(self.entrygrid.widgets[int(x)][int(y)].current_value):

                        try:
                            new_value = int(new_value)
                        except:
                            new_value = "\""+new_value+"\""
            
                        _row= [colname,new_value,self.pk_entry_sv.get(),"\""+pkval+"\""]   
                        rows.append(_row)

                        log.log(thisfuncname(),3,msg="add to dbupdate queue",x=x,y=y,colname=colname,new_value=new_value,pkval=pkval)
        
                        self.entrygrid.widgets[int(x)][int(y)].current_value = new_value
                        self.entrygrid.widgets[int(x)][int(y)].version += 1

        with database:
            for row in rows:
                try:
                    exec_str,result = tbl_rows_update(database,self.tblname_entry_sv.get(),
                                                      row)
                    log.log(thisfuncname(),4,func=tbl_rows_update,exec_str=exec_str,result=str(result))
                except Exception,e:
                    log.log(thisfuncname(),1,func=tbl_rows_update,error=str(e))
                
    @logger(log)                       
    def insert(self,database=None):
        
        if database==None:
            database = Database(self.dbname_entry_sv.get())
        
        dbclass = dbtblfactory(self.tblname_entry_sv.get())

        for x in range(1,self.maxnewrows):
            dm={}
            emptyrow=True
            for y in range(self.maxcols):    
                colname = self.newrowgrid.widgets[0][y].sv.get()
                value = self.newrowgrid.widgets[x][y].sv.get()
                if colname <> "" and colname.startswith("_") == False:
                    if value <> "":
                        dm[colname] = value
                        emptyrow=False
                    
            if emptyrow == False:
                dbobj = dbclass.datamembers(database=database,dm=dm)

                with database:
                    
                    try:
                        exec_str,result = dbobj.persist()
                        log.log(thisfuncname(),4,func=dbobj.persist,exec_str=exec_str,result=result)
                    except Exception, e:
                        log.log(thisfuncname(),1,func=dbobj.persist,error=str(e))
                    
        #self.clear(1,'newrowgrid')
        self.load(afterinsert=True)
            
    @logger(log)        
    def load(self,afterinsert=False,values=None):
        
        colwidths = []
        
        if afterinsert==True:
            # we dont need to reload the headers as this an update of existing table
            self.clear(1)

        database = Database(self.dbname_entry_sv.get())
        whereclauses = []
        
        if self.pred1_entry_sv.get() <> "":
            
            whereclauses.append([self.pred1_entry_sv.get(),
                                 self.pred1_op_entry_sv.get(),
                                 self.predval1_entry_sv.get()])

            log.log(thisfuncname(),9,msg="where clause specified",whereclauses=whereclauses)
            
        if self.pred2_entry_sv.get() <> "":
            
            whereclauses.append([self.pred2_entry_sv.get(),
                                 self.pred2_op_entry_sv.get(),
                                 self.predval2_entry_sv.get()])

            log.log(thisfuncname(),9,msg="where clause specified",whereclauses=whereclauses)
            
        if self.pred3_entry_sv.get() <> "":
            
            whereclauses.append([self.pred3_entry_sv.get(),
                                 self.pred3_op_entry_sv.get(),
                                 self.predval3_entry_sv.get()])

            log.log(thisfuncname(),9,msg="where clause specified",whereclauses=whereclauses)

            
        with database:
            colndefn,rows,exec_str = tbl_rows_get(database,self.tblname_entry_sv.get(),"*",whereclauses)
            
            self.lastquery_text_sv.set(exec_str)
            self.lastquery_rowcount_text_sv.set(str(len(rows)))
            
            log.log(thisfuncname(),3,func=tbl_rows_get,msg=str(len(rows))+"rows loaded",table=self.tblname_entry_sv.get())
                                    
            for y in range(len(colndefn)):
        
                self.dbcol_defn.append(colndefn[y])
                
                new_value = colndefn[y]
                
                print y
                
                self.entrygrid.widgets[0][y].sv.set(new_value)
                self.entrygrid.widgets[0][y].current_value = new_value
                
                self.newrowgrid.widgets[0][y].sv.set(new_value)
                self.newrowgrid.widgets[0][y].current_value = new_value
                
                # reset init_value for headers after we have loaded   
                # so we can determine a new column from an updated column
                self.entrygrid.widgets[0][y].init_value = new_value
                self.newrowgrid.widgets[0][y].init_value = new_value
                
            print rows
            #for x in range(len(rows)):
            for x in range(self.maxrows-1): # 1 taken up for header
                for y in range(len(rows[x])):
                    
                    #try:
                    new_value = rows[x][y]
                    
                    # current widget
                    widget = self.entrygrid.widgets[x+1][y]
                    
                    # this is so the entry widgets can distinguish between
                    # nothing loaded and a space loaded
                    if new_value == "": new_value = "<SPACE>"
                    
                    # +1 to avoid the header row
                    widget.sv.set(new_value)
                    widget.current_value = new_value
                    
                    # and set the style back to not updated
                    widget['style'] = 'OutOfFocus.Notchanged.TEntry'
                    
                    try:
                        if len(str(new_value)) > colwidths[y]: 
                            colwidths[y]=len(str(new_value))
                            
                    except IndexError:
                        colwidths.append(len(str(new_value)))

        # after load store the column headers for easy lookup later
        self.colnames = colndefn
        
        for i in range(len(colwidths)):
            self.entrygrid.canvasframe.grid_columnconfigure(i,weight=colwidths[i],uniform="foo")
            self.newrowgrid.canvasframe.grid_columnconfigure(i,weight=colwidths[i],uniform="foo")

    @logger(log)        
    def updates_get(self,gridname,ignoreaxes=False):
        
        return(sswizard_utils.updates_get(self,gridname,ignoreaxes))
    
if __name__ == "__main__":

    app = DBTableUI(maxentryrows=75, maxnewrowrows=10)
    app.mainloop()
