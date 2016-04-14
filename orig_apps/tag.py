#!/usr/bin/python
from sys import exit
from tag_util import TagDat,FilesDat
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView

VERBOSE = True
TAGSDAT = TagDat('/Users/burtnolej/.tag_pickle.dat',Tags)
FILESDAT = FilesDat('/Users/burtnolej/.file_pickle.dat',TaggedJSONFile)

l = Logger('/tmp/log.txt')

tags = TAGSDAT.recover()
files = FILESDAT.recover()

class TagDB(Database):
    pass

class Tags(DatabaseTable)
    def add(self,**kwargs):

class Tag(DatabaseRecord):
    pass

tagdb = TagDB("~/Downloads/gadflyZip/gadfly/scripts/",'use')

tt = tagdb.table(Tags())

#tv = tagdb.view(TagView)
#finance.loadviews()

sys.exit()

class TagView(DatabaseView):
    def init_load(self,arg=None,re=None):
        init_load_qry  = "select tag_name "
        init_load_qry += "from   Tags "
        init_load_qry += "order by name"
        self.__load(init_load_qry,re)
        
    def __load(self,qry,re=None):
        self.db.execute(qry)
        for col1 in self.db.fetchall():
            #window constructor needs a rec field called display_text
            self.add(cpy_name = str(col1),display_text=str(col1))

    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr.cpy_name] = dr
