import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)

from misc_utils_process import *
from misc_utils_enum import enum
from misc_utils import nxnarraycreate, thisfuncname

from type_utils import SetMemberPartial, DBSetMember, TextAlphaNumRO
from misc_utils_objectfactory import ObjFactory

import sswizard_utils
from sswizard_query_utils import *
from sswizard_config_utils import *

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from collections import OrderedDict

pink = '#%02x%02x%02x' % (255, 153, 153)
salmon = '#%02x%02x%02x' % (255, 204, 153)
lightyellow = '#%02x%02x%02x' % (255, 255, 153)
lightgreen = '#%02x%02x%02x' % (204, 255, 153)
lightturquoise = '#%02x%02x%02x' % (153, 255, 204)
lightblue = '#%02x%02x%02x' % (153, 255, 255)
lavender = '#%02x%02x%02x' % (153, 153, 255)
purple = '#%02x%02x%02x' % (204, 153, 255)
pink = '#%02x%02x%02x' % (255, 153, 204)
darkgreen = '#%02x%02x%02x' % (0, 102, 0)
burgundy = '#%02x%02x%02x' % (102, 0, 51)
karky = '#%02x%02x%02x' % (102, 102, 0)
darkburgundy = '#%02x%02x%02x' % (102, 0, 51)
darkgrey = '#%02x%02x%02x' % (0, 51, 51)
brown = '#%02x%02x%02x' % (102, 51, 0)
mauve = '#%02x%02x%02x' % (204, 204, 0)
navyblue = '#%02x%02x%02x' % (0, 0, 51)
darkyellow = '#%02x%02x%02x' % (155,140,6)
paleblue = '#%02x%02x%02x' %(173,217,222)
palegreen = '#%02x%02x%02x' %(183,229,183)
cerise = '#%02x%02x%02x' %(212, 7, 253)
red = '#%02x%02x%02x' %(255, 0, 0)
black = '#%02x%02x%02x' %(255, 255, 255)
white = '#%02x%02x%02x' %(0, 0, 0)
green = '#%02x%02x%02x' %(0, 255, 0)
blue = '#%02x%02x%02x' %(0, 0, 255)
lightgrey = '#%02x%02x%02x' % (211, 211, 211)

verydarkgrey = '#%02x%02x%02x' %(54, 46, 55)
dirtyyellow = '#%02x%02x%02x' %(242, 232, 19)

class schoolschedgeneric(dbtblgeneric):

    def __init__(self,of,database,recursion=True,**kwargs):
        self.recursion = recursion
        super(schoolschedgeneric,self).__init__(database=database,
                                                **kwargs)
        
        self.of = of
        self.database = database
        
        for k,v in kwargs['dm'].iteritems():
            if v <> 'None':
                if recursion == True:
                    # create objects for all member attributes
                    self.attr_set(v,k)
                                   
    def attr_set(self,name,clsname):        
        datamembers = dict(objtype=clsname,
                           userobjid=name,
                           name=name)
        
        setattr(self,clsname,self.of.new(schoolschedgeneric,
                                         clsname,
                                         objid=name, # unique key to store obj in of
                                         constructor='datamembers',
                                         database=self.database,
                                         of=self.of,
                                         modname=__name__,
                                         recursion=False,
                                         dm=datamembers))

            
        return(getattr(self,clsname))

class SSViewer(object):

    def __init__(self,dbname,refdbname):
        
        log.log(thisfuncname(),3,msg="initialize",dbname=dbname,refdbname=refdbname)

        self.colorpalette = dict(wp=green,subject=lightblue,ap='yellow',
                                 Movement=pink,ELA=salmon,Humanities=lightyellow,
                                 Counseling=lightgreen,Math=lightturquoise, 
                                 Music=lightblue,STEM=lavender,Art=purple,History=pink,
                                 Science=darkgreen,Core=karky,Chess=burgundy,
                                 computertime='darkgrey',Speech=darkburgundy,
                                 Student_News=darkgrey,Computer_Time=brown,
                                 Activity_Period=mauve,Melissa=navyblue,Amelia=darkgreen,
                                 Samantha=darkyellow, Alexa=paleblue, Paraic=palegreen, 
                                 Francisco=cerise,Rahul=verydarkgrey,Dylan=verydarkgrey,
                                 Moira=verydarkgrey,Issey=verydarkgrey, Daryl=verydarkgrey, 
                                 Karolina=verydarkgrey)
        

        self.fontpalette = dict(Amelia=green,Paraic=darkgreen,Stan=lavender,
                                Samantha=lightgreen,Alexa=blue,Francisco=purple,
                                Melissa=lightblue,Rahul=dirtyyellow,Dylan=dirtyyellow, 
                                Moira=dirtyyellow,Issey=dirtyyellow, Daryl=dirtyyellow, 
                                Karolina=dirtyyellow,Chess=pink,Student_News=lightyellow,
                                subject=blue)
        
        
        self.of = ObjFactory(True)
        
        self.refdatabase = Database(refdbname)        
        self.dbname = dbname
        self.database = Database(self.dbname)
        self.lastsaveversion=0

    def _color_get_multi(self,values):
        bgs=[]
        fgs=[]
        for value in values:
            _bg,_fg = self.color_get(value)
            bgs.append(_bg)
            fgs.append(_fg)
        return(bgs,fgs)
    
    def color_get(self,value):
        
        bg = lightgrey
        fg = black
            
        try:
            int(value)
            value = str(value)
        except ValueError:
            pass
        
        if value.count(" ") > 0:
            value= value.replace(" ","_")
            
        if value.count("[") == 1 and value.count("]") == 1:
            bg = red
        
        if value.count(".") > 0:
            value = value.split(".")[0]
            
        if self.colorpalette.has_key(value):
            bg = self.colorpalette[value]
            
        if self.fontpalette.has_key(value):
            fg = self.fontpalette[value]
            
            
        return(bg,fg)        
        
    def viewer(self,yaxis_type,xaxis_type,ztypes, source_type,source_value,
               conflicts_only='N',constraints=None,wratio=None,formatson=False):
            
        if source_value == "":
            source_objs = self.of.query(source_type)
        else:
            source_objs = [self.of.object_get(source_type,source_value)]
            
        xaxis_obj = self.of.query(xaxis_type)
        yaxis_obj = self.of.query(yaxis_type)
        
        count=0
        yaxis_enum = {}
        for _yaxis_obj in yaxis_obj:
            yaxis_enum[_yaxis_obj.name] = count
            count+=1
        
        xaxis_enum = self.enums[xaxis_type]['name2enum']
        
        values = [] # contains the values displayed on the grid

        values = [['']]    
        for yval in yaxis_enum.keys():
            values[0].append(yval)
            
        for xval in xaxis_enum.keys():
            values.append([xval])

        ymax = len(values[0])
        xmax = len(values)-1
        
        def _additem(celltext,item):
            
            if len(celltext) == 0:
                celltext.append(item)
            else:
                try:
                    celltext.index(item)
                except:
                    celltext.append(item)
            return(celltext)
                
        for yval,y in yaxis_enum.iteritems():
            
            for xval,x in xaxis_enum.iteritems():
                celltext=[]
                
                for source_obj in source_objs:
                    if source_obj.lessons.has_key(yval):
                        if source_obj.lessons[yval].has_key(xval):
   
                            _vals = source_obj.lessons[yval][xval]

                            for _val in _vals:
                                
                                if constraints <> None:
                                    flag=False
                                    for objtype,objval in constraints:
                                        
                                        if getattr(_val,objtype).name <> objval:
                                            flag=True
                                    if flag == True:
                                        continue
                                    
                                if ztypes == ['*']:
                                    if celltext == []:
                                        celltext.append(0)
                                    else:
                                        celltext[0] = celltext[0] + 1
                                    continue

                                _celltext = []
                                
                                for ztype in ztypes:
                                    if hasattr(_val,ztype) == True:
                                        zval = getattr(_val,ztype)
                                        
                                        try:
                                            _celltext.index(zval.name)
                                        except:
                                            _celltext = _additem(_celltext,zval.name)
                                            pass
                                            
                                try:      
                                    celltext.index(tuple(_celltext))
                                except:
                                    celltext.append(tuple(_celltext))
                                    
                values[x].append(celltext)
        
        sswizard_utils.gridreduce(values,[[]])

        if formatson==True:                
            for x in range(len(values)):
                for y in range(len(values[x])):
                    _value = values[x][y]

                    if isinstance(_value,list) == True:
                        if _value <> []:
                            values[x][y] = []
                            ''' uncomment if want to generate conflicts report'''
                            #if len(_value) == 1 and conflicts_only <> "Y":
                            if len(_value) == 1:
                                if isinstance(_value[0],tuple) == True:
                                    # 1 item, multi attributes
                                    bgs,fgs = self._color_get_multi(_value[0])
                                    _formats = []
                                    for i in range(len(_value[0])):
                                        _formats.append(dict(value=_value[0][i],bgcolor=bgs[i],fgcolor=fgs[i]))
                                        
                                    values[x][y].append(tuple(_formats))
                                elif isinstance(_value[0],list) == False:
                                    # 1 item, single value
                                    bg,fg = self.color_get(_value[0])

                                    print "1,1 attr",_value[0],bgs,fgs
                            # multiple items
                            ''' uncomment if want to generate conflicts report'''
                            #if len(_value) > 1 and conflicts_only == "Y":
                            if len(_value) > 1:
                                for __value in _value:
                                    bgs,fgs = self._color_get_multi(__value)
                                    _formats = []
                                    for i in range(len(__value)):
                                        _formats.append(dict(value=__value[i],bgcolor=bgs[i],fgcolor=fgs[i]))
                                        
                                    values[x][y].append(tuple(_formats))
                    else:
                        if x == 0 or y == 0:
                            values[x][y] = dict(value=_value,bgcolor=black,fgcolor=white)
                                
            
            return values

    def lesson_change(self,lesson):

        def _add(obj,xtype,ytype,lesson):
            
            xtype_id = getattr(lesson,xtype).objid
            ytype_id = getattr(lesson,ytype).objid
            
            # indexed by dow/period
            if obj.lessons.has_key(xtype_id) == False:
                obj.lessons[xtype_id] = {} 
    
            if obj.lessons[xtype_id].has_key(ytype_id) == False:
                obj.lessons[xtype_id][ytype_id] = []
                
            obj.lessons[xtype_id][ytype_id].append(lesson)
        
        adult = lesson.adult
        student = lesson.student

        # add the lesson to the adult object        
        if hasattr(adult,'lessons') == False:
            setattr(adult,'lessons',{})
            
        _add(adult,'dow','period',lesson) # indexed by dow/period
        _add(adult,'student','period',lesson) # indexed by student/period

        # add the lesson to the student object
        if hasattr(student,'lessons') == False:
            setattr(student,'lessons',{})
            
        _add(student,'dow','period',lesson) # indexed by dow/period
        _add(student,'adult','period',lesson) # indexed by adult/period
        _add(student,'period','recordtype',lesson) # indexed by adult/period
        _add(student,'student','recordtype',lesson) # indexed by adult/period
        

    @logger(log)       
    def load(self,saveversion, dow=None, prep=None, period=None, teacher=None, student=None, source=None,
             unknown='N'):
        
        self.of.reset()
            
        whereclause = []
        
        # unknown
        if unknown=='N':
            whereclause.append(['student',"<>","\"??\""])
            whereclause.append(['subject',"<>","\"??\""])
            whereclause.append(['teacher',"<>","\"??\""])
        log.log(thisfuncname(),3,msg="loading",unknown=str(unknown))
            
        # prep
        if prep==None:
            prep = -1
        else:
            whereclause.append(['prep',"=",prep])
        log.log(thisfuncname(),3,msg="loading",prep=str(prep))
        
        # period
        if period==None: 
            prep = -1
        else:
            whereclause.append(['period',"=","\""+period+"\""])            
        log.log(thisfuncname(),3,msg="loading",prep=str(prep))

        # dow
        if dow==None:
            dow = "all"
        else:
            whereclause.append( ['dow',"=","\""+dow+"\""])
        log.log(thisfuncname(),3,msg="loading",dow=str(dow))
        
        
        # teacher
        if teacher==None: 
            teacher = "all"
        else:
            whereclause.append( ['teacher',"=","\""+teacher+"\""])
        log.log(thisfuncname(),3,msg="loading",teacher=str(teacher))      
        
        # student
        if student==None: 
            student = "all"
        else:
            whereclause.append( ['student',"=","\""+student+"\""])
        log.log(thisfuncname(),3,msg="loading",student=str(student))
        
        # source
        if source==None: 
            source = "dbinsert"
        else:
            _sources = ["\"" + _source + "\"" for _source in source.split(",")]
            whereclause.append( ['source',"in","("+",".join(_sources)+")"])
        log.log(thisfuncname(),3,msg="loading",source=str(source))

        # get enums
        self.enums = sswizard_utils.setenums(dow,prep,self.refdatabase)

        # load from database
        cols = ['period','student','session','dow','teacher','subject','userobjid','status','substatus','recordtype','source']        
        with self.database:
            colndefn,rows,exec_str = tbl_rows_get(self.database,'lesson',cols,whereclause)
            
            log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
        
        cols = ['period','student','session','dow','adult','subject','userobjid','status','substatus','recordtype','source']
        
        # parse rows
        for row in rows:
            datamembers = {}
            for i in range(len(cols)):
                datamembers[cols[i]] = row[i]
            
            _,lessontype_code,_,_ = datamembers['session'].split(".")
            #lessontype = self.enums['lessontype']['code2name'][lessontype_code]      
            datamembers['objtype'] = 'lesson'                               

            lesson = self.of.new(schoolschedgeneric,'lesson',objid=datamembers['userobjid'],
                                 constructor='datamembers',database=self.database,
                                 of=self.of,modname=__name__,dm=datamembers)
            
            self.lesson_change(lesson)
                            
            log.log(thisfuncname(),3,msg="loading row",dm=datamembers)

        # post log with results
        log.log(thisfuncname(),3,msg="db rows loaded",num=len(rows))        
        for i in range(len(cols)):
            log.log(thisfuncname(),3,msg="lesson obj created",num=len(self.of.store[cols[i]]))

    def updates_get(self,gridname,ignoreaxes=False):
        
        return(sswizard_utils.updates_get(self,gridname,ignoreaxes))
        
    def _lastsaveversion_get(self):
        
        try:
            with self.database:
            
                colndefn,rows = tbl_query(self.database,"select max(saveversion) from lesson")                   
            return(rows[0][0])
        except Exception:
            return(-1)
        
if __name__ == "__main__":
    
    ssviewer = SSViewer('test_ssloader','test_ssloader')
    
    args = dict(saveversion=1)
    print "loading with args=",args,
    ssviewer.load(**args)

    print ssviewer.viewer('dow','period',['adult','subject'],"student","Peter",formatson=True)