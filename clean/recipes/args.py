
import unittest

from getopt import getopt, GetoptError, gnu_getopt

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
        options,remainder = getopt(['--witharg=foobar'],'',rules)

        self.assertEquals(options[0][0],'--witharg')
        self.assertEquals(options[0][1],'foobar')
        
        # combining novalue and value
        options,remainder = getopt(['--noarg','--witharg=foobar'],'',rules)
        for option, value in options:
            if option == '--witharg':
                self.assertNotEqual(value,"")  
            else:
                self.assertEqual(value,"")  
                
    def test_long_outoforder(self):
        
        # mixing value and no value args
        rules = ['noarg','witharg=']
        expected_result = [('--witharg','foobar'),('--noarg','')]
        options,remainder = getopt(['--witharg=foobar','--noarg'],'',rules)
        self.assertListEqual(options, expected_result)

        expected_result = [('--noarg',''),('--witharg','foobar')]
        options,remainder = getopt(['--noarg','--witharg=foobar'],'',rules)
        self.assertListEqual(options, expected_result)
        
    def test_catch_error_print_usage(self):
        # mixing value and no value args
        rules = ['noarg','witharg=']
   
        with self.assertRaises(GetoptError) as context:
            options,remainder = getopt(['--noarg=asdfsdf'],'',rules)
        
        if (str(context.exception) == 'option --noarg must not have an argument'):

            #print "\n\nusage: --witharg [valid arg] | --noarg"
            #print "error:",context.exception
            #print "\n"
            pass
    
    def test_from_cmdline(self):
        import sys
        rules = ['noarg','witharg=']
   
        # if you pass in a garbage option at cmdline getopt will ignore and keep
        # processing
        options,remainder = getopt(sys.argv,'',rules)
        
        # need to start from sys.argv[1:]
        with self.assertRaises(GetoptError) as context:
            options,remainder = getopt(sys.argv[1:],'',rules)
            
if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetopt)
    
    unittest.TextTestRunner(verbosity=2).run(suite)