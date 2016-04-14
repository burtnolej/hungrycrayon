from gadfly import gadfly
import sys
sys.path.append("/Users/burtnolej/Dev/pythonapps/util")
import misc_utils
import os
from random import randint
from datetime_util import MyDT
from collections import OrderedDict
from inspect import getmembers
from log_util import LogMeta

## constants
R_DRTY = "_dirty__"
R_OLDV = "_oldv__"
R_DEL = "_delete__"
T_PKEY = "_pkey__"
R_ID = "_id"
R_TS = "_last_update"
R_VER = "_version"
R_TBL = "table__"

class DBErrorZeroDataRecords(Exception):
    pass

class DBErrorDupePKeyInsert(Exception):
    pass

class DBErrorRecSchemaInvalid(Exception):
    pass

class Singleton(type):
    '''
    this is to be used as a __metaclass__
    __metaclass__ = Singleton
    '''
    _instances = {}
    def __call__(cls,*args,**kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,**kwargs)

        return cls._instances[cls]
    
class UniqueIDGenerator(object):
    __metaclass__ = Singleton
    
    def __init__(self,id_len=7):
        self.fn = "./uniqueid.dat"
        self.id_len = id_len
        self.list = []
        self.uniqueid = None

        if os.path.isfile(self.fn):
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

class Database(dict):

    __metaclass__ = LogMeta

    def __init__(self,gf_dir,type):
        '''type=use|create'''
        self._type = type
        self._gf_dir = gf_dir
        self._set_db_name()
        self._gf_init()
        self.logmeta = LogMeta # so we can get access to run logs
        
    def execute(self,query,query2=None):
        #print query,query2
        self._cursor.execute(query,query2)
        return()
    
    @property
    def __name__(self):
        return(self._db_name)

    def __repr__(self):
        return(str(self.__class__))
    
    def exists(self):  
        if os.path.exists(self._dir_name):
            return(True)
        return(False)
    
    def close(self):
        self._commit()
        self._close()
        
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
      
    def commit_to_gf(self):
        '''
        iterate through tables and views and 
        just process the table objects as views are read only and
        are handled in loadviews
        '''
        for k,v in self.iteritems():
            if issubclass(v.__class__,DatabaseTable):
                v.find_changed_records(self)
                
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
    
    def _set_dirs(self):
        if os.path.exists(self._dir_name):
            shutil.rmtree(self._dir_name)
        os.makedirs(self._dir_name)
        
    def create_gfplus_wrapper(self):
        gfp_exe = "python "
        gfp_exe += self._gf_dir + "gfplus.py "
        gfp_exe += self._db_name
        gfp_exe += " " + self._dir_name
        gfp_script_name = self._db_name + ".sh"
        misc_utils.write_text_to_file(gfp_script_name,gfp_exe)
        os.chmod(gfp_script_name,0777)
    create_gfplus_wrapper.log = True

    def table(self,table_class):
        table_object = table_class()
        table_object.db = self # keep ref to db so can reload itself
        self.__setitem__(table_object.__class__.__name__,table_object)
        return(table_object)
    table.log = True
    
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
        
    def _startup(self):
        self._gf_handle.startup(self._db_name,self._dir_name)
    
class DatabaseTable(dict):
        
    __metaclass__ = LogMeta
    
    def __init__(self,*arg,**kwargs):
        self._set_table_name(*arg,**kwargs)
        self._record_count = 0
        self._allow_amend_dupe_insert = True # assume amend if dupe key inserted

    def _set_table_name(self,*arg,**kwargs):
        self._table_name = str(self.__class__).split(".")[1][:-2]
    
    def _iter_records(self):
        for r in self.values():
            yield r
            
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

            sv = self._format_attribute_to_schema(k,v)
            wv = self._format_attribute_to_schema(pk_key,pk_val)


            excstr1 =  "update " + self._table_name
            excstr1 += " set " + k + "=" + sv
            excstr1 += " where " + pk_key + "=" + wv
            #print excstr1
            self._db.execute(excstr1)


        def del_rec_in_gf(self,rec):
            pk_val = rec._get_pk()
            pk_key = self._get_pk().lower()


            wv = self._format_attribute_to_schema(pk_key,pk_val)      

            excstr1  = "delete from " + self._table_name
            excstr1 += " where "+pk_key+"="+wv

            self._db.execute(excstr1)

        
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
                
    def get_data_items(self):
        for key,value in sorted(getmembers(self)):
            if not str(key).startswith("__") and not callable(value) and not str(key).endswith("__"):
                yield key,value
    def get_data_values(self):
        for key,value in sorted(getmembers(self)):
            # if not a __xyz__ or inmemory field xyz__
            if not str(key).startswith("__") and not callable(value) and not str(key).endswith("__"):
                yield value
    def _set_table(self,table,pk=None):
        setattr(self,R_TBL,table)
        
    def _set_id(self,pk):
        setattr(self,R_ID,_uniqueidgen.next())
        
    def _init_old_version(self,pk):
        setattr(self,R_OLDV,None)
    def _not_orig_version(self,pk):
        if self._get_old_version(pk) == None:
            return False
        return True
    def _get_old_version(self,pk):
        return(getattr(self,R_OLDV))
    def _set_old_version(self,pkey,orig_dr):
        '''
        make this record the old version by putting a reference to a copy of itself
        in attr R_OLDV
        '''
        setattr(self,R_OLDV,orig_dr)
        
        # increment version
        current_version = orig_dr._get_version()
        self._set_version(pkey,current_version+1)
    def _unset_dirty(self,pk):
        setattr(self,R_DRTY,False)
        
    _unset_dirty.log = True
    
    def _set_dirty(self,pk):
        setattr(self,R_DRTY,True)
        
    def _get_dirty(self,pk):
        return(getattr(self,R_DRTY))
    
    def _unset_delete(self,pk):
        setattr(self,R_DEL,False)
        
    def _set_delete(self,pk):
        setattr(self,R_DEL,True)      
    def _get_delete(self,pk):
            return(getattr(self,R_DEL))    
    def _update_timestamp(self,pk):
        setattr(self,R_TS,MyDT.now(display_fmt='%s.%f').value)
        
    def _get_pk(self):
        return(getattr(self,self._get_table_pk()))

    def _get_table(self,pk=None):
        return(getattr(self,R_TBL))
    
    def _get_table_pk(self):
        return(self._get_table()._get_pk())
    
    def _increment_version(self,pk,value=None):
        if not hasattr(self,R_VER):
            setattr(self,R_VER,1)
        else:
            setattr(self,R_VER,1+self._get_version())
            
    def _get_version(self):
        return(int(getattr(self,R_VER)))    
    _get_version.log = True
    
    def _set_version(self,pk,value):
        setattr(self,R_VER,value)
        
class Football(Database):
    pass

class Players(DatabaseTable):
    
    __metaclass__ = LogMeta
    
    def __init__(self):
        super(Players,self).__init__()
        self._set_pk("last_name")

    def _set_pk(self,pk_value):
        setattr(self,T_PKEY,pk_value)
        
    def _get_pk(self):
        return(getattr(self,T_PKEY))
    
    def rec_exists(self,pk):
        return(self.has_key(pk))
    
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
    
    def add_list(self,records):
        assert isinstance(records,list)
        for rec in records:
            self.add(**rec)
            
_players = [{'last_name':'bale','goals':0,'debut':'1/10/13'}]

football = Football("/usr/lib/python2.7/dist-packages/gadfly/scripts/","auto")

players = football.table(Players) # create table object instance   
players.add_list(_players) # add record to table obj inst
football.init_objects_in_db() # create table in gadflydb
football.commit_to_gf() # add records to gadflydb
football.close()
#football.delete_db()