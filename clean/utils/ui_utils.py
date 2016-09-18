from Tkinter import *
from Tkinter import Button as _tkbutton
from Tkinter import Label as _tklabel
from Tkinter import Entry as _tkentry

from ttk import *
import tkFont
from math import ceil,floor
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import nxnarraycreate, thisfuncname
from misc_utils_log import Log, logger
from misc_utils_enum import enum
from type_utils import isadatatype, TextAlphaNumRO
from image_utils import ImageCreate, rgbstr_get
ic = ImageCreate()

log = Log(cacheflag=True,logdir="/tmp/log",pidlogname=False,proclogname=False)

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
            if var.widgettype <> TkCombobox:
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

    def __init__(self,master,gridname,var,width,height,x,y,maxrows,maxcols,
                 gridcfg=None,widgetcfg=None,
                 gridcolstart=0,gridrowstart=0,
                 rowhdrcfg={},colhdrcfg={}):

        self.master = master # reference to ui root
        Frame.__init__(self,master)
        self.grid(row=0,column=0,sticky=NSEW)
        
        canvas = Canvas(self)
        frame = Frame(canvas)
        frame.grid(row=0,column=0,sticky=NSEW)

        vscrollbar = Scrollbar(self,orient="vertical",command=canvas.yview)
        vscrollbar.pack(side='right',fill='y')       
        canvas.configure(yscrollcommand=vscrollbar.set)
    
        hscrollbar = Scrollbar(self,orient="horizontal",command=canvas.xview)
        hscrollbar.pack(side='bottom',fill='x')        
        canvas.configure(yscrollcommand=hscrollbar.set,xscrollcommand=hscrollbar.set)
    
        canvas.pack(side="left",fill="both",expand=True)
        canvas.create_window((2,2),window=frame,anchor="nw",tags="frame")

        self.gridname = gridname
        
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
        for x in range(self.maxrows):
            ylbls=[]
            for y in range(self.maxcols):
                
                lbl = tkwidgetfactory(self,var,frame,master,
                                      name=",".join([gridname,str(x),str(y)]),
                                      **widgetcfg[x][y])
    
                lbl.grid(row=x,column=y,sticky=NSEW)
                   
                ylbls.append(lbl)
            self.widgets.append(ylbls)
         
        for i in range(self.gridcolstart,self.maxcols):
            self.grid_columnconfigure(i, weight=1, uniform="foo")
            
        for i in range(self.gridrowstart,self.maxrows):        
            self.grid_rowconfigure(i, weight=1, uniform="foo")

        if rowhdrcfg <> None: self.header_set(1,**rowhdrcfg)
        if colhdrcfg <> None: self.header_set(2,**colhdrcfg)   

        self.focus(0,0)
        self.ic = ImageCreate()
        
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
        self.post
        
    def unpostdropdown(self,event):
        self.unpost
        
    def propogate(self,event):
        parent = self.winfo_parent()
        self._nametowidget(parent).event_generate("<Next>")
        return "break"
            
    def complete(self):
       
        valid_state = 'Invalid'
        focus_state = 'InFocus'
        
        # check if function is because of a system load (ignore focus) or by a user selection
        if self.master.focus_get() == None:
            focus_state = 'OutOfFocus'

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
            
        self['style']=".".join([focus_state,valid_state,'TCombobox'])   
            
                
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

if __name__ == '__main__':
    master = Tk()
    wgt = GridTableWidget(master,5,8)
    master.mainloop()
    
    import pprint
    
    pprint.pprint(wgt.widget)