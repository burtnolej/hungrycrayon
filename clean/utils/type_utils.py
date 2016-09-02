class Validator(object):
    def __init__(self,name,**kwargs): 
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
    
    def validate(self,value):
        for validator in self.validations:
            
            if validator(value) == False:
                return False
            
        return True

class BIntType(BType):
    def __init__(self):
        validations.append(IntVdt())
        validations.append(BIntVdt())
        
class Basestr(Basetype):
    def validate(self,value):
        try:
            str(value)
        except:
            return False