from Tkinter import *
#from Tkinter import Button as Tkbutton
#from Tkinter import Label as Tklabel
from ttk import *
#from PIL import Image, ImageTk
from image_utils import ImageCreate, rgbstr_get, get_gif_filename
from collections import OrderedDict
from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate

from ui_utils import TkImageWidget, TkImageLabelGrid, geometry_get, font_scale, \
     tkwidgetfactory, geometry_get_dict, tkwidgetimage_set, fontscale, \
     TkCombobox, TkButton, TkEntry, TkLabel
import tkFont
import unittest

sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from format_utils import *
from type_utils import TextAlphaNum, TextAlphaNumRO, SetMemberPartial, DBSetMember
from ui_utils import tk_create_config, tkfrm_cfg, \
     tk_create_frame, tk_label_get_image

#fontscale = enum(sy = 2500,sx = 3500,
#                 minfpt = 8,maxfpt = 64,
#                 minwy=50,minwx=50)

defaultmaster = dict(height=300,width=200,
                     x=100,y=100)

defaultframe = dict(height=300,width=200,
                     x=0,y=0)

fullscreenmaster = dict(height=2500,width=3500,
                     x=0,y=0)


class TestTkComboBox(unittest.TestCase):
    def setUp(self):

        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))
        
        s = Style()
        s.configure('NotFocus.TCombobox',selectbackground='blue',
                    fieldbackground='red',
                    background='green')

        s2 = Style()
        s2.configure('Focus.TCombobox',selectbackground='blue',
                    fieldbackground='green',
                    background='green')
        
    def test_(self):
        
        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                                 'peach','pomegranate','passionfruit',
                                                                 'pear','grape','strawberry','raspberry',
                                                                 'rhubarb','mango','guava','apple',
                                                                 'Orange'])
        
        combo = TkCombobox(self.master,self.setmemberp)
        combo.grid(row=0,column=0,sticky=NSEW)

        combo2 = TkCombobox(self.master,self.setmemberp)
        combo2.grid(row=1,column=0,sticky=NSEW)
        combo2['style']='Hlight.TCombobox'
          
        self.master.mainloop()
        
    def tearDown(self):
        self.master.destroy()    
        
class TestTkWidgetFactory(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))
        
    def test_button(self):
        widget = tkwidgetfactory(Tkbutton,self.master,text='foobar')
        widget.pack(fill=BOTH,expand=1)
        
        self.assertIsInstance(widget,Tkbutton)
        
    def test_label(self):
        widget = tkwidgetfactory(Tklabel,self.master,text='foobar')
        widget.pack(fill=BOTH,expand=1)
        self.assertIsInstance(widget,Tklabel)
        
    def tearDown(self):
        self.master.destroy()

class TestFontScale(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_x_nochange(self):
        wx = 50
        wy = 50

        self.assertEquals(font_scale(fontscale,wx,wy),8)   
        
        
        self.assertEquals(font_scale(fontscale,wx,wy),8) 
        
    def test_x_minchange(self):
        wx = 75
        wy = 50

        self.assertEquals(font_scale(fontscale,wx,wy),9)      
    
    
    def test_x_maxchange(self):
        wx = 3460
        wy = 50

        self.assertEquals(font_scale(fontscale,wx,wy),64)    

    def test_x_middle(self):
        wx = 1749
        wy = 50

        self.assertEquals(font_scale(fontscale,wx,wy),36)
        
    def test_y_changebigger(self):
        wx = 75
        wy = 150

        self.assertEquals(font_scale(fontscale,wx,wy),10)       
          
class TestWidget(unittest.TestCase):
    
    def __init__(self,*arg,**kwargs):
        #self.master = Tk()
        super(TestWidget,self).__init__(*arg,**kwargs)
            
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
    
    def assertWidgetDimensions(self,widget,percent,**kw):
        
        if percent > 0.02 or percent < -0.02:
            raise Exception('do you really want to a percent >2%')
        
        dims = ['height','width','x','y']
        
        widget.update_idletasks() 

        #print kw
        
        for d in dims:
            
            if kw.has_key(d):
                upperbound = kw[d] + (kw[d]*percent)
                lowerbound = kw[d] - (kw[d]*percent)
                
                wininfo = getattr(widget,"winfo_"+d)()
                
                #print lowerbound,">=",wininfo,"<=",upperbound
                
                self.assertGreaterEqual(wininfo,lowerbound)
                self.assertLessEqual(wininfo,upperbound)
            
    def assertFilesEqual(self,file1,file2):
        
        #print "comparing",file1,file2
        
        cmd = ['diff',file1,file2]
    
        p = process_start(cmd)
    
        pstdout = p.stdout.read()
    
        if pstdout.find('No such file or directory') <> -1:
    
            raise Exception('no reference gif for this test',file2)
    
        self.assertEquals(pstdout.find('differ'),-1)
            
class TestTestWidget(TestWidget):

    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))
        
    def test_(self):
        self.master.configure(background='red')
        self.assertWidgetDimensions(self.master,0,**defaultmaster)
        
    def test_fail(self):
        self.master.configure(background='red')
        with self.assertRaises(AssertionError):
            self.assertWidgetDimensions(self.master,0,**fullscreenmaster)
        
    def test_percentpassupper(self):
        self.master.configure(background='red')
        
        self.assertWidgetDimensions(self.master,0.01,**defaultmaster)
        
    def test_percentpasslower(self):
        self.master.configure(background='red')
        self.assertWidgetDimensions(self.master,0.01,**defaultmaster)
        
    def tearDown(self):
        self.master.destroy() 
            
class TestUIRoot(TestWidget):

    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))
        
    def test_configure(self):
        self.master.configure(background='red')
        self.assertWidgetDimensions(self.master,0.01,**defaultmaster)
        
    def test_configure_badstr(self):
        cfg = '300x200+100+x'
        with self.assertRaises(TclError):
            self.master.geometry(cfg)
        
    def tearDown(self):
        self.master.destroy()
        
class TestUIFrame(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))
        self.master.configure(background='red')
        
    def test_pack_expand(self):
        self.frame = Frame(self.master)
        self.frame.pack(fill=BOTH,expand=1)
        self.assertWidgetDimensions(self.frame,0.01,**defaultframe)
        
    def test_manual_config(self):
        
        frame_offset = 10
        custommaster = dict(height=defaultmaster['height']-frame_offset,
                            width=defaultmaster['width']-frame_offset)   
        
        self.frame = Frame(self.master,**custommaster)
        self.frame.grid(row=5,column=5)
        self.assertWidgetDimensions(self.frame,0.01,**custommaster)
        
    def test_with_style(self):
        frame_offset = 10
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        
        custommaster = dict(height=defaultmaster['height']-frame_offset,
                            width=defaultmaster['width']-frame_offset)         

        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(**custommaster)
        
        self.assertWidgetDimensions(self.frame,0.01,**custommaster)

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()
        
class TestUIPack(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))
        self.master.configure(background='red')
        
    def test_(self):
        self.button = Button(self.master,text="Button")
        self.button.pack(fill=BOTH, expand=1)
        self.assertWidgetDimensions(self.button,0.01,**defaultframe)
        
    def test_sidebyside(self):
        button = Button(self.master,text="Button1")
        button.pack(side=LEFT, fill=BOTH,expand=1)
        button2 = Button(self.master,text="Button2")
        button2.pack(side=LEFT, fill=BOTH,expand=1)        

        _defaultframe = dict(defaultframe)
        _defaultframe['width'] = _defaultframe['width']/2
        self.assertWidgetDimensions(button,0.01,**_defaultframe)

        _defaultframe['x'] = _defaultframe['width']
        self.assertWidgetDimensions(button2,0.01,**_defaultframe)
          
    def test_ontop(self):
        button = Button(self.master,text="Button1")
        button.pack(side=TOP,fill=BOTH,expand=1)
        button2 = Button(self.master,text="Button2")
        button2.pack(side=TOP,fill=BOTH,expand=1)        

        _defaultframe = dict(defaultframe)
        _defaultframe['height'] = _defaultframe['height']/2        
        self.assertWidgetDimensions(button,0.01,**_defaultframe)

        _defaultframe['y'] = _defaultframe['height']
        self.assertWidgetDimensions(button2,0.01,**_defaultframe)
        
    def tearDown(self):
        self.master.destroy() 
        
class TestUIPack2x2(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))
        self.master.configure(background='red')
        
        self.leftframe = Frame(self.master)
        self.leftframe.pack(side=LEFT,fill=BOTH,expand=1)
        self.buttontopleft = Button(self.leftframe,text="topleft")
        self.buttontopleft.pack(fill=BOTH,expand=1)
        self.buttonbottomleft = Button(self.leftframe,text="bottomleft")
        self.buttonbottomleft.pack(fill=BOTH,expand=1)
    
        self.rightframe = Frame(self.master)
        self.rightframe.pack(side=LEFT,fill=BOTH,expand=1)
        self.buttontopright = Button(self.rightframe,text="topright")
        self.buttontopright.pack(fill=BOTH,expand=1)
        self.buttonbottomright = Button(self.rightframe,text="bottomright")
        self.buttonbottomright.pack(fill=BOTH,expand=1) 

    def test_topleft(self):

        _defaultframe = dict(defaultframe)
        _defaultframe['height'] = _defaultframe['height']/2 
        _defaultframe['width'] = _defaultframe['width']/2 
        self.assertWidgetDimensions(self.buttontopleft,0.01,**_defaultframe)
        
    def test_bottomleft(self):
        
        _defaultframe = dict(defaultframe)
        _defaultframe['height'] = _defaultframe['height']/2 
        _defaultframe['width'] = _defaultframe['width']/2 
        _defaultframe['y'] = _defaultframe['height']
        
        self.assertWidgetDimensions(self.buttonbottomleft,0.01,**_defaultframe)
        
    def test_topright(self):
        # x/y offsets are relative to the right hand frame so same
        # as previous 2
        _defaultframe = dict(defaultframe)
        _defaultframe['height'] = _defaultframe['height']/2 
        _defaultframe['width'] = _defaultframe['width']/2 
        
        self.assertWidgetDimensions(self.buttontopright,0.01,**_defaultframe)
        
    def test_bottomright(self):
        
        _defaultframe = dict(defaultframe)
        _defaultframe['height'] = _defaultframe['height']/2 
        _defaultframe['width'] = _defaultframe['width']/2 
        _defaultframe['y'] = _defaultframe['height']
        
        self.assertWidgetDimensions(self.buttonbottomright,0.01,**_defaultframe)
        
    def tearDown(self):
        
        self.leftframe.destroy()
        self.rightframe.destroy()
        self.master.destroy() 
        
class TestUIGrid2x2even(TestWidget):
    
    # basic grid; default widget sizes
    def setUp(self):
        self.master = Tk()
        
        self.custommaster = dict(height=52,width=166,x=0,y=0)

        self.button1 = Button(self.master,text="N")
        self.button1.grid(row=0,column=0,sticky=NW) 
        self.button2 = Button(self.master,text="SW")
        self.button2.grid(row=0,column=1,sticky=SW) 
        self.button3 = Button(self.master,text="NE")
        self.button3.grid(row=1,column=0,sticky=NE)
        self.button4 = Button(self.master,text="SE")
        self.button4.grid(row=1,column=1,sticky=SE)
        
    def test_master(self):
        self.assertWidgetDimensions(self.master,0.01,**self.custommaster)
    
    def test_nwbutton(self):
        self.custommaster['height'] = self.custommaster['height']/2 
        self.custommaster['width'] = self.custommaster['width']/2 
        
        self.assertWidgetDimensions(self.button1,0.01,**self.custommaster)
        
    def test_sebutton(self):
        self.custommaster['height'] = self.custommaster['height']/2 
        self.custommaster['width'] = self.custommaster['width']/2 
        self.custommaster['y'] = self.custommaster['height']
        self.custommaster['x'] = self.custommaster['width']

        self.assertWidgetDimensions(self.button4,0.01,**self.custommaster)

    def tearDown(self):
        self.master.destroy()

class TestUIGrid2x2evenlarge(TestWidget):
    
    # tests a grid that forces child widgets to expand
    # expand in a grid is accomplished by sticky=NSEW and
    # row and columnconfigure
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))

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

    def test_master(self):
        self.assertWidgetDimensions(self.master,0.01,**defaultmaster)

    def test_bottomright(self):
        
        _defaultmaster = dict(defaultmaster)
        
        _defaultmaster['height'] = _defaultmaster['height']/2 
        _defaultmaster['width'] = _defaultmaster['width']/2 
        _defaultmaster['y'] = _defaultmaster['height']
        _defaultmaster['x'] = _defaultmaster['width']
        
        self.assertWidgetDimensions(self.button4,0.01,**_defaultmaster)
        
    def tearDown(self):
        self.master.destroy()
        
        
class TestUIGridFocus(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.maxrows=10 # rows in the grid
        self.maxcols=10 # cols in the grid
        self.maxwidgets=self.maxrows*self.maxcols
        self.wwidth=48 # default button width with text of 3 chars
        self.wheight=29 # default button height
        self.wmheight=self.wheight*self.maxrows # master height
        self.wmwidth=self.wwidth*self.maxcols # master width

        widget_args=dict(background='white')
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)


        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                                 'peach','pomegranate','passionfruit',
                                                                 'pear','grape','strawberry','raspberry',
                                                                 'rhubarb','mango','guava','apple',
                                                                 'Orange'])
        
        self.tkilg = TkImageLabelGrid(self.master,self.setmemberp,self.wmwidth,self.wmheight,
                                      0,0,7,5,{},widgetcfg)
        
        

    def test_master(self):
        self.master.mainloop()

                                    
class TestUIGrid7x5odd(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.maxrows=7 # rows in the grid
        self.maxcols=5 # cols in the grid
        self.maxwidgets=self.maxrows*self.maxcols
        self.wwidth=48 # default button width with text of 3 chars
        self.wheight=29 # default button height
        self.wmheight=self.wheight*self.maxrows # master height
        self.wmwidth=self.wwidth*self.maxcols # master width

        self.mytextalphanum = TextAlphaNum(name='textalphanum')
        self.tkilg = TkImageLabelGrid(self.master,self.mytextalphanum,self.wmwidth,self.wmheight,
                                      0,0,7,5)
        
        

    def test_master(self):
        #self.master.mainloop()
        
        exp_results = dict(height=self.wmheight,
                           width=self.wmwidth,
                           x=0,
                           y=0)
        self.assertWidgetDimensions(self.master,0.01,**exp_results)
        
        self.assertEquals(len(self.master.children),self.maxwidgets)
        
        
    def test_middle(self):
        
        row=2
        col=3
        
        widget = self.tkilg.widgets[2][3]
        exp_results = dict(height=self.wheight,
                           width=self.wwidth,
                           x=self.wwidth*col,
                           y=self.wheight*row)
        self.assertWidgetDimensions(widget,0.01,**exp_results)
        
    def test_bottomright(self):
        
        row=6
        col=4

        widget = self.tkilg.widgets[6][4]
        
        exp_results = dict(height=self.wheight,
                           width=self.wwidth,
                           x=self.wwidth*col,
                           y=self.wheight*row)
        self.assertWidgetDimensions(widget,0.01,**exp_results)
        
    def tearDown(self):
        self.master.destroy()
        
class TestUIGridCustom(TestWidget):      
    # tests having top and side header rows/columns a different width
    
    def setUp(self):
        self.master = Tk()
        self.maxrows=7 # rows in the grid
        self.maxcols=5 # cols in the grid
        #self.maxwidgets=self.maxrows*self.maxcols
        self.wmheight=500 # master height
        self.wmwidth=500 # master width
        
        image_args = dict(pointsize=48,font='Helvetica',gravity='center',
                          rotate=90,label='foobar')
    
        gridcfg = nxnarraycreate(self.maxrows,self.maxcols,image_args)

        widget_args=dict(background='white',text='foo',borderwidth=2)
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)

        rowcfg = dict(width=2,foreground='yellow',text="x",background='green')
        colcfg = dict(height=2,foreground='yellow',text="y")
        
        self.mytextalphanumro = TextAlphaNumRO(name='textalphanum')
        
        self.tkilg = TkImageLabelGrid(self.master,self.mytextalphanumro,self.wmwidth,self.wmheight,
                                      0,0,self.maxrows,self.maxcols,
                                      gridcfg,widgetcfg,1,1,rowcfg,colcfg)
        
        self.tkilg.cell_set(0,0,**dict(background='white',width=2,height=2))
        self.tkilg.cell_set(1,1,**dict(background='pink',width=2,height=2))
                            
    def test_origin(self):
        exp_results = dict(height=36,width=22,x=0,y=0)
        self.assertWidgetDimensions(self.tkilg.widgets[0][0],0.01,**exp_results)
        
        
    def test_topheader(self):
        
        exp_results = dict(height=36,width=120,x=22,y=0)
        self.assertWidgetDimensions(self.tkilg.widgets[0][1],0.01,**exp_results)
        
    def test_left_leftheader(self):
        
        exp_results = dict(height=77,width=22,x=0,y=36)
        self.assertWidgetDimensions(self.tkilg.widgets[1][0],0.01,**exp_results)
    
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

    def test_master(self):
        
        exp_results = dict(height=58,width=97,x=0,y=0)
        self.assertWidgetDimensions(self.master,0.01,**exp_results)
    
    def test_lowerbutton(self):

        exp_results = dict(height=29,width=97,x=0,y=29)
        self.assertWidgetDimensions(self.button4,0.01,**exp_results)

    def tearDown(self):
        self.master.destroy()
        
class TestUIGrid2x2spanlarge(TestWidget):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get(**defaultmaster))
        
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

    def test_lowerbutton(self):

        _defaultmaster = dict(defaultmaster)
        
        _defaultmaster['height'] = _defaultmaster['height']/2 
        #defaultmaster['width'] = defaultmaster['width']
        _defaultmaster['y'] = _defaultmaster['height']
        _defaultmaster['x'] = 0
        #self.master.mainloop()
        self.assertWidgetDimensions(self.button4,0.01,**_defaultmaster)
 
    def tearDown(self):
        self.master.destroy()

class TestUILabelImage(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        custommaster = dict(height=800,width=200,
                             x=100,y=100)        

        self.master.geometry(geometry_get(**custommaster))
        
        self.image_args = dict(pointsize=48,
                               font='Helvetica',
                               gravity='center',
                               rotate=90)
        
        self.ic = ImageCreate()
        
    def test_label(self):
        
        label='foobar'
        
        self.mytextalphanumro = TextAlphaNumRO(name='textalphanum')
        
        self.lbl = tkwidgetfactory(self.mytextalphanumro,self.master)
        self.lbl.pack(fill=BOTH,expand=1)

        tkwidgetimage_set(self.ic,self.lbl,label,True,**self.image_args)
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   label,self.lbl.image_args)
    
        self.assertFilesEqual(exp_res,self.lbl.image)
        self.assertTrue(isinstance(self.lbl,Tklabel))
        
    def test_button(self):
        
        label='foobar'
        
        self.mytextalphanumro = TextAlphaNumRO(name='textalphanum')
        
        self.lbl = tkwidgetfactory(self.mytextalphanumro,self.master)
        self.lbl.pack(fill=BOTH,expand=1)

        tkwidgetimage_set(self.ic,self.lbl,label,True,**self.image_args)
    
        # extent gets determined by image_set method
        self.image_args['extent'] = self.lbl.image_size
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   label,self.image_args)
    
        self.assertFilesEqual(exp_res,self.lbl.image)
        self.assertTrue(isinstance(self.lbl,Tkbutton))
        
        
    def tearDown(self):
        self.master.destroy()
        

class TestUIFrameResizeFont(TestWidget):
    def setUp(self):
        self.master = Tk()
      
        self.maxrows=20 # rows in the grid
        self.maxcols=20 # cols in the grid
        self.wmheight=1300 # master height
        self.wmwidth=1200 # master width  

        custommaster = dict(height=self.wmheight,width=self.wmwidth,
                            x=0,y=0)        
    
        self.master.geometry(geometry_get(**custommaster))
        
        image_args = dict(pointsize=8,font='Helvetica',gravity='center',
                          rotate=0,label='foobar')
        gridcfg = nxnarraycreate(self.maxrows,self.maxcols,image_args)

        widget_args={'background':'white'}
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)

        
        self.mytextalphanumro = TextAlphaNumRO(name='textalphanum')
        
        self.tkilg = TkImageLabelGrid(self.master,self.mytextalphanumro,self.wmwidth,self.wmheight,
                                      0,0,self.maxrows,self.maxcols,
                                      gridcfg,widgetcfg)
        #self.tkilg = False
        
    def test_(self):
        
        self.master.bind('<Configure>',self.tkilg._draw)
        
        #self.tkilg.image_set()
        self.master.mainloop()

    
class TestUIFrameResize(TestWidget):

    def setUp(self):
        self.master = Tk()
        self.width=1200
        self.height=1300
        self.x=100
        self.y=100
        self.geom = geometry_get(self.height,self.width,
                                  self.x,self.y)        
        self.master.geometry(self.geom)
        
        self.frame = Frame(self.master)
        self.frame.place(width=200,height=200,x=100,y=100)
        self.frame.config()

        self.idle = False
      
        self.master.grid_columnconfigure(0, weight=1, uniform="foo")
        self.master.grid_rowconfigure(0, weight=1, uniform="foo2")
        
        self.frame.grid_columnconfigure(0, weight=1, uniform="foo")
        self.frame.grid_rowconfigure(0, weight=1, uniform="foo2")

        self.lbl = TkImageLabel(self.frame)
        self.lbl.grid(row=0,column=0,sticky=NSEW) 
    
        self.image_args = dict(pointsize=16,
                          font='Helvetica',
                          gravity='center',
                          rotate=90)

        self.draw()
        
        def d(event):
            if self.idle == False:
                self.master.after(1000,self.draw)
                self.idle = True
                
            
        self.master.bind('<Configure>',d)     
        
    def draw(self):
        

        
        self.idle = False
        self.lbl.image_set('foobar',**self.image_args)
        self.image_args['extent'] = self.lbl.image_size
        print "in draw"
            
    def test_(self):
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   'foobar',self.image_args)
    
        self.assertFilesEqual(exp_res,self.lbl.image)
        
        self.master.after(1000)
        self.frame.place(width=800,height=200,x=200,y=200)
        self.frame.config()
        self.master.update_idletasks()
        self.master.after(1000)
        self.master.update()
        
        self.image_args['extent'] = self.lbl.image_size
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   'foobar',self.image_args)
    
        self.assertFilesEqual(exp_res,self.lbl.image)    
        
        self.master.mainloop()

    def tearDown(self):
        self.master.destroy()
        
class TestUIButton(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        
    def test_font(self):

        font = tkFont.Font(family="Monospace", size=20)
        
        button = Tkbutton(self.master,font=font,text='foobar')
        button.pack(side=LEFT, fill=BOTH,expand=1)
        
    def tearDown(self):
        self.master.destroy()
        
    
class TestUILabel(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        self.width=800
        self.height=600
        self.x=0
        self.y=0
        self.geom = geometry_get(self.height,self.width,
                                  self.x,self.y)
        self.master.geometry(self.geom)
        
    def test_pack(self):
        
        lbl = Tklabel(self.master,text='text')
        lbl.pack(fill=BOTH,expand=1)
        
        exp_results = dict(height=self.height,width=self.width,x=0,y=0)
        self.assertWidgetDimensions(lbl,0.01,**exp_results)

    def test_pack_font(self):
        
        font = tkFont.Font(family="Helvetica", size=64)  
        lbl = Tklabel(self.master,text='text', font=font)
        lbl.pack(fill=BOTH,expand=1)

        exp_results = dict(height=self.height,width=self.width,x=0,y=0)
        self.assertWidgetDimensions(lbl,0.01,**exp_results)
     
    def tearDown(self):
        self.master.destroy()
        
class TestUIComboImageGrid(TestWidget):
    
    def setUp(self):
        self.master = Tk()
        
        self.maxrows=2 # rows in the grid
        self.maxcols=2 # cols in the grid
        self.wmheight=400 # master height
        self.wmwidth=400 # master width
        
        image_args = dict(pointsize=48,font='Helvetica',gravity='center',
                          rotate=90,label='foobar')
        gridcfg = nxnarraycreate(self.maxrows,self.maxcols,image_args)
        
        widget_args={}
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                                 'peach','pomegranate','passionfruit',
                                                                 'pear','grape','strawberry','raspberry',
                                                                 'rhubarb','mango','guava','apple',
                                                                 'Orange'])
        
        self.tkilg = TkImageLabelGrid(self.master,self.setmemberp,self.wmwidth,self.wmheight,
                                      0,0,self.maxrows,self.maxcols,
                                      gridcfg,widgetcfg)

        #self.tkilg.image_set()
        
    def test_topleft(self):

        self.tkilg.widgets[0][0].sv.set('passion')
        self.assertEqual(self.tkilg.widgets[0][0].sv.get(),'passionfruit')
        self.master.mainloop()
        
        
    def tearDown(self):
        self.master.destroy()
        
class TestUIVentryImageGrid(TestWidget):
    pass

class TestUILabelImageGrid(TestWidget):
                    
    def setUp(self):
        self.master = Tk()
        
        self.maxrows=2 # rows in the grid
        self.maxcols=2 # cols in the grid
        self.wmheight=400 # master height
        self.wmwidth=400 # master width

        image_args = dict(pointsize=48,font='Helvetica',gravity='center',
                          rotate=90,label='foobar')
        gridcfg = nxnarraycreate(self.maxrows,self.maxcols,image_args)
        
        widget_args={}
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        gridcfg[1][1]['rotate'] = 270
        

        self.mytextalphanumro = TextAlphaNumRO(name='textalphanum')
                
        self.tkilg = TkImageLabelGrid(self.master,self.mytextalphanumro,self.wmwidth,self.wmheight,
                                      0,0,self.maxrows,self.maxcols,
                                      gridcfg,widgetcfg)

        self.tkilg.image_set()

    def test_topleft(self):

        self.master.mainloop()
        widget = self.tkilg.widgets[0][0]
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   widget.label,widget.image_args)
    
        self.assertFilesEqual(exp_res,widget.image)
        
    def test_bottomright(self):
        
        widget = self.tkilg.widgets[1][1]
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   widget.label,widget.image_args)
    
        self.assertFilesEqual(exp_res,widget.image)

        
    def test_topright(self):
        
        widget = self.tkilg.widgets[0][1]
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   widget.label,widget.image_args)
    
        self.assertFilesEqual(exp_res,widget.image)

    def test_bottomleft(self):
        
        widget = self.tkilg.widgets[1][0]
        
        exp_res = get_gif_filename('/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs',
                                   widget.label,widget.image_args)
    
        self.assertFilesEqual(exp_res,widget.image)
        
    def tearDown(self):
        self.master.destroy()
        
class TestUILabelImageGridCustom(TestWidget):       
                    
    def setUp(self):
        self.master = Tk()
        self.maxrows=7 # rows in the grid
        self.maxcols=5 # cols in the grid
        #self.maxwidgets=self.maxrows*self.maxcols
        self.wmheight=500 # master height
        self.wmwidth=500 # master width

        image_args = dict(pointsize=16,font='Helvetica',gravity='center',
                          rotate=90,label='foobar')
        gridcfg = nxnarraycreate(self.maxrows,self.maxcols,image_args)
        
        widget_args=dict(background='black',text='foo')
        widgetcfg = nxnarraycreate(self.maxrows,self.maxcols,widget_args)
        
        rowcfg = dict(height=2,fg='yellow',text="x")
        colcfg = dict(width=2,fg='yellow',text="y")
        
        self.mytextalphanumro = TextAlphaNumRO(name='textalphanum')
        
        self.tkilg = TkImageLabelGrid(self.master,self.mytextalphanumro,self.wmwidth,self.wmheight,
                                      0,0,self.maxrows,self.maxcols,
                                      gridcfg,widgetcfg,1,1,rowcfg,colcfg)

        self.tkilg.cell_set(0,0,**dict(background='yellow',width=2,height=2))
        self.tkilg.cell_set(1,1,**dict(background='pink',width=2,height=2))

    def test_origin(self):
        
        self.tkilg.image_set()
        #self.tkilg.image_show()
        exp_results = dict(height=34,width=20,x=0,y=0)
        self.assertWidgetDimensions(self.tkilg.widgets[0][0],0.01,**exp_results)
        
        #self.master.mainloop()

    def test_topheader(self):
        
        exp_results = dict(height=34,width=120,x=20,y=0)
        self.assertWidgetDimensions(self.tkilg.widgets[0][1],0.01,**exp_results)
        
        #self.master.mainloop()
        
    def test_left_leftheader(self):
        
        exp_results = dict(height=77,width=20,x=0,y=34)
        self.assertWidgetDimensions(self.tkilg.widgets[1][0],0.01,**exp_results)
        
        #self.master.mainloop()'''
        
    def tearDown(self):
        self.master.destroy()
        
class TestTkcomboSetMember(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.setmemberp = SetMemberPartial(name='x{mylist}',set=['pineapple','grapefruit','banana',
                                                                 'peach','pomegranate','passionfruit',
                                                                 'pear','grape','strawberry','raspberry',
                                                                 'rhubarb','mango','guava','apple',
                                                                 'Orange'])
        
        self.combo = TkCombobox(self.master,self.setmemberp)
        
    def test_(self):
        self.combo.sv.set('p')
        self.assertEqual(self.combo.label.cget('text'),9)
        
    def tearDown(self):
        self.master.destroy()
        
class TestTkcomboDBSetMember(unittest.TestCase):
    def setUp(self):
        dbname = '/data/food'
        tbl_name = 'food'
        fldname = 'food_name'
        self.dbsetmember = DBSetMember(dbname,tbl_name,
                                     fldname,
                                     name='x{dblist}')
        
        self.master = Tk()
        self.master.geometry(geometry_get_dict(defaultmaster))  
        
        self.combo = TkCombobox(self.master,self.dbsetmember)
        
    def test_(self):
        
        self.combo.sv.set('d')
        self.assertEqual(self.combo.label.cget('text'),65)
        
        
    def tearDown(self):
        self.master.destroy()
        
if __name__ == "__main__":

    suite = unittest.TestSuite()

    '''
    # Test helper
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTestWidget))
    
    # Widget Factory
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkWidgetFactory))
    
    # Font Scaling
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFontScale))
    
    # Root/master window
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIRoot))
    
    # Frame
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIFrame))
    
    # Pack
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIPack))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIPack2x2))

    # ImageWidget
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelImage))

    # Grid
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2even))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2evenlarge))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid7x5odd))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGridCustom))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2span))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid2x2spanlarge))
    
    # ImageWidgetGrid
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelImageGrid))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUILabelImageGridCustom))

    # Button
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIButton))
    
    # LabelImageResizing    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIFrameResize))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIFrameResizeFont))
    '''
    
    # Combo
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkcomboSetMember))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkcomboDBSetMember))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTkComboBox))
    
    # Entry
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIVentryImageGrid))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIComboImageGrid))
    
    
    # Focus
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGridFocus))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)