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
                     x=100,y=1


                 

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
    
