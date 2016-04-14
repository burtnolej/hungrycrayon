#!/usr/bin/python

end = 10
num = 0

def counter():
    global num
    if num != end:
        num = num + 1
        return True
    return False


while counter():
    print num

print "done"
