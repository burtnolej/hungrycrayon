#!/usr/bin/python

import os
from os import stat
from os.path import getsize, join, isdir, isfile
from stat import *
from magic import from_file

from enum import Enum

FWDSLASH="/"

class enumOSWalk(Enum):
    abspath = 0
    files = 2

def read_osxfilesystem(rootdir):
    for subdir in os.walk(rootdir):
        for afile in subdir[enumOSWalk.files]:
            fullpath = subdir[enumOSWalk.abspath] + FWDSLASH + afile
            print afile + " is type " + from_file(fullpath) + " fullpath:" + fullpath


read_osxfilesystem("./test")
