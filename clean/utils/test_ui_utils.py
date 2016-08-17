from Tkinter import *
from ttk import *

import unittest

from ui_utils import tk_create_config, tkfrm_cfg, \
     tk_create_frame

def _dumpwgt2(wgt):
    
    attr = ['winfo_atom', 'winfo_atomname', 'winfo_cells', 'winfo_children', 'winfo_class', 'winfo_colormapfull', 'winfo_containing', 'winfo_depth', 'winfo_exists', 'winfo_fpixels', 'winfo_geometry', 'winfo_height', 'winfo_id', 'winfo_interps', 'winfo_ismapped', 'winfo_manager', 'winfo_name', 'winfo_parent', 'winfo_pathname', 'winfo_pixels', 'winfo_pointerx', 'winfo_pointerxy', 'winfo_pointery', 'winfo_reqheight', 'winfo_reqwidth', 'winfo_rgb', 'winfo_rootx', 'winfo_rooty', 'winfo_screen', 'winfo_screencells', 'winfo_screendepth', 'winfo_screenheight', 'winfo_screenmmheight', 'winfo_screenmmwidth', 'winfo_screenvisual', 'winfo_screenwidth', 'winfo_server', 'winfo_toplevel', 'winfo_viewable', 'winfo_visual', 'winfo_visualid', 'winfo_visualsavailable', 'winfo_vrootheight', 'winfo_vrootwidth', 'winfo_vrootx', 'winfo_vrooty', 'winfo_width', 'winfo_x', 'winfo_y']
    for a in attr:
        try:
            print a.ljust(20),getattr(wgt,a)()
        except TypeError:
            print a.ljust(20),'ERROR'
            pass
        
    for k,v in wgt.config().iteritems():
        print k.ljust(20),v[4]
    
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
    
class TestUIRoot(unittest.TestCase):

    def setUp(self):
        self.master = Tk()
        
    def test_draw_configure_root(self):
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        self.assertEquals(self.master.winfo_class(),'Tk')
        
    def test_draw_configure_root_with_str(self):
        cfg = '300x200+100+100'
        self.master.geometry(cfg)
        self.master.configure(background='red')
        self.assertEquals(self.master.winfo_class(),'Tk')
        
    def test_draw_configure_root_with_badstr(self):
        cfg = '300x200+100+x'
        with self.assertRaises(TclError):
            self.master.geometry(cfg)
        
    def tearDown(self):
        self.master.destroy()
        
class TestUIFrame(unittest.TestCase):
    
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
        self.assertEquals(self.frame.config()['height'][4],290)
        self.assertEquals(self.frame.config()['width'][4],190)
        
    def test_draw_frame_with_style(self):
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=180,width=280,x=10,y=10)
        self.frame.config()
        self.assertEquals(self.frame.config()['style'][4],
                          'mystyle.TFrame')

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()
         
    '''def test_draw_frame_with_config(self):
        self.frame = Frame(self.master)
        
        frame_style = Style()
        
        tk_create_config(frame_style,tkfrm_cfg,'myframe')
        tk_create_frame(self.master,'myframe')'''
 
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
        self.master.mainloop()
        
    def test_pack_sidebyside(self):
        #self.frame.pack()
        button = Button(self.master,text="Button1")
        button.pack(side=LEFT, fill=BOTH,expand=1)
        button = Button(self.master,text="Button2")
        button.pack(side=LEFT, fill=BOTH,expand=1)        
        #_dumpwgt2(self.frame)
        self.master.mainloop()
        
    def test_pack_ontop(self):
        #self.frame.pack()
        button = Button(self.master,text="Button1")
        button.pack(fill=BOTH,expand=1)
        button = Button(self.master,text="Button2")
        button.pack(fill=BOTH,expand=1)        
        #_dumpwgt2(self.frame)
        self.master.mainloop()
        
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
        self.master.mainloop()
        
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
        self.master.mainloop()
    
    def test_addentry_addtext(self):
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry.insert(0,'default value')
        self.master.mainloop()
        
    def test_addentry_add_delete_then_add(self):
        import time
        entry = Entry(self.frame)
        entry.pack(fill=X,expand=1)
        entry.insert(0,'default value')

        entry.delete(0,END)
        entry.insert(0,'another default value')
        
        self.master.mainloop()
        
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
        self.master.mainloop()
               
        
            
class TestUIGrid(unittest.TestCase):
    def setUp(self):
        self.master = Tk()
        self.master.geometry('300x200+100+100')
        self.master.configure(background='red')
        _style = Style()
        _style.configure('mystyle.TFrame',background='blue')
        self.frame = Frame(self.master,style='mystyle.TFrame')
        self.frame.place(height=160,width=260,x=20,y=20)
        self.frame.config()
        
    def test_add_grid(self):
        self.frame.grid(row=1,column=1)
        button = Button(self.master,text="NW")
        button.grid(row=1,column=1,sticky=NW) 
        button = Button(self.master,text="SW")
        button.grid(row=2,column=1,sticky=SW) 
        button = Button(self.master,text="NE")
        button.grid(row=1,column=2,sticky=NE)
        button = Button(self.master,text="SW")
        button.grid(row=3,column=3,sticky=SW)
        
        _dumpwgt2(self.frame)
        self.master.mainloop()

    def tearDown(self):
        self.frame.destroy()
        self.master.destroy()

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
    
if __name__ == "__main__":

    suite = unittest.TestSuite()
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIRoot))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIFrame))

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIGrid))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIPack))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIEntry))
  
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUIWidgets))
    unittest.TextTestRunner(verbosity=2).run(suite)
