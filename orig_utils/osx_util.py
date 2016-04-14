#!/usr/bin/python

import os
import commands

#fh = open("/private/tmp/slash.txt",'r')
#size = {}
#for line in fh:
#    size[int(line.split()[0])] = line.split()[1]##

#keys = size.keys()
#keys.sort()
#keys.reverse()

#for i in range(10):
#    fn = size[keys[i]]
#    print fn
#    stat = os.stat(fn)
#    print keys[i], fn, stat

import os
import commands
from collections import OrderedDict
from os.path import join, getsize, isfile, isdir, splitext

from sys import path,argv,exit,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import write_object_to_disk, read_object_from_disk, get_time_secs

def print_filedir(filedir):
    for filesize in filedir:
        filecount = len(filedir[filesize])
        print filesize*filecount,filesize,filecount
        
def dir_walk(path,write=False):
    filedir = OrderedDict()
    #path = "/"
    TotalSize = 0
    for item in os.walk(path):
        for fn in item[2]:
            try:
                ThisFileSize = getsize(join(item[0], fn))
                if not filedir.has_key(ThisFileSize):
                    filedir[ThisFileSize] = []
                filedir[ThisFileSize].append(item[0] +"/" + fn)
            except:
                print("error with file:  " + join(item[0], fn))

        
        master_filedir = read_object_from_disk("./filesystem.dat")
        if not master_filedir:
            master_filedir = OrderedDict()
        time_key = get_time_secs()
        master_filedir[time_key] = filedir
        write_object_to_disk(master_filedir,"./filesystem.dat")
        
        
        print_filedir(filedir)

def get_biggest_files(max_size=200):
    files = read_object_from_disk("./filesystem.dat")

    sizes = files.keys()
    sizes.sort()
    sizes.reverse()

    total_size = 0
    count=0
    big_count=0
    total_big_size=0
    for k,v in files.iteritems():
        if k/1024/1024 > max_size:
            print k/1024/1024,'MB',
            for filename in v:
                #if filename.split(".")[-1] in ['dmg','zip','gz']:
                print filename,
                #cmd = "ls " + "\"" + filename + "\""
                #print commands.getstatusoutput(cmd)
                big_count +=1
                total_big_size += k
            print
            
        total_size += k
        count += 1

    print 'total big size',total_big_size/1024/1024/1024,'GB','total big count',big_count
    print 'total size of rest',(total_size-total_big_size)/1024/1024/1024, 'GB','total count',count


#dir_walk("/",True)
get_biggest_files()
