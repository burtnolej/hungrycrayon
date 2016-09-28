from Tkinter import *
from Tkinter import Button as _tkbutton
from Tkinter import Label as _tklabel
from Tkinter import Entry as _tkentry
from Tkinter import Frame as _tkframe
from Tkinter import Canvas as _tkcanvas

from ttk import *
import tkFont
from math import ceil,floor
import sys
from misc_utils import nxnarraycreate, thisfuncname
from misc_utils_log import Log, logger
from misc_utils_enum import enum
from type_utils import isadatatype, TextAlphaNumRO
from image_utils import ImageCreate, rgbstr_get
ic = ImageCreate()

log = Log(cacheflag=True,logdir="/tmp/log",pidlogname=True,proclogname=True)

fontscale = enum(sy = 2500,sx = 3500,
                 minfpt = 8,maxfpt = 64,
                 minwy=50,minwx=50)


widget_config = {'cursor': 0, 
                 'style':0,
                 'height': 0,
                 'padding':0,
                 'width':0,
                 'borderwidth':0,  
                 'class': 0,
                 'takefocus':0, 
                 'relief':0}

tkfrm_cfg= enum.datamembers(dm={'background':'#000000',
                                'borderwidth':1,
                                'width':20,
                                'height':10})  

def tk_create_config(style,cfg,stylename):
    for k,v in cfg.attr_get_keyval(include_callable=False,
                                   include_nondataattr=False):
        style.configure(stylename,k=v)
        
def tk_create_frame(parent,stylename):
    return(Frame(parent,style=stylename))

def tk_label_get_image(widget,text,**kw):
    
    if kw.has_key('pointsize'):
        kw['pointsize'] = int((kw['pointsize']/3)*4)
        
    widget.update_idletasks()

    w = widget.winfo_width()
    h = widget.winfo_height()

    geom = "{0}x{1}".format(w,h)
    
    outputfiles = ic.create_image_file(text,
                                       size=geom,
                                       **kw)

    return(PhotoImage(file=outputfiles[0]))
    
def geometry_get_dict(d):
    return(geometry_get(*d.values()))
    
def geometry_get(height=0,width=0,x=0,y=0):
    return("{0}x{1}+{2}+{3}".format(width,height,x,y))

def _font_scale(fs,value):   

    wdelta = int(fs.sx/(fs.maxfpt-fs.minfpt+1))
    newfpt = int(fs.minfpt + ceil(value/wdelta))
    
    return(newfpt)
    

def font_scale(fs,wx,wy):

    newfpt_x = _font_scale(fs,wx)
    newfpt_y = _font_scale(fs,wy)
    
    return(max(newfpt_x,newfpt_y))


def tkwidgetimage_set(ic,widget,label,overwrite=False,**kwargs):
    
    widget.update_idletasks()
    
    widget.image_size = "{0}x{1}".format(widget.winfo_width(),widget.winfo_height())
    kwargs['extent'] = widget.image_size
    widget.image= ic.create_image_file(label,overwrite=overwrite,**kwargs)[0]
    
    widget.photo = PhotoImage(file=widget.image)
    widget.config(image=widget.photo)
    
    widget.image_args = kwargs
    widget.image_args['extent'] = widget.image_size
    

'''def tkwidgetfactory(widgettype,master,*args,**kwargs):
    
    class tkwidget(widgettype):
    
        def __init__(self,master,*args,**kwargs):
            widgettype.__init__(self,master,*args,**kwargs)
            self.widgettype = widgettype
            
            self.config(**kwargs)

        #staticmethod(tkwidgetimage_set)
        
    tkw = tkwidget(master,*args,**kwargs)
    tkw.config(**kwargs)
    
    return(tkw)'''


def tkwidgetfactory(app,var,master,toplevel,**kwargs):
    
    class tkwidget(var.widgettype):
    
        def __init__(self,master,widgettype):
            
            self.app = app
            self.toplevel = toplevel
            
            d={}
            if kwargs.has_key('name'):
                d = dict(name=kwargs['name'])
                kwargs.pop('name')
            
            widgettype.__init__(self,master,var,**d)
            
            # not every widget type accepts every option   
            if issubclass(var.widgettype,TkCombobox) == False:
                try:
                    kwargs.pop('values')
                except:
                    pass
            else:
                
                # if not passes in on values; try set attribute of the var
                if kwargs.has_key('values') == False:
                    kwargs['values'] = var.set
                    self.orig_values = var.set# keep a copy of full value list so dropdown values can be reset
                elif kwargs.has_key('values'):
                    self.orig_values = kwargs['values']
                else:
                    raise Exception('cannot find combo list either on var or passed in on kwargs')

            self.widgettype = widgettype
            
            self.config(**kwargs)

        #staticmethod(tkwidgetimage_set)
        
    return(tkwidget(master,var.widgettype))
#tkw = tkwidget(master,var.widgettype)
#tkw.config(**kwargs)        
#return(tkw)


#class TkImageLabelGrid():

class TkImageLabelGrid(Frame):

    def __init__(self,*args,**kwargs):
        self._createwidget(*args,**kwargs)
        
    @logger(log)
    def _createwidget(self,master,gridname,var,width,height,x,y,maxrows,maxcols,
                      scrollbar=True,clipboard=False,
                      gridcfg=None,widgetcfg=None,
                      gridcolstart=0,gridrowstart=0,
                      rowhdrcfg={},colhdrcfg={}):
    
        # toplevel
        self.master = master # reference to ui root
        Frame.__init__(self,master)    
        self.grid(row=0,column=0,sticky=NSEW)
        
        #self.master.grid_rowconfigure(0,weight=1,uniform='foo')
        #self.master.grid_columnconfigure(0,weight=1,uniform='foo')
        
        #self.current_inputmode = self.master.current_inputmode
        self.clipboard=[]
        self.clipboard_selection=-1
        self.current_inputmode = "Normal"
        
        # canvas
        self.canvas = _tkcanvas(self)
        self.canvas.pack(side=RIGHT,fill=BOTH,expand=True,anchor=N)
        
        # canvasframe
        self.canvasframe = Frame(self.canvas)
        self.canvasframe.pack(side = LEFT, fill = BOTH, expand = True,anchor=N)

        self.canvas_window = self.canvas.create_window((0,0),window=self.canvasframe,anchor=N)

        vscrollbar = Scrollbar(self,orient="vertical",command=self.canvas.yview)
        
        if scrollbar == True:
            vscrollbar.pack(side=RIGHT,fill=Y)         
        
        self.canvas.config(yscrollcommand=vscrollbar.set)        

        self.canvas.config(background='green')
        self.gridname = gridname
    
        self.canvasframe.bind("<Configure>",self.resize_canvasframe)  
        self.canvas.bind("<Configure>",self.reset_framewidth)
        
        self.current_yfocus=0
        self.current_xfocus=0
        
        self.gridcfg = gridcfg
        self.widgetcfg = widgetcfg
        self.gridcolstart = gridcolstart
        self.gridrowstart = gridrowstart
        
        self.width=width
        self.height=height
        self.x=x
        self.y=y
                
        self.idle = False
        
        if self.gridcfg == None:
            self.gridcfg = nxnarraycreate(maxrows,maxcols)
            
        if self.widgetcfg == None:
            widgetcfg = nxnarraycreate(maxrows,maxcols)
            
        self.maxrows = maxrows
        self.maxcols = maxcols
        
        self.label='foobar'
    
        self.widgets=[]

        self.canvasframe.grid_rowconfigure(0,weight=1,uniform='foo')
        self.canvasframe.grid_columnconfigure(0,weight=1,uniform='foo')  
        
        for x in range(self.maxrows):
            ylbls=[]
            for y in range(self.maxcols):
                
                lbl = tkwidgetfactory(self,var,self.canvasframe,master,
                                      name=",".join([gridname,str(x),str(y)]),
                                      **widgetcfg[x][y])        
                
    
                lbl.grid(row=x,column=y,sticky=NSEW)
                   
                ylbls.append(lbl)
            self.widgets.append(ylbls)

        for i in range(self.gridcolstart,self.maxcols):
            self.canvasframe.grid_columnconfigure(i, weight=1, uniform="foo")
            
        for i in range(self.gridrowstart,self.maxrows):        
            self.canvasframe.grid_rowconfigure(i, weight=1, uniform="foo")
    
        if rowhdrcfg <> None: self.header_set(1,**rowhdrcfg)
        if colhdrcfg <> None: self.header_set(2,**colhdrcfg)   

        self.ic = ImageCreate()
        
        if clipboard == True:
            self.bind_all("<Control-Key>",self.modeset)
        
    def clipboard_paste(self):
        
        _clipboard = self.clipboard[self.clipboard_selection-1]
        
        _,tx,ty = self.focus_get().winfo_name().split(",")
        
        tx = int(tx)
        ty = int(ty)
        
        # workout offset from the first cell saved in the selection
        ox,oy = _clipboard[0]
        dx = tx-ox
        dy = ty-oy
        log.log(thisfuncname(),9,msg="paste clipboard",clipboard= _clipboard,tag="clipboard")
        for x,y in _clipboard:
            
            newx = x+dx
            newy = y+dy
            self.widgets[newx][newy].sv.set(self.widgets[x][y].sv.get())
        
    def clipboard_add_selection(self,cut=False):
        _clipboard = []
        
        if self.current_inputmode == "Normal": # single cell copy
            _,tx,ty = self.focus_get().winfo_name().split(",")
            widget = self.widgets[int(tx)][int(ty)]
            _clipboard.append((int(tx),int(ty)))
            widget.copy_state=False
            widget.unhighlight()
        else:
            
            for x in range(1,self.maxrows):
                for y in range(1,self.maxcols):
                    if self.widgets[x][y].copy_state == True:
                        widget = self.widgets[x][y]
                        _,tx,ty = widget.winfo_name().split(",")
                        _clipboard.append((int(tx),int(ty)))
                        widget.copy_state=False
                        widget.unhighlight()
                        
                        if cut==True: # delete source cell content
                            self.widgets[x][y].set("")
                            
            self.current_inputmode = "Normal"
            #self.inputmode_label_sv.set(self.current_inputmode)            
                
        log.log(thisfuncname(),9,msg="added to clipboard",clipboard= _clipboard,tag="clipboard")
         
        self.clipboard.append(_clipboard)
        #self.clipboard_size_label_sv.set(len(self.clipboard))
        
        # set the current clipboard selection to the latest
        self.clipboard_selection = len(self.clipboard)
        #self.clipboard_selected_label_sv.set(self.clipboard_selection)
        
        log.log(thisfuncname(),9,msg="input mode set",currentmode= self.current_inputmode,tag="clipboard")
        
    def selection_clear(self):
        for x in range(1,self.maxrows):
            for y in range(1,self.maxcols):
                if self.widgets[x][y].copy_state == True:
                    self.widgets[x][y].unhighlight()
                    self.widgets[x][y].copy_state == False
                    

        log.log(thisfuncname(),9,msg="input mode set",currentmode= self.current_inputmode,
                newmode="Normal",tag="clipboard")

        self.current_inputmode = "Normal"
        self.inputmode_label_sv.set(self.current_inputmode)
                
    def modeset(self,event):
        
        print self
        
        log.log(thisfuncname(),9,msg="input mode",currentmode= self.current_inputmode,tag="clipboard")
        new_inputmode = None
        if event.keysym == "s":
            new_inputmode = "Select"
        elif event.keysym == "r":
            self.selection_clear()
        elif event.keysym == "c":
            self.clipboard_add_selection()
        elif event.keysym == "x":
            self.clipboard_add_selection(cut=True)
        elif event.keysym == "n":
            if self.clipboard_selection == len(self.clipboard):
                self.clipboard_selection = 1
            else:
                self.clipboard_selection+=1
            self.clipboard_selected_label_sv.set(self.clipboard_selection)
            log.log(thisfuncname(),9,msg="clipboard selection set",selection=self.clipboard_selection,tag="clipboard")
        elif event.keysym == "v":
            self.clipboard_paste()
        elif event.keysym == "d":
            print self.clipboard
        else:
            pass
        
        if new_inputmode <> None:
            #self.inputmode_label_sv.set(new_inputmode)
        
            log.log(thisfuncname(),9,msg="input mode set",newmode=new_inputmode,tag="clipboard")
            self.current_inputmode = new_inputmode
            
            self.widgets[0][0].sv.set(new_inputmode)
            
    def reset_framewidth(self,event):
        self.canvas.itemconfig(self.canvas_window,width=event.width)
        
    def resize_canvasframe(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        
    def refocus(self,event):
        
        name,y,x = str(event.widget).split(".")[-1].split(",")
        
        x=int(x)
        y=int(y)
        
        if event.keycode==113 or event.keysym=='u':
                x=x-1
        elif event.keycode == 114 or event.keysym=='o':
                x=x+1
        elif event.keycode == 111 or event.keysym=='i':
                y=y-1
        elif event.keycode == 116 or event.keysym=='j':
                y=y+1
                
        if x<0: x=self.maxcols-1
        if y<0: y=self.maxrows-1
        if x>self.maxcols-1: x=0
        if y>self.maxrows-1: y=0
        
        self.focus(x,y)
        
    def focus(self,x=None,y=None):
        
        if x==None: x = self.current_xfocus
        if y==None: y = self.current_yfocus
        
        self.widgets[int(y)][int(x)].focus()
        self.current_yfocus=y
        self.current_xfocus=x

    def _draw(self,event):
        if self.idle == False:
            self.master.after(250,self.image_set)
            
            self.idle = True
        
    def image_set(self):
        
        newfontscale = font_scale(fontscale,
                                  self.master.winfo_width(),
                                  self.master.winfo_height())
        
        for x in range(len(self.widgets)):
            for y in range(len(self.widgets[0])):
                if self.gridcolstart <> 0 and self.gridrowstart <> 0:
                    if x ==0 and y ==0: continue
                widget = self.widgets[x][y]

                # image_set takes label as an arg not a kwarg
                # so need to remove it
                
                if self.gridcfg[x][y].has_key('label'):
                    #label = self.gridcfg[x][y]['label']
                    widget.label = self.gridcfg[x][y]['label']    
                    
                    self.gridcfg[x][y].pop('label')
                    
                # update font size based on latest resize
                self.gridcfg[x][y]['pointsize'] = newfontscale

                tkwidgetimage_set(self.ic,widget,widget.label,False,**self.gridcfg[x][y])
        self.idle = False
        
        #self.image_show()
            
    def image_show(self):

        for x in range(len(self.widgets)):
            for y in range(len(self.widgets[0])):
                if self.gridcolstart <> 0 and self.gridrowstart <> 0:
                    if x ==0 and y ==0: continue
                widget = self.widgets[x][y]
                widget.config(image=widget.photo)
                
    def cell_set(self,x,y,**args):
        widget = self.widgets[x][y]
        widget.config(**args)
        
    def header_set(self,orientation=0,**args):
        ''' 1 is vertical, 2 horizontal, None/0 is both '''
        
        y = self.maxcols
        x = self.maxrows
        
        if orientation == 1:
            x =1
        elif orientation == 2:
            y = 1
            
        coords = [(_x,_y) for _y in range(y) for _x in range(x)]
        
        for x,y in coords:
            self.cell_set(x,y,**args)
            
    def dump_grid(self):
        ''' return the text contents of the grid in a n x n array
        ignores blank spaces'''
        contents=[]
        for x in range(self.maxrows):
            column=[]
            empty_column=True
            for y in range(self.maxcols):
                widget = self.widgets[x][y]
                value = widget.sv.get()
                if value <> "":
                    column.append(value)
                    empty_column=False
                    
            if not empty_column:
                contents.append(column)
        return contents
    
class TKBase(object):
    def __init__(self,widget,**kwargs):
        
        self.widget = widget
        parent = self.widget.winfo_parent()
        gparent = self._nametowidget(parent).winfo_parent()
        
        #self.toplevel = self._nametowidget(gparent)
        #self.toplevel = self.app

        if hasattr(self.toplevel,'update_callback'):
            self.set_update_trace()
        else:
            log.log(thisfuncname(),3,msg='no update_callback method found on',widget=str(self.toplevel))
            
        #self.sv=StringVar() 
        
        self.version = 0
        self.current_value = self.init_value = ""    

        self.widget.s = Style()
        
        self.widget.s.configure(".".join(['InFocus','Notchanged',self.widget.winfo_class()]),
                         fieldbackground='yellow',
                         foreground='black')
        
        self.widget.s.configure(".".join(['OutOfFocus','Notchanged',self.widget.winfo_class()]),
                         fieldbackground='white',
                         foreground='black')
        
        self.widget.s.configure(".".join(['InFocus','Changed',self.widget.winfo_class()]),
                         fieldbackground='yellow',
                         foreground='red')
        
        self.widget.s.configure(".".join(['OutOfFocus','Changed',self.widget.winfo_class()]),
                         fieldbackground='white',
                         foreground='red')
        
        self.widget.s.configure(".".join(['InFocus','Label',self.widget.winfo_class()]),
                         fieldbackground='grey',
                         foreground='black')
        
        self.widget.s.configure(".".join(['OutOfFocus','Label',self.widget.winfo_class()]),
                         fieldbackground='grey',
                         foreground='black')
    
        
        #self.init_value= self.current_value = ""

        self.widget.bind("<Down>",self.refocus)
        self.widget.bind("<Left>",self.refocus)
        self.widget.bind("<Right>",self.refocus)
        self.widget.bind("<Up>",self.refocus)
        
        # for some reason TEntry does not treat Style same as combo so can make these calls in TkBase
        if self.winfo_class() == 'TEntry':
            self.widget['style']=".".join(['OutOfFocus','Notchanged',self.widget.winfo_class()])
            
            self.widget.bind('<FocusIn>',self.highlight)
            self.widget.bind('<FocusOut>',self.highlight)
            
        
    def set_update_trace(self):
        ''' this is the default and works for any widget that has a StringVar assigned to -textvariable
        otherwise you need to '''
        
        widget_class = str(self.widget.winfo_class())

        
        try:
            self.sv.trace("w",lambda name,index,mode,sv=self.sv:
                          self.toplevel.update_callback(self.widget,self.sv.get()))
            log.log(thisfuncname(),10,func=self.sv.trace,widgetclass=widget_class, widget=self.toplevel)

        except Exception, e:
            log.log(thisfuncname(),1,func=self.sv.trace,widgetclass=widget_class, widget=self.toplevel,error=str(e))

    def highlight(self,event):
        _,state,_ = self['style'].split(".")
        
        if event.type == '9':
            self['style']=".".join(['InFocus',state,self.winfo_class()])    
            
        elif event.type == '10':
            self['style']=".".join(['OutOfFocus',state,self.winfo_class()])
          
        self.selectall()
        
    def selectall(self,event=None):
        self.selection_range(0, END)
           
    def refocus(self,event):
        #parent = self.winfo_parent()
        #self._nametowidget(parent).refocus(event)
        self.app.refocus(event)
        return "break"

class TkEntryBool(Entry,TKBase):
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')

        self.sv=StringVar()    
        Entry.__init__(self,master,
                          textvariable=self.sv,
                          **kwargs)
        
        TKBase.__init__(self,self,**kwargs)
        
        #self.widget.config(relief=FLAT,borderwidth=1,highlightthickness=0)
        self.style_on = ".".join(['On','Notchanged',self.widget.winfo_class()])
        self.widget.s.configure(self.style_on,fieldbackground='green',foreground='black',
                                relief=FLAT,borderwidth=1,highlightthickness=0)
        
        log.log(thisfuncname(),10,func=self.__init__)
        
    def highlight(self,event):
        
        if event.type == '9':
            if self.widget['style'] <> self.style_on:
                self.orig_style = self.widget['style']
                self.widget['style'] = self.style_on
            else:
                self.widget['style'] = self.orig_style
        
class TkEntry(Entry,TKBase):
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')

        self.sv=StringVar()    
        Entry.__init__(self,master,
                          textvariable=self.sv,
                          **kwargs)
        
        TKBase.__init__(self,self,**kwargs)

        self.sv.trace("w",lambda name,index,mode,sv=self.sv:
                      self.changed(self.sv))
        
        log.log(thisfuncname(),10,func=self.__init__)
                      
    def changed(self,sv):
        #new_value = sv.get()
        #self.current_value = new_value
        focus_state = "InFocus"
        
        # check if function is because of a system load (ignore focus) or by a user selection
        if str(self.master.focus_get()) <> str(self):
            focus_state = 'OutOfFocus'
             
        if str(self.current_value) <> str(self.init_value):
            parent = self.winfo_parent()
            gparent = self._nametowidget(parent).winfo_parent()
            #self._nametowidget(gparent).updates[str(self.winfo_name())] = new_value

            self['style']=".".join([focus_state,'Changed',self.winfo_class()])
        else:
            self['style']=".".join([focus_state,'Notchanged',self.winfo_class()])
                                      #'InFocus.Notchanged.TEntry'


class TkGridEntry(TkEntry):
    
    
    def __init__(self,*args,**kwargs):
        super(TkGridEntry,self).__init__(*args,**kwargs)
        self.copy_state=False
        
        
        self.s.configure(".".join(['Select','Notchanged',self.winfo_class()]),
                         fieldbackground='LightPink',background='white')
        
    def unhighlight(self):
        _,state,cls = self['style'].split(".")
        self['style'] = ".".join(['OutOfFocus',state,cls])
        
    def highlight(self,event):
        
       
        log.log(thisfuncname(),9,style=self['style'],inputmode=self.app.current_inputmode,tag="clipboard")
        
        _,state,_ = self['style'].split(".")

        # cannot set this earlier as cell widget could be created before its put into the widgets array
        # used by highlighter so you can see the col/row hdr associated with cell in focus
        _,x,y = self.winfo_name().split(",")

        if hasattr(self,'xhdrwidget') == False:            
            self.xhdrwidget = self.app.widgets[0][int(y)]
            self.yhdrwidget = self.app.widgets[int(x)][0]

        if event.type == '9':

            #if self.toplevel.current_inputmode == "Select":
            if self.app.current_inputmode == "Select":
                self['style']=".".join(['Select',state,self.winfo_class()])
                self.copy_state=True
                
                log.log(thisfuncname(),9,msg="combo in select mode",style=self['style'],tag="clipboard")
            else:
                self['style']=".".join(['InFocus',state,self.winfo_class()])    
                self.xhdrwidget['style']=".".join(['InFocus',state,self.winfo_class()])
                self.yhdrwidget['style']=".".join(['InFocus',state,self.winfo_class()])
                self.copy_state=False

        elif event.type == '10':
            #if self.toplevel.inputmode_label_sv.get() <> "Select":
            if self.app.current_inputmode <> "Select":
                
                self['style']=".".join(['OutOfFocus',state,self.winfo_class()])
                self.xhdrwidget['style']=".".join(['OutOfFocus',state,self.winfo_class()])
                self.yhdrwidget['style']=".".join(['OutOfFocus',state,self.winfo_class()])
                self.copy_state=False
            #elif self.toplevel.inputmode_label_sv.get() == "Select":
            elif self.app.current_inputmode == "Select":
                self['style']=".".join(['Select',state,self.winfo_class()])
                self.copy_state=True

        self.selectall()
        
        


class TkLabel(_tklabel,TKBase):
    def __init__(self,master,var,**kwargs):
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        self.current_value = self.init_value = ""
        self.sv=StringVar()
        _tklabel.__init__(self,master,
                          textvariable=self.sv,
                          **kwargs)
                
        TKBase.__init__(self,self,
                        **kwargs)
            
class TkImageWidget(TkLabel):
#class TkImageLabel(Tkbutton):
    
    def __init__(self,master,var,**kwargs):
        TkLabel.__init__(self,master,var)
        #Tkbutton.__init__(self,master)
        
        self.config(**kwargs)
        self.ic = ImageCreate()
    
    def image_set(self,label,**kwargs):
        
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.image_size = "{0}x{1}".format(self.width,self.height)
        
        kwargs['extent'] = self.image_size
        self.image= self.ic.create_image_file(label,
                                         #overwrite=True,
                                         **kwargs)[0]
        
        self.photo = PhotoImage(file=self.image)
        self.config(image=self.photo)


class TkButton(_tkbutton):
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        _tkbutton.__init__(self,master,**kwargs)
        

class TkCombobox(Combobox,TKBase):
    
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        self.sv=StringVar() 
    
        Combobox.__init__(self,master,textvariable=self.sv,
                          **kwargs)

        TKBase.__init__(self,self,**kwargs)

        # over writing TKBase
        self.s.configure(".".join(['InFocus','Valid',self.winfo_class()]),
                         fieldbackground='yellow',background='green')
        
        self.s.configure(".".join(['OutOfFocus','Valid',self.winfo_class()]),
                         fieldbackground='white',background='green')
        
        self.s.configure(".".join(['InFocus','Invalid',self.winfo_class()]),
                        fieldbackground='yellow',background='white')
        
        self.s.configure(".".join(['OutOfFocus','Invalid',self.winfo_class()]),
                        fieldbackground='white',background='white')

        # this line needs to stay in TkComboBox - otherwise cannot call self['style']
        self['style']='OutOfFocus.Invalid.TCombobox'

        self.sv.trace("w",lambda name, index, mode,
                      sv=self.sv: self.complete())
        
        # this line needs to stay in TkComboBox - otherwise cannot call self['style'] in highlight
        self.bind('<FocusIn>',self.highlight)
        self.bind('<FocusOut>',self.highlight)

        self.bind("<Control-Down>",self.postdropdown)
        self.bind("<Control-Up>",self.unpostdropdown) 
        

    def postdropdown(self,event):
        self.post()
        
    def unpostdropdown(self,event):
        self.unpost()
        
    def propogate(self,event):
        parent = self.winfo_parent()
        self._nametowidget(parent).event_generate("<Next>")
        return "break"
            
    def complete(self):

        current_focus_state,_,_ = self['style'].split(".")
        valid_state = 'Invalid'
        #focus_state = 'InFocus'
        
        # check if function is because of a system load (ignore focus) or by a user selection
        if self.master.focus_get() == None:
            current_focus_state = 'OutOfFocus'

        # always use the chars up to the most recent char only to start the complete
        # otherwise we create a dupe char if the input continues to be correct after a match is created
        input = self.sv.get()[:self.index(INSERT)]
        #input = self.sv.get()
        if input <> "":
            hits = self.rematch(input,self['values'])
            
            if len(hits) == 1:
                self.update_values(hits)
                self.sv.set(hits[0])
                valid_state = 'Valid'
                
            elif len(hits)>1:
                    
                self.update_values(hits)
            else:
                self.update_values(self.orig_values)
        else:
            self.update_values(self.orig_values)
            
        self['style']=".".join([current_focus_state,valid_state,'TCombobox'])   
            
                
    def update_values(self,newvalues):
        #self.combo.config(values=newvalues)
        self.config(values=newvalues)
        
    def rematch(self,expr,list):
        
        r = re.compile(expr.lower())
            
        match = []
        for item in list:
            results = r.findall(item.lower())
            if len(results) > 0:
                match.append(item)
                
        match.sort()
        return(match)


class TkGridCombobox(TkCombobox):
    
    
    def __init__(self,*args,**kwargs):
        super(TkGridCombobox,self).__init__(*args,**kwargs)
        self.bind("<Alt_L>",self.copypaste)
        self.copy_state=False
        
        self.s.configure(".".join(['Select','Invalid',self.winfo_class()]),
                         fieldbackground='LightPink',background='white')
        
        self.s.configure(".".join(['Copy','Invalid',self.winfo_class()]),
                         fieldbackground='LightCyan',background='white')
    
        self.s.configure(".".join(['OutOfFocus','Invalid',self.winfo_class()]),
                         fieldbackground='white',background='white')

        
    def copypaste(self,event):
        if self.copy_state==False: 
            self.copy_state=True
        else:
            self.copy_state=False
        
    def unhighlight(self):
        _,state,cls = self['style'].split(".")
        self['style'] = ".".join(['OutOfFocus',state,cls])
        
    def highlight(self,event):
               
        print "highlight"
                
        _,state,_ = self['style'].split(".")

        # cannot set this earlier as cell widget could be created before its put into the widgets array
        # used by highlighter so you can see the col/row hdr associated with cell in focus
        _,x,y = self.winfo_name().split(",")
        
        if hasattr(self,'xhdrwidget') == False:            
            self.xhdrwidget = self.app.widgets[0][int(y)]
            self.yhdrwidget = self.app.widgets[int(x)][0]
            
        if event.type == '9':
            
            #if self.toplevel.current_inputmode == "Select":
            if self.app.current_inputmode == "Select":
                    
                self['style']=".".join(['Select',state,self.winfo_class()])
                self.copy_state=True
            else:
                self['style']=".".join(['InFocus',state,self.winfo_class()])    
                self.xhdrwidget['style']=".".join(['InFocus',state,self.winfo_class()])
                self.yhdrwidget['style']=".".join(['InFocus',state,self.winfo_class()])
                self.copy_state=False
            
        elif event.type == '10':
            #if self.toplevel.inputmode_label_sv.get() <> "Select":
            if self.app.current_inputmode <> "Select":
                self['style']=".".join(['OutOfFocus',state,self.winfo_class()])
                self.xhdrwidget['style']=".".join(['OutOfFocus',state,self.winfo_class()])
                self.yhdrwidget['style']=".".join(['OutOfFocus',state,self.winfo_class()])
                self.copy_state=False
            #elif self.toplevel.inputmode_label_sv.get() == "Select":
            elif self.app.current_inputmode == "Select":
                self['style']=".".join(['Select',state,self.winfo_class()])
                self.copy_state=True
        
        self.selectall()
        
    
if __name__ == '__main__':
    master = Tk()
    wgt = GridTableWidget(master,5,8)
    master.mainloop()
    
    import pprint
    
    pprint.pprint(wgt.widget)
