
from random import randint
from sys import path,argv,exit,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import write_object_to_disk,read_object_from_disk,Singleton,Logger, write_to_file, switch, in_method_log
from test_util import UnitTest, DBTestFailed
from log_util import LogMeta
from datetime_util import MyDT
from inspect import getmembers
from os import path, makedirs, chmod
import shutil
from collections import OrderedDict
from gadfly import gadfly
import subprocess
from types import IntType,StringType, FloatType
import re
from functools import wraps
import copy
from table_print import Table


# 0825 - todo
# update all to using constants
# move the rec setters/getters into DatabaseRecord
# make them instancemethods so they can be call generally

## constants
R_DRTY = "_dirty__"
R_OLDV = "_oldv__"
R_DEL = "_delete__"
T_PKEY = "_pkey__"
R_ID = "_id"
R_TS = "_last_update"
R_VER = "_version"
R_TBL = "table__"

def db_query_dec(db_obj,loc,type):
    def actual_dec(func):
        @wraps(func)
        def decorator(*arg):
            db = db_obj(loc,type)
            qry_str = func(*arg)
            db.run_qry(qry_str)
            db.print_fetchall()
            db.close()
        return(decorator)
    return actual_dec

class QryResultTable(Table):
    ''''
    prints log stores in the form "time","super","func","stack_len",
    "args","results"]. log store is a list of dicts
    '''
    def __init__(self,*args):
        super(QryResultTable,self).__init__(*args)
        
    def _cell_generator(self,object):
        for i in object:
            yield [j for j in i]

class DBErrorZeroDataRecords(Exception):
    pass

class DBErrorDupePKeyInsert(Exception):
    pass

class DBErrorRecSchemaInvalid(Exception):
    pass

class Database(dict):
    '''
    contains tables or view objects
    '''
    __metaclass__ = LogMeta

    def __init__(self,gf_dir,type):
        '''
        type=use|create db

        '''
        self._type = type
        self._gf_dir = gf_dir
        self._set_db_name()
        self._gf_init()
        self.logmeta = LogMeta # so we can get access to run logs

    @property
    def __name__(self):
        return(self._db_name)

    def __repr__(self):
        return(str(self.__class__))

    def table_exists_in_gf(self,table_name):
        '''
        return True if the table 'table_name' already exists in the
        gadfly database
        '''
        qry_str =  "select count(*) "
        qry_str += "from __table_names__ "
        qry_str += "where table_name = \'" + table_name.upper() + "\'"
        self.execute(qry_str)
        res = self.fetchall_single_val()
            
        if res == 0: return(False)
        return(True)
    table_exists_in_gf.log = True

    def commit_to_gf(self):
        '''
        iterate through tables and views and 
        just process the table objects as views are read only and
        are handled in loadviews
        '''
        for k,v in self.iteritems():
            if issubclass(v.__class__,DatabaseTable):
                v.find_changed_records(self)
    commit_to_gf.log = True

    def init_objects_in_db(self):
        '''
        initialise database entities (tables/views) in memory
        create in db or load objects from database
        '''
        for k,v in self.iteritems():
            if v.db._type == "create": # recreate blank table
                if v._record_count == 0:
                    raise DBErrorZeroDataRecords("DatabaseTable object",k,"needs at least 1 record to be created")
                v.create_in_gf(v.db)
                v._new = True
            else: # load objects from db
                v.load_from_gf()
        return(len(self))
    init_objects_in_db.log = True

    def close(self):
        self._commit()
        self._close()
    close.log = True
        
    def table(self,table_class):
        table_object = table_class()
        table_object.db = self # keep ref to db so can reload itself
        self.__setitem__(table_object.__class__.__name__,table_object)
        return(table_object)
    table.log = True

    def view(self,view_class):
        view_object = view_class()
        view_object.db = self # keep ref to db so can reload itself
        self.__setitem__(view_object.__class__.__name__,view_object)
        return(view_object)

    def _gf_init(self):
        if self._type == 'auto': # set to use if exists
            if self.exists():
                self._type = 'use'
            else:
                self._type = 'create'
               
        if self._type == 'create':
            self._set_dirs()
            self._gf_handle = gadfly()
            self._startup()
            self.create_gfplus_wrapper()
            print 'db opened with \'create\''
        elif self._type == 'use':
            self._gf_handle = gadfly(self._db_name,self._dir_name)
            print 'db opened with \'use\''
        else:
            raise Exception('usage argv[1] = create|use')

        self._get_cursor()
    _gf_init.log = True

    def pprint(self):
        for table_name,table_rec in self.iteritems():
            print table_name
            table_rec.pprint()

    def create_gfplus_wrapper(self):
        gfp_exe = "python "
        gfp_exe += self._gf_dir + "gfplus.py "
        gfp_exe += self._db_name
        gfp_exe += " " + self._dir_name
        gfp_script_name = self._db_name + ".sh"
        write_to_file(gfp_script_name,gfp_exe)
        chmod(gfp_script_name,0777)
    
    def delete_db(self):
        '''
        physically remove the gadfly _Database directory from the
        working directory
        '''
        import shutil
        shutil.rmtree(self._dir_name) 
        
    def _set_db_name(self):
        self._db_name = str(self.__class__).split(".")[1][:-2]
        self._dir_name = "_" + self._db_name + "_dir"

    # GF Wrappers
    def _startup(self):
        self._gf_handle.startup(self._db_name,self._dir_name)
            
    def _get_cursor(self):
        self._cursor = self._gf_handle.cursor()
        
    def _commit(self):
        self._gf_handle.commit()
    _commit.log = True

    def _close(self):
        self._gf_handle.close()

    def _set_dirs(self):
        if path.exists(self._dir_name):
            shutil.rmtree(self._dir_name)
        makedirs(self._dir_name)

    def exists(self):
        if path.exists(self._dir_name):
            return(True)
        return(False)
        
    def fetchall_single_val(self):
        rows = self._fetchall()
        return rows[0][0]

    def fetchall_num_rows(self):
        rows = self._fetchall()
        return len(rows)

    def fetchall_descr_val_pair(self):
        '''
        return col_name,value pairs in a generator
        i.e. [('last_name', 'messi'),('debut', '1/12/13')]
        '''
        rows = self._fetchall()
        desc = self._cursor.description

        for i in range(len(rows)):
            if len(desc) == 1:
                yield (desc[0][0].lower(),str(rows[i][0]))
            else:
                yield [(desc[j][0].lower(),str(rows[i][j])) for j in range(len(desc))]
        
    def fetchall(self):
        '''
        return results in a generator
        '''
        rows = self._fetchall()
        desc = self._cursor.description

        for i in range(len(rows)):
            if len(desc) == 1:
                yield str(rows[i][0])
            else:
                yield tuple([str(rows[i][j]) for j in range(len(desc))])
        
    def fetchall_list(self):
        '''
        return results in a list of tuples with col names in row 1
        [('Name','Debut',_,'Goals'),
        ('messi', '1/12/13', 'False', '1500'),
        ('bale', '1/10/13', 'False', 'True')]
        '''
        rows = self._fetchall()
        desc = self._cursor.description

        l = []
        l.append(self.parse_descr(desc))
        
        for i in range(len(rows)):
            if len(desc) == 1:
                l.append(str(rows[i][0]))
            else:
                l.append(tuple([str(rows[i][j]) for j in range(len(desc))]))
        return(l)
    
    def fetchall_list_of_dict(self):
        '''
        [{'last_name':'bale','debut','1/10/13','goals',0},
            {'last_name':'messi','debut':'1/12/13', 'goals', 1500}]
        '''
        rows = self._fetchall()
        desc = self.fetchall_desc_list()

        l = []
        
        for i in range(len(rows)):
            d = {}
            for j in range(len(desc)):     
                d[desc[j]] = rows[i][j]
            
            l.append(d)
        return(l)

    def fetchall_pkey_dict(self,pkey):
        '''
        if pkey=last_name
        [{'bale': {'last_name':'bale','debut','1/10/13','goals',0},
          'messi: {'last_name':'messi','debut':'1/12/13', 'goals', 1500}]
        '''
        
        rows = self._fetchall()
        desc = self.fetchall_desc_list()

        d = {}
        for i in range(len(rows)):
            _d = {}
            for j in range(len(desc)):     
                _d[desc[j]] = rows[i][j]
            
            if d.has_key(_d[pkey]):
                raise Exception('dupe primary key')
            d[_d[pkey]] = _d 
        return(d)

    def parse_descr(self,d):
        '''
        i.e. [('LAST_NAME', 'DEBUT', 'DELETE__', 'DIRTY__')]
        '''
        rowsn = len(d)
        colsn = len(d[0])
        l=[]
        
        for i in range(rowsn):
            for j in range(colsn):
                if d[i][j] != None:
                    l.append(d[i][j].lower())
        return(tuple(l))
        
    def fetchall_desc_list(self):
        '''
        i.e. ['LAST_NAME', 'DEBUT', 'DELETE__','GOALS']
        '''
        return self.parse_descr(self._description())
                    
    def _description(self):
        return(self._cursor.description)

    def desc_list(self):
        '''
        return column names from last query in a list
        '''
        l = []
        for row in self._description():
            l.append(row[0])
        return(l)
        
    def _fetchall(self):
        return(self._cursor.fetchall())

    def fetchall_like(self,field,expr):
        p = re.compile(expr)
        #p = re.compile(r'^b.*')
        
        res = self._cursor.fetchall()
        col_idx = self.column_index(field)
        for col in res:
            if len(p.findall(col[col_idx])) > 0:
                   yield(col)

    def run_qry(self,qry_str,lh=None):
        if not lh:
            import sys
            lh = sys.stdout
        self.execute(qry_str)

        rq_table = QryResultTable(self.fetchall_list())
        rq_table.printout(lh)
        
    def print_fetchall(self):
        for record in self.fetchall():
            for i in range(0,len(record)):
                print record[i].ljust(20),
            print
            
    def pp(self):
        return(self._cursor.pp())
        
    def execute(self,query,query2=None):
        #print query,query2
        self._cursor.execute(query,query2)
        return()
    execute.log = True

    def column_index(self,col_name):
        desc = self.description()
        for i in range(0,len(desc)):
            if desc[i] == col_name.upper(): return(i)
        return(False)

    def description(self):
        return([field[0] for field in self._cursor.description])

    @property
    def cursor(self):
        return(self._cursor)
        
    def __call__(self):
        #return(self._cursor)
        return(self)

    def __del__(self):
        self._commit()
        self._close()



class UniqueIDGenerator(object):
    __metaclass__ = Singleton
    
    def __init__(self,id_len=7):
        self.fn = "./uniqueid.dat"
        self.id_len = id_len
        self.list = []
        self.uniqueid = None

        if path.isfile(self.fn):
            self.list = read_object_from_disk(self.fn)
    __init__.log = True

    def stats(self):
        return(len(self.list))
        
    def next(self):
        count = 1
        self.uniqueid = str(randint(1,9999999)).ljust(7,'0')
        while (self.uniqueid in self.list):
            self.uniqueid = str(randint(1,9999999)).ljust(7,'0')
            count += 1
        self.list.append(self.uniqueid)
        
        #return(str(len(self.list)),self.uniqueid,str(count))
        return(self.uniqueid)
    next.log = True

    def __del__(self):
        write_object_to_disk(self.list,self.fn)

_uniqueidgen = UniqueIDGenerator()

class DatabaseTable(dict):
    '''
    for writing. create if it does not exist in the db and insert
    to if it does
    '''
    __metaclass__ = LogMeta
    def __init__(self,*arg,**kwargs):
        self._set_table_name(*arg,**kwargs)
        self._record_count = 0
        self._allow_amend_dupe_insert = True # assume amend if dupe key inserted
    __init__.log = True

    #### SETTERS and GETTERS

    def __repr__(self):
        return(str(self.__class__))

    # pkey
    def _get_pk(self):
        return(getattr(self,T_PKEY))

    def _set_pk(self,pk_value):
        setattr(self,T_PKEY,pk_value)

    def _iter_records(self):
        for r in self.values():
            yield r
    _iter_records.log = True

    def _get_table_record_dict(self):
        '''
        returns from memory the records in the structure
        if pkey=last_name
        [{'bale': {'last_name':'bale','debut','1/10/13','goals',0},
          'messi: {'last_name':'messi','debut':'1/12/13', 'goals', 1500}]
        '''
        d={}
        pk_key = self._get_pk().lower()
        for rec in self._iter_records():
            _d = {}
            pk_val = rec._get_pk()
            for k,v in rec.get_data_items():
                _d[k]=v
            d[pk_val] = _d
        return(d)
            
        
    @staticmethod
    def _get_table(table_name):
        return (Database[table_name])

    def _get_record(self,pk_value):
        return(self[pk_value])

    def _schema_has_field(self,pred):
        return(self._schema.has_key(pred))
        
    def delete_rec(self,pkey):
        '''
        delete the record with primary key = pkey
        '''
        rec = self[pkey]
        rec._set_delete(pkey)
        rec._set_dirty(pkey) 
    delete_rec.log = True
        
    def update_rec(self,pkey,pred,value):
        '''
        updating 1 field in a record. copy the orig rec and make it oldv
        of the new_rec
        '''
        orig_rec = self[pkey]
        new_rec = orig_rec.copy()
              
        if self._schema_has_field(pred) and new_rec._has_field(pred):
            new_rec._set_old_version(pkey,orig_rec)
            new_rec._set_field_value(pred,value)
            new_rec._set_dirty(pkey)
        elif self._schema.has_key(pred):
            new_rec._set_field_value(pred,value)
            new_rec._set_dirty(pkey)
        else:
            raise "column not in schema" + str(pred)
        
        self[pkey] = new_rec
    update_rec.log = True

    def get_rec_field_value(self,pkey,pred):
        rec = self[pkey]
        return(getattr(rec,pred))
    
    def get_rec_version(self,pkey):
        rec = self[pkey]
        return(getattr(rec,R_VER))
    
    def _get_pk(self):
        '''
        overide this in the subclass if you want a different pkey
        '''
        return(getattr(self,T_PKEY))

    def add_list(self,records):
        assert isinstance(records,list)
        for rec in records:
            #self.add(self,**rec)
            self.add(**rec)
    add_list.log = True

    def rec_exists(self,pk):
        return(self.has_key(pk))
    rec_exists.log = True

    def add(self,**kwargs):
        new_dr = DatabaseRecord(self,**kwargs)

        pkey = new_dr._get_pk()

        if self.rec_exists(pkey):            
            # check _allow_amend_dupe_insert flag, if True then assume 
            # that this is an update of an existing otherwise raise an exception
            # as this is dupe key
            if not self._allow_amend_dupe_insert:
                raise DBErrorDupePKeyInsert(pkey)
            
            # get orig record         
            orig_dr = self[pkey]
            
            # make orig record the old version
            new_dr._set_old_version(pkey,orig_dr)
            
            # overwrite old record in table with new record
            self[pkey] = new_dr
            
            # set new rec as dirty so we know to update into gadflydb
            new_dr._set_dirty(pkey)
            
            # return the new record
            return(self[pkey])
        else:
            self[pkey] = new_dr

        new_dr._set_dirty(pkey)
        self._record_count+=1
        return(new_dr)
    add.log = True


    def record_exists(self,pk):
        return(self.has_key(pk))
    record_exists.log = True
        
    def load_from_gf(self):
        '''
        populate object with existing records in gadfly table
        '''
        self._new=True
        table_name = self._table_name
        if self.db.table_exists_in_gf(table_name):
            self._new = False

            qry_str = "select * from " + table_name
            
            self.db.execute(qry_str)
            cols = self.db.desc_list()

            for row in self.db.fetchall():
                dr = DatabaseRecord.lists(self,row,cols)
                # dont check for dupe pkey trust db
                self[dr._get_pk()] = dr
        self._set_schema(table_name)
    load_from_gf.log = True

    def get_num_records(self):
        return(len(self))

    def empty(self):
        self.clear()
        
    def __del__(self):
        #print "# " +self._table_name + str(len(self)) + "rows"
        pass

    def create_in_gf(self,db):
        '''
        build a create table record of the format
        'create table Player(id varchar,last_name varchar)
        '''
        self._db = db
        self._set_schema(self._table_name)
        exec_string = "create table " + self._table_name
        attr_string = ",".join(str(attr) + " " + str(self._schema[attr]) for attr in sorted(self._schema.keys()))
        exec_string = exec_string + "(" + attr_string + ")"
        self._db.execute(exec_string)
    create_in_gf.log = True

    def ins_rec_in_gf(self,ins_key_list):
        '''
        insert new records in batch format and updates 1 by 1
        build an insert record of the format
        C = 'insert into player (attr1,attr2,..n) values (?, ?, n)'
        D = '[(rec1_val1,rec1_val2,..n),(rec2_val1,rec2_val2,..n),n)]'
        execute(C,D)
        '''
        val_list=[]
        for key in ins_key_list:
            val_list.append(tuple(v for v in self[key].get_data_values()))
        
        attrstr = ",".join(str(attr) for attr in sorted(self._schema.keys()))
        qmstr = ",".join('?' for j in range(0,len(self._schema.keys())))
        excstr1  = "insert into " + self._table_name
        excstr1 += "(" + attrstr + ") values (" + qmstr + ")"
        excstr2 = val_list
        
        self._db.execute(excstr1,excstr2)
    ins_rec_in_gf.log = True

    def upd_rec_in_gf(self,rec):
        '''
        and build update string
        'update table set update_field=xyz where field=abc'
        '''
        updaten=0
  
        pk_val = rec._get_pk()
        pk_key = self._get_pk().lower()
        
        for k,v in rec.compare_records(rec._get_old_version(pk_val),True):
            updaten+=1
            
            if not self._allow_schema_invalid:
                sv = self._format_attribute_to_schema(k,v)
                wv = self._format_attribute_to_schema(pk_key,pk_val)
            else:
                
                _type = self._get_type(k,v)
                sv = self._format_attribute_to_schema(k,v,_type)
                
                _type = self._get_type(pk_key,pk_val)
                wv = self._format_attribute_to_schema(pk_key,pk_val,_type)
                
            excstr1 =  "update " + self._table_name
            excstr1 += " set " + k + "=" + sv
            excstr1 += " where " + pk_key + "=" + wv
            #print excstr1
            self._db.execute(excstr1)
    upd_rec_in_gf.log = True
            
    def del_rec_in_gf(self,rec):
        pk_val = rec._get_pk()
        pk_key = self._get_pk().lower()
        
        if not self._allow_schema_invalid:
            wv = self._format_attribute_to_schema(pk_key,pk_val)
        else:
            _type = self._get_type(pk_key,pk_val)
            wv = self._format_attribute_to_schema(pk_key,pk_val,_type)        

        excstr1  = "delete from " + self._table_name
        excstr1 += " where "+pk_key+"="+wv

        self._db.execute(excstr1)
    del_rec_in_gf.log = True

    def _check_schema(self,rec):
        '''
        check if the record is schema valid or not
        '''
        for k,v in rec.get_data_items():
            if self._get_type(k,v) != self._schema[k]:
                raise DBErrorRecSchemaInvalid(k,type(v),self._schema[k])
            
        return True
    
    def find_changed_records(self,db):
        self._db = db
        self._set_schema(self._table_name) # if it doesnt already exist

        ins_batch_list = []
        for rec in self._iter_records():
            
            # if schema integrity set then check
            if not self._allow_schema_invalid:
                self._check_schema(rec)
                
            pk = rec._get_pk()
            if rec._get_dirty(pk):
                if rec._not_orig_version(pk):
                    self.upd_rec_in_gf(rec)
                elif rec._get_delete(pk):
                    self.del_rec_in_gf(rec)
                    self.pop(pk)
                else:
                    ins_batch_list.append(pk)
            rec._unset_dirty(pk)
        if len(ins_batch_list)>0:
            self.ins_rec_in_gf(ins_batch_list)
    find_changed_records.log = True

    def _set_table_name(self,*arg,**kwargs):
        self._table_name = str(self.__class__).split(".")[1][:-2]

    def _get_type(self,key,value):
        if key.find('id') != -1:
            return('varchar')
        elif len(str(value).split(".")) == 2:
            return('float')
        #elif len(str(value).split("/")) == 3:
        #    return('datetime')
        elif value in [True,False] and value not in [0,1]:
            return('varchar')
        else:            
            try:
                int(value)
                return('integer')
            except:
                return('varchar')
    _get_type.log = True

        
    def _set_schema(self,tn):
        if hasattr(self,'_schema'):
            return('exists')
        
        self._schema = OrderedDict()
        i=0
        for key,record in self.iteritems():
            _tmp_schema = {}
            for key,value in record.get_data_items():
                _tmp_schema[key] = self._get_type(key,value)
        
        if len(self._schema.keys()) == 0:
            self._schema = _tmp_schema
        else:
            return(False)
        # check that all records imply the same schema
        assert (_tmp_schema == self._schema)
        return (self._schema.items())
    _set_schema.log = True
        
    def _format_attribute_to_schema(self,attr,value,format=None):
        '''
        if format is not none; then format the value to that type not to the schema
        this is needed when schema enforcement is off
        '''
        if format == None:
            attr_dt = self._schema[attr]
        else:
            attr_dt = format

        if attr_dt == 'varchar':
            return ("'" + str(value) + "'")
        elif attr_dt == 'float':
            return str(value)
        elif attr_dt == 'integer':
            return str(value)
        
        return(fvalue)
        
    def print_status(self,text,obj,id):
        print text.ljust(10),
        print str(obj.__class__.__name__).ljust(15),
        print str(id).ljust(20),
        print str(self.__class__.__name__).ljust(15)

class DatabaseView(dict):
    def __init__(self,*arg,**kwargs):
        self.other = DatabaseTable(*arg,**kwargs)

    def load(self,qry,db,arg=None,re=None):
        db.execute(qry)
        for res in db.fetchall():
            self.add(res)
        
    def add(self,**kwargs):
        '''
        need to implement
        '''
        
    def empty(self):
        self.other.empty()
        
    def __del__(self):
        self.other.__del__()

    def _set_table_name(self,*arg,**kwargs):
        self.other.set_table_name(*arg,**kwargs)

    def print_status(self,text,obj,id):
        self.other.print_status(text,obj,id)

    def pprint(self):
        for k,v in self.iteritems():
            v.pprint()
        
class DatabaseRecord(object):
    __metaclass__ = LogMeta
    def __init__(self,table,*arg,**kwargs):
        
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        self._set_table(table)
        pk = self._get_pk()        
        self._set_id(pk)
        self._unset_delete(pk) 
        self._unset_dirty(pk)
        # need to make it old_ == None not whether exists or not
        self._init_old_version(pk)
        self._update_timestamp(pk)
        self._increment_version(pk)
    __init__.log = True

    def copy(self):
        table = getattr(self,R_TBL)
        delattr(self,R_TBL) # del attr
        new_dr = copy.deepcopy(self)
        new_dr._set_table(table)
        self._set_table(table)
        return new_dr
    
    def _set_table(self,table,pk=None):
        setattr(self,R_TBL,table)
    _set_table.log = True

    def _get_table(self,pk=None):
        return(getattr(self,R_TBL))
        
    def _set_version(self,pk,value):
        setattr(self,R_VER,value)
        
    def _increment_version(self,pk,value=None):
        if not hasattr(self,R_VER):
            setattr(self,R_VER,1)
        else:
            setattr(self,R_VER,1+self._get_version())
    _increment_version.log = True

    def _has_field(self,pred):
        return(hasattr(self,pred))

    def _set_field_value(self,pred,value):
        setattr(self,pred,value)
    _set_field_value.log = True

    def _get_field_value(self,pred):
        return(getattr(self,pred))
    _get_field_value.log = True

    def _get_version(self):
        return(int(getattr(self,R_VER)))
    _get_version.log = True
    
    def _update_timestamp(self,pk):
        setattr(self,R_TS,MyDT.now(display_fmt='%s.%f').value)
    _update_timestamp.log = True

    def __repr__(self):
        return(str(self.__class__))

    def _set_id(self,pk):
        setattr(self,R_ID,_uniqueidgen.next())
    _set_id.log = True

    def _get_table_pk(self):
        return(self._get_table()._get_pk())
    _get_table_pk.log = True
        
    def _get_pk(self):
        return(getattr(self,self._get_table_pk()))
    _get_pk.log = True

    def _not_orig_version(self,pk):
        #return(hasattr(self,R_OLDV))
        if self._get_old_version(pk) == None:
            return False
        return True
               
    def _get_old_version(self,pk):
        return(getattr(self,R_OLDV))
    _get_old_version.log = True

    def _init_old_version(self,pk):
        '''
        add the attr and set to blank otherwise a record
        with a prev version will have more attr's that one without
        '''
        setattr(self,R_OLDV,None)
        
    def _set_old_version(self,pkey,orig_dr):
        '''
        make this record the old version by putting a reference to a copy of itself
        in attr R_OLDV
        '''
        setattr(self,R_OLDV,orig_dr)
        
        # increment version
        current_version = orig_dr._get_version()
        self._set_version(pkey,current_version+1)
    _set_old_version.log = True

    def _get_dirty(self,pk):
        return(getattr(self,R_DRTY))
    _get_dirty.log = True

    def _set_dirty(self,pk):
        setattr(self,R_DRTY,True)
    _set_dirty.log = True
    
    def _unset_dirty(self,pk):
        setattr(self,R_DRTY,False)
    _unset_dirty.log = True

    def _get_delete(self,pk):
        return(getattr(self,R_DEL))
    _get_delete.log = True

    def _set_delete(self,pk):
        setattr(self,R_DEL,True)
    _set_delete.log = True

    def _unset_delete(self,pk):
        setattr(self,R_DEL,False)
    _unset_delete.log = True

    @classmethod
    def lists(cls,table,fields,cols):
        '''
        take a list of fields and a list of cols
        '''
        assert len(fields) == len(cols)
        cls1 = cls.__new__(cls) # get an empty rec without an id
        cls1._unset_dirty(None)
        cls1._unset_delete(None)
        cls1._init_old_version(None)
        cls1._set_table(table)
        for f in range(0,len(fields)):
            setattr(cls1,cols[f].lower(),fields[f])
        return(cls1)
    
    def compare_records(self,rec,db_flag=False):
        '''
        return a generator of differences between common fields
        in 2 DatabaseRecords. boolean arg db specifys to only check for
        db fields (fields that start with _db_)
        sorted alphabetically to ensure consistent ordering with other
        field generation methods elsewhere
        ''' 
        for key,value in self.get_data_items():
            if str(value) != str(getattr(rec,key)):
                yield key,value
                
    compare_records.log = True
                        
    def pprint(self):
        print self
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                print key,value
        print

    def pprint_all(self):
        print self
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__"):
                print key,value
        print

    def pprint_all_flat(self):
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value):
                print value,
        print
    
    def get_data_values(self):
        for key,value in sorted(getmembers(self)):
            # if not a __xyz__ or inmemory field xyz__
            if not str(key).startswith("__") and not callable(value) and not str(key).endswith("__"):
                yield value

    def get_data_items(self):
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value) and not str(key).endswith("__"):
            #if not str(key).startswith("__") and not callable(value):
                yield key,value

if __name__ == '__main__':
    pass

