import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)

from misc_utils import nxnarraycreate, thisfuncname
from misc_utils_objectfactory import ObjFactory
import sswizard_utils
from ssviewer_utils_palette import *

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

#import ssviewer_utils_palette

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
    

def _getpage(grid,pagelen,pagenum):
    
    numrows = len(grid)
     
    startrow = 0
    if pagenum <> 1:
        startrow = ((pagenum-1)*pagelen)
     
    endrow=pagelen
    if numrows > pagelen:
        endrow =  (pagenum*pagelen)-1
        
    if endrow > numrows:
        endrow = numrows-1
         
    if startrow > numrows:
        startrow = numrows-pagelen
        endrow = numrows-1
    return(startrow,endrow)


def dataset_list(of,enums,pagelen=30,pagenum=1):
    
    source_objs = of.query('lesson')
        
    grid = []
    colnames = list(source_objs[0].dm.keys())

    grid.append(colnames)
    
    startrow,endrow = _getpage(source_objs,pagelen,pagenum)

    for i in range(startrow,endrow+1):        
        grid.append(source_objs[i].dm.values())
          
    return grid,colnames

    
def dataset_pivot(of,enums,yaxis_type,xaxis_type,ztypes, source_type,source_value,
           conflicts_only='N',constraints=None,wratio=None,formatson=False):
    
    ''' query in memory objects; pivot data and create a table of results; return in 2d array '''
        
    if source_value == "":
        source_objs = of.query(source_type)
    else:
        source_objs = [of.object_get(source_type,source_value)]
        
    xaxis_obj = of.query(xaxis_type)
    yaxis_obj = of.query(yaxis_type)
    
    count=0
    yaxis_enum = {}
    for _yaxis_obj in yaxis_obj:
        yaxis_enum[_yaxis_obj.name] = count
        count+=1
    
    xaxis_enum = enums[xaxis_type]['name2enum']
    
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
    
    return values

def dataset_serialize(values,formatson,schema=None):

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
                                bgs,fgs = _color_get_multi(_value[0])
                                
                                _formats = []
                                for i in range(len(_value[0])):
                                    args = dict(value=_value[0][i],bgcolor=bgs[i],fgcolor=fgs[i])
                                    if schema<>None: args['valuetype'] = schema['ztypes'][i]
                                    _formats.append(args)
                                    
                                    
                                values[x][y].append(tuple(_formats))
                            elif isinstance(_value[0],list) == False:
                                # 1 item, single value
                                bg,fg = color_get(_value[0])

                                print "1,1 attr",_value[0],bgs,fgs
                        # multiple items
                        ''' uncomment if want to generate conflicts report'''
                        #if len(_value) > 1 and conflicts_only == "Y":
                        if len(_value) > 1:
                            for __value in _value:
                                bgs,fgs = _color_get_multi(__value)
                                _formats = []
                                for i in range(len(__value)):
                                    args = dict(value=__value[i],bgcolor=bgs[i],fgcolor=fgs[i])
                                    if schema<>None: args['valuetype'] = schema['ztypes'][i]
                                    _formats.append(args)

                                    
                                values[x][y].append(tuple(_formats))
                else:
                    #if x == 0 or y == 0:
                    if x == 0:
                        args = dict(value=_value,bgcolor=colors.black,fgcolor=colors.white)
                        if schema<>None: 
                            if isinstance(schema['yaxis'],list):
                                args['valuetype'] = schema['yaxis']
                        values[x][y] = args
                    elif y == 0:
                        args = dict(value=_value,bgcolor=colors.black,fgcolor=colors.white)
                        if schema<>None: args['valuetype'] = schema['xaxis']
                        values[x][y] = args
                    else:
                        
                        bg,fg = color_get(_value)
                        #bgs,fgs = _color_get_multi(_value)
                        args = dict(value=_value,bgcolor=bg,fgcolor=fg)
                        if schema<>None: args['valuetype'] = schema['colnames'][y]
                        values[x][y] = args
                            
    return values
    
def _lesson_change(lesson):

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

def dataset_load(database,refdatabase,of,enums,saveversion=1,unknown='N',prep=-1,period="all",
                 dow="all",teacher="all",student="all",source="dbinsert"):
    
    of.reset()
    
    whereclause = []
    
    # saveversion
    log.log(thisfuncname(),3,msg="loading",saveversion=str(saveversion))
    whereclause.append(['saveversion',"=",saveversion])
    
    # unknown
    if unknown=='N':
        whereclause.append(['student',"<>","\"??\""])
        whereclause.append(['subject',"<>","\"??\""])
        whereclause.append(['teacher',"<>","\"??\""])
    log.log(thisfuncname(),3,msg="loading",unknown=str(unknown))
        
    # prep
    if  prep <> -1:
        whereclause.append(['prep',"=",prep])
    log.log(thisfuncname(),3,msg="loading",prep=str(prep))
    
    # period
    if period <> "all":
        whereclause.append(['period',"=","\""+period+"\""])            
    log.log(thisfuncname(),3,msg="loading",prep=str(prep))

    # dow
    if dow <> "all":
        whereclause.append( ['dow',"=","\""+dow+"\""])
    log.log(thisfuncname(),3,msg="loading",dow=str(dow))
    
    # teacher
    if teacher <> "all":
        whereclause.append( ['teacher',"=","\""+teacher+"\""])
    log.log(thisfuncname(),3,msg="loading",teacher=str(teacher))      
    
    # student
    if student <> "all":
        whereclause.append( ['student',"=","\""+student+"\""])
    log.log(thisfuncname(),3,msg="loading",student=str(student))
    
    # source
    #if source <> "dbinsert":
    _sources = ["\"" + _source + "\"" for _source in source.split(",")]
    whereclause.append( ['source',"in","("+",".join(_sources)+")"])
    log.log(thisfuncname(),3,msg="loading",source=str(source))

    # load from database
    cols = ['period','student','session','dow','teacher','subject','userobjid','status','substatus','recordtype','source']        
    with database:
        colndefn,rows,exec_str = tbl_rows_get(database,'lesson',cols,whereclause)

        log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
    
    cols = ['period','student','session','dow','adult','subject','userobjid','status','substatus','recordtype','source']
    
    # parse rows
    for row in rows:
        datamembers = {}
        for i in range(len(cols)):
            datamembers[cols[i]] = row[i]
        
        _,lessontype_code,_,_ = datamembers['session'].split(".")
        datamembers['objtype'] = 'lesson'                               

        lesson = of.new(schoolschedgeneric,'lesson',objid=datamembers['userobjid'],
                             constructor='datamembers',database=database,
                             of=of,modname=__name__,dm=datamembers)
        
        _lesson_change(lesson)
                        
        log.log(thisfuncname(),3,msg="loading row",dm=datamembers)

    # post log with results
    log.log(thisfuncname(),3,msg="db rows loaded",num=len(rows))        
    for i in range(len(cols)):
        log.log(thisfuncname(),3,msg="lesson obj created",num=len(of.store[cols[i]]))
    
