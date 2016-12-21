import sys
import os
from os import path as ospath
from misc_utils import nxnarraycreate

from database_table_util import tbl_query, tbl_rows_update, tbl_rows_get, tbl_exists, tbl_create, tbl_rows_insert, \
     DBException, dbtblfactory, _gencoldefn, _quotestrs
from database_util import Database
from collections import OrderedDict
from misc_utils_log import Log, logger
from misc_utils import thisfuncname

from shutil import copyfile

from sswizard_query_utils import _sessionenum, _maxlessonenum, _maxsessionenum

log = Log(cacheflag=True,logdir="/tmp/log",pidlogname=False,proclogname=False)

def _updaterecordval(record, new_value,obj_type,cols):
    _idx = cols.index(obj_type)
    record.pop(_idx)
    record.insert(_idx,new_value) 
    return(record)

def update_callback(ui,widget,new_value):        
    ''' via BaseTk class; all entry widgets assign a callback to the change event
    to call this function if it exists '''
    
    #put event on here too
    if str(widget.current_value) <> str(new_value):
        
        widget.version += 1
        
        log.log(thisfuncname(),10,msg="updating "+str(widget.winfo_name()),current_value=str(widget.current_value),new_value=new_value,version=str(widget.version))
        widget.config(foreground='red')
        
        # record event in update log
        ui.updates[str(widget.winfo_name())] = (new_value,widget.version)
    else:
        widget.config(foreground='black')
        log.log(thisfuncname(),9,msg="skipping "+str(widget.winfo_name()),current_value=str(widget.current_value),new_value=new_value,version=str(widget.version))       
            
def updates_get(ui,gridname,ignoreaxes=False):
    maxx = maxy = -1
    if ignoreaxes == True: maxx = maxy = 0
    update_keys = [ [gridname,update.split(",")[1],update.split(",")[2]] for update in ui.updates.keys() if update.split(",")[0] == gridname if int(update.split(",")[1]) > maxx if int(update.split(",")[2]) > maxy]
    
    if len(update_keys)==0:
        log.log(thisfuncname(),3,msg="updates requested but none found",gridname=gridname)
        #raise Exception("no updates registered for",gridname)
    else:
       
        if ignoreaxes == False:
            offset = 1
        else:
            offset = 0
    
        xsize= max([int(key[1]) for key in update_keys]) + offset
        ysize= max([int(key[2]) for key in update_keys]) + offset
        
        # text values of widgets
        values = nxnarraycreate(int(xsize),int(ysize),"")
        for key in update_keys:
            
            if ignoreaxes == False:
                offset = 0
            else:
                offset = -1
            
            values[int(key[1])+offset][int(key[2])+offset] = ui.updates[str(",".join(key))]
        
        # background color of widgets
        bgcolor = nxnarraycreate(int(xsize),int(ysize),"")
        for key in update_keys:
            
            grid = getattr(ui,gridname)
            
            #_color = self.balancegrid.widgets[int(key[1])][int(key[2])].cget('background')
            _color = grid.widgets[int(key[1])][int(key[2])].cget('background')
            bgcolor[int(key[1])-1][int(key[2])-1] = _color
    
        return values,bgcolor
    return 0,0
    
def widget_current_values_get(ui,gridname,rownum,minversion=1):
    # dump init_values and current_value attributes of all widgets
    grid = getattr(ui,gridname)
    
    values = []
    for y in range(ui.maxcols):
        init_value = grid.widgets[rownum][y].init_value
        current_value = grid.widgets[rownum][y].current_value
        
        if current_value <> "" or init_value <> "":
            values.append((init_value,current_value))
            
    return values


def dropdown_build(database,
                   widgetargs,
                   exec_func,
                   prep,
                   dow="Monday",
                   rowheaderexecfunc=None,
                   columnheaderexecfunc=None,
                   ui=None):
    
    xoffset=0
    yoffset=0
    
    log.log(thisfuncname(),3,msg="creating dropdowns lists",dow=dow,prep=prep)

    # if not creating dropdowns for the headers increment the count
    if rowheaderexecfunc == None: yoffset=1
    if columnheaderexecfunc == None: xoffset=1
    

    output = []
    with database:
        for y in range(yoffset,len(widgetargs[0])):
            colndefn,values,exec_str = exec_func(database,y,prep,dow)
            
            # pull out distinct and make a single list
            values = [value[0] for value in values]
            values = list(set(values))
            
            # add a 'values' attr for each widget
            for x in range(xoffset,len(widgetargs)):
                widgetargs[x][y]['values'] = values
                
            log.log(thisfuncname(),10,msg="generated data dropdowns",num=len(values),query=exec_str)
                
        if rowheaderexecfunc <> None:
            colndefn,values,exec_str = rowheaderexecfunc(database,"prep",prep)
            
            values = [value[0] for value in values]
            
            for x in range(len(widgetargs)):
                widgetargs[x][0]['values'] = values
                if ui <> None:
                    ui.widgets[x][0].sv.set(values[x])
                    
            log.log(thisfuncname(),10,msg="generated row hdr dropdowns",num=len(values),query=exec_str)
                    
        if columnheaderexecfunc <> None:
            colndefn,values,exec_str = columnheaderexecfunc(database)
            
            values = [value[0] for value in values]
            
            for y in range(len(widgetargs[0])):
                widgetargs[0][y]['values'] = values
                if ui <> None:
                    ui.widgets[0][y].sv.set(values[y])
                    
            log.log(thisfuncname(),10,msg="generated col hdr dropdowns",num=len(values),query=exec_str)


    return(widgetargs)

@logger(log)
#def getdbenum(enums,database,fldname,tblname,pred1=None,predval1=None):
def getdbenum(enums,database,fldname,tblname,**kwargs):
    '''
    every table has a code column which is a 2 digit unique mnemonic
    
    given a name lookup a code
    given a code lookup a name
    given a code/name get an enumeration
    get names, codes
    '''
    #database = Database(dbname)
    exec_str = "select {1},code,enum from {0}".format(tblname,fldname)

    where_str = ""
    for key,value in kwargs.iteritems():
        if where_str == "":
            where_str = " where {0} = {1}".format(key,value)
        else:
            where_str = where_str + " and {0} = {1}".format(key,value)

    exec_str = exec_str + where_str
    
    import sqlite3
    
    with database:
        try:
            coldefn,values,_ = tbl_query(database,exec_str)
        except DBException, e:
            log.log(thisfuncname(),0,exception=e,msg=e.message,tblname=tblname,fldname=fldname)
    
    enums[tblname] = {}
    #name2code = dict((row[0],row[1]) for row in values)
    
    # explicit loop as OrderedDict only keeps order when items are added after initialization
    name2code = OrderedDict()
    name2enum = OrderedDict()
    code2enum = OrderedDict()
    
    for k,v,e in values:
        if v == 'None' or e == None:
            log.log(thisfuncname(),1,msg="none value detected",tblname=tblname,key=str(k))
            continue
 
        name2code[k] = v
        name2enum[k] = int(e)
        code2enum[v] = int(e)
    
    # unknown/none is represented with '??'
    name2code['??'] = '??'
        
    enums[tblname]['name2code'] = name2code
    enums[tblname]['code2name'] = dict(zip(name2code.values(),name2code.keys()))
    #enums[tblname]['name2enum'] = dict((value,enum) for enum,value in enumerate(name2code.keys()))
    #enums[tblname]['code2enum'] = dict((value,enum) for enum,value in enumerate(name2code.values()))
    
    enums[tblname]['name2enum'] =name2enum
    enums[tblname]['enum2name'] = dict(zip(name2enum.values(),name2enum.keys()))
    enums[tblname]['code2enum'] = code2enum
    
    enums[tblname]['name'] = enums[tblname]['name2code'].keys()
    enums[tblname]['code'] = enums[tblname]['name2code'].values()
    
    log.log(thisfuncname(),3,msg="created enums",tblname=tblname,names=enums[tblname]['name'])
            

def lookupenum(enums,converttype,fieldtype,code):
    try:
        name = enums[fieldtype][converttype][code]
    except KeyError, e:
        msg = "lookup failed: type={0},field ={1},code={2} [{3}]".format(converttype,fieldtype,code,e.message,enums[fieldtype])
        log.log(thisfuncname(),2,msg=msg)
        raise Exception(msg)
    return(name)
    
def setenums(dow,prep,database):

    enums = {'maps':{},'enums':{},'codes':{}}
    getdbenum(enums,database,'name','dow')
    getdbenum(enums,database,'name','period')
    
    arg = {}
    if prep <> -1: arg = dict(prep=prep)
        
    getdbenum(enums,database,'name','student',**arg)
    getdbenum(enums,database,'name','adult',**arg)
    
    arg = {}
    if dow <> "all": 
        dow_name = lookupenum(enums,'code2name','dow',dow)
        arg = dict(dow="\""+dow_name+"\"")
        
    getdbenum(enums,database,'code','session',**arg)
    getdbenum(enums,database,'name','recordtype')
    #getdbenum(enums,database,'name','lessontype')
    getdbenum(enums,database,'name','subject')
    
  
    return enums

def setconfig():
    
    config = {'student':{}}
    _studentcolor = _colorexecfunc('student')
    

def sessiontagtoid(tag,enums):
    
    teacher_code,lessontype_code,subject_code = value.split(".")
    teacher_enum = enums['teacher'][teacher_code]
    lessontype_enum = enums['teacher'][lessontype_code]
    subject_enum = enums['subject'][subject_code]
    
def session_code_gen(dbname,dryrun=False):
    
    database = Database(dbname)
    
    exec_str =  "select s.name,lt.code || '.' || s.code"
    exec_str += " from subject as s,lessontype as lt"
    exec_str += " where s.lessontype = lt.name"
    
    with database:
        colnames,rows = tbl_query(database,exec_str)
    
    subject_lookup = dict((row[0],row[1]) for row in rows)
    
    exec_str = "select teacher,subject,__id,code,type,day from session"
    
    with database:
        colnames,rows = tbl_query(database,exec_str)
    
    enums = setenums('All','-1',database)
    
    for row in rows:
        teacher = row[0]
        subject = row[1]
        __id = row[2]
        oldcode = row[3]
        lessontype = row[4]
        dow = row[5]
        
        if dow == None:
            dow = "??"
            
        if teacher == None:
            teacher_code = "??"
        
        lessontype_code = "??"
        if lessontype == "WP":
            lessontype_code = "WP"
        
        if subject == None:
            subject_code = lessontype_code + ".??"  
        elif subject_lookup.has_key(subject) == False:
            subject_code = lessontype_code + ".??"
        else:
            subject_code =subject_lookup[subject]
            
        teacher_code = enums['adult']['name2code'][teacher]
        #session_code = ".".join([teacher_code,subject_code,])
        dow_code = enums['dow']['name2code'][dow]
        session_code = ".".join([teacher_code,subject_code,dow_code])
        
        
        if oldcode <> session_code:
            with database:
                exec_str,_ = tbl_rows_update(database,'session',
                                  ['code',"\""+session_code+"\"",'__id',"\""+__id+"\""],
                                  dryrun=dryrun)

                print exec_str,oldcode
                log.log(thisfuncname(),4,msg="session code updated",execstr=exec_str,oldcode=oldcode)
    
        #except Exception, e:
        #    print row,"failed", e
    
    
@logger(log)
def dbbulkloader(database,dbrecords,tblname,cols,maxsize=300):
    with database:
	dbcoldefn = _gencoldefn(dbrecords[0],cols)

	if not tbl_exists(database,tblname) ==True:
	    tbl_create(database,tblname,dbcoldefn)
	    
	dbrecords = _quotestrs(dbrecords)
	
	if len(dbrecords) > maxsize:
	    for starti in range(0,len(dbrecords),maxsize):
		if starti+maxsize > len(dbrecords):
		    endi = len(dbrecords)
		else:
		    endi = starti + maxsize

		tbl_rows_insert(database,tblname,cols,dbrecords[starti:endi])
		log.log(thisfuncname(),10,msg="loaded rows to "+tblname,numrow=endi-starti)
	else:
	    tbl_rows_insert(database,tblname,cols,dbrecords)
	    log.log(thisfuncname(),10,msg="loaded rows to "+tblname,numrow=len(dbrecords))	    

def _isenum(enums,objtype,value):
    
    ''' ensures that value is an enum by converting from name if required ''' 
    try:
	if value in enums[objtype]['enum2name'].keys(): 
	    return value
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup enum2name",objtype=objtype,value=str(value))
	return "??"
    
    try:
	if value in enums[objtype]['name']:
	    return enums[objtype]['name2enum'][value]
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup name2enum",objtype=objtype,value=str(value))
	return "??"
    
    try:
	if value in enums[objtype]['code2enum'].keys():
	    return enums[objtype]['code2enum'][value]
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup code2enum",objtype=objtype,value=str(value))
	return "??"
    
def _isname(enums,objtype,value):    
    ''' ensures that value is a name by converting from code if required ''' 
    
    try:
	if value in enums[objtype]['name']: 
	    return value
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup name",objtype=objtype,value=str(value))
	return "??"
    
    try:
	if value in enums[objtype]['code2name'].keys():
	    return enums[objtype]['code2name'][value]
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup code2name",objtype=objtype,value=str(value))
	return "??"
    
    try:
	if value in enums[objtype]['enum2name'].keys():
	    return enums[objtype]['enum2name'][value]
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup enum2name",objtype=objtype,value=str(value))
	return "??"
    
def _iscode(enums,objtype,value):    
    ''' ensures that value is a code by converting from code if required ''' 
    try:
	if value in enums[objtype]['code2name'].keys():
	    return value
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup code2name",objtype=objtype,value=str(value))
	return "??"
	
    try:
	if value in enums[objtype]['name']:
	    return enums[objtype]['name2code'][value]
    except KeyError:
	log.log(thisfuncname(),2,msg="could not lookup name2code",objtype=objtype,value=str(value))
	return "??"

def _loadprepmapper(database):
    cols = ['name','prep']

    with database:
	_,rows,_ = tbl_rows_get(database,'student',cols)

    d = dict((row[0],row[1]) for row in rows)
    return d

def _getuserobjid(enums,cols,d):
    # take in a list of field names and convert all to enums
    return(".".join(map(str,[_isenum(enums,col,d[col]) for col in cols])))	    
    
@logger(log)
def dbinsert_direct(database,records,tblname,source,masterstatus=True,keepversion=False):
    '''
    
    records : list of records where a record is of the form ('period','dow','subject','adult','student','type')
    
    assumes all fields have been validated; student can be list or a single name
    
    if this is being called after primary_record_set, pass in false as masterstatus and status will be set
    to complete/incomplete depending on values
    '''
    
    from misc_utils import IDGenerator
    from datetime import datetime
    
    dbrows = []
    
    count=0
    
    enums = {'maps':{},'enums':{},'codes':{}}

    getdbenum(enums,database,'name','period')
    getdbenum(enums,database,'name','student')
    getdbenum(enums,database,'name','dow')
    getdbenum(enums,database,'name','subject')
    getdbenum(enums,database,'name','adult')
    
    prepmap = _loadprepmapper(database)
    
    
    if tblname == 'session':
	with database:
	    _,_session_count,_ = _maxsessionenum(database)	
	    
	tablerow_count = int(_session_count[0][0])+1
    elif tblname == 'lesson':
	with database:
	    _,_lesson_count,_ = _maxlessonenum(database)		    
    
	tablerow_count = int(_lesson_count[0][0])+1
	
    lcols = ['period','dow','subject','adult','student','recordtype']
    scols = ['period','dow','subject','adult','student','recordtype','numstudents']
    
    for record in records:

	# prepare fields to complete record
	if tblname == 'session':
	    
	    d = dict(zip(scols,record))
	    d['dow'] = _isname(enums,'dow',d['dow'])
	    d['period'] = _isenum(enums,'period',d['period'])
	    d['code'] = ".".join([d['adult'],d['subject'],d['dow'],_isname(enums,'period',d['period'])])
	    d['lessoncount'] = 0
	    #d['userobjid'] = _getuserobjid(enums,['period','dow','subject','adult'],d)
	    
	    # if student is a list and has more than 1 member, set prep to unknown (-1)
	    if isinstance(d['student'],list) == True:
		if len(d['student']) == 1:
		    d['prep'] = int(prepmap[d['student'][0]])
		else:
		    d['prep'] = -1
		#d['numstudents'] = len(d['student']) # keep track of the number of students in this session (aka the number of lessons that exist)
		
	    else:
		d['prep'] = int(prepmap[d['student']])
		#d['numstudents'] = 0
	    d.pop('student')
	    
	    # specify if a session was created without children (ie student could not be
	    # determined from info provided in the input file
	    if d['numstudents'] == 0:
		d['status'] = "nochildrenatinit"
	    else:
		d['status'] = "childrenatinit"

	elif tblname == 'lesson':

	    d = dict(zip(lcols,record))

	    d['dow'] = _iscode(enums,'dow',d['dow'])
	    d['period'] = _isname(enums,'period',d['period'])
	    d['session'] = ".".join([d['adult'],d['subject'],_isname(enums,'dow',d['dow']),d['period']])
	    d['prep'] = int(prepmap[d['student']])
	    d['userobjid'] = _getuserobjid(enums,['period','dow','student','adult','subject'],d)

	    d['saveversion'] = 1
	   
	    #d.pop('type')
    
	    # set status
	    d['status'] = "complete"
	    if d['adult'] == '??' or d['subject'] == '??':
		d['status'] = "incomplete"
	      
	d['teacher'] = d['adult']
	d.pop('adult')

	if masterstatus == True:
	    d['substatus'] = d['status']
	    d['status'] = 'master'
	else:
	    d['substatus'] = "notset"  
	    
	d['__id'] = IDGenerator().getid()
	

	if keepversion == True:
	    #d['__version'] = "init"
	    d['__version'] = "current"
	    d['__timestamp'] = datetime.now().strftime("%y-%m-%d_%H:%M:%S")
	    
	else:
	    d['__timestamp'] = datetime.now().strftime("%H:%M:%S")
	    
		
	d['enum'] = tablerow_count
	d['source'] = source
    
	dbrows.append(d.values())
	
	if count ==0: dbcols = d.keys()
	
	tablerow_count+=1

    dbbulkloader(database,dbrows,tblname,dbcols)
    
    
@logger(log)
def dbinsert_lesson(self,**kwargs):
    
    cols = ['teacher','dow','subject','source','students']
    
    

def dbinsert(database,dbclassname,rows,colnames):
    
    dbclass = dbtblfactory(dbclassname)

    for x in range(len(rows)):
        dm={}
        emptyrow=True
        for y in range(len(colnames)): 
            colname = colnames[y]
            value = rows[x][y]
            if colname <> "" and colname.startswith("_") == False:
                if value <> "":
                    dm[colname] = value
                    emptyrow=False
                
        if emptyrow == False:
            dbobj = dbclass.datamembers(database=database,dm=dm)

            with database:
                try:
                    exec_str,result = dbobj.persist()
                    log.log(thisfuncname(),4,func=dbobj.persist,exec_str=exec_str,result=result)
                except Exception, e:
                    log.log(thisfuncname(),1,func=dbobj.persist,error=str(e))


def updatelessoncount():
    ''' iterate over each session and using the session code, count how many lessons exist
    for that session '''
    pass
    
def gridreduce(grid,blanks,headeroffset=1):
    # remove any all blank rows or columns
    # where blank is a list of things that mean blank
    # assumes the grid is a list of rows
    # headeroffset indicates to not include header row or column in determination
    
    gridh = len(grid)
    gridw = len(grid[0])
    
    notblankcols = []
    for y in range(headeroffset,gridw):
	if len([x for x in range(headeroffset,gridh) if grid[x][y] not in blanks]) == 0:
	    notblankcols.append(y)
    
    notblankrows = []
    for x in range(headeroffset,gridh):
	if len([y for y in range(headeroffset,gridw) if grid[x][y] not in blanks]) == 0:
	    notblankrows.append(x)
    
    # need to start with biggest index first otherwise indexes change
    notblankrows.reverse()
    
    for rowidx in notblankrows:
	grid.pop(rowidx)

    notblankcols.reverse()
    
    for row in grid:
	for colidx in notblankcols:
	    row.pop(colidx)

def gridrollup(grid,keys,schema):
    gridh = len(grid)
    gridw = len(grid[0])

    for y in range(1,gridh):
	for x in range(1,gridw):
	    if isinstance(grid[y][x],list) == True:
		if len(grid[y][x]) > 0:
		    cell = grid[y][x]
		    grid[y][x] = cellrollup(cell,keys,schema)
		    grid[y][x].sort()
    
    #return grid
    
def cellrollup(grid,keys,schema):
    ''' if a cell has multi subrows like below
    
    [(u'Movement', u'Dylan', u'Peter'), 
    (u'Movement', u'Dylan', u'Clayton'), 
    (u'Movement', u'Dylan', u'Booker'), 
    (u'Movement', u'Dylan', u'Bruno'), 
    (u'Student News', u'Dylan', u'Bruno'), 
    (u'Movement', u'Dylan', u'Nathaniel'), 
    (u'Movement', u'Dylan', u'Tristan'), 
    (u'Movement', u'Dylan', u'Ashley'), 
    (u'Movement', u'Dylan', u'Thomas')]
    
    based on the rollup keys (adult,subject) we would get
    [(u'Movement', u'Dylan', u'Peter,Clayton, Booker, Bruno,Nathaniel,Tristan,Ashley,Thomas'), 
    (u'Student News', u'Dylan', u'Bruno')]
    
    '''
    schemakeys = schema['ztypes'].split(",")
    
    # determine which keys are not part of the rollup key
    # so they can be concatenated
    from copy import deepcopy
    
    nonrollupkeys = deepcopy(schemakeys)
    for key in keys:
	nonrollupkeys.remove(key)
    
    nonrollupkeydict = dict([(key, []) for key in nonrollupkeys])
	
    rollupkeyvals = {}
    
    
    for row in grid:
	# join values to valuetypes
	
	rowd = dict(zip(schemakeys,row))
 
	# create the unique rollup key values
	rollupkey = []
	for key in keys:
	    rollupkey.append(rowd[key])
	
	if rollupkeyvals.has_key(",".join(rollupkey)) == False:
	    rollupkeyvals[",".join(rollupkey)] = deepcopy(nonrollupkeydict)
	    
	for nonrollupkey in nonrollupkeys:
	    rollupkeyvals[",".join(rollupkey)][nonrollupkey].append(rowd[nonrollupkey])
	    
	for key in keys:
	    rollupkeyvals[",".join(rollupkey)][key] = rowd[key]
    
    output=[]
    for k,v in rollupkeyvals.iteritems():
	_output=[]
	for schemakey in schemakeys:
	    if isinstance(v[schemakey],list) == True:
		_output.append(",".join(v[schemakey]))
	    else:
		_output.append(v[schemakey])
	output.append(tuple(_output))
	
    return output

	
    
def getdatabase():

    DBPATH = os.environ['DBPATH']
    DBNAME = os.environ['DBNAME']

    if DBNAME <> "":
	dbname=os.path.join(DBPATH,DBNAME)
	refdbname=os.path.join(DBPATH,DBNAME)
    elif len(sys.argv) == 2:
	dbname=os.path.join(DBPATH,sys.argv[1])
	refdbname=os.path.join(DBPATH,sys.argv[1])
	sys.argv.pop(1)
    else:
	raise Exception("provide a database name on cndline or set $DBNAME/$DBPATH")    
    
    print "using database", dbname
    return(dbname,refdbname)
    
if __name__ == "__main__":
    
    session_code_gen('quadref',False)
