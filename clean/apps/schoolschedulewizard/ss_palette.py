from misc_utils_log import Log, logger
from misc_utils import thisfuncname
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,pidlogname=True,proclogname=False)
from Tkinter import *
from Tkinter import Label as tklabel
from Tkinter import Entry as tkentry
from Tkinter import Frame as tkframe
from ttk import *
import tkFont

class FontPickerFrame(Frame):
    
    def __init__(self,master,error_sv,example_label,example_label_sv,text,family="Helvetica",pointsize="12",weight="normal"):
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
            self.error_sv,example_label.config(font=font)
            
            log.log(thisfuncname(),3,msg="updating font",font=font)
            return 0
        except Exception,e:
            self.error_sv.set(e)    
            
class RGBPickerFrame(Frame):
    def __init__(self,master,config,error_sv,example_label,example_label_sv,text,r=0,g=0,b=0,labels=True):
        Frame.__init__(self,master)     

        self.error_sv = error_sv
        self.example_label_sv = example_label_sv
        self.example_label = example_label
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
        
        try:
            self.msg_label_sv.set("")
        except:
            pass
        
        try:
            hexcode = self.gethexcode(self.red_entry_sv.get(), self.green_entry_sv.get(), self.blue_entry_sv.get())
            config =  {self.config:hexcode}
            self.example_label.config(**config)
            log.log(thisfuncname(),3,msg="updating config",config=config)
            return 0
        except Exception,e:
            self.error_sv.set(e)
            
        return -1
    
class RGBPaletteFrame(Frame):
    def __init__(self,master,num_slots=8):
        Frame.__init__(self,master)     

        self.s = Style()
        
        self.s.configure(".".join(['InFocus','Unset','TEntry']),fieldbackground='yellow',foreground='black')
        self.s.configure(".".join(['OutOfFocus','Set','TEntry']),fieldbackground='white',foreground='black')

        self.widgets = []

        for i in range(num_slots):
            _entry_sv = StringVar()
            _entry = Entry(master,)
            _entry.grid(row=i,column=0)        
            self.grid_rowconfigure(i,weight=1,uniform="foo",name=i)
            self.widgets.append(_entry)
            
            self.widget.bind('<FocusIn>',self.highlight)
            self.widget.bind('<FocusOut>',self.highlight)
            
        self.grid_columnconfigure(i,weight=1,uniform="foo")
    
        self.widgets[0].set_focus()
        
    def highlight(self,event):
        _,state,_ = self['style'].split(".")
        
        if event.type == '9':
            self['style']=".".join(['InFocus',state,'TEntry'])    
            
        elif event.type == '10':
            self['style']=".".join(['OutOfFocus',state,'TEntry'])
            
        self.infocuswidget = event.widget
         
    def set(self,bgcolor,fgcolor,family,weight,pointsize):
        
        _,widgetindex = self.infocuswidget.winfo_name().split(".")
        
        _style = ".".join([str(self.infocuswidget),'Set','TEntry'])
        self.s.configure(_style,fieldbackground=bgcolor,foreground=fgcolor,
                         font=family)
        
        self.infocuswidget.config(text=bgcolor)
        self.infocuswidget['style'] = _style
        
if __name__ == "__main__":
    master = Tk()
    
    master.style = Style()
    #('clam', 'alt', 'default', 'classic')
    master.style.theme_use("default")

    master.style.configure('TCombobox',fieldbackground='lightgreen')
    master.style.configure('TEntry',fieldbackground='lightgreen')
    master.style.configure('TFrame',background='lightgrey', bd=1, relief=RAISED)
    master.style.configure('TLabel',fieldbackground='lightgreen')

    frame = Frame(master)
    frame.grid(row=0,column=0,sticky=NSEW)
    
    msg_label_sv = StringVar()
    msg_label = tklabel(frame,text="",textvariable=msg_label_sv, bd=3)
    msg_label.grid(row=4,column=0,columnspan=2,sticky=NSEW)
    
    example_label_sv = StringVar()
    example_label = tklabel(frame,textvariable=example_label_sv, bd=3)
    example_label.grid(row=3,column=0,columnspan=2,sticky=NSEW,pady=2)
    example_label_sv.set("Aa Bb Cc Dd Ee 123 %^&*#@")

    bgrgbframe = RGBPickerFrame(frame,"background",msg_label_sv,example_label,example_label_sv,"Background",255,0,0)
    bgrgbframe.grid(row=0,column=0,sticky=NSEW)
    fgrgbframe = RGBPickerFrame(frame,"foreground",msg_label_sv,example_label,example_label_sv,"Foreground",0,255,0)
    fgrgbframe.grid(row=0,column=1,sticky=NSEW)
    fontpkrframe = FontPickerFrame(frame,msg_label_sv,example_label,example_label_sv,"Font","Helvetica")
    fontpkrframe.grid(row=1,column=0,columnspan=2,sticky=NSEW)

    rgbpalette = RGBPaletteFrame(8)
    rgbpalette.grid(row=6,column=0,columnspan=2,sticky=NSEW)
    
    set_button = Button(frame,text="set",command=rgbpalette.set)
    set_button.grid(row=5,column=0,columnspan=2,sticky=NSEW)

    frame.grid_columnconfigure(0,weight=1,uniform="foo")
    frame.grid_columnconfigure(1,weight=1,uniform="foo")

    frame.grid_rowconfigure(0,weight=1,uniform="foo")
    
    master.mainloop()