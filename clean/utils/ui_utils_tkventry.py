from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
#from Tkinter import Entry as Tkentry
from ttk import *
import tkFont
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from ui_utils import  geometry_get, tkwidgetfactory, geometry_get_dict
from type_utils import isadatatype
    
class TkValidEntry(object):
    
    def __init__(self,master,name,width,default,var):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        self.frame = Frame(master)
        self.var = var
        self.label = Tklabel(self.frame,
                             text=name,
                             width=width,
                             anchor=W,
                             justify=LEFT)
        
        self.label.pack(side=LEFT,padx=5,pady=5,fill=BOTH,expand=1)
        
        sv = StringVar()
        self.sv = sv
        '''self.entry= tkwidgetfactory(self.var.widgettype,
                                    self.frame,
                                    textvariable=self.sv,
                                    width=15,
                                    x=100)'''
        
        self.entry= tkwidgetfactory(self.var,
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
                                   text='',
                                   width=1,
                                   anchor=W,
                                   background='lightblue',
                                   justify=LEFT)
        
        self.statuslabel.pack(side=LEFT,padx=5,pady=5,
                             fill=BOTH,expand=1)
        
        self.ruleslabel = Tklabel(self.frame,
                                  text=self.var.name(),
                                  width=16,
                                  anchor=W,
                                  justify=LEFT)
        
        self.ruleslabel.pack(side=LEFT,padx=5,pady=5,
                             fill=BOTH,expand=1)

        self.validate()
        
    def grid(self,**kwargs):
        self.frame.grid(**kwargs)
        
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
  
class TkEntry(Entry):
    def __init__(self,master,var,**kwargs):
        Entry.__init__(self,master,**kwargs)
        
class TkCombobox(object):
    
    def __init__(self,master,var):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        self.frame = Frame(master)
        self.frame.pack(side=LEFT)
        self.sv=StringVar()
        self.values = var.set

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
            hits = self.rematch(input,self.values)
            
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
        print "update",newvalues
        self.combo.config(values=newvalues)
        self.label.config(text=len(newvalues))
        
    def rematch(self,expr,list):
        
        r = re.compile(expr)
            
        match = []
        for item in list:
            results = r.findall(item.lower())
            if len(results) > 0:
                match.append(item)
                
        match.sort()
        return(match)
    
    def config(self,**kwargs):
        self.combo.config(**kwargs)
        
    def pack(self,**kwargs):
        self.combo.pack(**kwargs)
        
    def bind(self,*args,**kwargs):
        self.combo.bind(*args,**kwargs)
        
    def focus_set(self,*args,**kwargs):
        self.combo.focus_set(*args,**kwargs)
        