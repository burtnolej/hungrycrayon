#!/usr/bin/python

import os
from os import stat
import commands
from os.path import getsize, join, isdir, isfile
from stat import *
from magic import from_file
from inspect import getmembers
import simplejson as json
from multiprocessing.pool import ThreadPool
import threading
from time import strftime
from time import time
from subprocess import call, Popen, PIPE, check_output
from datetime_util import MyDT
from misc_util import get_filehandle, write_json_to_disk,functime
from elasticsearch_util import ElasticSearchHandler
from test_util import Tester
from datetime_util import MyDT

modes = {S_IFSOCK:'S_IFSOCK',S_IFLNK:'S_IFLNK',S_IFREG:'S_IFREG',S_IFDIR:'S_IFDIR',S_IFBLK:'S_IFBLK',S_IFCHR:'S_IFCHR',S_IFBLK:'S_IFBLK'}

class FlatFileSystem(dict):
    size = 0
    count = 0
    
    def add_file(self,file):
        self.__setitem__(file.inode,file)

    def pprintrecs(self):
        for k,v in self.iteritems():
            print
            v.pprint()

    def read_osxfilesystem(self,rootdir):
        self.root = rootdir
        for subdir in os.walk(rootdir):
            for f in subdir[2]:
                abs_name = join(subdir[0],f)
                parent_dir = abs_name.split("/")[-3]
                try:
                    f = File(f,abs_name,parent_dir)
                    self.add_file(f)
                    self.size = self.size + f.size
                    self.count+=1
                except Exception,e:
                    print "ERROR",abs_name
                
    def printstast(self):
        print "size(MB):",float(self.size/1024/1024),
        print "#files:",self.count,
        print "root:",self.root

    def getsize(self):
        return(self.size)

    def getcount(self):
        return(self.count)

class JSONFile(object):

    index='test-index'
    doc_type='tweet'
    
    def __init__(self,absname, relname=None,parent=None,es=None):
        self.parent = parent
        self.absname = absname
        self.relname = str(self.absname.split("/")[-1:][0])

        self.get_file_stat_all()
        self.type = self.get_file_type()
        self.dict_rep = self.as_dict()
        if es==None:
            pass
        else:
            self.write_json2es(es)
        #self.print_json2file(fh)
        #self.pprint()

    def get_file_stat(self,ref):
        sr = stat(self.absname)
        return(sr.__getitem__(ref))

    def get_file_stat_all(self):
        tz_str = 'Europe/London'
        
        sr = stat(self.absname)
        self.size = sr.__getitem__(ST_SIZE)
        self.inode = sr.__getitem__(ST_INO)
        self.uid = sr.__getitem__(ST_UID)
        self.gid = sr.__getitem__(ST_GID)
        access_s = sr.__getitem__(ST_ATIME)

        ## need to explicitly pass in the timeone
        try:
            self.access_dt = secs_to_datetime(access_s,tz_str)
            modify_s = sr.__getitem__(ST_MTIME)
            self.modify_dt = secs_to_datetime(modify_s,tz_str)
            create_s = sr.__getitem__(ST_CTIME)
            self.create_dt = secs_to_datetime(create_s,tz_str)
            self.mode = sr.__getitem__(ST_MODE)
        except:
            pass
                

    def get_file_type(self):
        try:
            result = from_file(self.absname)
            return(result)
        except Exception,e:
            return(None)
            
    def as_dict(self):
        d = {}
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                d.__setitem__(key,value)
        return(d)        
        
    def pprint(self):
        print(json.dumps(self.dict_rep, sort_keys=True, indent=4 * ' '))

    def print_json2file(self,fh):
        write_json_to_disk(self.dict_rep,fh)

    def write_json2es(self,es):
        es.add_record(self.dict_rep,self.index,self.doc_type)

def _read_osxfilesystem(rootdir):
    #print rootdir
    pass



class ReadOSXFileSystem(threading.Thread):
    '''
    traverse file system from 'rootdir'
    '''
    def __init__(self,rootdir,threads):
        self.reg_time = time() # time in secs when thread registered
        self.file_count = 0 # number of files in rootdir
        self.dir_size = 0 # total size of all files in rootdir
        threads.append(t) # add thread id to list for execution later
        

    def start(self):
        self.start_time = time() # time in secs when thread started
        
    def __del__(self):
        self.end_time = time()
        self.total_time = self.start_time - self.end_time
        self.avg_proc_time = self.file_count/self.total_time

    
def read_osxfilesystem(rootdir,es):
    global tsize
    global tcount
    stime=time()
    
    count = 0
    size = 0
    for subdir in os.walk(rootdir):
        for f in subdir[2]:
            abs_name = join(subdir[0],f)
            parent_dir = abs_name.split("/")[-3]
            try:
                f = JSONFile(f,abs_name,parent_dir,es)
                size = size + f.size
                del f
                count+=1
            except Exception,e:
                print e
            
    #print size,count,
    #print round(float(time()-stime),2),"mins",
    #print rootdir
    tsize+=size
    tcount+=count

def read_dir(rootdir,depth,maxdepth,threads,es):
    depth+=1
    global tsize,tcount
    for node in os.listdir(rootdir):
        abs_path = os.path.join(rootdir,node)
        if os.path.isdir(abs_path):
            if not os.path.islink(abs_path):
                if depth >= maxdepth:
                    # down 2 levels start checking now for size < 1gb
                    dir_size = getdirsize(abs_path) 
                    if dir_size < 500:
                        
                        t = threading.Thread(target=read_osxfilesystem, args=([abs_path,es]))
                        threads.append(t)
                        #print abs_path,t
                    else:
                        read_dir(abs_path,depth,maxdepth,threads,fh)
                else:
                    read_dir(abs_path,depth,maxdepth,threads)
        else:
            # its just a file
            try:
                f = File(node,abs_path,rootdir)
                tsize+=f.size
                tcount+=1
                del f
            except:
                pass
    
def stats(runs):
    tsize=0
    tcount=0
    for run in runs:
        tsize+=run.getsize()
        tcount+=run.getcount()
        #run.pprintrecs()
    print tcount,"files",round(float(tsize)/1024/1024,2),"MB",

@functime
def getdirsize_pipe(dir):
    try:
        #pipe = Popen(['du','-sm',dir],stdout=PIPE)
        pipe = Popen(['du','-sk',dir],stdout=PIPE)
        (pipeop,_) = pipe.communicate()
        print pipeop
        return(int(pipeop.split('\t')[0])*1024)
    except:
        pass

def get_file_stat(f,ref):
    '''ref=ST_SIZE'''
    sr = stat(f)
    print sr
    return(sr.__getitem__(ref))
                
def getdirsize(tag,start_path = '.',max_depth=2):
    '''
    we need to keep track of the size allocated to the dir inode
    each file is worth 34 and each dir 68. getdirsize uses du so
    takes that into account
    '''
    nodes=[]
    today = MyDT.now(display_fmt='%m-%d-%y').value
    time = MyDT.now(display_fmt='%H:%M:%S').value
    
    dirs=[]
    skip=[]
    cur_depth = len(start_path.split('/'))
    total_size=68

    # do files first as you wont want to iterated into dir if at max depth
    for f in os.listdir(start_path):
        fp = os.path.join(start_path, f)

        if os.path.isdir(fp):
            dirs.append(fp)
        else:
            try:
                file_size = os.path.getsize(fp)
                total_size += file_size
                total_size += 34
                nodes.append({'type':'file',
                              'path':start_path,
                              'name':f,
                              'tsize':total_size,
                              'fsize':file_size,
                              'date':today,
                              'time':time,
                              'secs':tag})
            except OSError, e:
                skip.append(fp)

    for d in dirs:
        if os.path.islink(d):
            total_size += 42
        elif os.path.ismount(d):
            total_size += 50 # guess
        else:
            if cur_depth<=max_depth:
                (_nodes,_size) = getdirsize(tag,d)
                total_size += _size
                nodes += _nodes
            else:
                file_size = int(gnu_du(d))
                total_size += file_size
                total_size += 68
                nodes.append({'type':'sum',
                              'path':start_path,
                              'name':d.split("/")[-1],
                              'tsize':total_size,
                              'fsize':file_size,
                              'date':today,
                              'time':time,
                              'secs':tag})

    return nodes,total_size

def create_empty_file(bs,c,fn):
    cmd_list = ['dd','if=/dev/zero','of='+fn,'bs='+str(bs),'count='+str(c)]
    run_cmd(cmd_list)

def gnu_du(fn):
    out_fd = open('/tmp/log.err','w')
    cmd_list=['/usr/local/bin/gnu_du',
              '-skb',
              '--apparent-size',
              fn]
    a = Popen(cmd_list,stdout=PIPE) # notice stderr
    (_pipe,_) = a.communicate()
    return(_pipe.split("\t")[0])
    
def run_cmd(cmd_list):
    out_fd = open('/tmp/log.err','w')
    a = Popen(cmd_list,stderr=out_fd) # notice stderr
    a.communicate()
    
def getdirsize2(start_path = '.',max_depth=2):
    total_size = 0
    file_count = 0
    skip = []
    dir_flag=True
    current_depth=0

    for dirpath, dirnames, filenames in os.walk(start_path):
        print dirnames
        # get current depth
        c_depth = len(dirpath.split('/'))

        # always size all the files in a dir
        for f in filenames:
            file_count+=1
            fp = os.path.join(dirpath, f)
                
            try:
                file_size = os.path.getsize(fp)
                total_size += file_size
                print 'file',fp,file_size,c_depth
            except OSError, e:
                print e
                skip.append(fp)
                pass

        # if we are at max depth sum the dirs at this level then exit
        if c_depth > max_depth:
            for d in dirnames:
                fp = os.path.join(dirpath, d)
                try:
                    file_size = os.path.getsize(fp)
                    total_size += file_size
                    print 'dir',fp,file_size,c_depth
                except OSError, e:
                    print e
                    skip.append(fp)
                    pass
            #return total_size,file_count,skip,dir_flag

def read_dir_iter(dir):
    
    if os.path.isdir(dir):
        for file in os.listdir(dir):
            abs_path = os.path.join(dir,file)
            yield abs_path
    #yield dir

def relname(fn):
    return(fn.split("/")[-1])
    
def read_dir(dir,extension=None):
    l=[]

    try:
        for file in os.listdir(dir):
            if file.endswith(extension):
                l.append(os.path.join(dir,file))
    except OSError:
        raise OSError
    return(l)


def read_file_delim(filename,delim,header=False):

    records,header = [],[]

    try:
        fh = open(filename, 'r+')
    except IOError:
        raise IOError

    header=None
    if header:
        header = fh.readline().split(delim)
        fh.next

    for line in fh:
        records.append(line.split(delim))

    return(header,records)
        

class BadExtension(Exception):
    pass

def trim_justnotes_int_suffix(full_s):
    '''
    trim the justnotes extension of *copy*<int> from a string
    '''

    
    from types import IntType

    #split out any extensions
    c=-1
    while (full_s[c] != '.'):
        c-=1
        
    s = full_s[:c]
    ext = full_s[c:]

    if ext!='.txt' and ext!='.txt~':
        raise BadExtension(ext)

    # loop until all consecutive int chars are popped off
    # the end of the string or until popped off = full string
    # which is what happens in edge case where filename is an int
    c=-1
    try:
        while ((type(int(s[c:])) == IntType) and
               s[c:] != s):
            c-=1
    except ValueError:
        pass

    c+=2

    #check then if " copy " is next
    if (s[c-6:c] == " copy "):
        return(s[:c-6]+ext)
    else:
        return(full_s)
    
if __name__ == '__main__':

    tests = [['filename copy 123.txt','filename.txt'],
             ['filename cpy 123.txt','filename cpy 123.txt'],
             ['filename copy 234343.txt','filename.txt'],
             ['filename copy.txt','filename copy.txt'],
             ['141344.txt','141344.txt']]

    for test in tests:
        if test[1] == trim_justnotes_int_suffix(test[0]):
            print "PASSED",test
        else:
            print "FAILED",test
    
    #es = ElasticSearchHandler()
    #fh = get_filehandle()
    #stime=time()
    #tsize=0
    #tcount=0

    #runs = []
    #threads = []
    #read_dir("/Users/burtnolej/Dev/",0,1,threads,es)
    #read_dir("/Users/burtnolej/Dev/pythonapps/util/fstest",0,1,runs,threads)

    #[t.start() for t in threads]
    #[t.join() for t in threads]

    #print round(float(tsize)/1024/1024,2),"mb",
    #print tcount,"files",
    #stats(runs)
    #print round(float((time()-stime)/60),2),"mins"

    #print getdirsize("/Users")
    #fh.close()

