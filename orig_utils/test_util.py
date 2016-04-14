#!/usr/bin/python
import xml.etree.ElementTree as xmltree
import sys

class TestUnexpectedResult(Exception):
    pass

class Tester(object):
    def test(self,description,pos_test,exception,**fields):
        self.description = description
        self.pos_test = pos_test
        self.exception = exception
        self.fields = fields
        self.results_actual = None # gets overidden

        # unpack the fields
        for k,v in fields.iteritems():
            setattr(self,k,v)
        result = self._test(**fields)
        self.log(result)

    def _test(self,**fields):
        # testing an attribute not being set

        for k,v in fields.iteritems():
            if v == None:
                delattr(self,k)
            else:
                setattr(self,k,v)

        try:
            self.run()
            # no exceptions have been thrown
            if self.pos_test: # if +ve test then success
                return True
            return False # otherwise its a fail
        except getattr(sys.modules[__name__], self.exception):
            if self.pos_test == 'True':
                return False
            return True # only successful if -ve test

    def run(self):
        #this will be overridden
        pass

    def log(self,result):
        print str(result)
        print "".ljust(3),"exception".ljust(10),"=",self.exception
        print "".ljust(3),"pos_test".ljust(10),"=",str(self.pos_test)

        for k,v in self.fields.iteritems():
            print "".ljust(3),k.ljust(10),"=",v
        print "".ljust(3),"actual".ljust(10),"=",self.results_actual

def get_type(s):

    #is it a boolean
    if s in ['True']:
        return(True)
    elif s in ['False']:
        return(False)

    #is it a list
    if s == '[]':
        return(list())
    elif type(s) == list:
        return(s)

    #is it a float
    try:
        return(float(s))
    except ValueError:
        pass
    
    #is it a int
    try:
        return(int(s))
    except ValueError:
        pass

    print s
    #its a string
    return(s)

    
def test_xml_iter(tree,key):
    def atb(d): # we assume that only 1 attrib exists
        return(d[d.keys()[0]])

        
    for test in tree.findall(key):
        arg = []
        kw = {}
        o = atb(test.attrib)
        for el in test.getchildren():
            count = len(el.getchildren())
            if count > 0: # then assume its a 'field'
                for sel in el.getchildren(): # get 'value'
                    if sel.attrib['type'] == 'list' or sel.attrib['type'] == 'tuple':
                        kw[atb(el.attrib)] = [] #el.attrib is field nm
                        for ssel in sel.getchildren():
                            kw[atb(el.attrib)].append(get_type(ssel.text))
                        if sel.attrib['type'] == 'tuple':
                            kw[atb(el.attrib)] = tuple(kw[atb(el.attrib)])
                    else:
                        kw[atb(el.attrib)] = get_type(sel.text)
            else: # only need to add fields to arg
                arg.append(atb(el.attrib))
        yield o,arg,kw


def run_tests(xmlcfg):
    tree = xmltree.parse(xmlcfg)

    for o,arg,fields in test_xml_iter(tree,'test'):
        clsobj = globals()[o]  # get test class instance
        clsobj(*arg,**fields)


class DBTestFailed(Exception):
    pass        

class DBTestFailedNumRows(Exception):
    pass
        
class DBTestFailedNoFields(Exception):
    pass

class DBTestFailedFieldTypes(Exception):
    pass
    
class DBTestFailedFieldValues(Exception):
    pass
    
class UnitTest(object):
    def __init__(self,test_name):
        self.name = test_name

    @classmethod
    def db_test(cls,db,test_name):
        cls._db = db
        cls1 = cls(test_name)
        return(cls1)

    def diff(self,l1,l2):
        ls1 = sorted(l1)
        ls2 = sorted(l2)
        
        if len(ls1)>len(ls2):
            pass
        else:
            tmp_ls1 = ls1
            ls1=ls2
            ls2=tmp_ls1
            
        for i in range(len(ls1)):
            if i >= len(ls2):
                return(ls1[i].lower())
            elif ls1[i].lower() != ls2[i].lower():
                return(ls1[i].lower())
            else:
                pass
        
    def check_dbresults(self,tests):
        rowsn=0
        testrecsn=0
        tablel={}
        for test in tests:
            table = test['table']  
            tablel[table] = None # create a dict of tables used in test
            if test.has_key('records'): # if not then zero rec test
                testrecs = test['records']
                for testrec in testrecs:
                    testrecsn+=1
                    pk = test['pk']
                    pkval = testrec[pk]
                    qry_str  = "select * from " + table + " "
                    qry_str += "where " + pk + " = '" + str(pkval) + "'"
                    testrec['status']='Loaded:' + table
                    self._db.execute(qry_str)
                    for rec in self._db.fetchall_descr_val_pair():
                        testrec['status']='Executed qry:' + table
                        for fields in rec:
                            col_name,value = tuple(fields)
                            if col_name.endswith("__"):
                                pass # generated field
                            elif not testrec.has_key(col_name):
                                err_str = col_name + " does not exist"
                                raise DBTestFailed(err_str)
                            elif str(testrec[col_name]) != str(value):
                                err_str = col_name + " diff value " + str(value) + " " + str(testrec[col_name])
                                raise DBTestFailed(err_str)
                        testrec['status']='Passed'
                for testrec in testrecs:
                    if testrec['status'] != 'Passed':
                        err_str = 'incomplete test:'+testrec['status'] + str(testrec)
                        testrec.pop('status')
                        raise DBTestFailed(err_str)
                    testrec.pop('status')

        # test that the number of rows in the db matches the testcases
        for t in tablel:
            self._db.execute("select * from " + t)
            rowsn += self._db.fetchall_num_rows()

        if rowsn != testrecsn:
            err_str = "#rows" + str(rowsn) + " in db " + str(testrecsn) + " in testcases"
            raise DBTestFailed(err_str)

        # test that the number of cols in the db matches the testcases
        for test in tests:
            self._db.execute("select * from " + test['table'])
            cols = self._db.fetchall_desc_list()
            colsn = len(cols)

            if hasattr(test,'records'): # if not then zero rec test               if colsn != len(test['records'].keys()):
                    err_str = "#cols" + str(colsn) + " in db "
                    err_str += str(len(test['records'].keys()))
                    err_str += " in testcases" + "("
                    err_str += ",".join(c for c in cols) + ")("
                    err_str += ",".join(t for t in test['records'].keys()) +")"

                    diffel = self.diff(test['records'].keys(),cols)

                    if diffel != None and diffel != 'id':
                        raise DBTestFailed(err_str)

            
