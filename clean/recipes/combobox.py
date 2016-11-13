import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from Tkinter import *
from ttk import *

master = Tk()

sv = StringVar()

c = Combobox(master,values=['A','B','C'],textvariable=sv)
c.pack(side=LEFT,fill=BOTH,expand=True)

c.current(0)

c.config(values=['D','E','F'])

sv.set("")

master.mainloop()
