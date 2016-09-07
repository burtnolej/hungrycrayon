from Tkinter import *
from Tkinter import Button as _tkbutton
from Tkinter import Label as _tklabel
from Tkinter import Entry as _tkentry
from ttk import *
import tkFont
from math import ceil,floor
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import nxnarraycreate
from misc_utils_enum import enum
from type_utils import isadatatype, TextAlphaNumRO
from image_utils import ImageCreate, rgbstr_get
ic = ImageCreate()

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


def tkwidgetfactory(var,master,**kwargs):
    
    class tkwidget(var.widgettype):
    
        def __init__(self,master,widgettype):
            widgettype.__init__(self,master,var)
            self.widgettype = widgettype
            
            self.config(**kwargs)

        #staticmethod(tkwidgetimage_set)
        
    tkw = tkwidget(master,var.widgettype)
    tkw.config(**kwargs)
    
    return(tkw)

class TkImageWidget(object):
#class TkImageLabel(Tkbutton):
    
    def __init__(self,master,**kwargs):
        Tklabel.__init__(self,master)
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

class TkImageLabelGrid():
    
    
    ''' need to pass in a var here not a widget type
        also need to create my own label and button class (like entry) '''
    
    def __init__(self,master,var,width,height,x,y,maxrows,maxcols,
                 gridcfg=None,widgetcfg=None,
                 gridcolstart=0,gridrowstart=0,
                 rowhdrcfg={},colhdrcfg={}):
        self.master = master

        self.gridcfg = gridcfg
        self.widgetcfg = widgetcfg
        self.gridcolstart = gridcolstart
        self.gridrowstart = gridrowstart
        
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.geom = geometry_get(self.height,self.width,
                                      self.x,self.y)
        self.master.geometry(self.geom)
                
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
                
                lbl = tkwidgetfactory(var,self.master,**widgetcfg[x][y])
                lbl.grid(row=x,column=y,sticky=NSEW)
                               
                ylbls.append(lbl)
            self.widgets.append(ylbls)
         
        for i in range(self.gridcolstart,self.maxcols):
            self.master.grid_columnconfigure(i, weight=1, uniform="foo")
            
        for i in range(self.gridrowstart,self.maxrows):        
            self.master.grid_rowconfigure(i, weight=1, uniform="foo")

        if rowhdrcfg <> None: self.header_set(1,**rowhdrcfg)
        if colhdrcfg <> None: self.header_set(2,**colhdrcfg)   

        self.ic = ImageCreate()
        
    def _draw(self,event):
        if self.idle == False:
            self.master.after(250,self.image_set)
            
            self.idle = True
                
        #self.master.bind('<Configure>',_draw)
        
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
        
    '''for x in range(len(self.widgets)):
        for y in range(len(self.widgets[0])):
            widget = self.widgets[x][y]
            widget.config(image=widget.photo)'''
        

    '''self.widgets[0][1].config(image=self.widgets[0][1].photo)
    self.widgets[1][0].config(image=self.widgets[1][0].photo)
    self.widgets[1][1].config(image=self.widgets[1][1].photo)'''
        #self.widgets[0][0].config(image=self.widgets[0][0].photo)
    
    
class TkEntry(_tkentry):
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        _tkentry.__init__(self,master,**kwargs)

class TkLabel(_tklabel):
    def __init__(self,master,var,**kwargs):
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')        
        _tklabel.__init__(self,master,**kwargs)

class TkButton(_tkbutton):
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        _tkbutton.__init__(self,master,**kwargs)

class TkCombobox(Combobox):
    
    def __init__(self,master,var,**kwargs):
        
        if not isadatatype(var):
            raise Exception('arg datatype must be a valid type')
        
        self.frame = Frame(master)
        self.frame.pack(side=LEFT)

        self.values = var.set
        self.sv=StringVar()
        Combobox.__init__(self,master,values=self.values,
                           textvariable=self.sv,
                           **kwargs)
        
        self.textstr = TextAlphaNumRO(name='textalphanum')
        self.textstr(str(len(self.values)))
        
        self.label = TkLabel(self.frame,self.textstr,
                             text=self.textstr)
        self.label.pack(side=LEFT,expand=1,fill=Y)

        self.sv.trace("w",lambda name, index, mode, 
                  sv=self.sv: self.complete())
        
    def complete(self):
        input = self.sv.get()
        if input <> "":
            hits = self.rematch(input,self.values)
            
            if len(hits) == 1:
                self.update(hits)
                self.sv.set(hits[0])
            elif len(hits)>1:
                self.update(hits)
                #self.config(values=hits)
                #current = self.sv.get()
                #self.sv.set("{0} ({1})".format(current,str(len(hits))))
                #master.event_generate("<Down>")
                #combo.focus_force()
            else:
                self.update(self.values)
                #self.config(values=self.values)
        else:
            self.update(self.values)
            
                
    def update(self,newvalues):
        print "update",newvalues
        #self.combo.config(values=newvalues)
        self.config(values=newvalues)
        self.label.config(text=len(newvalues))
        
    def rematch(self,expr,list):
        
        r = re.compile(expr)
            
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