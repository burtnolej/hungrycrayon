from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from Tkinter import Entry as Tkentry
from ttk import *
import tkFont
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from ui_utils import  geometry_get, tkwidgetfactory, geometry_get_dict


class Validator(object):
    def __init__(self,name,**kwargs): 
        self.name = name
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
        
    def __call__(self,value):
        print "validating rule",self.name
        return(self.validate(value))
        
    def validate(self,value):
        if hasattr(self,'lbound'):
            if int(value) < self.lbound:
                return False

        if hasattr(self,'ubound'):
            if int(value) > self.ubound:
                return False
        return True
    
class TkValidEntry(object):
    
    def __init__(self,master,name,width,default,
                 widgettype):
        
        self.validators = []
        
        self.frame = Frame(master)
 
        self.label = Tklabel(self.frame,
                             text=name,
                             width=width,
                             anchor=W,
                             justify=LEFT)
        
        self.label.pack(side=LEFT,padx=5,pady=5,
                        fill=BOTH,expand=1)
        
        sv = StringVar()
        self.sv = sv
        self.entry= tkwidgetfactory(widgettype,
                                    self.frame,
                                    textvariable=self.sv,
                                    width=15,
                                    x=100)
        self.sv.set(default)
        self.entry.pack(side=LEFT,padx=5,pady=5,fill=BOTH,expand=1)
        
        #self.entry.bind("<Tab>",self.focus_next_widget)

        self.entry.bind("<FocusIn>",self.select_all)

        sv.trace("w",lambda name, index, mode, 
                 sv=self.sv: self.validate())
        
        self.statuslabel = Tklabel(self.frame,
                                  text=self.validators_get(),
                                  width=1,
                                  anchor=W,
                                  background='lightblue',
                                  justify=LEFT)
        
        self.statuslabel.pack(side=LEFT,padx=5,pady=5,
                             fill=BOTH,expand=1)
        
        self.ruleslabel = Tklabel(self.frame,
                                  text=self.validators_get(),
                                  width=16,
                                  anchor=W,
                                  justify=LEFT)
        
        self.ruleslabel.pack(side=LEFT,padx=5,pady=5,
                             fill=BOTH,expand=1)

        self.validate()
        
    def grid(self,**kwargs):
        self.frame.grid(**kwargs)
        
    def validators_get(self):
        return([v.name for v in self.validators])
    
    def register_validator(self,validator):
        self.validators.append(validator)
        self.ruleslabel.config(text=validator.name)
        self.validate()
        
    def validate(self):
        print "validate"
        for validator in self.validators:
            
            if validator(self.sv.get()) == True:
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