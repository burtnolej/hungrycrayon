from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from ttk import *
from PIL import Image, ImageTk
from image_utils import ImageCreate, rgbstr_get
from collections import OrderedDict
from misc_utils_process import *

import tkFont
import unittest

sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from format_utils import *

from ui_utils import tk_create_config, tkfrm_cfg, \
     tk_create_frame, GridTableWidget, tk_label_get_image

def _dumpwgt2(wgt):
    
    wgt.update_idletasks()
    
    attr = ['winfo_atom', 'winfo_atomname', 'winfo_cells', 'winfo_children', 'winfo_class', 'winfo_colormapfull', 'winfo_containing', 'winfo_depth', 'winfo_exists', 'winfo_fpixels', 'winfo_geometry', 'winfo_height', 'winfo_id', 'winfo_interps', 'winfo_ismapped', 'winfo_manager', 'winfo_name', 'winfo_parent', 'winfo_pathname', 'winfo_pixels', 'winfo_pointerx', 'winfo_pointerxy', 'winfo_pointery', 'winfo_reqheight', 'winfo_reqwidth', 'winfo_rgb', 'winfo_rootx', 'winfo_rooty', 'winfo_screen', 'winfo_screencells', 'winfo_screendepth', 'winfo_screenheight', 'winfo_screenmmheight', 'winfo_screenmmwidth', 'winfo_screenvisual', 'winfo_screenwidth', 'winfo_server', 'winfo_toplevel', 'winfo_viewable', 'winfo_visual', 'winfo_visualid', 'winfo_visualsavailable', 'winfo_vrootheight', 'winfo_vrootwidth', 'winfo_vrootx', 'winfo_vrooty', 'winfo_width', 'winfo_x', 'winfo_y']
    for a in attr:
        try:
            print a.ljust(20),getattr(wgt,a)()
        except TypeError:
            print a.ljust(20),'ERROR'
            pass
        
    #for k,v in wgt.config().iteritems():
    #    print k.ljust(20),v[4]
    
def _dumpwgt(tk):
    #tk = getattr(wgt,'tk')
    for attr in dir(tk):
        if not callable(getattr(tk,attr)):
            print attr,getattr(tk,attr)
        else:
            try:
                print attr,getattr(tk,attr)()
            except TypeError:
                print attr,"error"
                
            
'''class TestWidget(unittest.TestCase):
    
    
    def assertWidgetDimensions(self,widget,factor,**kw):
        
        dims = ['height','width','x','y']
        
        widget.update_idletasks() 

        for d in dims:
            print "testing",d,"args",kw
            self.assertEquals(getattr(widget,"winfo_"+d)(),
                              kw[d]/factor)    


class TestUIRoot(unittest.TestCase):

    def setUp(self):
        self.master = Tk()
        
    def test_draw_configure_root(self):
        self.master.geometry('300x200+200+100')
        self.master.configure(background='red')
        self.master.update_idletasks()
        
        self.assertEquals(self.master.winfo_height(),200)
        self.assertEquals(self.master.winfo_width(),300)
        self.assertEquals(self.master.winfo_x(),200)
        self.assertEquals(self.master.winfo_y(),100)
        
    def test_draw_configure_root_with_str(self):
        cfg = '300x200+200+100'
        self.master.geometry(cfg)
        self.master.configure(background='red')
        self.master.update_idletasks()
        self.assertEquals(self.master.winfo_geometry(),cfg)
        
    def test_draw_configure_root_with_badstr(self):
        cfg = '300x200+100+x'
        with self.assertRaises(TclError):
            self.master.geometry(cfg)
        
    def tearDown(self):
        try:
            self.master.destroy()
        except:
            pass'''
        
'''class TestUIFrame(unittest.TestCase):
    
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        
    def test_draw_frame(self):
        self.frame = Frame(self.master)
        
        self.assertEquals(self.frame.widgetName,'ttk::frame')
        self.assertEquals(self.frame.children,{})
        self.assertEquals(self.frame.winfo_class(),'TFrame')
        
    def test_draw_frame_manual_config(self):
        self.frame = Frame(self.master,
                           height=290,
                           width=190)
        self.frame.grid(row=5,column=5)
        
        self.frame.update_idletasks()
        
        self.assertEquals(self.frame.winfo_height(),290)
        self.assertEquals(self.frame.winfo_width(),190)
        self.assertEquals(self.frame.winfo_x(),0)
        self.assertEquals(self.frame.winfo_y(),0)
        
    def test_draw_frame_with_style(self):
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=180,width=280,x=10,y=10)

        self.frame.update_idletasks()
        
        self.assertEquals(self.frame.winfo_height(),180)
        self.assertEquals(self.frame.winfo_width(),280)
        self.assertEquals(self.frame.winfo_x(),10)
        self.assertEquals(self.frame.winfo_y(),10)

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()'''
          
class TestUIPack(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    def test_pack(self):
        self.frame.pack()
        button = Button(self.master,text="Button")
        button.pack(fill=BOTH, expand=1)
        
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_sidebyside(self):
        #self.frame.pack()
        button = Button(self.master,text="Button1")
        button.pack(side=LEFT, fill=BOTH,expand=1)
        button = Button(self.master,text="Button2")
        button.pack(side=LEFT, fill=BOTH,expand=1)        
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_ontop(self):
        #self.frame.pack()
        button = Button(self.master,text="Button1")
        button.pack(fill=BOTH,expand=1)
        button = Button(self.master,text="Button2")
        button.pack(fill=BOTH,expand=1)        
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_2x2_in_frame(self):
        #self.frame.pack()
        leftframe = Frame(self.frame)
        leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)  
        rightframe = Frame(self.frame)
        rightframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(rightframe,text="butinframe1.2")
        button.pack(fill=BOTH,expand=1)
        button = Button(rightframe,text="butinframe1.2")
        button.pack(fill=BOTH,expand=1) 
        #_dumpwgt2(self.frame)
        self.master.mainloop()
                
    def test_pack_2x2(self):
        #self.frame.pack()
        leftframe = Frame(self.master)
        leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(leftframe,text="Button1.1")
        button.pack(fill=BOTH,expand=1)
        button = Button(leftframe,text="Button2.1")
        button.pack(fill=BOTH,expand=1)  
        rightframe = Frame(self.master)
        rightframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(rightframe,text="Button1.2")
        button.pack(fill=BOTH,expand=1)
        button = Button(rightframe,text="Button2.2")
        button.pack(fill=BOTH,expand=1) 
        #_dumpwgt2(self.frame)
        #self.master.mainloop()
        
    def test_pack_20x20(self):
        widgetgrid=[]
        for column in range(20):
            widgetcolumn=[]
            frame = Frame(self.master)
            frame.pack(side=LEFT,fill=BOTH,expand=1)
            for row in range(20):
                button = Button(frame,text=str(row)+"."+str(column))
                button.pack(fill=BOTH,expand=1)
                widgetcolumn.append(button)
            widgetgrid.append(widgetcolumn)

        self.assertEquals(widgetgrid[0][0].winfo_class(),'TButton')
        #_dumpwgt2(widgetgrid[19][19])
        #_dumpwgt2(widgetgrid[0][0])
        #self.master.mainloop()

    def tearDown(self):
        try: # not every test is creating a frame
            self.frame.destroy()
        except:
            pass
        
        self.master.destroy()
     
     
class TestUIButtonConfig(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        '''self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()'''
        
    def test_config_font(self):
         
        button = Tkbutton(self.master,text='foobar')
        button.pack(side=LEFT, fill=BOTH,expand=1)        

         
        font = tkFont.Font(family="Monospace", size=20)
        button.configure(font=font)
 
        #self.master.mainloop()
           
    def test_grid_config_font(self):
        
        button = Tkbutton(self.master,text='foobar')
        button.grid(row=0,column=0)        

        font = tkFont.Font(family="Monospace", size=36)
        
        #button.configure(font=font)
        
    def test_2x2grid_config_font(self):
        
        button1 = Tkbutton(self.master,text='foobar')
        button1.grid(row=0,column=0)
        button2 = Tkbutton(self.master,text='foobar')
        button2.grid(row=1,column=0)     
        button3 = Tkbutton(self.master,text='foobar')
        button3.grid(row=0,column=1)     
        button4 = Tkbutton(self.master,text='foobar')
        button4.grid(row=1,column=1)     

        font = tkFont.Font(family="Monospace", size=36)
        
        button2.configure(font=font)

        #self.master.mainloop()
        
    def test_2x2grid_config_font_from_list(self):
        
        buttons = []
        
        button = Tkbutton(self.master,text='foobar')
        button.grid(row=0,column=0)
        buttons.append(button)
        
        button = Tkbutton(self.master,text='foobar')
        button.grid(row=1,column=0)
        buttons.append(button)
        
        button = Tkbutton(self.master,text='foobar')
        button.grid(row=0,column=1)
        buttons.append(button)
        
        button = Tkbutton(self.master,text='foobar')
        button.grid(row=1,column=1)
        buttons.append(button)

        font = tkFont.Font(family="Monospace", size=36)
        
        for button in buttons:
            button.configure(font=font)

        self.master.mainloop()
        
    def tearDown(self):
        try: # not every test is creating a frame
            self.frame.destroy()
        except:
            pass
        
        self.master.destroy()        
        
class TestUIButton(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    def test_setgettext(self):
        
        def callback(button):
            ctext = button.cget("text")
            
            ntext = str(int(ctext) + 1)
            button.config(text=ntext)
            
        button = Button(self.master,text="0",command=lambda:callback(button))
        button.pack(fill=BOTH,expand=1)   
        
    def test_dimensions(self):
        button = Tkbutton(self.frame,text="dsds")
        button.config(height=5,width=5)
        button.pack(side=LEFT)   
        button = Tkbutton(self.frame,height = 1,width=4)
        button.pack(side=LEFT)    
        button = Tkbutton(self.frame,height = 3,width=10)
        button.pack(side=LEFT)    
        #self.master.mainloop()
        
    def test_colors(self):
        
        from random import randint

        def callback(button):

            r=randint(0,255)
            g=randint(0,255)
            b=randint(0,255)
            mycolor = '#%02x%02x%02x' % (r, g, b)
            button.config(bg=mycolor)
            button.config(text=mycolor)
        
        button = Tkbutton(self.frame,command=lambda:callback(button))
        button.pack(side=LEFT, fill=BOTH,expand=1)
        #self.master.mainloop()
        
    def test_font(self):
         
        font = tkFont.Font(family="Monospace", size=20)   
        # slant=tkFont.ITALIC
        # weight=tkFont.BOLD

        button = Tkbutton(self.frame,font=font,text='foobar')
        button.pack(side=LEFT, fill=BOTH,expand=1)
        #self.master.mainloop()
        
    def test_image(self):
        
        photo = PhotoImage(file="../scripts/buildgifs/8:30-9:10-270-68-68-rgb(97,91,92).gif")
        font = tkFont.Font(family="Monospace", size=20)   
        # slant=tkFont.ITALIC
        # weight=tkFont.BOLD

        mycolor = '#%02x%02x%02x' % (97, 91, 92) # #615b5c

        
        print mycolor
        self.master.grid()
        button = Tkbutton(self.master)
        button = Tklabel(self.master)
        button.config(image=photo,width="100",height="100",bg=mycolor)
        button.grid()
        #button.pack(side=LEFT, fill=BOTH,expand=1)
        self.master.mainloop()
        
    def tearDown(self):
        try: # not every test is creating a frame
            self.frame.destroy()
        except:
            pass
        
        self.master.destroy()
        
        
class TestUIEntry(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    
    def test_addentry(self):
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        #self.master.mainloop()
    
    def test_addentry_addtext(self):
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry.insert(0,'default value')
        #self.master.mainloop()
        
    def test_addentry_add_delete_then_add(self):
        import time
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry.insert(0,'default value')

        entry.delete(0,END)
        entry.insert(0,'another default value')
        
        #self.master.mainloop()
        
    def test_addentry_stringvar(self):
        
        def callback(v,y):
            v.set(y.get())
            
        v= StringVar()
        entry = Entry(self.frame, textvariable=v)
        entry.insert(0,'to be updated')
        entry.pack(fill=BOTH,expand=1)
        
        y= StringVar()
        entry = Entry(self.frame, textvariable=y)
        entry.insert(0,'input text here')
        entry.pack(fill=BOTH,expand=1)
        
        button = Button(self.frame,command=lambda:callback(v,y))
        button.pack(fill=BOTH,expand=1)
        #self.master.mainloop()
          
          
class TestUIGrid2x2evenlarge(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('500x500+0+0')
        
        self.button1 = Button(self.master,text="NW")
        self.button1.grid(row=0,column=0,sticky=NSEW) 
        self.button2 = Button(self.master,text="NE")
        self.button2.grid(row=0,column=1,sticky=NSEW) 
        self.button3 = Button(self.master,text="SW")
        self.button3.grid(row=1,column=0,sticky=NSEW)
        self.button4 = Button(self.master,text="SE")
        self.button4.grid(row=1,column=1,sticky=NSEW)
        
        self.master.columnconfigure(0,weight=1,uniform='foobar')
        self.master.columnconfigure(1,weight=1,uniform='foobar')
        self.master.rowconfigure(0,weight=1,uniform='foobar')
        self.master.rowconfigure(1,weight=1,uniform='foobar')

    def assertWidgetDimensions(self,widget,factor,**kw):
        
        dims = ['height','width','x','y']
        
        widget.update_idletasks() 

        for d in dims:
            #print "testing",d,"args",kw
            self.assertEquals(getattr(widget,"winfo_"+d)(),
                              kw[d]/factor)
        
    def test_add_grid_2x2master(self):
        
        self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
        
class TestUIGrid2x2even(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        
        self.button1 = Button(self.master,text="NW")
        self.button1.grid(row=0,column=0,sticky=NW) 
        self.button2 = Button(self.master,text="SW")
        self.button2.grid(row=0,column=1,sticky=SW) 
        self.button3 = Button(self.master,text="NE")
        self.button3.grid(row=1,column=0,sticky=NE)
        self.button4 = Button(self.master,text="SE")
        self.button4.grid(row=1,column=1,sticky=SE)

    def assertWidgetDimensions(self,widget,factor,**kw):
        
        dims = ['height','width','x','y']
        
        widget.update_idletasks() 

        for d in dims:
            #print "testing",d,"args",kw
            self.assertEquals(getattr(widget,"winfo_"+d)(),
                              kw[d]/factor)
        
    def test_add_grid_2x2master(self):
        
        exp_results = dict(height=52,width=166,x=0,y=0)
        self.assertWidgetDimensions(self.master,1,**exp_results)
    
    def test_add_grid_2x2nwbutton(self):

        exp_results = dict(height=26,width=83,x=0,y=0)
        self.assertWidgetDimensions(self.button1,1,**exp_results)
        
    def test_add_grid_2x2sebutton(self):
        
        exp_results = dict(height=26,width=83,x=83,y=26)
        self.assertWidgetDimensions(self.button4,1,**exp_results)

    def tearDown(self):
        self.master.destroy()
        
class TestUIGrid7x5odd(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.maxrows=7 # rows in the grid
        self.maxcols=5 # cols in the grid
        self.maxwidgets=self.maxrows*self.maxcols
        self.wwidth=48 # default button width with text of 3 chars
        self.wheight=29 # default button height
        self.wmheight=self.wheight*self.maxrows # master height
        self.wmwidth=self.wwidth*self.maxcols # master width
        
        self.buttons=[]
        for x in range(self.maxrows):
            ybuttons=[]
            for y in range(self.maxcols):
                _name = str(x)+":"+str(y)
                button = Tkbutton(self.master,text=_name,name=_name)
                button.grid(row=x,column=y)
                ybuttons.append(button)
            self.buttons.append(ybuttons)

    def _winfo_get(self,widget):
        
        dims = ['height','width','x','y','name']
        
        widget.update_idletasks() 

        return [(d,getattr(widget,"winfo_"+d)()) for d in dims]  
        
    def winfo_get(self,widget):

        parent = self._winfo_get(widget)
        children = []
        
        if len(widget.children) <> 0:
            children = [self._winfo_get(child) for child in widget.children.values()]
        
        return(parent,children)
                  
    def assertWidgetDimensions(self,widget,factor,**kw):
        
        dims = ['height','width','x','y']
        
        widget.update_idletasks() 

        for d in dims:
            wdim = getattr(widget,"winfo_"+d)()
            self.assertEquals(wdim,kw[d]/factor)
        
    def test_add_grid_7x5master(self):
        exp_results = dict(height=self.wmheight,
                           width=self.wmwidth,
                           x=0,
                           y=0)
        self.assertWidgetDimensions(self.master,1,**exp_results)
        
        self.assertEquals(len(self.master.children),self.maxwidgets)
        
        
    def test_add_grid_7x5middle(self):
        
        row=2
        col=3
        
        widget = self.buttons[row][col]
        exp_results = dict(height=self.wheight,
                           width=self.wwidth,
                           x=self.wwidth*col,
                           y=self.wheight*row)
        self.assertWidgetDimensions(widget,1,**exp_results)
        
    def test_add_grid_7x5bottomright(self):
        
        row=6
        col=4
        
        widget = self.buttons[row][col]
        exp_results = dict(height=self.wheight,
                           width=self.wwidth,
                           x=self.wwidth*col,
                           y=self.wheight*row)
        self.assertWidgetDimensions(widget,1,**exp_results)
        
        #self.master.mainloop()
        
    def test_add_grid_7x5_font24pt(self):
        
        row=6
        col=4
        
        print 
        font = tkFont.Font(family="Helvetica", size=32)
        
        for widget in self.master.children.values():
            widget.configure(font=font)
        
        print self.winfo_get(self.master)
        
        #self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
class TestUIGrid2x2span(TestWidget):
    def setUp(self):
        self.master = Tk()
        
        self.button1 = Tkbutton(self.master,text="NW")
        self.button1.grid(row=0,column=0) 
        self.button2 = Tkbutton(self.master,text="SW")
        self.button2.grid(row=0,column=1)
        self.button4 = Tkbutton(self.master,text="NE")
        self.button4.grid(row=1,columnspan=3,sticky=NSEW)

    def test_add_grid_2x2master(self):
        
        exp_results = dict(height=58,width=97,x=0,y=0)
        self.assertWidgetDimensions(self.master,1,**exp_results)
    
    def test_add_grid_2x2lowerbutton(self):

        exp_results = dict(height=29,width=97,x=0,y=29)
        self.assertWidgetDimensions(self.button4,1,**exp_results)

    def tearDown(self):
        self.master.destroy()
        
        
class TestUIGrid2x2spanlarge(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('500x500+0+0')
        
        self.button1 = Tkbutton(self.master,text="NW")
        self.button1.grid(row=0,column=0,sticky=NSEW) 
        self.button2 = Tkbutton(self.master,text="SW")
        self.button2.grid(row=0,column=1,sticky=NSEW)
        self.button4 = Tkbutton(self.master,text="NE")
        self.button4.grid(row=1,columnspan=3,sticky=NSEW)
        
        self.master.columnconfigure(0,weight=1,uniform='foobar')
        self.master.columnconfigure(1,weight=1,uniform='foobar')
        self.master.rowconfigure(0,weight=1,uniform='foobar')
        self.master.rowconfigure(1,weight=1,uniform='foobar')


    def test_add_grid_2x2master(self):
        
        self.master.mainloop()
        

class TestUIWidgets(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.frame = Frame(self.master)
        self.frame.grid(row=2,column=2)

    def test_button(self):
        button = Button(self.frame,text="foobar")
        button.grid(row=1,column=1)   
        self.assertTrue(isinstance(self.frame.children[button._name],Button))
        
        self.assertEquals(button,'button')
        #_dumpwgt(button)
        #self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
        
class TestUIInheritance(unittest.TestCase):
    
    class MyWgt(Frame):
        
        def __init__(self, master=None):
            _style = Style()
            _style.configure('mystyle.TFrame',background='blue')
            Frame.__init__(self, master,style='mystyle.TFrame')

            self.place(height=160,width=260,x=20,y=20)
            self.config()
            
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')

    def test_(self):
        wgt = self.MyWgt(self.master)
        
        leftframe = Frame(wgt)
        leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)
        button = Button(leftframe,text="butinframe1.1")
        button.pack(fill=BOTH,expand=1)  

        #self.master.mainloop()


class TestUITable(unittest.TestCase):

    class MyTblWgt(Frame):

        def __init__(self,master=None,width=5,height=5):
            _style = Style()
            _style.configure('mystyle.TFrame',background='blue')

            self.widgetgrid=[]
            # add on 1 for title row/column
            for column in range(width+1):
                widgetcolumn=[]
                frame = Frame(master)
                frame.pack(side=LEFT,fill=Y,expand=1,anchor='n')                  
                for row in range(height+1):
                    if row==0 and column==0:                        
                        button = Tkbutton(frame,text='',height=1,anchor='n')
                        button.pack(side=TOP)
                    elif row==0:
                        button = Tkbutton(frame,text='')
                        button.pack(fill=X)
                    elif column==0:
                        button = Tkbutton(frame,text='')
                        button.pack(fill=Y,expand=1)
                    else:
                        cellouterframe = Frame(frame,style='mystyle.TFrame')
                        cellouterframe.pack(fill=BOTH,expand=1,anchor='w')
                        
                        cellinnerframe = Frame(cellouterframe)
                        cellinnerframe.pack(side=LEFT,fill=BOTH,expand=1)
                        
                        topbutton=Tkbutton(cellinnerframe,width=50,height=2,text='')
                        topbutton.pack(fill=Y,expand=1,)
                        midbutton=Tkbutton(cellinnerframe,width=50,height=2,text='')
                        midbutton.pack(fill=Y,expand=1,)
                        botbutton=Tkbutton(cellinnerframe,width=50,height=2,text='')
                        botbutton.pack(fill=Y,expand=1,)
                    widgetcolumn.append(button)
                self.widgetgrid.append(widgetcolumn)
                
    def setUp(self):
        self.master = Tk()
        self.master.geometry('2200x1000+100+100')

    def test_create(self):
        wgt = self.MyTblWgt(self.master,5,5)
        for row in wgt.widgetgrid:
            for w in row:
                self.assertTrue(isinstance(w,Tkbutton))
        self.master.mainloop()
        
    '''def test_update(self):
        wgt = self.MyTblWgt(self.master,5,5)
        
        for row in wgt.widgetgrid:
            for w in row:
                self.assertTrue(isinstance(w,Tkbutton))
        self.master.mainloop()
        
    def test_controls(self):
        controlframe = Frame(self.master)
        controlframe.pack(side=RIGHT)          
        gridframe = Frame(self.master)
        gridframe.pack(side=LEFT,fill=BOTH,expand=1)        

        wgt = self.MyTblWgt(gridframe,5,5)
        
        for row in wgt.widgetgrid:
            for w in row:
                self.assertTrue(isinstance(w,Tkbutton))
                
   
        entry = Entry(controlframe)
        entry.pack(side=TOP)
        entry.insert(0,'default value')
        entry = Entry(controlframe)
        entry.pack(side=TOP)
        entry.insert(0,'default value')
        self.master.mainloop()       ''' 
     
class TestUIGridTableBasic(unittest.TestCase):
    

    def setUp(self):
        self.master = Tk()
        
    def test_create_small_dump_details(self):
        wgt = GridTableWidget(self.master,2,2)
        wgt.table_update_all_text('foobar')
        #font = tkFont.Font(family="Helvetica", size=16)
        #wgt.table_update_all_fonts(font)
        wgt.table_dump_info(wgt)
        wgt.table_dump_header_info()
        self.master.mainloop()
        
    
class TestUIGridTable(unittest.TestCase):

    def setUp(self):
        self.master = Tk()
        self.test_text = [[['david','',''],['brian','',''],['phil','',''],['bruce','',''],['peter','','']],
                [['basil','',''],['tim','',''],['gary','',''],['steve','',''],['paul','','']],
                [['val','',''],['nancy','',''],['grace','',''],['jane','',''],['jon','','']],
                [['turnip','',''],['potato','',''],['radisch','',''],['lettuce','',''],['beetroot','','']],
                [['bill','',''],['damian','',''],['barry','',''],['dave','',''],['luke','','']],
                [['jamie','',''],['larry','',''],['harry','',''],['george','',''],['matilda','','']],
                [['james','',''],['briece','',''],['bonny','',''],['sanjay','',''],['sachin','','']],
                [['graham','',''],['banana','',''],['pony','',''],['wellies','',''],['beans','','']]]

        
        #self.master.geometry('2200x1000+100+100')

    def test_create(self):
        wgt = GridTableWidget(self.master,5,8)
        
        self.assertEquals(len(wgt.widget),8)
        self.assertEquals(len(wgt.widget[0]),5)
        self.assertEquals(len(wgt.widget[0][0]),3)
        #self.master.mainloop()
        
        ''' 
        def test_update_text(self):
    
        
        wgt = GridTableWidget(self.master,5,8)   
        wgt.table_update_content(self.test_text)

        self.assertEquals(wgt.table_get_content(),text)'''

        
        ''' 
        def test_update_text(self):
    
        
        wgt = GridTableWidget(self.master,5,8)   
        wgt.table_update_content(self.test_text)

        self.assertEquals(wgt.table_get_content(),text)'''
        
    '''def test_init_datagrid(self):
        wgt = GridTableWidget(self.master,5,8) 
        exp_res = [[['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']],
                   [['','',''],['','',''],['','',''],['','',''],['','','']]]
        
        self.assertEquals(wgt._init_datagrid(),exp_res)'''
        
    '''def test_update_color(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_content(self.test_text)
        colors = wgt._init_datagrid()
        colors[0][0][0] = whiteblack14i
        colors[1][0][0] = burgundywhite18
        colors[7][3][0] = yellowburgundy14
        wgt.table_update_colors(colors)

    def test_update_text(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_content(self.test_text)

        self.assertEquals(wgt.table_get_content(),self.test_text)
        
    def test_update_font(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_content(self.test_text)
        
        mono20 = tkFont.Font(family="Monospace", size=20)
        mono10 = tkFont.Font(family="Monospace", size=8)
        #mono15b = tkFont.Font(family="Monospace", size=8,weight=tkFont.BOLD)
        #mono20i = tkFont.Font(family="Monospace", size=8,slant=tkFont.ITALIC)
        
        fonts = wgt._init_datagrid()
        fonts[0][0][0] = mono20
        #fonts[1][0][0] = mono10
        #fonts[7][3][0] = mono15b
        #fonts[7][4][0] = mono20i
        wgt.table_update_font(fonts)
        
    def test_update_all_font(self):
        helv36 = tkFont.Font(family="Helvetica", size=18)
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_all_text('foobar')
        wgt.table_update_all_fonts(helv36)
        self.master.mainloop()
        
    def test_update_all_text(self):
        wgt = GridTableWidget(self.master,5,8)
        wgt.table_update_all_text('foobar')
        self.master.mainloop()'''
        
    '''def test_update_top_label_text(self):
        wgt = GridTableWidget(self.master,5,8)
        
        helv36 = tkFont.Font(family="Helvetica", size=18)
        wgt.table_update_all_fonts(helv36)
        labels = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        for i in range(len(labels)):
            
            wgt.columnheaderwidget[i].config(text=labels[i])
            wgt.columnheaderwidget[i].config(font=helv36)     
        self.master.mainloop()'''
        
    def test_update_top_label_image(self):
        
        fontfamily = "Helvetica"
        fontsize=36
        tkrgb = '#%02x%02x%02x' % (214, 210, 208)
        
        photo = PhotoImage(file="/tmp/foobar.gif")
        wgt = GridTableWidget(self.master,5,8)
        #font = tkFont.Font(family=fontfamily, size=fontsize)
        #wgt.table_update_all_fonts(font)
        wgt.table_update_all_text('foobar')

        rowheaderimages=[]
        labels = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        for i in range(len(labels)):
            
            rowheaderimages.append(tk_label_get_image(wgt.columnheaderwidget[i],
                                       labels[i],
                                       pointsize=fontsize,
                                       font=fontfamily,
                                       background=tkrgb,
                                       gravity='center'))
            
        for i in range(len(rowheaderimages)):
            
            wgt.columnheaderwidget[i].config(image=rowheaderimages[i])

        colheaderimages=[]
        labels = ['0830-915','0915-1000','1000-1045','1045-1130',
                  '1130-1215','1215-1300','1300-1345','1345-1430']
        for i in range(len(labels)):
            
            colheaderimages.append(tk_label_get_image(wgt.rowheaderwidget[i],
                                       labels[i],
                                       pointsize=fontsize,
                                       font=fontfamily,
                                       background=tkrgb,
                                       rotate=90,
                                       gravity='center'))
            
        for i in range(len(colheaderimages)):

            wgt.rowheaderwidget[i].config(image=colheaderimages[i])

        self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
        
class TestUILabel(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        #self.master.geometry('800x600+100+100')
        #self.master.configure(background='red')
        self.ic = ImageCreate()
        
        #_style = Style()
        #_style.configure('mystyle.TFrame',background='blue')
        #self.frame = Frame(self.master,style='mystyle.TFrame')
        #self.frame.place(height=160,width=260,x=20,y=20)
        #self.frame.config()
        
    '''def test_label_pack(self):
        
        lbl = Tklabel(self.master,text='text')
        lbl.pack(fill=BOTH,expand=1)
        #self.master.mainloop()
        lbl.update_idletasks()
        
        self.assertEquals(lbl.winfo_height(),600)
        self.assertEquals(lbl.winfo_width(),800)
        self.assertEquals(lbl.winfo_x(),0)
        self.assertEquals(lbl.winfo_y(),0)
    
    def test_label_pack_font(self):
        
        font = tkFont.Font(family="Monospace", size=1000)  
        lbl = Tklabel(self.master,text='text', font=font)
        lbl.pack(fill=BOTH,expand=1)
        
        lbl.update_idletasks()
    
        self.assertEquals(lbl.winfo_height(),600)
        self.assertEquals(lbl.winfo_width(),800)
        self.assertEquals(lbl.winfo_x(),0)
        self.assertEquals(lbl.winfo_y(),0)

    def assertFilesEqual(self,file1,file2):
        
        cmd = ['diff',file1,file2]
    
        p = process_start(cmd)
    
        pstdout = p.stdout.read()
    
        if pstdout.find('No such file or directory') <> -1:
    
            raise Exception('no reference gif for this test',exp_res)
    
        self.assertEquals(pstdout.find('differ'),-1)'''

            
        

        
 
  
    '''def test_draw_expand_image_rotate(self):
        self.master.geometry('500x500+10+10')
        
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame,text='text')
        lbl.pack(fill=BOTH,expand=1)  

        photo = tk_label_get_image(lbl,'text',rotate=90)

        lbl.config(image=photo)
        
    def test_draw_expand_image_2labels(self):
        self.master.geometry('500x500+10+10')
        
        fontfamily = "Helvetica"
        fontsize=48
        tkrgb = '#%02x%02x%02x' % (214, 210, 208)

        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame)
        lbl.place( width=500,height=250,x=0,y=0)

        font = tkFont.Font(family=fontfamily, size=fontsize)  
        lbl2 = Tklabel(self.frame,text='label text',font=font,background=tkrgb)
        lbl2.place( width=500,height=250,x=0,y=250)

        photo = tk_label_get_image(lbl,
                                   'label image',
                                   pointsize=fontsize,
                                   font=fontfamily,
                                   background=tkrgb,
                                   gravity='center')
        lbl.config(image=photo)
        
    def test_draw_expand_image_2labels_both_images(self):
        self.master.geometry('500x500+10+10')
        
        fontfamily = "Helvetica"
        fontsize=48
        tkrgb = '#%02x%02x%02x' % (214, 210, 208)

        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.pack(fill=BOTH,expand=1)

        lbl = Tklabel(self.frame)
        lbl.place( width=500,height=250,x=0,y=0)

        lbl2 = Tklabel(self.frame)
        lbl2.place( width=500,height=250,x=0,y=250)

        photo = tk_label_get_image(lbl,
                                   'label image',
                                   pointsize=fontsize,
                                   font=fontfamily,
                                   background=tkrgb,
                                   gravity='center')
        lbl.config(image=photo)
        
        photo2 = tk_label_get_image(lbl2,
                                   'label image2',
                                   pointsize=fontsize,
                                   font=fontfamily,
                                   background=tkrgb,
                                   gravity='center')
        lbl2.config(image=photo2)
        
        self.master.mainloop()'''
        
    def tearDown(self):
        self.master.destroy()
        
class TkImageLabel(Tklabel):
    
    def __init__(self,master,**kwargs):
        
        Tklabel.__init__(self,master,text='text')
        self.config(**kwargs)
        self.ic = ImageCreate()
    
    def image_set(self,label,**kwargs):
        
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        
        size = "{0}x{1}".format(self.height,self.width)
        
        print size
        
        kwargs['extent'] = size
        self.image= self.ic.create_image_file(label,
                                         overwrite=True,
                                         **kwargs)[0]
        
        self.photo = PhotoImage(file=self.image)
        self.config(image=self.photo)
        
        #self.config(width=self.width)
        #self.config(height=self.height)
        
        
class TestUILabelGridImagePackBasic(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.ic = ImageCreate()
        
        self.lbl = TkImageLabel(self.master)
    
        self.lbl.pack(fill=BOTH,expand=1)  
        
    def test_label_pack_image(self,**kwargs):
        
        exp_res = "/home/burtnolej/Development/pythonapps3/clean/utils/test_misc/test_label_pack_image.gif"

        self.lbl.image_set('label',pointsize=36,
                           font='Helvetica',
                           gravity='center',
                           rotate=90)

        exp_results = dict(height=30,
                           width=21,
                           x=0,
                           y=0)
        
        self.assertWidgetDimensions(self.lbl,1,**exp_results)
        
        
        self.master.mainloop()
        
    def tearDown(self):
        self.master.destroy()

class TestUILabelGridImageGridBasic(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.ic = ImageCreate()
        
        self.lbl = TkImageLabel(self.master)
        self.lbl.grid(row=0,column=0)
        self.lbl2 = TkImageLabel(self.master)
        self.lbl2.grid(row=1,column=0)  
        
    def test_label_pack_image_top(self,**kwargs):
        
        exp_res = "/home/burtnolej/Development/pythonapps3/clean/utils/test_misc/test_label_pack_image.gif"

        self.lbl.image_set('label',pointsize=36,
                           font='Helvetica',
                           gravity='center',
                           rotate=90)

        exp_results = dict(height=30,
                           width=21,
                           x=3,
                           y=0)
        
        self.assertWidgetDimensions(self.lbl,1,**exp_results)

        
    def test_label_pack_image_both(self,**kwargs):
        
        exp_res = "/home/burtnolej/Development/pythonapps3/clean/utils/test_misc/test_label_pack_image.gif"


        self.lbl.image_set('label',pointsize=36,
                           font='Helvetica',
                           gravity='center',
                           rotate=90)
        
        self.lbl.config(image=self.lbl.photo)


        self.lbl2.image_set('label',pointsize=72,
                           font='Helvetica',
                           gravity='center',
                           rotate=180)

        exp_results = dict(height=30,
                           width=21,
                           x=0,
                           y=30)
        
        self.assertWidgetDimensions(self.lbl2,1,**exp_results)
        
        
    def tearDown(self):
        self.master.destroy()
        
class TestUILabelGridImageGridBasic2x2(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('500x500+0+0')
        
        self.ic = ImageCreate()
        
        self.lbl = TkImageLabel(self.master,borderwidth=0)
        self.lbl.grid(row=0,column=0,sticky=NSEW)
        self.lbl2 = TkImageLabel(self.master,borderwidth=0)
        self.lbl2.grid(row=1,column=0,sticky=NSEW)
        
        self.lbl3 = TkImageLabel(self.master,borderwidth=0)
        self.lbl3.grid(row=0,column=1,sticky=NSEW)
        self.lbl4 = TkImageLabel(self.master,borderwidth=0)
        self.lbl4.grid(row=1,column=1,sticky=NSEW)
        
        self.master.columnconfigure(0,weight=1,uniform='foobar')
        self.master.columnconfigure(1,weight=1,uniform='foobar')
        self.master.rowconfigure(0,weight=1,uniform='foobar')
        self.master.rowconfigure(1,weight=1,uniform='foobar')
        
        
    def test_label_pack_image_both(self,**kwargs):
        
        self.lbl.image_set('label',pointsize=36,
                           font='Helvetica',
                           gravity='center',
                           rotate=90)
        
        self.lbl.config(image=self.lbl.photo)


        self.lbl2.image_set('label',pointsize=36,
                           font='Helvetica',
                           gravity='center',
                           rotate=180)
        
        self.lbl3.image_set('label',pointsize=36,
                           font='Helvetica',
                           gravity='center',
                           rotate=90)
        
        self.lbl3.config(image=self.lbl.photo)


        self.lbl4.image_set('label',pointsize=72,
                           font='Helvetica',
                           gravity='center',
                           rotate=180)


        self.lbl4.config(image=self.lbl.photo)

        exp_results = dict(height=30,
                           width=21,
                           x=0,
                           y=30)
        
        self.master.mainloop()
        
        
    def tearDown(self):
        self.master.destroy()
        
class TestUILabelGridImageGrid2x2(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.maxrows=4 # rows in the grid
        self.maxcols=4 # cols in the grid
        self.maxwidgets=self.maxrows*self.maxcols
        self.wwidth=48 # default button width with text of 3 chars
        self.wheight=29 # default button height
        self.wmheight=self.wheight*self.maxrows # master height
        self.wmwidth=self.wwidth*self.maxcols # master width
        
        red='#%02x%02x%02x' % (255, 0, 0)
        
        self.buttons=[]
        for x in range(self.maxrows):
            ybuttons=[]
            for y in range(self.maxcols):
                _name = str(x)+":"+str(y)
                button = TkImageLabel(self.master,
                                      text=_name,
                                      background=red,
                                      relief=SUNKEN,
                                      borderwidth=1,
                                      width=10,
                                      height=10)
                button.grid(row=x,column=y)
                ybuttons.append(button)
            self.buttons.append(ybuttons)
            
        '''for i in range(self.maxcols):
            self.master.grid_columnconfigure(i, weight=1, uniform="foo")
        
        for i in range(self.maxrows):        
            self.master.grid_rowconfigure(i, weight=1, uniform="foo2")    '''
        
    def test_label_pack_add_images(self,**kwargs):
        
        r = 0
        g = 0
        b = 0
        offset = 10
        for row in self.buttons:
            for widget in row:
                r+=offset
                g+=offset
                b+=offset
                bg='#%02x%02x%02x' % (r, g, b)

                widget.image_set('label',pointsize=36,
                                   font='Helvetica',
                                   gravity='center',
                                   background=bg,
                                   rotate=90)
                
        self.master.mainloop()

        
    def tearDown(self):
        self.master.destroy()   
        

class TestUILabelGridImage(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.ic = ImageCreate()
        
        self.wwidth=21 # default button width with text of 3 chars
        self.wheight=17 # default button height
        
        self.lbl1bg='#%02x%02x%02x' % (203, 24, 32)
        self.lbl2bg='#%02x%02x%02x' % (12, 224, 132)
        self.lbl3bg='#%02x%02x%02x' % (100, 200, 200)
        self.lbl4bg='#%02x%02x%02x' % (100, 0, 200)
    
        font = tkFont.Font(family="Helvetica", size=32)
    
        self.lbl = TkImageLabel(self.master,
                                     text='lb1',
                                     borderwidth=0)
                                     #relief=SUNKEN)
        self.lbl.grid(row=0,column=0,columnspan=2,sticky=NSEW)  
    
        self.lbl2 = TkImageLabel(self.master,
                                      text='lb2',
                                      borderwidth=0)
                                      #relief=SUNKEN)
        self.lbl2.grid(row=1,column=0,columnspan=1,sticky=S)
    
        self.lbl3 = TkImageLabel(self.master,
                                      text='lb3',
                                      borderwidth=0)
                                      #relief=SUNKEN)
        self.lbl3.grid(row=1,column=1,sticky=S)
    
        self.lbl4 = TkImageLabel(self.master,
                                      text='lb4',
                                      borderwidth=0)
                                      #relief=SUNKEN)
        self.lbl4.grid(row=0,column=2,columnspan=1,rowspan=2,sticky=NSEW)

        for i in range(3):
            self.master.grid_columnconfigure(i, weight=1, uniform="foo")
        
        for i in range(2):        
            self.master.grid_rowconfigure(i, weight=1, uniform="foo2")
            
    def test_label_grid_image_master(self):

        exp_results = dict(height=self.wheight*2,
                           width=self.wwidth*3,
                           x=0,
                           y=0)
        
        #self.master.mainloop()
            
        self.assertWidgetDimensions(self.master,1,**exp_results)
        
    def test_label_grid_image_rightwidget(self):

        exp_results = dict(height=self.wheight*2,
                           width=self.wwidth*1,
                           x=self.wwidth*2,
                           y=0)
        
        self.master.mainloop()
            
        self.assertWidgetDimensions(self.lbl4,1,**exp_results)
        
    def test_label_grid_image_rightwidget_with_image(self):


        
        
        self.lbl4.update_idletasks()
        
        exp_results = dict(height=self.wheight*2,
                           width=self.wwidth*1,
                           x=self.wwidth*2,
                           y=0)
        
        
        self.lbl4.image_set(label='lbl4',
                            pointsize=11,
                            background=self.lbl4bg,
                            gravity='south',
                            rotate=90)
        
        self.master.mainloop()
            
        self.assertWidgetDimensions(self.lbl4,1,**exp_results)
        
    '''def test_label_grid_image_rightwidget_with_image(self):

        self.lbl4.update_idletasks()
        
        exp_results = dict(height=self.wheight*2,
                           width=self.wwidth*1,
                           x=self.wwidth*2,
                           y=0)
        
        self.lbl.image_set(label='lbl1',
                      pointsize=12,
                      background=self.lbl1bg,
                      font='Helvetica',
                      gravity='center',
                      rotate=180)
    
        self.lbl2.image_set(label='lbl2',
                       pointsize=36,
                       background=self.lbl2bg,
                       font='URW-Palladio-Roman',
                       gravity='center',
                       rotate=270)
    
        self.lbl3.image_set(label='lbl3',
                       pointsize=22,
                       background=self.lbl3bg,
                       font='Waree-Oblique',
                       gravity='north')
    
        self.lbl4.image_set(label='lbl4',
                       pointsize=11,
                       background=self.lbl4bg,
                       gravity='south',
                       rotate=90)
        
        #self.master.mainloop()'''
        
    def tearDown(self):
        self.master.destroy()   


if __name__ == "__main__":

    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIRoot))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIFrame))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelGridImagePackBasic))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelGridImageGridBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelGridImageGridBasic2x2))  
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2evenlarge))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelGridImage))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelGridImageGrid2x2))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2even))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid7x5odd))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2span))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2spanlarge))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIPack))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIEntry))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIWidgets))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIInheritance))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUITable))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIButton))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIButtonConfig))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGridTable))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGridTableBasic))
    
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)
