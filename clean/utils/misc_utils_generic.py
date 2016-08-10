import sys
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils import Log,IDGenerator

class GenericBase(object):
    
    def _setattr(self,attr,suffix=''):
        for key,value in attr.iteritems():
            setattr(self,suffix+key,value)
            
    def __init__(self,**kwarg):
        self._setattr(kwarg)
        self.log = Log()
        self.id =  IDGenerator().getid()
        
    def attr_get_keyval(self,include_callable=True, 
                        include_baseattr=True,
                        include_nondataattr=True):
        ''' ignore contains a list of suffixes. all attr with this
        suffix should be ignored'''
        from inspect import getmro, getmembers
    
        new_attr=[]
        basecls = getmro(self.__class__)
    
        for _name,_val in getmembers(self):
            baseattr=False
            dataattr=False
            
            # this is used internally and will never be returned
            # use obj.name to access
            if _name == 'dm':
                continue
            
            if hasattr(self,'dm') == True:
                if _name in getattr(self,'dm').keys():
            #if _name.startswith('_dm_') == True:
                    dataattr=True
                #_name = _name.replace('_dm_','')
                
            for cls in basecls:
                if hasattr(cls,_name):
                    baseattr=True     
            
            if not _name.startswith("__"):
                
                if callable(_val) and include_callable == False:
                    continue
                      
                if baseattr==True and include_baseattr == False:
                    continue
                
                if dataattr==False and include_nondataattr == False:
                    continue

                new_attr.append((_name,_val))
        return(new_attr) 

    @classmethod
    def datamembers(cls,**kwarg):
        ''' constructor is used when special attributes want to be added
        to the object for extraction later; their names are mangled with
        a suffix of _dm_ so they can be identified later. this is usually
        for writing objects to a datatbase etc'''
        
        if not kwarg.has_key('dm'):
            raise Exception('dm arg not set; are you using the correct constructor')
        
        _datamembers = kwarg['dm']
        
        #kwarg.pop('datamembers')
        
        if not isinstance(_datamembers,dict):
            raise Exception("arg datamember must be of type dict")

        for dm in _datamembers.keys():
            if dm in kwarg.keys():
                raise Exception("attr",dm,"cannot appear in both dm and regular attr") 
        
        cls1 = cls(**kwarg)
        
        #cls1._setattr(_datamembers,'_dm_')
        cls1._setattr(_datamembers)
        
        return(cls1)