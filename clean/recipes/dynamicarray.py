


from array import array 


class darray(object):
    def __init__(self):
        self.columns={}
        
    def __getitem__(self,x):
        a = array('i')
        a.insert(5,1)
        return(a)
        
    def __setitem__(self,x,z):
        print x,z
        

da = darray()


# set
da[3]=4

# get

a = da[4]
print a[5]