import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNum
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get
from misc_utils import nxnarraycreate

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, \
     tbl_rows_update, dbtblfactory

from Tkinter import *
from ttk import *
import tkFont

class DBTableUI(Frame):
    def __init__(self,master):

        self.lastsaveversion=0
        
        # any children that change update this 
        # key is the name and value is the new val
        # the name is likely to be the tkwidgetid.x,y
        self.updates = {}
        
        # dbm columns are added here as they are loaded
        # .index+1 will give the col # on the grid that corresponds
        # useful for looking up pk values for updates
        self.dbcol_defn = []
        
        self.master = master
        self.maxrows=30 # rows in the grid
        self.maxcols=12 # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*20 # master height
        wmwidth=wwidth*20 # master width 

        #geom = geometry_get(wmheight,wmwidth,0,0)
        #self.master.geometry(self.geom)
        
        #master.geometry(geom)
        
        Frame.__init__(self,master)
        #master.bind("<Prior>",self.focus_next_widget)
        self.bind("<Prior>",self.focus_next_widget)
        self.grid()

        widget_args=dict(background='white')
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        #rowcfg = dict(height=2,width=2,text="x")
        #colcfg = dict(height=2,width=2,text="y")

        mytextalphanum = TextAlphaNum(name='textalphanum')

        #self.entrygrid = TkImageLabelGrid(self.master,mytextalphanum,wmwidth,wmheight,
        self.entrygrid = TkImageLabelGrid(self,mytextalphanum,wmwidth,wmheight,
                             0,0,self.maxrows,self.maxcols,
                             {},widgetcfg)
                             #{},widgetcfg,1,1,rowcfg,colcfg)
        self.entrygrid.grid(row=0,sticky=NSEW)

        controlpanel = Frame(master)
        controlpanel.grid(row=1,sticky=NSEW)
                
        self.dbname_label = Label(controlpanel,text="database")
        self.dbname_label.grid(column=0,row=0,sticky=NSEW)
        self.dbname_label.focus_get()
        
        self.dbname_entry_sv = StringVar()
        self.dbname_entry = Entry(controlpanel,textvariable=self.dbname_entry_sv)
        self.dbname_entry.grid(column=1,row=0,sticky=NSEW)
        self.dbname_entry.focus_get()
        self.dbname_entry_sv.set("htmlparser")

        self.tblname_label = Label(controlpanel,text="table")
        self.tblname_label.grid(column=2,row=0,sticky=NSEW)
        self.tblname_label.focus_get()
        
        self.tblname_entry_sv = StringVar()
        self.tblname_entry = Entry(controlpanel,textvariable=self.tblname_entry_sv)
        self.tblname_entry.grid(column=3,row=0,sticky=NSEW)
        self.tblname_entry.focus_get()
        self.tblname_entry_sv.set("lesson")
        
        self.clone_label = Label(controlpanel,text="clone id")
        self.clone_label.grid(column=4,row=0,sticky=NSEW)
        self.clone_label.focus_get()
        
        self.clone_entry_sv = StringVar()
        self.clone_entry = Entry(controlpanel,textvariable=self.clone_entry_sv)
        self.clone_entry.grid(column=5,row=0,sticky=NSEW)
        self.clone_entry.focus_get()
        self.clone_entry_sv.set(1)
        
        self.pkentry_label = Label(controlpanel,text="pk")
        self.pkentry_label.grid(column=6,row=0,sticky=NSEW)
        self.pkentry_label.focus_get()
        
        self.pk_entry_sv = StringVar()
        self.pk_entry = Entry(controlpanel,textvariable=self.pk_entry_sv)
        self.pk_entry.grid(column=7,row=0,sticky=NSEW)
        self.pk_entry.focus_get()
        self.pk_entry_sv.set("__id")
  

        self.dbload_button = Button(controlpanel,command=self.load,text="dbload",name="dbl")
        self.dbload_button.grid(column=0,row=1,columnspan=1,sticky=NSEW)
        self.dbload_button.focus_get()

        self.clear_button = Button(controlpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(column=2,row=1,columnspan=1,sticky=NSEW)
        self.clear_button.focus_get()
        
        self.dbinsert_button = Button(controlpanel,command=self.insert,text="dbinsert",name="dbi")
        self.dbinsert_button.grid(column=3,row=1,columnspan=1,sticky=NSEW)
        self.dbinsert_button.focus_get()
        
        self.dbsavechanges_button = Button(controlpanel,command=self.update,text="dbsavechgs",name="dbc")
        self.dbsavechanges_button.grid(column=4,row=1,columnspan=1,sticky=NSEW)
        self.dbsavechanges_button.focus_get()

        self.clone_button = Button(controlpanel,command=self.clone,text="clone",name="cln")
        self.clone_button.grid(column=5,row=1,columnspan=1,sticky=NSEW)
        self.clone_button.focus_get()
        
        self.newrowgrid = TkImageLabelGrid(self.master,mytextalphanum,wmwidth,wmheight,
                             0,0,2,self.maxcols,
                             {},widgetcfg)
                             #{},widgetcfg,1,1,rowcfg,colcfg)
        self.newrowgrid.grid(row=2,sticky=NSEW)

                
        self.master.grid_columnconfigure(0, weight=1, uniform="foo")
        self.master.grid_rowconfigure(0, weight=1, uniform="foo")
            
            
    def clone(self):
        for y in range(self.maxcols):
            colname = self.entrygrid.widgets[0][y].sv.get()
            value = self.entrygrid.widgets[int(self.clone_entry_sv.get())][y].sv.get()
            
            if colname <> "" and colname.startswith("_") == False:
                self.newrowgrid.widgets[1][y].sv.set(value)
    
    def clear(self):
        
        for x in range(self.maxrows):
            for y in range(self.maxcols):
                self.entrygrid.widgets[x][y].sv.set("")
                self.entrygrid.widgets[x][y].config(background='white')

                
        for x in range(self.maxrows):
            for y in range(self.maxcols):
                self.newrowgrid.widgets[x][y].sv.set("")
                self.newrowgrid.widgets[x][y].config(background='white')

                
    def focus_next_widget(self,event):
        print "focuschange"
        #nextwidget = self.master.tk_focusNext()
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
    def update(self):
        
        database = Database(self.dbname_entry_sv.get())
        
        pkcolnum = self.dbcol_defn.index(self.pk_entry_sv.get())
                  
        rows=[]
        for key in self.updates.keys():
            row=[]
            x,y = key.split(",")
            colname = self.newrowgrid.widgets[0][int(y)].sv.get()
            
            if int(x)==0:
                # table column alter
                print "alter",colname,
                
                current_value = self.entrygrid.widgets[0][int(y)].sv.get()
                
                try:
                    self.dbcol_defn.index(current_value)
                except:
                    print "add"
            else:
                pkval = self.entrygrid.widgets[int(x)][pkcolnum].sv.get()
                
                value = self.updates[key]
                try:
                    value = int(value)
                except:
                    value = "\""+value+"\""
    
                rows.append([colname,
                             value,
                             self.pk_entry_sv.get(),
                             "\""+pkval+"\""])
            
        print rows
        with database:
            tbl_rows_update(database,
                            self.tblname_entry_sv.get(),
                            rows)
                                   
    def insert(self):
        database = Database(self.dbname_entry_sv.get())
        
        dbclass = dbtblfactory(self.tblname_entry_sv.get())
        
        #class lesson(dbtblgeneric):
        #    pass
        
        dm={}
        for y in range(self.maxcols):
            colname = self.newrowgrid.widgets[0][y].sv.get()
            value = self.newrowgrid.widgets[1][y].sv.get()
            if colname <> "" and colname.startswith("_") == False:
                dm[colname] = value
                
        dbobj = dbclass.datamembers(database=database,dm=dm)        

        with database:
            dbobj.persist()
            
    def load(self,values=None):

        database = Database(self.dbname_entry_sv.get())
        
        with database:
            colndefn,rows = tbl_rows_get(database,self.tblname_entry_sv.get())
                                    #saveversion',str(self.dbload_entry_sv.get())))
                                    
            for y in range(len(rows[0])):
        
                self.dbcol_defn.append(colndefn[y])
                
                new_value = colndefn[y]
                
                self.entrygrid.widgets[0][y].init_value = new_value
                self.entrygrid.widgets[0][y].current_value = new_value

                self.entrygrid.widgets[0][y].sv.set(new_value)
                self.entrygrid.widgets[0][y].config(background='grey',
                                                    foreground='yellow')
                
                self.newrowgrid.widgets[0][y].sv.set(new_value)
                self.newrowgrid.widgets[0][y].config(background='grey',
                                                    foreground='yellow')
                
            
            for x in range(len(rows)):
                for y in range(len(rows[x])):
                    try:
                        new_value = rows[x][y]
                        
                        # this is so the entry widgets can distinguish between
                        # nothing loaded and a space loaded
                        if new_value == "": new_value = "<SPACE>"
                        
                        # +1 to avoid the header row
                        self.entrygrid.widgets[x+1][y].init_value = new_value
                        self.entrygrid.widgets[x+1][y].current_value = new_value
                        self.entrygrid.widgets[x+1][y].sv.set(new_value)
                        
                    except:
                        pass
                
if __name__ == "__main__":
    master = Tk()
    
    
    
    ui = DBTableUI(master)

    master.mainloop()