

from Tkinter import *
#from ttk import *


def pagescroll():
    delta = 10
    
    print "croll"
    canvas.yview("scroll",delta,"units")
            
class Grid(Frame):
    
    def __init__(self,maxx,maxy,name,**config):
        Frame.__init__(self,master)
        
        self.canvas = Canvas(self, bg = 'pink')
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)
        
        self.canvasframe = Frame(self.canvas, bg = 'purple')
        self.canvasframe.pack(side = LEFT, fill = BOTH, expand = True)
        
        self.canvas_frame = self.canvas.create_window((0,0),window=self.canvasframe,anchor=NW)
        
        mail_scroll = Scrollbar(self.canvas, orient = "vertical", command = self.canvas.yview)
        #mail_scroll.pack(side = RIGHT, fill = Y)
        
        self.canvas.config(yscrollcommand = mail_scroll.set)
        
        self.canvasframe.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind('<Configure>', self.FrameWidth)


        for x in range(maxx):
            for y in range(maxy):
                b = Button(self.canvasframe,text="")
                b.grid(row=x,column=y,sticky=NSEW)
                b.config(**config)

                
        for x in range(maxx):
            self.canvasframe.grid_rowconfigure(x,weight=1,uniform=name)
            
        for y in range(maxy):   
            self.canvasframe.grid_columnconfigure(y,weight=1,uniform=name)            

    def FrameWidth(self,event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
    
    def OnFrameConfigure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
master = Tk()
master.geometry("1000x1000+0+0")

uicolhdr = Grid(1,1,"uicolhdr",background="yellow")
uicolhdr.grid(row=0,sticky=NSEW)

uiohdr = Grid(1,1,"uirowhdr",background="yellow")
uiohdr.grid(row=0,column=1,sticky=NSEW)

uirowhdr = Grid(10,1,"uirowhdr",background="lightgreen")
uirowhdr.grid(row=1,column=1,rowspan=2,sticky=NSEW)

uitop = Grid(26,1,"uitop",background="lightgreen")
uitop.grid(row=1,sticky=NSEW)
uibottom = Grid(28,1,"uibottom",background="lightblue")
uibottom.grid(row=2,sticky=NSEW)

#master.grid_rowconfigure(0,weight=1,uniform='foo2')
master.grid_rowconfigure(1,weight=1,uniform='foo')
master.grid_rowconfigure(2,weight=1,uniform='foo')
master.grid_columnconfigure(0,weight=100,uniform='foo')
master.grid_columnconfigure(1,weight=1,uniform='bar')

master.mainloop()