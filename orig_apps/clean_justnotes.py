#!/usr/bin/python
from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from filesystem_util import read_dir, trim_justnotes_int_suffix,BadExtension
from misc_util import Logger
from tag_util import TaggedJSONFile
from shutil import copyfile,copystat,copy2
from os import path

#SOURCE_DIR = '/Users/burtnolej/Documents/Justnotes.Mar1'
SOURCE_DIR = '/Users/burtnolej/Documents/Justnotes.test'
TARGET_DIR = '/Users/burtnolej/Documents/Justnotes.new'

#l = Logger('/tmp/log.txt')

for abs_fn in read_dir(SOURCE_DIR):
    rel_fn = abs_fn.split("/")[-1]
    print 'cp',rel_fn,

    try:
        if abs_fn == trim_justnotes_int_suffix(abs_fn):

            new_abs_fn = path.join(TARGET_DIR,rel_fn) 
            print 'ok'
            copy2(abs_fn,new_abs_fn)
        else:
            print 'skip'
    except BadExtension,e:
        print 'bad file extension',e
