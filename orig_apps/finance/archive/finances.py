#!/usr/bin/python

from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list,write_object_to_disk,read_object_from_disk
from collections import OrderedDict
import re
import uniqueid
from gadfly import gadfly
import os,shutil
from uniqueid import UniqueIDGenerator

_uniqueidgen = UniqueIDGenerator() # singleton ??

class Record:
    def pprint(self):
        for field in self.__dict__.keys():
            if field != "pk":
                print str(field).rjust(15),str(getattr(self,field)).ljust(25)
       
class Table(object):
    def __init__(self):
        self.records = OrderedDict()

    def add_record(self,**kwargs):
        rec = self._get_empty_record_obj()
        for key,value in kwargs.iteritems():
            if key.startswith("pk_"):
                rec.pk = key
            setattr(rec,key,value)

        if not self.records.has_key(getattr(rec,rec.pk)):
                self.records.__setitem__(getattr(rec,rec.pk),rec)
                return(rec)
        return(self.records.__getitem__(getattr(rec,rec.pk)))

    def _get_empty_record_obj(self):
            rec = Record()
            rec.pk = "_id"
            setattr(rec,"_id",_uniqueidgen.next())
            return(rec)
        
    def __iter__(self):
        for _id,r in self.records.iteritems():
            yield _id,r

    def iterkey(self):
        for _id,r in self:
            yield getattr(r,r.pk)

    def pprintkey(self):
        for k in self.iterkey():
            print k,

    def pprint(self):
        for _id,record in self:
            title = str(_id) + " " + str(record)
            print title
            print "".ljust(len(title),"-")
            record.pprint()

        print "\nno. items: " + str(len(self.records))
        
    def find(self,key):
        return(self.records.has_key(key))

class Transaction(Table):
    pass

class CounterpartyCollection(dict):
    
class Counterparty(Entity):
    def __init__(self,**kwargs):
        '''
        basic constructor no manipulation of args needed
        '''
        super(Counterparty,self).__init__()
        self._id = _uniqueidgen.next()
        for key,value in kwargs.iteritems():
            if key.startswith("pk_"):
                self.pk = key
            setattr(self,key,value)

        self.add_record()

    @classmethod
    def pos(long_descr):
        super(Counterparty,self).__init__()
        self._id = _uniqueidgen.next()

        lds = long_descr.split() # create a list of words
        cpy = lds[2]
        if len(cpy) < 6:
            cpy = cpy + " " + lds[3][0:6]
            record.tran_type = "POS"

        return(self.add_record())

    @classmethod
    def 2201(long_descr):
        lds = long_descr.split() # create a list of words
        cpy = lds[1][7:][0:10]
                if len(cpy) < 6:
                    cpy = cpy + " " + lds[2][0:6]
                    if len(cpy) < 10 and len(lds) > 3:
                        cpy = cpy + " " + lds[3][0:6]
                record.tran_type = "POS"

    def strip_spaces(cpy):
                        cpy = "".join(cpy.split()) # take the spaces out
                if len(lds) < 6:
                    loc = lds[len(lds)-2][(len(lds)-2)-10:]
                else:
                    loc = "".join(ldso[len(lds)-3:])

    def find_sname(self,sname):
        for c_id,c in self:
            if c._sname == sname:
                return True
        return False

    def add_record(self,**kwargs):

        if not self.records.has_key(getattr(self,self.pk)):
                self.records.__setitem__(getattr(self,self.pk),self)
                return(self)
        return(self.records.__getitem__(getattr(self,self.pk)))

class CouttsFinanceDataParser(object):
    
    def __init__(self,fn):
        self.raw_list = file2list(fn)
        self.cpy = Counterparty()
        self.tran = Transaction()

    def parse_raw_list(self):
       '''
        take the coutts csv file and map each tran as best possible
        to a Tran object.
        _long_descr will be a blob of _counterparty and _tran_type
        and will be processed by a later method
        '''
       for line in self.raw:
           fields = line.split(",")
           self.tran.add_record(_id = _uniqueidgen.next(),
                                _tran_date = fields[2],
                                _long_descr = fields[3],
                                _ccy = fields[4],
                                _debit_amt = fields[5],
                                _credit_amt = fields[6],
                                _balance = fields[7])
             
    def get_counterparty(self):
        for _id, record in self.tran:
            if record._long_descr.startswith("POS"):
                c = Counterparty.pos(record._long_descr)
                setattr(record,"_cpy_id",c._id)
            elif record._long_descr.startswith("2201") or record._long_descr.startswith("4097"):
                c = Counterparty.2201(record._long_descr)
                setattr(record,"_cpy_id",c._id)


cfdp = CouttsFinanceDataParser("./coutts-transactions-up-to-250713-50l.csv")
cfdp.parse_raw_list()
cfdp.get_counterparty()
#cfdp.cpy.pprintkey()
ocfdp.cpy.pprint()
#cfdp.tran.pprint()

del cfdp

_uniqueidgen.__del__()
