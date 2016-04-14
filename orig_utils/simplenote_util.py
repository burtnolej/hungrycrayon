#!/usr/bin/python
from table_print import Table
from misc_util import write_object_to_disk,read_object_from_disk
from misc_util import switch
from simplenote import Simplenote
from db_util import Database, DatabaseTable, DatabaseRecord

import sys

class MySimpleNote(Simplenote):
    def __init__(self,username,password,num=10000):
        self._note_list = []
        self._handle = Simplenote(username,password)
        self._note_list,_ = self._handle.get_note_list(num)
        self._get_note_content()

    def get_notes(self):
        for _note in self._note_list:
            yield _note
            
    def get_note_list(self,num):
        MySimpleNote.note_list,_ = self._handle.get_note_list(num)
    
    def print_note_list(self):
        for note in self._note_list:
            self.print_note(note)

    def print_note(self,note):
        for k,v in note.iteritems():
            print k.ljust(20),v
        print
    
    def _get_note_content(self):
        for _note in self._note_list:
            key  = _note['key']
            content,status = self._handle.get_note(key)
            _note['content'] = content['content']
            _note['title'] = content['content'].split("\n")[0]

    def get_tags_from_note(self,note):
        return(note['tags'])

if __name__ == '__main__':

    sn = MySimpleNote("burtnolej@gmail.com","natwest1",1)
    sn.print_note_list()


