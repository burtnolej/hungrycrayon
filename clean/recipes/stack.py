import unittest

class Test_Stack(unittest.TestCase):

    def test_get_caller_frame(self):
        
        from inspect import stack
        from os.path import basename
        
        def _func():
            
            currentstack = stack()
            #level =0
            #for frame in stack():
            #    print "level".rjust(20),str(level)
            #    print "frameobj".rjust(20),str(frame[0])
            #    print "sourcefile".rjust(20),basename(frame[1])
            #    print "lineno".rjust(20),frame[2]
            #   print "func".rjust(20),frame[3]
            #    print "code".rjust(20),";".join(frame[4]).strip()
            #    print
            #    level+=1
            
            currentframe = currentstack[0]
            callerframe = currentstack[1]
            
            self.assertEquals(basename(currentframe[1]),"stack.py")
            self.assertEquals(currentframe[3],"_func")
            self.assertTrue(int(currentframe[2]>0))
                   
        _func()
        
    def test_get_caller_frame(self):
        
        from inspect import stack
        from os.path import basename
        
        def _func():
            
            callerframe = stack()[1]
               
            self.assertEquals(basename(callerframe[1]),"stack.py")
            self.assertEquals(callerframe[3],"test_get_caller_frame")
            self.assertTrue(int(callerframe[2]>0))             
        _func()
            
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Stack)
    unittest.TextTestRunner(verbosity=2).run(suite) 