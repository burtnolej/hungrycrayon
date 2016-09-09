import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNum
from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get
from misc_utils import nxnarraycreate

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get

from Tkinter import *
from ttk import *
import tkFont

class DBTableUI(object):
    def __init__(self,master):

        self.lastsaveversion=0
        
        self.master = master
        self.maxrows=30 # rows in the grid
        self.maxcols=10 # cols in the grid
        maxwidgets=self.maxrows*self.maxcols
        wwidth=48 # default button width with text of 3 chars
        wheight=29 # default button height
        wmheight=wheight*self.maxrows # master height
        wmwidth=wwidth*10 # master width 

        geom = geometry_get(wmheight,wmwidth,0,0)
        #self.master.geometry(self.geom)
        
        master.geometry(geom)
        master.bind("<Prior>",self.focus_next_widget)

        widget_args=dict(background='white')
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        #rowcfg = dict(height=2,width=2,text="x")
        #colcfg = dict(height=2,width=2,text="y")

        mytextalphanum = TextAlphaNum(name='textalphanum')

        self.entrygrid = TkImageLabelGrid(self.master,mytextalphanum,wmwidth,wmheight,
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

        self.dbload_button = Button(controlpanel,command=self.load,text="dbload",name="dbl")
        self.dbload_button.grid(column=0,row=1,columnspan=2,sticky=NSEW)
        self.dbload_button.focus_get()
        
        self.clear_button = Button(controlpanel,command=self.clear,text="clear",name="clr")
        self.clear_button.grid(column=2,row=1,columnspan=2,sticky=NSEW)
        self.clear_button.focus_get()    
                
        self.master.grid_columnconfigure(0, weight=1, uniform="foo")
        self.master.grid_rowconfigure(0, weight=1, uniform="foo")
            
    def clear(self):
        
        for x in range(self.maxrows):
            for y in range(self.maxcols):
                self.entrygrid.widgets[x][y].sv.set("")
                
    def focus_next_widget(self,event):
        print "focuschange"
        #nextwidget = self.master.tk_focusNext()
        if str(event.widget)[-3:] == "svb":
            self.entrygrid.focus()
        else:
            self.save_button.focus_set()
        return("break")
    
    def load(self,values=None):

        database = Database(self.dbname_entry_sv.get())
        
        with database:
            colndefn,rows = tbl_rows_get(database,self.tblname_entry_sv.get())
                                    #saveversion',str(self.dbload_entry_sv.get())))
            
            for x in range(len(rows)):
                for y in range(len(rows[x])):
                    try:
                        self.entrygrid.widgets[x][y].sv.set(rows[x][y])
                    except:
                        pass
                
if __name__ == "__main__":
    master = Tk()
    
    
    
    ui = DBTableUI(master)

    master.mainloop()