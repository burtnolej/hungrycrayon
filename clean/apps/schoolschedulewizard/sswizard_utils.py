import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import nxnarraycreate

from database_table_util import tbl_query, tbl_rows_update, DBException
from database_util import Database
from collections import OrderedDict
from misc_utils_log import Log, logger
from misc_utils import thisfuncname
from shutil import copyfile

log = Log(cacheflag=True,logdir="/tmp/log",pidlogname=False,proclogname=False)

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
    
    if rowheaderexecfunc <> None: yoffset=1    
    if columnheaderexecfunc <> None: xoffset=1

    output = []
    with database:
        for y in range(yoffset,len(widgetargs[0])):
        #for x in range(xoffset,len(widgetargs)):
            colndefn,values = exec_func(database,y,prep,dow)
            
            values = [value[0] for value in values]
            
            values = list(set(values))
            for x in range(xoffset,len(widgetargs)):
            #for y in range(yoffset,len(widgetargs[x])):
                widgetargs[x][y]['values'] = values
                
        if rowheaderexecfunc <> None:
            colndefn,values = rowheaderexecfunc(database)
            
            values = [value[0] for value in values]
            
            for x in range(len(widgetargs)):
                widgetargs[x][0]['values'] = values
                if ui <> None:
                    ui.widgets[x][0].sv.set(values[x])

        if columnheaderexecfunc <> None:
            colndefn,values = columnheaderexecfunc(database)
            
            values = [value[0] for value in values]
            
            for y in range(len(widgetargs[0])):
                widgetargs[0][y]['values'] = values
                if ui <> None:
                    ui.widgets[0][y].sv.set(values[y])

    return(widgetargs)

@logger(log)
def getdbenum(enums,dbname,fldname,tblname,pred1=None,predval1=None):
    '''
    every table has a code column which is a 2 digit unique mnemonic
    
    given a name lookup a code
    given a code lookup a name
    given a code/name get an enumeration
    get names, codes
    '''
    database = Database(dbname)
    exec_str = "select {1},code from {0}".format(tblname,fldname)
    if pred1 <> None:
        exec_str = exec_str + " where {0} = {1}".format(pred1,predval1)


    import sqlite3
    
    with database:
        try:
            coldefn,values = tbl_query(database,exec_str)
        except DBException, e:
            log.log(thisfuncname(),0,exception=e,msg=e.message)
    
    enums[tblname] = {}
    #name2code = dict((row[0],row[1]) for row in values)
    
    # explicit loop as OrderedDict only keeps order when items are added after initialization
    name2code = OrderedDict()
    for k,v in values:
        if v == 'None':
            log.log(thisfuncname(),0,msg="none value detected",tblname=tblname,key=str(k))
 
        name2code[k] = v
    
    # unknown/none is represented with '??'
    name2code['??'] = '??'
        
    enums[tblname]['name2code'] = name2code
    enums[tblname]['code2name'] = dict(zip(name2code.values(),name2code.keys()))
    enums[tblname]['name2enum'] = dict((value,enum) for enum,value in enumerate(name2code.keys()))
    enums[tblname]['code2enum'] = dict((value,enum) for enum,value in enumerate(name2code.values()))
    enums[tblname]['name'] = enums[tblname]['name2code'].keys()
    enums[tblname]['code'] = enums[tblname]['name2code'].values()
    
    log.log(thisfuncname(),3,msg="created enums",tblname=tblname,names=enums[tblname]['name'])
            

def setenums(dow,prep,dbname):

    enums = {'maps':{},'enums':{},'codes':{}}
    
    getdbenum(enums,dbname,'name','period')
    #getdbenum(enums,dbname,'name','period')
    
    if prep <> "-1":
        getdbenum(enums,dbname,'name','student','prep',prep)
        getdbenum(enums,dbname,'name','adult','prep',prep)
    else:
        getdbenum(enums,dbname,'name','student')
        getdbenum(enums,dbname,'name','adult')
        
    getdbenum(enums,dbname,'code','session')
    getdbenum(enums,dbname,'name','lessontype')
    getdbenum(enums,dbname,'name','subject')
    getdbenum(enums,dbname,'name','dow')
  
    return enums

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
    
    enums = setenums('All','-1',dbname)
    
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
                if dryrun == True:
                    print exec_str,oldcode
                else:
                    log.log(thisfuncname(),4,msg="session code updated",execstr=exec_str,oldcode=oldcode)
    
        #except Exception, e:
        #    print row,"failed", e
    

    
if __name__ == "__main__":
    
    session_code_gen('quadref',False)
