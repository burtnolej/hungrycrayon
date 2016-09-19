from misc_utils import nxnarraycreate

from database_table_util import tbl_query
from database_util import Database
from collections import OrderedDict
from misc_utils_log import Log, logger
from misc_utils import thisfuncname

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
                   rowheaderexecfunc=None,
                   columnheaderexecfunc=None,
                   ui=None):
    
    xoffset=0
    yoffset=0
    
    if rowheaderexecfunc <> None: yoffset=1    
    if columnheaderexecfunc <> None: xoffset=1

    output = []
    with database:
        for x in range(xoffset,len(widgetargs)):
            colndefn,values = exec_func(database,x)
            
            values = [value[0] for value in values]
    
            for y in range(yoffset,len(widgetargs[x])):
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

    with database:
        coldefn,values = tbl_query(database,exec_str)
    
    enums[tblname] = {}
    name2code = dict((row[0],row[1]) for row in values)
    enums[tblname]['name2code'] = name2code
    enums[tblname]['code2name'] = zip(name2code.values(),name2code.keys())
    enums[tblname]['name2enum'] = dict((value,enum) for enum,value in enumerate(name2code.keys()))
    enums[tblname]['code2enum'] = dict((value,enum) for enum,value in enumerate(name2code.values()))
    enums[tblname]['name'] = enums[tblname]['name2code'].keys()
    enums[tblname]['code'] = enums[tblname]['name2code'].values()            
            
def setenums(dow,prep,dbname):

    enums = {'maps':{},'enums':{},'codes':{}}
    
    getdbenum(enums,dbname,'name','period')
    getdbenum(enums,dbname,'name','period')
    getdbenum(enums,dbname,'name','student','prep',prep)
    getdbenum(enums,dbname,'name','adult','prep',prep)
    getdbenum(enums,dbname,'tag','session')
    getdbenum(enums,dbname,'name','lessontype')
    getdbenum(enums,dbname,'name','subject')
    getdbenum(enums,dbname,'name','dow')
  
    return enums

def sessiontagtoid(tag,enums):
    
    teacher_code,lessontype_code,subject_code = value.split(".")
    teacher_enum = enums['teacher'][teacher_code]
    lessontype_enum = enums['teacher'][lessontype_code]
    subject_enum = enums['subject'][subject_code]
    