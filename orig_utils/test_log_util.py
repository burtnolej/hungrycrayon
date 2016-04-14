#!/usr/bin/python
from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from log_util import LogMeta

class ClassLogMeta():
    __metaclass__ = LogMeta

    def funcA(self,*arg):
        self.funcB("C")

    def funcB(self,*arg):
        self.funcC(*arg)

    def funcC(self,*arg):
        pass

    funcC.log = True
    funcA.log = True

clm = ClassLogMeta()
clm.funcA("A")
#clm.funcB("B")
