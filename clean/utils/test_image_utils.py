import unittest
from image_utils import ImageCreate, rgbstr_get
import magic
import Image
from subprocess import call, check_output
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_process import *
from time import sleep
from datetime import datetime

class TestImageCreate(unittest.TestCase):
    
    def setUp(self):
        self.wait=0.25
        pass
    
    def test_create_1image_basic(self):
        
        #tkgrey = rgbstr_get(240,240,237)
        #white = rgbstr_get(255,255,255)
        #black = rgbstr_get(0,0,0)
    
        ic = ImageCreate()
    
        inputfiles = "basic"
        outputfiles = ic.create_image_file(inputfiles)

        im = Image.open(outputfiles[0])
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
        self.assertEquals(im.format,'GIF')
      
    def test_create_1image_largefont(self):
    
        ic = ImageCreate()
    
        inputfiles = "pointsize=64"
        outputfiles = ic.create_image_file(inputfiles,pointsize=64)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
    def test_create_1image_redbg(self):

        ic = ImageCreate()
        ps = 64
        red = rgbstr_get(255,0,0)
        
        inputfiles = "bg=red"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           background=red)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
    def test_create_1image_bluefg(self):

        ic = ImageCreate()
        ps = 64
        blue = rgbstr_get(0,0,255)
        
        inputfiles = "fill=blue"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           fill=blue)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
        
    def test_create_1image_rotate90c(self):

        ic = ImageCreate()
        ps = 64
        
        inputfiles = "rotate=90"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           rotate=90)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
    def test_create_1image_rotate90antic(self):

        ic = ImageCreate()
        ps = 64
        
        inputfiles = "rotate=-90"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           rotate=270)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
    def test_create_1image_size(self):

        ic = ImageCreate()
        ps = 64
        extent = '400x400'
        
        inputfiles = "size=400x400"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           extent=extent)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
    def test_create_1image_aligncenter(self):

        ic = ImageCreate()
        ps = 64
        extent = '400x400'
        gravity='center'
        
        inputfiles = "gravity=center"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           extent=extent,
                                           gravity=gravity)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
    def test_create_1image_font(self):
        
        '''convert -list font (to list fonts)'''

        ic = ImageCreate()
        ps = 64
        font = 'Ubuntu-Mono-Regular'
        
        inputfiles = "font=Ubuntu-mono font"
        outputfiles = ic.create_image_file(inputfiles,
                                           pointsize=ps,
                                           font=font)

        im = Image.open(outputfiles[0])
        self.assertEquals(im.format,'GIF')
        
        cmd = ['display','-geometry','750x750+7500+740',outputfiles[0]]
        p = process_start(cmd)
        sleep(self.wait)
        process_kill(p)
        
      
    def test_create_1image_largefont_multi(self):
        
        labels = ['Monday','Tuesday','Wednesday']
        ps = 64
        now =str(datetime.now().strftime("%m%d%y"))
        
        exp_res = []
        for lbl in labels:
            exp_res.append("ic_{0}/{1}-{2}.gif".format(now,lbl,ps))
    
        ic = ImageCreate()
    
        outputfiles = ic.create_image_file(labels,pointsize=ps)
        
        self.assertEquals(outputfiles,exp_res)
        
        self.assertEquals(len(outputfiles),3)
        
        for i in range(len(outputfiles)):
            im = Image.open(outputfiles[i])
            self.assertEquals(im.format,'GIF')
            
            cmd = ['display','-geometry','750x750+7500+740',outputfiles[i]]
            p = process_start(cmd)
            sleep(self.wait)
            process_kill(p)
        
        
        
class TestImageCreateFails(unittest.TestCase):
    def test_create_1image_badfontsize(self):

        ic = ImageCreate()
    
        inputfiles = "foobar"
        
        with self.assertRaisesRegexp(Exception,'ImageCreate failure'):
            outputfiles = ic.create_image_file(inputfiles,pointsize='ss')
        

if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreate))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestImageCreateFails))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)