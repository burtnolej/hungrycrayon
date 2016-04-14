#!/usr/bin/python

class DatabaseTable(object):
    pass

class TableA(DatabaseTable):
    pass

class TableB(DatabaseTable):
    pass

class Database(dict):
    def table(self,table_name):
        t = globals().__getitem__(table_name)()
        self.__setitem__(table_name,t)
        return(t)

    def pprint(self):
        for k,v in self.iteritems():
            print k,v

db = Database()
db.table('TableA')
db.table('TableB')


db.pprint()

