#!/usr/bin/python

class Car():

    color = None
    speed = None

    def __init__(self,color,speed):
        self.color = color
        self.speed = speed
    @classmethod
    def blob(cls,color_speed):
        color, speed = color_speed.split()
        car1 = cls(color,speed)
        return car1

c1 = Car('red',123)
c2 = Car.blob('green 175')
