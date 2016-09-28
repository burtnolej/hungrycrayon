import unittest
from image_utils import ImageCreate, rgbstr_get, get_gif_filename
import magic
import Image
from subprocess import call, check_output
import sys
from misc_utils_process import *
from time import sleep
from datetime import datetime
from collections import OrderedDict

settings = ['gravity','background','pointsize','font']
image_operator = ['rotate','extent']
  
class TestImageCreateBasic(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
    
    def test_create_1image_basic(self):
    
        args=OrderedDict()
        inputfiles = "foobar"
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        result = p.stdout.read().find('differ')
        self.assertEquals(result,-1)
        
    def test_create_1image_basic_fail(self):
    
        args=OrderedDict()
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.inputfiles = "foobdddar"
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        result = pstdout.find('differ')
        self.assertNotEquals(result,-1)

    def tearDown(self):
        import os
        self.ic = ImageCreate()
        os.remove(self.outputfiles[0])
        
class TestImageCreatepointsize(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_pointsize_64(self):

        args = OrderedDict(pointsize=64)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        result = p.stdout.read().find('differ')
        self.assertEquals(result,-1)
        
    def test_create_1image_pointsize_12(self):

        args = OrderedDict(pointsize=12)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        result = p.stdout.read().find('differ')
        self.assertEquals(result,-1)
        
    def test_create_1image_pointsize_24(self):

        args = OrderedDict(pointsize=24)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        result = p.stdout.read().find('differ')
        self.assertEquals(result,-1)
        
    def tearDown(self):
        import os
        self.ic = ImageCreate()
        os.remove(self.outputfiles[0])
        
class TestImageCreateBackground(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_background_red(self):

        red = '#%02x%02x%02x' % (255, 0, 0)

        args = OrderedDict(background=red)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        result = p.stdout.read().find('differ')
        self.assertEquals(result,-1)
        
    def test_create_1image_background_tkgrey(self):

        args = OrderedDict(background='#d6d2d0')
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
        
        result = p.stdout.read().find('differ')
        self.assertEquals(result,-1)
        
    def test_create_1image_background_fail(self):

        red = '#%02x%02x%02x' % (255, 0, 0)
        blue = '#%02x%02x%02x' % (0, 0, 255)

        args = OrderedDict(background=red)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        args = OrderedDict(background=blue)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertNotEquals(pstdout.find('differ'),-1)
    
    def tearDown(self):
        import os
        self.ic = ImageCreate()
        os.remove(self.outputfiles[0])
        
class TestImageCreateRotate(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_rotate90(self):

        args = OrderedDict(rotate=90)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def test_create_1image_rotate270(self):

        args = OrderedDict(rotate=270)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def tearDown(self):
        import os
        os.remove(self.outputfiles[0])
      
class TestImageCreateextent(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_extent200x200(self):

        args = OrderedDict(extent='200x200')
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def test_create_1image_extent200x800(self):

        args = OrderedDict(extent='200x800')
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def tearDown(self):
        import os
        os.remove(self.outputfiles[0])
       
class TestImageCreateGravity(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_gravitycenter(self):

        args = OrderedDict(gravity='center')
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def tearDown(self):
        import os
        os.remove(self.outputfiles[0])
        
class TestImageCreateFont(unittest.TestCase):
    
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_fonthelvetica(self):

        args = OrderedDict(font='Helvetica')
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def tearDown(self):
        import os
        os.remove(self.outputfiles[0])

class TestImageCreateMultiSetting(unittest.TestCase):
    

    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = "foobar"
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
        
    def test_create_1image_red800x200(self):
        
        ''' setting and image operator - so testing that args are going 
        either side of label/file'''

        red = '#%02x%02x%02x' % (255, 0, 0)
        
        args = OrderedDict(background=red,extent='800x200')
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def test_create_1image_red_48(self):
        
        ''' 2 settings '''

        red = '#%02x%02x%02x' % (255, 0, 0)
        
        args = OrderedDict(background=red,pointsize=48)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def test_create_1image_red_48_Helvetica_90_800x200(self):
        
        ''' all settings '''

        red = '#%02x%02x%02x' % (255, 0, 0)
        
        args = OrderedDict(background=red,
                           pointsize=48,
                           extent='800x200',
                           font='Helvetica',
                           rotate=90)
        exp_res = get_gif_filename(self.testfiledir,self.inputfiles,args)
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        cmd = ['diff',self.outputfiles[0],exp_res]
               
        p = process_start(cmd)
    
        pstdout = p.stdout.read()

        if pstdout.find('No such file or directory') <> -1:
            
            raise Exception('no reference gif for this test',exp_res)
        
        self.assertEquals(pstdout.find('differ'),-1)
        
    def tearDown(self):
        import os
        os.remove(self.outputfiles[0])
             
class TestImageCreateMultiFile(unittest.TestCase):
        
    def setUp(self):
        
        self.ic = ImageCreate()
        self.inputfiles = ['foobar','barfoo']
        self.testfiledir = "/home/burtnolej/Development/pythonapps3/clean/utils/test_gifs"
      
    def test_create_1image_largefont_multi(self):
        
        red = '#%02x%02x%02x' % (255, 0, 0)
        
        args = OrderedDict(background=red,
                           pointsize=48,
                           extent='800x200',
                           font='Helvetica',
                           rotate=90)
        
        exp_res = [get_gif_filename(self.testfiledir,lbl,args) for lbl in self.inputfiles]
        
        self.outputfiles = self.ic.create_image_file(self.inputfiles,**args)
        
        for i in range(len(self.outputfiles)):
            cmd = ['diff',self.outputfiles[i],exp_res[i]]
                   
            p = process_start(cmd)
        
            pstdout = p.stdout.read()
    
            if pstdout.find('No such file or directory') <> -1:
                
                raise Exception('no reference gif for this test',exp_res)
            
            self.assertEquals(pstdout.find('differ'),-1)
        
    def tearDown(self):
        import os
        for f in self.outputfiles:
            os.remove(f)
       
class TestImageCreateFails(unittest.TestCase):
    def test_create_1image_badfontextent(self):

        ic = ImageCreate()
    
        inputfiles = "foobar"
        
        with self.assertRaisesRegexp(Exception,'ImageCreate failure'):
            outputfiles = ic.create_image_file(inputfiles,pointsize='ss')
        

if __name__ == "__main__":

    suite = unittest.TestSuite()
    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateBasic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreatepointsize))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateBackground))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateRotate))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateextent))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateGravity))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateFont))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateMultiSetting))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateMultiFile))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateFails))
    
    unittest.TextTestRunner(verbosity=2).run(suite)
