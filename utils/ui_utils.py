import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
import Tkinter as tk
import tkFont

master = tk.Tk()

from xml_utils import get_xml_elements,get_xml_element,get_xml_child_elements, get_xml_root

# for each database in the schema file
elements = get_xml_elements(sys.argv[1],".//element")
row=1
for element in elements:
    label = get_xml_child_elements(element)['label']
    width = get_xml_child_elements(element)['width']
    label = get_xml_child_elements(element)['label']
            
    if get_xml_child_elements(element)['uitype'] == 'input':
        _label = tk.Label(master,text=label,width=width,height=2)
        _label.grid(row=row,column=1,sticky=tk.E)
        _text = tk.Text(master,width=width,height=2)
        _text.grid(row=row,column=2,stick=tk.W)
        row=row+1
        
master.mainloop()