#!/usr/bin/python
from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Logger
from sys import exit
from tag_util import TagDat,FilesDat,TagHandler, TaggedJSONFile
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView

class TagDB(Database):
    pass

class Tags(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Tags,self).__init__(*args,**kwargs)
        self._PKEY = "id__"
        
    def tag(self,**kwargs):
        t = Tag(**kwargs)
        self[kwargs.__getitem__('id__')] = t

class Tag(DatabaseRecord):
    pass

class Files(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Files,self).__init__(*args,**kwargs)
        self._PKEY = "inode"
        
    def file(self,**kwargs):
        t = File(**kwargs)
        self[kwargs.__getitem__('inode')] = t

class File(DatabaseRecord):
    pass

VERBOSE = True
TAGSDAT = TagDat('/Users/burtnolej/.tag_pickle.dat',Tags)
FILESDAT = FilesDat('/Users/burtnolej/.file_pickle.dat',TaggedJSONFile)
NOTESDIR = '/Users/burtnolej/Documents/Justnotes.test'

tagdb = TagDB("~/gadfly/scripts/",'create')
tt = tagdb.table(Tags)
ft = tagdb.table(Files)
#dc = tagdb.table(DateConversions)

l = Logger('/tmp/log.txt')

if TAGSDAT.exists():
    TAGSDAT.remove()
    FILESDAT.remove()
    
mth = TagHandler(TAGSDAT=TAGSDAT,FILESDAT=FILESDAT,NOTESDIR=NOTESDIR)

# get tags in dict form and add to the TagDB 'Tag' table
for rec in mth.tags.get_dict_records_gen():
    tt.add(**rec)
        
for rec in mth.files.get_dict_records_gen():
    ft.add(**rec)

mth.cleanup()
tagdb.init_objects_in_db()
tagdb.commit_to_gf()
tagdb.close()
