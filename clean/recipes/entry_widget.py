from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from Tkinter import Entry as Tkentry
from ttk import *

from re import findall

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate

from ui_utils import TkImageWidget, TkImageLabelGrid, geometry_get, font_scale, \
     tkwidgetfactory, geometry_get_dict, tkwidgetimage_set, fontscale
import tkFont

defaultmaster = dict(height=300,width=600,
                     x=100,y=100)



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

class TkentryPanel(Frame):
    
    def __init__(self,master,**kwargs):
        Frame.__init__(master,**kwargs)
        
    
        
    
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

class TkCombobox(object):
    
    def __init__(self,master,values):
        
        self.frame = Frame(master)
        self.frame.pack()
        self.sv=StringVar()
        self.values = values

        self.combo = Combobox(self.frame,
                          values=self.values,
                          textvariable=self.sv)
        self.combo.pack(side=LEFT,expand=1,fill=Y)
        
        self.label = Tklabel(self.frame,
                             text=len(self.values))
        self.label.pack(side=LEFT,expand=1,fill=Y)

        self.sv.trace("w",lambda name, index, mode, 
                  sv=self.sv: self.complete())
        
    def complete(self):
        input = self.sv.get()
        if input <> "":
            hits = rematch(input,self.values)
            
            if len(hits) == 1:
                self.update(hits)
                self.sv.set(hits[0])
            elif len(hits)>1:
                self.update(hits)
                #self.config(values=hits)
                #current = self.sv.get()
                #self.sv.set("{0} ({1})".format(current,str(len(hits))))
                #master.event_generate("<Down>")
                #combo.focus_force()
            else:
                self.update(self.values)
                #self.config(values=self.values)
        else:
            self.update(self.values)
            
                
    def update(self,newvalues):
        self.combo.config(values=newvalues)
        self.label.config(text=len(newvalues))
        
        
        
    
def rematch(expr,list):
    
    r = re.compile(expr)
        
    match = []
    for item in list:
        results = r.findall(item.lower())
        if len(results) > 0:
            match.append(item)
            
    match.sort()
    return(match)
                 

if __name__ == "__main__":       
  
    def complete():
        if sv.get() <> "":
    
            hits=[]
            for v in values:
                if v.startswith(sv.get()):
                    hits.append(v)
            if len(hits) == 1:
                sv.set(hits[0])
            elif len(hits)>1:
                combo.config(values=hits)
                #master.event_generate("<Down>")
                #combo.focus_force()
            else:
                combo.config(values=values)
                
    master = Tk()  
    values=['pineapple','grapefruit','banana',
            'peach','pomegranate','passionfruit',
            'pear','grape','strawberry','raspberry',
            'rhubarb','mango','guava']
    sv=StringVar()
    combo = Combobox(master,
                     #choices=['a','b','c'],
                     values=values,
                     textvariable=sv)
    sv.trace("w",lambda name, index, mode, 
              sv=sv: complete())

    def printme():
        print "me"
    
    combo.pack(expand=1,fill=BOTH)
    master.mainloop()
    
