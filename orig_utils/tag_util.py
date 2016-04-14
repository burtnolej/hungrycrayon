import os.path
import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE
import shlex
from misc_util import write_object_to_disk, read_object_from_disk, Logger, get_filehandle,switch
from datetime_util import MyDT 
from filesystem_util import JSONFile,trim_justnotes_int_suffix
from inspect import getmembers
import datetime
from pytz import timezone


'''
class TagHandler:
   member functions: recover, persist
   member variables: files (Files), tags (Tags)
x
class Files isa dict(lists):
   key=inode
   value=TaggedJSONFile reference
   member functions: add (file_stat_vals),get (file_inode)
   member variables:

class Tags isa dict of lists:
   key=tagname
   value=list of TaggedJSONFile references

class TaggedJSONFile isa JSONFile

'''
 
def verbose(func):
    def _verbose(*args,**kwargs):
        pass
        #func(*args,**kwargs)
    return _verbose

class DatFile(object):
    def __init__(self,path,obj):
        self.path = path
        self.obj = obj

    def exists(self):
        return(os.path.isfile(self.path))

    def remove(self):
        self.logprint(self.path,'removed')
        os.remove(self.path)
        
    def recover(self):
        self.dat = read_object_from_disk(self.path)
        
        if self.compatible():
            self.logprint('recover',self.path,'with',len(self.dat.keys()),'items')
            return(self.dat)
        else:

            raise Exception('incompatible')

    @verbose
    def logprint(*args):
        print args

class TagDat(DatFile):
    def compatible(self):
        return(True)

class FilesDat(DatFile):
    def get_recovered_inst_var_sz(self):
        self.first_item = self.dat.__getitem__(self.dat.keys()[0])
        self.rec_inst_var_sz = self.first_item._get_num_methods(self.first_item)

    def get_inst_var_sz(self):
        inst = self.obj()
        self.inst_var_sz = inst._get_num_methods(inst)

    def compatible(self):
        self.get_recovered_inst_var_sz()
        self.get_inst_var_sz()
                
        if self.inst_var_sz != self.rec_inst_var_sz:
            print 'member variables in',self.path,'have changed',self.rec_inst_var_sz,'vs',self.inst_var_sz
            return(False)
 

            print self.first_item,'member variables in',self.path,'are the same' 
        return(True)

class Stats(object):

    def __init__(self):
        self.tag_exists=[]
        self.tag_added=[]
        self.tagged_file_exists={}
        self.tagged_file_added={}
        self.file_exists=[]
        self.file_added=[]
        self.file_skipped=[]
        
    def _get_stats(self):
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                yield key,value

    def pprint_summary(self):
        for key,value in self._get_stats():
            print key.ljust(20),len(value)

class TaggedJSONFile(JSONFile):
    def __init__(self,filename=None):
        ''' object representation of a flat file
        var:size,inode,uid,gid,atime,mtime,ctime,mode,type
        sub classed to add the associated tags

        if filename=None then create a dummy file to create a dummy
        TaggedJSONFile class instance with'''
        if filename==None:
            filename = '/tmp/tag_util.tmp'
            fh = open(filename,'w').close()
            
        super(TaggedJSONFile,self).__init__(filename)
        self._get_tags(filename)
        self._get_content(filename)

    def _pathify(filename):
        path = os.path.join(NOTESDIR,filename)
        return(path)

    def _get_tags(self,filename):
        self.tag_names = self.parse_output(self._run_openmeta(filename))
        
    def _get_content(self,filename):
        fh = get_filehandle(filename,'r')
        self.content = fh.read()
        fh.close()

    def _run_openmeta(self,filename):
        ''' wrapper around openmeta osx binary '''
        cli_args = ['openmeta']
        cli_args.append('-p')
        cli_args.append(filename)
        proc = Popen(
            cli_args,
            stdout=PIPE
            )
    
        stdout, stderr = proc.communicate()
        return stdout

    def parse_output(self,clioutputstring):
        '''extract list of tags from openmeta output '''
        lines = clioutputstring.splitlines()
        tags = shlex.split(lines[1][6:])
        return tags

    @staticmethod
    def get_relname(self):
        return(self.absname.split("/")[-1]) 

    @staticmethod
    def _get_userdef_methods():
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                yield key,value

    @staticmethod
    def _get_num_methods(self):
        i=0
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                i+=1
        return(i)
        
class Files(dict):

    _dirty = False

    def __init__(self,dat,stats=None):
        self.stats=stats
        self.dat=dat

    def add(self,tjf):
        ''' arg tfj=instance of TaggedJSONFile '''
        if not self._file_exists(tjf):
            self._add_file(tjf)

    def _add_file(self,tjf,similar=False):
        '''
        if similar==False, allow files to be added that only vary by a integer value suffix
        so if filename==testfile3.txt, then convert to testfile.txt.
        this will handle the Justnotes sync bug where it increments the filename integer suffix by 1 
        '''
        self.__setitem__(str(tjf.inode),tjf)
        self._dirty = True
        self.stats.file_added.append(tjf)
        self.logprint('file_added',tjf.inode)
            
    def get_file_size(self,tjf):
        return(tfj.size)
        
    def _file_exists(self,tjf):
        '''
        check whether a file exists by looking for its inode in memory
        '''
        if self.has_key(tjf.inode):
            self.stats.file_exists.append(tjf)
            self.logprint('file_exists',tjf.inode)
            return(True)
        else:
            return(False)

    def get_todays_files(self,dt_str=None):
        '''
        returns all the files created today if dt not specified
        dt can be any day specified in the format %Y-%m-%d
        '''
        if dt_str==None:
            dt = get_midnight_today()
            print dt
        else:
            dt = str_fmt_to_datetime(dt_str,'%Y-%m-%d')

        dt_1day = add_day_offset(dt)
        
        for k,v in self.iteritems():
            modify_dt_est = v.modify_dt.astimezone(timezone('US/Eastern'))
            if modify_dt_est > dt and modify_dt_est < dt_1day:
                print datetime_to_str_fmt(modify_dt_est,'%d/%m %H:%M'),
                print v.relname[:-4][:20].ljust(20),v.tag_names

    
    def get_inode_detail(self,inode):
        f = self.__getitem__(inode)
        print f.absname
        print f.access_dt
        print f.create_dt
        print f.modify_dt
        
    def persist(self):
        if self._dirty:
          no_files = len(self.keys())
          self.logprint('persist',self.dat.path,'with',no_files,'files')
          write_object_to_disk(self,self.dat.path)
        else:
            self.logprint(self.__class__,'has no changes to persist')

    def pprint(self):
        for key,value in self.iteritems():
            print key,value.relname,value.create_dt,value.modify_dt

    @staticmethod
    def _get_userdef_methods():
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                yield key,value

    @staticmethod
    def _get_num_methods(self):
        i=0
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                i+=1
        return(i)

    @verbose
    def logprint(*args):
        print args

    def get_dict_records(self):
        l=[]
        for key,value in self.iteritems():
            rec={}
            rec.__setitem__('inode',key)
            l.append(rec)
        return(l)

    def get_dict_records_gen(self):
        l=[]
        for key,value in self.iteritems():
            rec={}
            rec.__setitem__('inode',key)
            rec.__setitem__('modify_secs',datetime_to_secs(value.modify_dt))
            #rec.__setitem__('relname',value.relname)
            #rec.__setitem__('create_dt',create_dt_val)
            #rec.__setitem__('modify_dt',value.modify_dt)
            yield(rec)


class Tags(dict):

    _dirty = False

    def __init__(self,dat,stats=None):
        self.stats=stats
        self.dat = dat

    def add(self,tjf):
        ''' arg tfj=instance of TaggedJSONFile '''
        for tag in tjf.tag_names:
            if not self._tag_exists(tag):
                tagged_files = {}
                self._add_tag(tag,tagged_files)
                self._add_tagged_file(tagged_files,tjf)
            else:
                tagged_files = self.__getitem__(tag)
                if not self._tagged_file_exists(tagged_files,tjf):
                    self._add_tagged_file(tagged_files,tjf)

    def _add_tag(self,tag,tagged_files):
        self.__setitem__(tag,tagged_files)
        self.stats.tag_added.append(tag)
        self.logprint('tag_added',tag)

    def _add_tagged_file(self,tagged_files,tjf):
        tagged_files.__setitem__(tjf.inode,tjf)
        self._dirty = True
        self.stats.tagged_file_added.__setitem__(tjf.inode,tjf)
        self.logprint('tagged_file_added',tjf.inode)
        
    def _tagged_file_exists(self,tagged_files,tjf):
        if tagged_files.has_key(tjf.inode):
            self.stats.tagged_file_exists.__setitem__(tjf.inode,tjf)
            self.logprint('tagged_file_exists',tjf.inode)
            return(True)
        else:
            return(False)
        
    def _tag_exists(self,tag):
        if self.has_key(tag):
            self.stats.tag_exists.append(tag)
            self.logprint('tag_exists',tag)
            return(True)
        else:
            return(False)

    def pprint(self):
        for key,value in self.iteritems():
            tag_count = len(self.__getitem__(key))
            print key,tag_count,value.keys()

    def get_dict_records(self):
        l=[]
        for key,value in self.iteritems():
            tag_count = len(self.__getitem__(key))
            for inode in value.keys():
                rec={}
                rec.__setitem__('name',key)
                rec.__setitem__('file',inode)
                l.append(rec)
        return(l)

    def get_dict_records_gen(self):
        for key,value in self.iteritems():
            tag_count = len(self.__getitem__(key))
            for inode in value.keys():
                rec={}
                rec.__setitem__('name',key)
                rec.__setitem__('file',inode)

                yield(rec)

    def persist(self):
        if self._dirty:
            no_tags = len(self.keys())
            self.logprint('persist',self.dat.path,'with',no_tags,'tags')
            write_object_to_disk(self,self.dat.path)
        else:
            self.logprint(self.__class__,'has no changes to persist')
    @staticmethod
    def _get_userdef_methods():
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                yield key,value

    @staticmethod
    def _get_num_methods(self):
        i=0
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                i+=1
        return(i)

    @verbose
    def logprint(*args):
        print args


class TagHandler(object):
    def __init__(self,**kwargs):
        for kw in sorted(kwargs.keys()):
            setattr(self,kw,kwargs[kw])

        assert getattr(self,'TAGSDAT')
        assert getattr(self,'FILESDAT')
        assert getattr(self,'NOTESDIR')
        
        self.stats=Stats()
        if self._not_first_run(self):
            self.tags = self.TAGSDAT.recover()
            print self.tags
            self.files = self.FILESDAT.recover()
            print self.files
            self.tags._dirty = False
            self.files._dirty = False
            self.tags.stats = self.stats
            self.files.stats = self.stats
        else:
            self.tags = Tags(self.TAGSDAT,self.stats)
            self.files = Files(self.FILESDAT,self.stats)

        for filename in self.read_note_dir():
            tjf = TaggedJSONFile(filename) 
            # if Justnotes files, ignore copies
            if tjf.absname == trim_justnotes_int_suffix(tjf.absname):
                self.tags.add(tjf)
                self.files.add(tjf)
            else:
                self.stats.file_skipped.append(tjf)
                self.logprint('file_skipped',tjf.inode)

    def read_note_dir(self):
        for file in os.listdir(self.NOTESDIR):
            abs_path = os.path.join(self.NOTESDIR,file)
            yield abs_path


    @staticmethod
    def _not_first_run(self):
        return(self.TAGSDAT.exists())

    def cleanup(self):
        self.stats.pprint_summary()
        self.logprint(self.tags.pprint())
        self.logprint(self.files.pprint())
        self.tags.persist()
        self.files.persist()

    @verbose
    def logprint(*args):
        print args


def proc_args(idx):
    if len(sys.argv) == 1:
        return(None)
    else:
        return(sys.argv[idx])

if __name__ == '__main__':

    VERBOSE = True
    TAGSDAT = TagDat('/Users/burtnolej/.tag_pickle.dat',Tags)
    FILESDAT = FilesDat('/Users/burtnolej/.file_pickle.dat',TaggedJSONFile)

    #l = Logger('/tmp/log.txt')

    for case in switch(proc_args(1)):
        if case('-cleanup'):
            # delete dats
            TAGSDAT.remove()
            FILESDAT.remove()
            break
        if case('-check-dat'):
            if TAGSDAT.exists():
                tags = TAGSDAT.recover()
                files = FILESDAT.recover()
            else:
                if VERBOSE: print 'first run: no dat files'
            break
        if case('-today'):
            if TAGSDAT.exists():
                tags = TAGSDAT.recover()
                files = FILESDAT.recover()
                files.get_todays_files()
            break
        if case('-day'):
            if TAGSDAT.exists():
                tags = TAGSDAT.recover()
                files = FILESDAT.recover()
                files.get_todays_files(sys.argv[2])
            break
        if case('-inode'):
            if TAGSDAT.exists():
                tags = TAGSDAT.recover()
                files = FILESDAT.recover()
                files.get_inode_detail(sys.argv[2])
            break
        if case('tags'):
            if TAGSDAT.exists():
                tags = TAGSDAT.recover()
                files = FILESDAT.recover()
                tags.pprint_summary()
            break
        if case():
            print "no flags"
            mth = TagHandler()
            mth.cleanup()
            break
        


     
