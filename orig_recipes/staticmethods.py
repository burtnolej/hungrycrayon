#!/usr/bin/python


class MyClass(object):

    mylist = ['a','b']

    @staticmethod
    def get_len():
        print len(MyClass.mylist)


MyClass.get_len()
