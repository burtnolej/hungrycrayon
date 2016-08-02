class foobar():
    
    blahblah = 'teehee'
    
    def boo(self):
        return("boo")

class foobar2():

    
    def boo2(self):
        a = 'var'
        b = 'avar'
        
        return("boohoo")
    
    def boohoo(self,banana):
        return("boohoo")

class mybase():
    pass

class foobar3(mybase):
    def boo3(self):
        self.foobar = foobar()
        return("boo")

def myfunc(fe, fi, fo, fum):
    foo = 'bar'
    pass

mylocal='blahblah'