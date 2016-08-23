from subprocess import Popen, STDOUT, PIPE
from time import sleep
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils_process import process_instances_get, process_kill, \
     process_start

from misc_utils_enum import enum
from image_utils import parse_convert_stdout
from os import remove
import unittest

class TestSubProcess(unittest.TestCase):
            
    def setUp(self):
        
        self.label = 'foobar'
        
    def test_success(self):

        # some external command to test with whose outputs are known
        cmd = ['convert','-verbose','label:'+self.label,'-pointsize','22','/tmp/foobar.gif']
        
        p = process_start(cmd)
        status = parse_convert_stdout(p,self.label)
        
        self.assertEquals(status[0],0)
        self.assertTrue(status[1],'37x13')
        self.assertTrue(status[2],'/tmp/foobar.txt')
        
    def test_failure(self):
        # known external command --verbose is a bad switch
        cmd = ['convert','--verbose','label:'+self.label,'-pointsize','22','/tmp/foobar.gif']
        
        p = process_start(cmd)
        status = parse_convert_stdout(p,self.label)
        self.assertTrue(status[0],1)
        
    def test_failure_grabstderr(self):
        # known external command --verbose is a bad switch
        cmd = ['convert','--verbose','label:'+self.label,'-pointsize','22','/tmp/foobar.gif']
        
        p = process_start(cmd)
        
        stderr =  parse_convert_stdout(p,self.label)[1]
        self.assertTrue(stderr.startswith('convert.im6'))
        
    def test_killprocess(self):
        
        import os
        import signal
        
        # some process that runs until killed
        cmd = ['display','-geometry','750x750+7500+740','/tmp/foobar.gif']
        
        process_start(cmd)
        pids=process_instances_get('display')
        self.assertEquals(len(pids),1)
        
        process_kill(pids[0][0])
        pids=process_instances_get('display')
        self.assertEquals(len(pids),0)
        
    def test_killprocess_popen(self):
        ''' passing in a Popen object not a pid '''
        import os
        import signal
        
        # some process that runs until killed
        cmd = ['display','-geometry','750x750+7500+740','/tmp/foobar.gif']
        
        p = process_start(cmd)
        pids=process_instances_get('display')
        self.assertEquals(len(pids),1)
        
        process_kill(p)
        pids=process_instances_get('display')
        self.assertEquals(len(pids),0)
        
class TestProcessUp(unittest.TestCase):
    
    def setUp(self):
        self.findpids=[]
        
        # some process that runs until killed
        cmd = ['find','/','-name','foobar','-print']

        for i in range(5):
            self.findpids.append(process_start(cmd))

    def test_processup(self):
        
        pids=process_instances_get('find')
        self.assertEquals(len(pids),5)
        
    def tearDown(self):
        
        for p in self.findpids:
            p.kill()


if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSubProcess))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestProcessUp))

    unittest.TextTestRunner(verbosity=2).run(suite)