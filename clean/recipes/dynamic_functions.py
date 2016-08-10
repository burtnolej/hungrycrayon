
from inspect import stack
import functools
import new

def apply_defaults(cls):
    defaults = {}
   
    for attr in ['a','b']:
    
        def outer(cls,attr):
            def func():
                return(getattr(cls,'_dm_'+attr))
            return func
    
        f = new.function(outer(cls,attr).__code__,
                         globals(),
                         attr,
                         closure=outer(cls,attr).func_closure)   
   
        setattr(cls,attr,property(fget=f))
        
    return cls
                
@apply_defaults
class myclass2(object):
    
    _dm_a = 123
    _dm_b = 456
    
mc = myclass2()
print mc.a

#myclass2 = apply_defaults(myclass2)

print dir(myclass2)

print myclass2.a

'''class myclass(object):
    slots = {}
    
    def __init__(self):
        self._dm_a = 123
        self._dm_b = 123
        
        for attr in ['a','b']:

            def outer(self,attr):
                def func():
                    return(getattr(self,'_dm_'+attr))
                return func

            f = new.function(outer(self,attr).__code__,
                             globals(),
                             attr,
                             closure=outer(self,attr).func_closure)
            slots[attr]=f
            
      
    setattr(self,attr,property(fget=f))'''
            
        
'''mc = myclass()

print mc.a
print mc.b'''