import sys
import os

from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)

from misc_utils import nxnarraycreate, thisfuncname
from misc_utils_objectfactory import ObjFactory
from misc_utils_generic import IDGenerator
import sswizard_utils
from ssviewer_utils_palette import *
#from ssviewer_utils_palette import init_formats

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query, tbl_rows_insert, \
     tbl_rows_update, tbl_exists, tbl_create

from ssviewer_utils_palette import dbformats_get, dbcolors_get

from copy import deepcopy

dbname,_ = sswizard_utils.getdatabase()

colorpalette = dbformats_get(dbname,'bgcolor')
fontpalette = dbformats_get(dbname,'fgcolor')
colors = dbcolors_get(dbname)

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
       
    def persist(self,createtable=True):

        self._metadata_set()

        try:
            _idx = self.tbl_col_defn.index('adult')
            self.tbl_col_defn.remove('adult')
            self.tbl_col_defn.insert(0,'teacher')
        except:
            pass
        
        if not tbl_exists(self.database,self.tbl_name) ==True:
            tbl_create(self.database,
                       self.tbl_name,
                       self.tbl_col_defn)

        try:
            _idx = self.tbl_col_names.index('adult')
            self.tbl_col_names.remove('adult')
            self.tbl_col_names.insert(0,'teacher')
        except:
            pass

        # and also objtype is not persisted
        try:
            _idx = self.tbl_col_names.index('objtype')
            self.tbl_col_names.pop(_idx)
            self.tbl_row_values[0].pop(_idx)
        except:
            pass
        
        result,exec_str = tbl_rows_insert(self.database,
                                          self.tbl_name,
                                          self.tbl_col_names,
                                          self.tbl_row_values)

        return(result,exec_str)


    def update(self,field,newvalue,dbname=None):

        # this is needed to get around the sqlite limitation that
        # an sqlite cursor can only be used in the thread it was instantiated in
        if dbname <> None:
            database = Database(dbname)
        else:
            database = self.database
            
        # this is over writing the base class update
        
        # these are hacks; and the datatypes id/adult need to be
        # called the same thing internally all the time
        # until then though ....

        # remove the id field as its set on the object from the
        # internal __id field for convenience but should not be repersisted
        # as the database layer will create the new __id for any revisions
        
        _oldidobj = getattr(self,'id')
        #_id = getattr(self,'id').name
        #setattr(self,"__id",_id)
        setattr(self,"__id",_oldidobj.name)
            
        delattr(self,'id')

        self.tbl_row_value_get(False)
        self.tbl_col_defn_get(False)
        self.tbl_name_get()

        # and also 
        try:
            _idx = self.tbl_col_names.index('adult')
            self.tbl_col_names.remove('adult')
            self.tbl_col_names.insert(0,'teacher')
        except:
            pass

        # and also objtype is not persisted
        try:
            _idx = self.tbl_col_names.index('objtype')
            self.tbl_col_names.pop(_idx)
            self.tbl_row_values[0].pop(_idx)
        except:
            pass

        currentrecord = dict(zip(self.tbl_col_names,self.tbl_row_values[0]))

        _id = IDGenerator().getid()
        _ts = self._gettimestamp()

        newrecord = deepcopy(currentrecord)
        newrecord['__version'] = "\"current\""
        newrecord[field] = "\"" + str(newvalue) + "\""
        newrecord['__id'] = "\""+_id+"\""
        newrecord['saveversion'] = 1

        newrecord['__timestamp'] = "\""+_ts+"\""

        if currentrecord[field] <> newrecord[field]:
            # create a new row in the database with version "current"

            with database:
                result,exec_str = tbl_rows_insert(database,
                                                  self.tbl_name,
                                                  newrecord.keys(),
                                                  [newrecord.values()])
    
                # update version of current row to version "version"
                tbl_rows_update(database,self.tbl_name,['__version',"\"version\"",
                                                             '__id',"\""+getattr(self,"__id")+"\""])

            # update in mem object to new val and new db version id and timestamp
            
            # assumes that field is also an objects whose value is in the name attr
            _oldobj = getattr(self,field)
            setattr(_oldobj,'name',newvalue)

            # give the new updated record the same database ref id as prev version
            setattr(_oldidobj,"name",_id)
            setattr(self,'id',_oldidobj)
            
            #setattr(self,'id',_id)
            setattr(self,'__version',"current")
            setattr(self,'__timestamp',_ts)
    

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


def dataset_list(of,enums,pagelen=30,pagenum=1,constraints=None,columns=None):

    source_objs = of.query_advanced('lesson',constraints)
        
    grid = []
    colnames = list(source_objs[0].dm.keys())

    grid.append(colnames)
    
    startrow,endrow = _getpage(source_objs,pagelen,pagenum)

    for i in range(startrow,endrow+1):
        if columns== None:
            grid.append(source_objs[i].dm.values())
        else:
            _l=[]
            for col in columns:
                _l.append(source_objs[i].dm[col])
            grid.append(_l)
            
    return grid,colnames

def dataset_record(of,clsname,objid):
    
    if of.object_exists(clsname,objid) == True:   
        obj = of.object_get(clsname,objid)
        return(obj.dm)

    return({})
    
def dataset_pivot(of,enums,yaxis_type,xaxis_type,ztypes, source_type,source_value,
           conflicts_only='N',constraints=None,wratio=None,formatson=False,rollupson=False):
    
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
                            
                            if constraints <> None and constraints <> []:
                                flag=False
                                
                                
                                for objtype,objval in constraints:

                                    if str(getattr(_val,objtype).name) <> str(objval):
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
    
    if rollupson == True:
        sswizard_utils.gridrollup(values,['subject','adult'],dict(ztypes='subject,adult,student'))

    return values


def dataset_serialize(values,formatson,schema=None):

    #if formatson==True:                
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
                                    args = dict(value=_value[0][i])
                                    #args = dict(value=_value[0][i],bgcolor=bgs[i],fgcolor=fgs[i])
                                    if schema<>None: args['valuetype'] = schema['ztypes'][i]
                                    
                                    
                                    if formatson==True:
                                        args['bgcolor'] = bgs[i]
                                        args['fgcolor'] = fgs[i]
                                        
                                    _formats.append(args)
                                    
                                    
                                values[x][y].append(tuple(_formats))
                            elif isinstance(_value[0],list) == False:
                                # 1 item, single value
                                _formats = []
                                
                                args = dict(value=_value[0])
                                
                                if formatson==True:
                                    args['bgcolor'] = bgs[i]
                                    args['fgcolor'] = fgs[i]
                                         
                                _formats.append(args)
                                values[x][y].append(tuple(_formats))
                                
                        # multiple items
                        ''' uncomment if want to generate conflicts report'''
                        #if len(_value) > 1 and conflicts_only == "Y":
                        if len(_value) > 1:
                            for __value in _value:
                                bgs,fgs = _color_get_multi(__value)
                                _formats = []
                                for i in range(len(__value)):
                                    #args = dict(value=__value[i],bgcolor=bgs[i],fgcolor=fgs[i])
                                    args = dict(value=__value[i])
                                    if schema<>None: args['valuetype'] = schema['ztypes'][i]
                                    
                                    if formatson==True:
                                        if formatson==True:
                                            args['bgcolor'] = bgs[i]
                                            args['fgcolor'] = fgs[i]
                                    _formats.append(args)

                                    
                                values[x][y].append(tuple(_formats))
                else:
                    #if x == 0 or y == 0:
                    if x == 0:
                        
                        args = dict(value=_value,bgcolor=colors.black,fgcolor=colors.white)
                        if schema<>None: 
                            #if isinstance(schema['yaxis'],list):
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
    subject = lesson.subject

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

    # add the lesson to the subject object        
    if hasattr(subject,'lessons') == False:
        setattr(subject,'lessons',{})
        
    _add(subject,'dow','period',lesson) # indexed by dow/period
    
    
def dataset_add(database,refdatabase,of,enums,prepmap,datamembers,keepversion=False):
    '''
    in the datamembers dict needs to come 'period','student','dow','adult','subject','recordtype'
    
    values need to be the names for dow, so 'Monday','Tuesday' etc'''

    datamembers['session'] = ".".join([datamembers['adult'],datamembers['subject'],datamembers['dow'],
                               sswizard_utils._isname(enums,'period',datamembers['period'])])
    
    datamembers['userobjid'] = sswizard_utils._getuserobjid(enums,['period','dow','student','adult','subject'],datamembers)
    
    # check that the userobjid does not already exist
    if of.object_exists('lesson',datamembers['userobjid']) == True:
        raise Exception("id already in use",datamembers['userobjid'])
    
    datamembers['objtype'] = 'lesson'   
    datamembers['status'] = 'complete'
    datamembers['prep'] = int(prepmap[datamembers['student']])
    datamembers['source']="manual"
    datamembers['saveversion']=1
        
    # switch to code
    datamembers['dow'] = sswizard_utils._iscode(enums,'dow',datamembers['dow'])
    
    with database:
        _,_lesson_count,_ = sswizard_utils._maxlessonenum(database)
        datamembers['enum'] = int(_lesson_count[0][0])+1

    lesson = of.new(schoolschedgeneric,'lesson',objid=datamembers['userobjid'],
                         constructor='datamembers',database=database,
                         of=of,modname=__name__,dm=datamembers)
    
    _lesson_change(lesson)
    
    log.log(thisfuncname(),10,msg="lesson obj added",dm=datamembers)
    
    with database:
        lesson.persist()
    return(lesson)
    

def dataset_load(database,refdatabase,of,enums,saveversion=1,unknown='N',prep=-1,period="all",
                 dow="all",teacher="all",student="all",source="dbinsert",keepversion=False):
    
    of.reset()
    
    whereclause = []
    if keepversion==True:
        ''' if versioning enabled make sure to only recover the latest/current version '''
        whereclause = [['__version','=',"\"current\""]]
    
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
    cols = ['period','student','session','dow','prep','teacher','subject','userobjid','status','substatus','recordtype','source','__id']        
    with database:
        colndefn,rows,exec_str = tbl_rows_get(database,'lesson',cols,whereclause)

        log.log(thisfuncname(),9,msg="dbread",exec_str=exec_str)
    
    cols = ['period','student','session','dow','prep','adult','subject','userobjid','status','substatus','recordtype','source','id']
    
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
    
