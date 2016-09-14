from misc_utils import nxnarraycreate, Log

log = Log()
def update_callback(ui,widget,new_value):        
    ''' via BaseTk class; all entry widgets assign a callback to the change event
    to call this function if it exists '''
    
    #put event on here too
    if str(widget.current_value) <> str(new_value):
        
        widget.version += 1 # only increment widget version if contents are changing
        log.log(widget,3,"updating","key=",str(widget.winfo_name()),"current_value=",widget.current_value,"new_value=",new_value,"version=",str(widget.version))
        
        widget.config(foreground='red')
        
        # if this is the first update
        if widget.version == 1: 
            widget.current_value = new_value
        
        # record event in update log
        ui.updates[str(widget.winfo_name())] = (new_value,widget.version)
    else:
        widget.config(foreground='black')
        
        log.log(widget,3,"skipping as","key=",str(widget.winfo_name()),"current_value=",widget.current_value,"new value=",new_value,"version=",str(widget.version)) 

def updates_get(ui,gridname,ignoreaxes=False):
    maxx = maxy = -1
    if ignoreaxes == True: maxx = maxy = 0
    update_keys = [ [gridname,update.split(",")[1],update.split(",")[2]] for update in ui.updates.keys() if update.split(",")[0] == gridname if int(update.split(",")[1]) > maxx if int(update.split(",")[2]) > maxy]
    
    if len(update_keys)==0:
        log.log(ui,3,"updates requested but none found",gridname)
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
            #values[int(key[1])-1][int(key[2])-1] = ui.updates[str(",".join(key))]
        
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