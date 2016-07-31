import sys
from os import walk, getcwd
from os.path import basename, splitext, join
import unittest
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from module_utils import __load_module__ as load_module


def testsuite_get(rootdir=None):
    
    if rootdir==None:
        rootdir=getcwd()
        
    suite = unittest.TestSuite()
    testsummary={}
    for root, dirs, files in walk(rootdir):
        for file in files:
            if file.startswith("test_") and splitext(file)[1] == ".py":
                try:
                    module = load_module(join(root,file))
                    
                    for item in dir(module):
                        if item.startswith('Test_'):
                            suite.addTest(unittest.TestLoader().loadTestsFromTestCase(getattr(module,item)))
                            print "info:loaded test=",str(item).ljust(20),"from",join(basename(root),file)
                            if not testsummary.has_key(file) == True:
                                testsummary[file] = []
                            testsummary[file].append(str(item))
                                
                except ImportError, e:
                    print "error",e
    return(suite, testsummary)

def testsuite_run(suite):
    return(unittest.TextTestRunner().run(suite))
    
def testsuite_results(testresult):
    
    print testresult.errors
    for testcase,trace in testresult.failures:
        _trace = trace.split("\n")
        print "failure",testcase, _trace[-2],basename(_trace[1])
    print testresult.testsRun
    
'''def printusage(msg):
    print "\nusage: --witharg [valid arg] | --noarg"
    print msg
    exit()

rules = ['input=']
input_file = None

try:
    options,remainder = getopt(sys.argv[1:],'',rules)
except GetoptError, e:
    printusage("error:",e.msg)

args={}
for option, value in options:
    if option == '--input':
        args[option[2:]] = value

if not args.has_key('input') or not isfile(args['input']):
    printusage("error: --input arg must be set to a real file")
    
xmlfile = py2xml(args['input'])
print "info: passing",xmlfile,"to xml2freemind"
fmfile = xml2freemind(xmlfile,1).output_filename
print "info: result written to",fmfile
'''


