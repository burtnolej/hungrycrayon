from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
#from Tkinter import Entry as Tkentry
from ttk import *
import tkFont
import sys
from ui_utils import  geometry_get, tkwidgetfactory, geometry_get_dict
from type_utils import isadatatype
    
class BaseTkValidEntry(Frame):
    
    def __init__(self,master,name,width,default,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        Frame.__init__(self,master)
        self.var = var
        
        sv = StringVar()
        self.sv = sv
        
        self.entry= tkwidgetfactory(self.var,self,textvariable=self.sv,**kwargs)
        
        self.sv.set(default)
        self.entry.grid()
        
        sv.trace("w",lambda name, index, mode, sv=self.sv: self.validate())
        
        self.entry.bind("<FocusIn>",self.select_all)
        
        self.set_callbacks()
        
        self.s = Style()
        
    def validate(self):
        
        if self.var(self.sv.get()) == True:
            
            self.s.configure('TCombobox',background='green')
            self['style']='TCombobox'
            
            return

        self.s.configure('TCombobox',background='red')
        self['style']='A.TCombobox'

    def select_all(self,event):       
        event.widget.selection_range(0,END)
        return("break")
    
class TkValidEntry(BaseTkValidEntry):    
    
    def __init__(self,master,name,width,default,var):
        
        BaseTkValidEntry.__init__(self,master,name,width,default,var)
        
        self.label = Tklabel(self,text=name,width=width,anchor=W,justify=LEFT)
        
        self.label.grid(row=0,column=0,sticky=NSEW)
        
        self.statuslabel = Tklabel(self,text='',width=1,anchor=W,background='lightblue',justify=LEFT)
        
        self.statuslabel.grid(row=0,column=2,sticky=NSEW)
        
        self.ruleslabel = Tklabel(self,text=self.var.name(),width=16,anchor=W,justify=LEFT)

        self.ruleslabel.grid(row=0,column=3,sticky=NSEW)

        self.grid_rowconfigure(0, weight=1, uniform="foo")
        
    def validate(self):
        
        print "validate"
        if self.var(self.sv.get()) == True:
            self.statuslabel.config(background='lime')
            return
            
        self.statuslabel.config(background='pink')
        
    def focus_next_widget(self,event):
        nextwidget = event.widget.tk_focusNext()
        nextwidget.focus()        
        nextwidget.selection_range(0,END)
        return("break")
    
    def select_all(self,event):       
        event.widget.selection_range(0,END)
        return("break")
