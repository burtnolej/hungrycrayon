
import unittest

from getopt import getopt, GetoptError

class TestGetopt(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_long_1arg_novalue(self):
        
        # first argument is the args that have been read in. this would be 
        # replaced by sys.argv in normal operation
        # second argument is the validation rules, so in this case we should expect
        # 1 type of option with no value
        rules = ['noarg']
        validargs = ['--noarg']
        
        options,remainder = getopt(['--noarg'],'',rules)
        for option, value in options:
            self.assertIn(option,validargs)
         
        # its also valid to pass in no arg  
        options,remainder = getopt([],'',rules)
        for option, value in options:
            self.assertIn(option,validargs)
            
        # but will fail if an unknown arg is passed in  
        with self.assertRaises(GetoptError):
            options,remainder = getopt(['--foobar'],'',rules)
    
        # but will fail if a value for option is passed in
        with self.assertRaises(GetoptError):
            options,remainder = getopt(['--noarg=foobar'],'',rules)

    def test_long_multiargs_novalue(self):
        
        rules = ['noarg','noarg2']
        validargs = ['--noarg','--noarg2']
        options,remainder = getopt(['--noarg','--noarg2'],'',rules)
        for option, value in options:
            self.assertIn(option,validargs)
         
        # its also valid to pass in no arg  
        options,remainder = getopt([],'',rules)
        for option, value in options:
            self.assertIn(option,validargs)
            
        # but will still fail if an unknown arg is passed in  
        with self.assertRaises(GetoptError):
            options,remainder = getopt(['--foobar'],'',rules)
    
        # but will work if we just pass 1
        options,remainder = getopt(['--noarg2'],'',rules)
        for option, value in options:
            self.assertIn(option,validargs)
            
    def test_long_multiargs_withvalue(self):
        
        rules = ['noarg','noarg2','witharg=']
        validargs = ['--noarg','--noarg2','--witharg']
        options,remainder = getopt(['--witharg=foobar'],'',rules)

        self.assertEquals(options[0][0],'--witharg')
        self.assertEquals(options[0][1],'foobar')

        
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetopt)
    
    unittest.TextTestRunner(verbosity=2).run(suite)