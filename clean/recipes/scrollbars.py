import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from ui_utils import TkImageLabelGrid, geometry_get_dict, geometry_get

from Tkinter import *
from ttk import *

master = Tk()
geom = geometry_get(200,200,0,0)

master.geometry(geom) 

class ScrollingCanvas(Frame):
    
    def __init__(self):
        Frame.__init__(self,master)
        canvas = Canvas(master)
        frame = Frame(canvas)

        yscrollbar = Scrollbar(master,orient="vertical",command=canvas.yview)
        yscrollbar.pack(side='right',fill='y')       
        canvas.configure(yscrollcommand=yscrollbar.set)
        
        hscrollbar = Scrollbar(master,orient="horizontal",command=canvas.xview)
        hscrollbar.pack(side='bottom',fill='x')        
        canvas.configure(yscrollcommand=yscrollbar.set,xscrollcommand=hscrollbar.set)

        canvas.pack(side="left",fill="both",expand=True)
        canvas.create_window((4,4),window=frame,anchor="nw",tags="frame")
        
        button = Button(frame,text="topleft")
        button.grid(row=0,column=0,sticky=NSEW)
        button = Button(frame,text="topright")
        button.grid(row=0,column=1,sticky=NSEW)
        button = Button(frame,text="bottonleft")
        button.grid(row=1,column=0,sticky=NSEW)
        button = Button(frame,text="bottomright")
        button.grid(row=1,column=1,sticky=NSEW)
        button = Button(frame,text="topleft")
        button.grid(row=2,column=0,sticky=NSEW)
        button = Button(frame,text="topright")
        button.grid(row=3,column=0,sticky=NSEW)
        button = Button(frame,text="bottonleft")
        button.grid(row=4,column=0,sticky=NSEW)
        button = Button(frame,text="bottomright")
        button.grid(row=1,column=1,sticky=NSEW)
        
sc = ScrollingCanvas()
sc.pack(side='top',fill="both",expand=True)
sc.mainloop()