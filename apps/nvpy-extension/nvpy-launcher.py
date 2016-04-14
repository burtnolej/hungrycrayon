from sys import path
path.append("/usr/share/nvpy/nvpy") 
from nvpy import main
from os import curdir, getcwd, chdir

# nvpy uses the CWD to look for cfg and db files/dirs
chdir("/home/burtnolej")

# launch nvpy
main("burtnolejusa")



