

class Basetype(object):
    def validate(self,value):
        return True

class Baseint(Basetype):
    ''' free int; any value '''
    def __init__(self,name,**kwargs): 
        self.name = name
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
        
    def __call__(self,value):
        return(self.validate(value))

    def validate(self,value):
        if hasattr(self,'lbound'):
            if int(value) < self.lbound:
                return False

        if hasattr(self,'ubound'):
            if int(value) > self.ubound:
                return False
        return True

class Mstr(Baseint):
    ''' string that is the member of a list '''
    pass

