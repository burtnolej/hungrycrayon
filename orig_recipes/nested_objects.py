#!/usr/bin/python

import inspect
from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from table_print import SimpleTable
from types import InstanceType
from misc_util import Logger

class XYZ():
    pass
class Node(object):
    object_count=0
    def __init__(self,depth,width,count):
        Node.object_count+=1
        print "".ljust(depth*5),depth,width,count,self

        if depth > 1:
            return

        self.depth = depth
        self.width = width
        self.parent = self
        self.children = []
        #self.mixed_list = ['a',1,Node,['b',2,XYZ()]]
        self.mixed_list = ['a',1,Node]
        
        depth = self.depth+1
        for width in range(0,2):
            # make sure we call the sub class contructor
            obj = self.__class__(depth,width,Node.object_count)
            self.children.append(obj)

class MyNode(Node):
    def __init__(self,depth,width,count):
            super(MyNode,self).__init__(depth,width,count)
            self.node_count = count            

def myfunc():
    attr = MyNode(0,0,0)
    pass
    
class MyClass():
    def __init__(self):
        self.attr1 = "a"
        self.attr2 = 1
        self.func = myfunc

if __name__ == '__main__':
    #logger = Logger()

    node = MyNode(0,0,0)
    #for i in range(0,10):
    #    print "run:",i
    #    deep_pretty_print_object(anobject)

    #l = ['a','b',{'c':3,'d':4,'e':['x','y','z',MyClass()]}]
    l = ['a','b',{'c':3,'d':4,'e':['x','y','z']}]
    #l = ['a','b',MyClass()]
    #MyTable(node,"").deep_print()
    #MyTable(l,"").deep_print()
    #t = MyTable(l,"")

    SimpleTable(l,"").deep_print()

    #del logger
