#!/usr/bin/python
import sys
import gc
import types
import inspect

class Bike():
    pass

class Car(object):
    car_list = []
    subclassed = None

    def __init__(self,color,max_speed,subclassed=False):
        self.color=color
        self.max_speed=max_speed
        self.car_list.append(self)
        Car.subclass = True
        print self

    def _get_count(self):
        return(len(self.car_list))

    def __iter__(self):
        for c in self.car_list:
            yield c.color

class RacingCar(Car):
    def __init__(self,*args):
        super(RacingCar,self).__init__(*args)
        

class Node(object):
    object_count=0
    def __init__(self,depth=1,width=1,count=0):
        Node.object_count+=1
        print "".ljust(depth*5),depth,width,count,self

        if depth > 1:
            return

        self.depth = depth
        self.width = width
        self.parent = self
        self.children = []
        depth = self.depth+1
        for width in range(0,2):
            obj = Node(depth,width,Node.object_count)
            self.children.append(obj)

class MyNode(Node):
    def __init__(self,*args):
        super(MyNode,self).__init__(*args)


class MyClass():
        def __init__(self):
                self.mylist = [Bike(),Car("red",135)]
                self.myinstance = Bike()
                self.myobject = Car("gree",120)
                self.myint = 1

if __name__ == '__main__':

        #mynode = MyNode(5,10,0)

        #mini = Car('red',125)
        #jeep = Car('brown',140)

        #print Car.car_list
        #Car.car_list=[]

        #truck = Car('blue',80)
        #print Car.car_list

        rc = RacingCar('green',250,True)
        print rc.__class__.__bases__[0].__name__
        print issubclass(rc.__class__,Car)

        for r in rc:
                print r



    
    
