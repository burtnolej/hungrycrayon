
import sys
from os.path import isfile
from getopt import getopt, GetoptError, gnu_getopt

sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/scripts/xml2freemind")
from module_utils import py2xml
from xml2freemind import xml2freemind

def printusage(msg):
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


