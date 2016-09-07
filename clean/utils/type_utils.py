import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from database_table_util import tbl_rows_get
from database_util import Database
import re

__all__ = ['RealInt','BoundRealInt','SetMemberPartial','SetMember','DBSetMember', \
           'DBSetMemberPartial']

class _Validator(object):
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

class _RealIntVdt(_Validator):
    def validate(self,value):
        try:
            int(value)
        except:
            return False
        
class _BoundRealIntVdt(_Validator):
    ''' Bounded int validator '''
    
    def __init__(self,**kwargs):
        if not kwargs.has_key('ubound') and not kwargs.has_key('lbound'):
            raise Exception('ubound or lbound argument must be passed')
        super(_BoundRealIntVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        if hasattr(self,'lbound'):
            if int(value) < self.lbound:
                return False

        if hasattr(self,'ubound'):
            if int(value) > self.ubound:
                return False
        return True
    
class BaseType(object):
    def __init__(self):
        self.validations = []
        
        # default to using a Tkentry
        #from Tkinter import Entry as Tkentry
        from ui_utils_tkventry import TkEntry
        self.widgettype = TkEntry
    
    def __call__(self,value):
        return(self.validate(value))
    
    def validate(self,value):
        for validator in self.validations:
            
            if validator(value) == False:
                return False
            
        return True
    
    def name(self):
        namestr=""
        names = [validator.name for validator in self.validations]
        return(",".join(names))

class RealInt(BaseType):
    def __init__(self,**kwargs):
        
        super(RealInt,self).__init__()
        self.validations.append(_RealIntVdt(**kwargs))
        
class BoundRealInt(RealInt):
    ''' bounded int type ; support upper and/or lower bound
    ubound,lbound need to be passed in as kw args'''
    def __init__(self,**kwargs):
        
        super(BoundRealInt,self).__init__(**kwargs)
        self.validations.append(_BoundRealIntVdt(**kwargs))
        
class _SetMemberVdt(_Validator):
    def __init__(self,**kwargs):
        if not kwargs.has_key('set'):
            raise Exception('set must be passed')
        super(_SetMemberVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        if value in getattr(self,'set'):
            return True
        return False
    
class _SetMemberPartialVdt(_Validator):
    ''' matches on unique partial strings 
    i.e er in ,set=['cherry','banana','grape','apple'] but ap not as
    appears twice. also ignores case '''
    def __init__(self,**kwargs):
        if not kwargs.has_key('set'):
            raise Exception('set must be passed')
        super(_SetMemberPartialVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        r = re.compile(value.lower())
        
        hits=0
        for item in getattr(self,'set'):
            results = r.findall(item.lower())
            if len(results)>0: hits+=1
        if hits==1: return True
        return False
    
    
class BaseSetMember(BaseType):
    def __init__(self,**kwargs):
        # could be multiple validators but first one (and only one) will/must have the set assigned
        # create a local instance variable so users dont need to go search for the set

        self.set = kwargs['set']
        super(BaseSetMember,self).__init__()
        
        from ui_utils import TkCombobox
        self.widgettype = TkCombobox

    
class SetMemberPartial(BaseSetMember):
    def __init__(self,**kwargs):
        
        super(SetMemberPartial,self).__init__(**kwargs)
        self.validations.append(_SetMemberPartialVdt(**kwargs))
        
class SetMember(BaseSetMember):
    def __init__(self,**kwargs):
        
        super(SetMember,self).__init__(**kwargs)
        
        self.validations.append(_SetMemberVdt(**kwargs))
                
        #self.set = kwargs['set']
        
class DBSetMember(BaseSetMember):
    def __init__(self,dbname,tblname,fldname,**kwargs):
        
        database = Database(dbname)
        with database:
            rows = tbl_rows_get(database,tblname,
                                         [fldname])
            
            # rows is a tuple; list is element 2
            kwargs['set'] = [row[0] for row in rows[1]]
        
        super(DBSetMember,self).__init__(**kwargs)
        self.validations.append(_SetMemberVdt(**kwargs))
        
class _TextAlphaNumVdt(_Validator):
    
    def __init__(self,**kwargs):
        super(_TextAlphaNumVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        r = re.compile("^[a-zA-Z0-9]*$")
        
        try:
            if r.match(value).group: return True
        except AttributeError:
            return False
        
class TextAlphaNum(BaseType):
    def __init__(self,**kwargs):
        
        super(TextAlphaNum,self).__init__()
        self.validations.append(_TextAlphaNumVdt(**kwargs))
        
class TextAlphaNumRO(TextAlphaNum):
    ''' readonly so has a Tklabel widget type '''
    def __init__(self,**kwargs):
        
        super(TextAlphaNumRO,self).__init__(**kwargs)
        from ui_utils import TkLabel
        self.widgettype = TkLabel
        
def isadatatype(datatype):
  
    try:
        if issubclass(datatype,BaseType): return True
    except TypeError:
    
        if hasattr(datatype,'__class__'):
            datatype = datatype.__class__
            if issubclass(datatype,BaseType):
                return True
            
    return False    