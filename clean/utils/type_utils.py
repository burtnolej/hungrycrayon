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

class IntVdt(Validator):
    def validate(self,value):
        try:
            int(value)
        except:
            return False
        
class BIntVdt(Validator):
    ''' Bounded int validator '''
    
    def __init__(self,**kwargs):
        if not kwargs.has_key('ubound') and not kwargs.has_key('lbound'):
            raise Exception('ubound or lbound argument must be passed')
        super(BIntVdt,self).__init__(**kwargs)
        
    def validate(self,value):
        if hasattr(self,'lbound'):
            if int(value) < self.lbound:
                return False

        if hasattr(self,'ubound'):
            if int(value) > self.ubound:
                return False
        return True

class BType(object):
    def __init__(self):
        self.validations = []
    
    def __call__(self,value):
        return(self.validate(value))
    
    def validate(self,value):
        for validator in self.validations:
            
            if validator(value) == False:
                return False
            
        return True

class IntType(BType):
    def __init__(self,**kwargs):
        
        super(IntType,self).__init__()
        self.validations.append(IntVdt(**kwargs))
        
class BIntType(IntType):
    ''' bounded int type ; support upper and/or lower bound
    ubound,lbound need to be passed in as kw args'''
    def __init__(self,**kwargs):
        
        super(BIntType,self).__init__(**kwargs)
        self.validations.append(BIntVdt(**kwargs))
        
class Basestr(BType):
    def validate(self,value):
        try:
            str(value)
        except:
            return False