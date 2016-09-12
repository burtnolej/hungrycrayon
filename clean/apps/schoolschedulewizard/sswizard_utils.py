

from misc_utils import nxnarraycreate

def updates_get(ui,gridname,ignoreaxes=False):
    maxx = maxy = -1
    if ignoreaxes == True: maxx = maxy = 0
    update_keys = [ [gridname,update.split(",")[1],update.split(",")[2]] for update in ui.updates.keys() if update.split(",")[0] == gridname if int(update.split(",")[1]) > maxx if int(update.split(",")[2]) > maxy]
    
    if len(update_keys)==0:
        raise Exception("no updates registered for",gridname)
       
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
    