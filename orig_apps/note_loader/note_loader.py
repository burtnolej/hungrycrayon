#!/usr/bin/python

from sys import path,argv,exit
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import write_object_to_disk,read_object_from_disk,switch, Logger, timesecs_to_datesecs, secs_to_datetime
from simplenote_util import MySimpleNote 
from db_util import Database, DatabaseTable, DatabaseRecord
import procs
#import proc_util
import sys

l = Logger("/private/tmp/log.txt")

class DateConversions(DatabaseTable):
    pass

class NotesDB(Database):
    pass

class Notes(DatabaseTable):
    pass

class NoteTags(DatabaseTable):
    pass

class Tags(DatabaseTable):
    def get_pkey(self,dr):
        return(dr._db_name)

ndb = NotesDB("~/Downloads/gadflyZip/gadfly/scripts/",'create')
tags = ndb.table(Tags())
notetags = ndb.table(NoteTags())
notes = ndb.table(Notes())
dcc = ndb.table(DateConversions())

sn = MySimpleNote("burtnolej@gmail.com","natwest1",10)

for _note in sn.get_notes():
    c_secs = _note['createdate']
    c_datetime = secs_to_datetime(float(c_secs))
    dcc.add_db(date = c_datetime,
               secs = int(float(c_secs)),
               datatype = 'datetime',
               actiontype = 'create')

    mn_c_date,mn_c_secs = timesecs_to_datesecs(float(c_secs))
    dcc.add_db(date = mn_c_date,
               secs = mn_c_secs,
               datatype = 'date',
               actiontype = 'create')
    
    m_secs = _note['modifydate']
    m_datetime = secs_to_datetime(float(m_secs))
    dcc.add_db(date = m_datetime,
               secs = int(float(m_secs)),
               datatype = 'datetime',
               actiontype = 'modify')
    
    mn_m_date,mn_m_secs = timesecs_to_datesecs(float(m_secs))
    dcc.add_db(date = mn_m_date,
               secs = mn_m_secs,
               datatype = 'date',
               actiontype = 'modify')
               
    # add note               
    note_rec = notes.add_db(content = _note['content'],
                            modified_secs = int(float(m_secs)),
                            created_secs = int(float(mn_c_secs)),
                            title = _note['title'])

    for tag_name in _note['tags']:
        # create tag record for each new tag
        tag_rec = tags.add_db(name = tag_name)
        # create note tag record for each tag the note uses
        tagnote_rec = notetags.add_db(noteid=note_rec._db_id,
                                      tagid=tag_rec._db_id)
    
ndb.commit()
ndb.close()


for rec in procs.q_d('create'):
    print rec
