#!/usr/bin/python

class A():
    def __init__(self):
        print "a"

class B(A):
    def __init__(self):
        print A.__init__(self)
        #print super(B,self)
        #super(B,self).__init__()
        print "b"

c = B()



'<mapversion="0.9.0"><nodeTEXT="formats.xml"><nodeTEXT="foobar"><fontBOLD="false"ITALIC="False"NAME="SansSerif"SIZE="18"/></node></node></map>'
'<mapversion="0.9.0"><nodeTEXT="formats.xml"><nodeBACKGROUND_COLOR="#85144B"COLOR="#FFFFFF"STYLE="bubble"TEXT="foobar"><fontBOLD="false"ITALIC="False"NAME="SansSerif"SIZE="18"/></node></node></map>'

