

import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")

import code_utils

import os

import xml.etree.ElementTree as xmltree

class Engine():
    def __init__(self, horsepower):
        self.horsepower_set(horsepower)
        
    def horsepower_set(self,horsepower):
        self.horsepower = horsepower
  
'''
class Gearbox():
    def __init__(self,gears_num):
        self.num_set(gears_num)
    
    def num_set(self,gears_num):
        self.gears_num = num_gears
        
class Wheels():
    def __init__(self,wheels_num):
        self.num_set(wheels_num)
    
    def num_set(self,num):
        self.num = num
        
class Vehicle():
    def __init__(self):
        self.engine = Engine(100)
        self.gearbox = Gearbox(5)
        self.location_set(0,0,0)
        
    def move(self,direction):
        pass
    
    def location_set(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
class Car(Vehicle):
    def __init__(self):
        self.engine = Engine(300)
        self.gearbox = Gearbox(6)
        self.wheels = Wheels(4)
        
def build():
    
    mycar = Car()
    pass
    
'''

if __name__ == '__main__':
    code_utils.code2xml(sys.modules[__name__],globals()['__file__'])