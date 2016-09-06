import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from database_table_util import tbl_rows_get
from database_util import Database

class Validator(object):
    def __init__(self,name,**kwargs):
        if name == None:
            raise Exception('name argument must be passed')
        
        self.name = name
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
        
    def __call__(self,value):
        return(self.validate(value))
        
    def validate(self,value):
        True

class RealIntVdt(Validator):
    def validate(self,value):
        try:
            int(value)
        except:
            return False
        
class BoundRealIntVdt(Validator):
    ''' Bounded int validator '''
    
    def __init__(self,**kwargs):
        if not kwargs.has_key('ubound') and not kwargs.has_key('lbound'):
            raise Exception('ubound or lbound argument must be passed')
        super(BoundRealIntVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        if hasattr(self,'lbound'):
            if int(value) < self.lbound:
                return False

        if hasattr(self,'ubound'):
            if int(value) > self.ubound:
                return False
        return True

class SetMemberVdt(Validator):
    def __init__(self,**kwargs):
        if not kwargs.has_key('set'):
            raise Exception('set must be passed')
        super(SetMemberVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        if value in getattr(self,'set'):
            return True
        return False
    
class BaseType(object):
    def __init__(self):
        self.validations = []
    
    def __call__(self,value):
        return(self.validate(value))
    
    def validate(self,value):
        for validator in self.validations:
            
            if validator(value) == False:
                return False
            
        return True

class RealInt(BaseType):
    def __init__(self,**kwargs):
        
        super(RealInt,self).__init__()
        self.validations.append(RealIntVdt(**kwargs))
        
class BoundRealInt(RealInt):
    ''' bounded int type ; support upper and/or lower bound
    ubound,lbound need to be passed in as kw args'''
    def __init__(self,**kwargs):
        
        super(BoundRealInt,self).__init__(**kwargs)
        self.validations.append(BoundRealIntVdt(**kwargs))
        
class SetMember(BaseType):
    def __init__(self,**kwargs):
        
        super(SetMember,self).__init__()
        self.validations.append(SetMemberVdt(**kwargs))
        
class DBSetMember(BaseType):
    def __init__(self,dbname,tblname,fldname,**kwargs):
        
        database = Database(dbname)
        with database:
            rows = tbl_rows_get(database,tblname,
                                         [fldname])
            
            # rows is a tuple; list is element 2
            kwargs['set'] = [row[0] for row in rows[1]]
        
        super(DBSetMember,self).__init__()
        self.validations.append(SetMemberVdt(**kwargs))
        
class Basestr(BaseType):
    def validate(self,value):
        try:
            str(value)
        except:
            return False