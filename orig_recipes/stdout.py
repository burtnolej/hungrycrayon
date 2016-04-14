#!/usr/bin/python

'''
in Logger class sets self.sys.stdout to logger handle
'''

from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Logger
logger = Logger()
del logger
