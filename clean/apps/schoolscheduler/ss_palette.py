from misc_utils_log import Log, logger
from misc_utils import thisfuncname
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,pidlogname=True,proclogname=False)
from Tkinter import *
from Tkinter import Label as tklabel
from Tkinter import Entry as tkentry
from Tkinter import Frame as tkframe
from Tkinter import Button as tkbutton
from ttk import *
import tkFont

class FontPickerFrame(Frame):
    
    def __init__(self,master,error_sv,text,family="Helvetica",pointsize="12",weight="normal"):
        Frame.__init__(self,master)
        
        self.error_sv = error_sv
        
        rgb_label = Label(self,text=text,anchor=CENTER)
        rgb_label.grid(row=0,column=0,columnspan=2,pady=2)
    
        family_label = Label(self,text="Family",anchor=W)
        family_label.grid(row=1,column=0,sticky=E)
        self.family_entry_sv = StringVar()
        family_entry = Combobox(self,width=13,textvariable=self.family_entry_sv,
                                 values=tkFont.families())
        family_entry.grid(row=1,column=1,sticky=W,pady=2,padx=4)
        self.family_entry_sv.set(family)
        
        pointsize_label = Label(self,text="Pointsize")
        pointsize_label.grid(row=2,column=0,sticky=E)
        self.pointsize_entry_sv = StringVar()
        pointsize_entry = Entry(self,textvariable=self.pointsize_entry_sv,width=3)
        pointsize_entry.grid(row=2,column=1,sticky=W,pady=2,padx=4)
        self.pointsize_entry_sv.set(pointsize)
        
        weight_label = Label(self,text="Font",anchor=E,justify=RIGHT)
        weight_label.grid(row=3,column=0,sticky=E,pady=6)
        self.weight_entry_sv = StringVar()
        weight_entry = Combobox(self,width=13,textvariable=self.weight_entry_sv,values=["bold","italic","normal"])
        weight_entry.grid(row=3,column=1,sticky=W,padx=4)
        self.weight_entry_sv.set(weight)
        
        self.weight_entry_sv.trace("w",lambda name,index,mode,sv=self.weight_entry_sv:self.onchange())
        self.pointsize_entry_sv.trace("w",lambda name,index,mode,sv=self.pointsize_entry_sv:self.onchange())
        self.family_entry_sv.trace("w",lambda name,index,mode,sv=self.family_entry_sv:self.onchange())
        
        self.grid_columnconfigure(0,weight=1,uniform="foo")
        self.grid_columnconfigure(1,weight=2,uniform="foo")

        for i in range(4):
            self.grid_rowconfigure(i,weight=1,uniform="foo")
    
    @logger(log)
    def onchange(self):
        
        try:
            self.msg_label_sv.set("")
        except:
            pass
        
        try:
            font = tkFont.Font(family=self.family_entry_sv.get(),
                               size=self.pointsize_entry_sv.get(),
                               weight=self.weight_entry_sv.get()) 
            self.pick_widget.config(font=font)
            
            log.log(thisfuncname(),3,msg="updating font",font=font)
            return 0
        except Exception,e:
            self.error_sv.set(e)    
            
class RGBPickerFrame(Frame):
    def __init__(self,master,config,error_sv,text,r=0,g=0,b=0,labels=True):
        Frame.__init__(self,master)     

        self.error_sv = error_sv
        self.config = config
        
        rgb_label = Label(self,text=text,anchor=CENTER)
        rgb_label.grid(row=0,column=0,columnspan=2,pady=2)  
        
        _column=0
        if labels==True:
            red_label = Label(self,text="Red")
            red_label.grid(row=1,column=0,sticky=E)
            _column=1

        self.red_entry_sv = StringVar()
        red_entry = Entry(self,textvariable=self.red_entry_sv,width=3)
        red_entry.grid(row=1,column=_column,sticky=NS,pady=2)
        self.red_entry_sv.set(r)

        if labels==True: 
            green_label = Label(self,text="Green")
            green_label.grid(row=2,column=0,sticky=E)
            _column=1
        
        self.green_entry_sv = StringVar()
        green_label = Entry(self,textvariable=self.green_entry_sv,width=3)
        green_label.grid(row=2,column=_column,sticky=NS,pady=2)
        self.green_entry_sv.set(g)
        
        if labels==True: 
            blue_label = Label(self,text="Blue")
            blue_label.grid(row=3,column=0,sticky=E)
            _column=1
        
        self.blue_entry_sv = StringVar()
        blue_label = Entry(self,textvariable=self.blue_entry_sv,width=3)
        blue_label.grid(row=3,column=_column,sticky=NS,pady=4)
        self.blue_entry_sv.set(b)

        self.red_entry_sv.trace("w",lambda name,index,mode,sv=self.red_entry_sv:self.onchange())
        self.green_entry_sv.trace("w",lambda name,index,mode,sv=self.green_entry_sv:self.onchange())
        self.blue_entry_sv.trace("w",lambda name,index,mode,sv=self.blue_entry_sv:self.onchange())
        
        self.grid_columnconfigure(0,weight=1,uniform="foo")
        
        if labels==True:
            self.grid_columnconfigure(1,weight=1,uniform="foo")
        
        for i in range(4):
            self.grid_rowconfigure(i,weight=1,uniform="foo")
            
        self.onchange()
        
    @logger(log)
    def gethexcode(self,r,g,b):
        return('#%02x%02x%02x' % (int(r),int(g),int(b)))
    
    @logger(log)
    def onchange(self):
        
        if hasattr(self,'pick_widget') == False:
            log.log(thisfuncname(),3,msg="no pick label/button defined to display selection")
        else:
            try:
                self.msg_label_sv.set("")
            except:
                pass
            
            try:
                hexcode = self.gethexcode(self.red_entry_sv.get(), self.green_entry_sv.get(), self.blue_entry_sv.get())
                config =  {self.config:hexcode}
                self.pick_widget.config(**config)
                log.log(thisfuncname(),3,msg="updating config",config=config)
                return 0
            except Exception,e:
                self.error_sv.set(e)
            
        return -1
    
    
class ConfigPicker(Tk):
    
    def __init__(self):
        Tk.__init__(self)
    
        self.style = Style()
    
        #('clam', 'alt', 'default', 'classic')
        self.style.theme_use("default")
        
        self.style.configure('TCombobox',fieldbackground='lightgreen')
        self.style.configure('TEntry',fieldbackground='lightgreen')
        self.style.configure('TFrame',background='lightgrey', bd=1, relief=RAISED)
        self.style.configure('TLabel',fieldbackground='lightgreen')

        self.frame = Frame(self)
        self.frame.grid(row=0,column=0,sticky=NSEW)
    
        msg_label_sv = StringVar()
        msg_label = tklabel(self.frame,text="",textvariable=msg_label_sv, bd=3)
        msg_label.grid(row=4,column=0,columnspan=2,sticky=NSEW)
    
        self.num_picks=0

        self.bgrgbframe = RGBPickerFrame(self.frame,"background",msg_label_sv,"Background",255,0,0)
        self.bgrgbframe.grid(row=0,column=0,sticky=NSEW)
        
        self.fgrgbframe = RGBPickerFrame(self.frame,"foreground",msg_label_sv,"Foreground",0,255,0)
        self.fgrgbframe.grid(row=0,column=1,sticky=NSEW)
        
        self.fontpkrframe = FontPickerFrame(self.frame,msg_label_sv,"Font","Helvetica")
        self.fontpkrframe.grid(row=1,column=0,columnspan=2,sticky=NSEW)
    
        self.frame.grid_columnconfigure(0,weight=1,uniform="foo")
        self.frame.grid_columnconfigure(1,weight=1,uniform="foo")
    
        self.frame.grid_rowconfigure(0,weight=1,uniform="foo")
        
        self.set_pick()

    def set_pick(self):
        pick = tkbutton(self.frame,text="Aa Bb Cc Dd Ee 123 %^&*#@", bd=3,command=self.set_pick)
        pick.grid(row=3+self.num_picks,column=0,columnspan=2,sticky=NSEW,pady=2)
        self.num_picks = self.num_picks + 1
        
        self.bgrgbframe.pick_widget = pick
        self.fgrgbframe.pick_widget = pick
        self.fontpkrframe.pick_widget = pick
                        
    
        
if __name__ == "__main__":
    
    app = ConfigPicker()
    app.mainloop()