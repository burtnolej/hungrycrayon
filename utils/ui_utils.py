import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
import Tkinter as tk
import tkFont

master = tk.Tk()
inputfm = tk.Frame(master)
gridfm = tk.Frame(master)

nextgridrow=2

from xml_utils import get_xml_elements,get_xml_element,get_xml_child_elements, get_xml_root
    
def invoke(frame,funcname):
    i=1
    kwargs={}
    for key,widget in inputwid.iteritems():
        val=widget.get("1.0",tk.END).strip()
        kwargs[key] = val

        i=i+1
    print funcname,kwargs
    
    
    funcname(kwargs)

elements = get_xml_elements(sys.argv[1],".//element")
row=1

inputwid={}

db=get_xml_elements(sys.argv[1],".//db")[0].text
table=get_xml_elements(sys.argv[1],".//table")[0].text
execfunc=get_xml_elements(sys.argv[1],".//execfunc")[0].text

for element in elements:
    label = get_xml_child_elements(element)['label']
    width = get_xml_child_elements(element)['width']
    
      
    if get_xml_child_elements(element)['uitype'] == 'input':
        dbcolumn = get_xml_child_elements(element)['dbcolumn']
        default = get_xml_child_elements(element)['default']
        _label = tk.Label(inputfm,text=label,width=width,height=2)
        _label.grid(row=row,column=1,sticky=tk.E)
        _text = tk.Text(inputfm,width=width,height=2)
        _text.grid(row=row,column=2,sticky=tk.W)
        _text.insert(tk.END,default)
        inputwid[dbcolumn]=_text
       
    elif get_xml_child_elements(element)['uitype'] == 'button':
        _button = tk.Button(inputfm,text=label,width=width,height=2,\
                            command=lambda: invoke(gridfm,execfunc))        
        _button.grid(row=row,column=1,sticky=tk.S)
        
    row=row+1

i=1
for key in inputwid.keys():
    _label = tk.Label(gridfm,text=key,width=width,height=2)
    _label.grid(row=1,column=i,sticky=tk.E)
    i = i+1
    
inputfm.grid(row=1,column=1,sticky=tk.W)
gridfm.grid(row=1,column=2,sticky=tk.N)

master.mainloop()