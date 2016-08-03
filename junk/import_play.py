import unittest

class foobar():
    
    def blah(self):
        import unittest
    
    def blahblah(self):
        
    
print globals()['unittest']

del unittest

f = foobar()
f.blah()
print globals()['unittest']

