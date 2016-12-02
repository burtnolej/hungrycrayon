
import os

from misc_utils_enum import enum
from database_util import Database, tbl_remove, tbl_exists, tbl_create
from database_table_util import tbl_rows_insert
from sswizard_query_utils import _colorexecfunc, _formatsexecfunc
import sswizard_utils
from misc_utils import IDGenerator
from datetime import datetime

__all__ = ['colors','_color_get_multi','color_get','colorpalette','fontpalette']


colors = enum(pink = '#%02x%02x%02x' % (255, 153, 153),
              salmon = '#%02x%02x%02x' % (255, 204, 153),
              lightyellow = '#%02x%02x%02x' % (255, 255, 153),
              lightgreen = '#%02x%02x%02x' % (204, 255, 153),
              lightturquoise = '#%02x%02x%02x' % (153, 255, 204),
              lightblue = '#%02x%02x%02x' % (153, 255, 255),
              lavender = '#%02x%02x%02x' % (153, 153, 255),
              purple = '#%02x%02x%02x' % (204, 153, 255),
              darkgreen = '#%02x%02x%02x' % (0, 102, 0),
              burgundy = '#%02x%02x%02x' % (102, 0, 51),
              karky = '#%02x%02x%02x' % (102, 102, 0),
              darkburgundy = '#%02x%02x%02x' % (102, 0, 51),
              darkgrey = '#%02x%02x%02x' % (0, 51, 51),
              brown = '#%02x%02x%02x' % (102, 51, 0),
              mauve = '#%02x%02x%02x' % (204, 204, 0),
              navyblue = '#%02x%02x%02x' % (0, 0, 51),
              darkyellow = '#%02x%02x%02x' % (155,140,6),
              paleblue = '#%02x%02x%02x' %(173,217,222),
              palegreen = '#%02x%02x%02x' %(183,229,183),
              cerise = '#%02x%02x%02x' %(212, 7, 253),
              red = '#%02x%02x%02x' %(255, 0, 0),
              black = '#%02x%02x%02x' %(255, 255, 255),
              white = '#%02x%02x%02x' %(0, 0, 0),
              green = '#%02x%02x%02x' %(0, 255, 0),
              blue = '#%02x%02x%02x' %(0, 0, 255),
              lightgrey = '#%02x%02x%02x' % (211, 211, 211),              
              verydarkgrey = '#%02x%02x%02x' %(54, 46, 55),
              dirtyyellow = '#%02x%02x%02x' %(242, 232, 19))



colorpalette =  dict(wp=colors.green,
                     subject=colors.lightblue,
                     ap=colors.darkyellow,
                     Movement=colors.pink,
                     ELA=colors.salmon,
                     Humanities=colors.lightyellow,
                     Counseling=colors.lightgreen,
                     Math=colors.lightturquoise, 
                     Music=colors.lightblue,
                     STEM=colors.lavender,
                     Art=colors.purple,
                     History=colors.pink,
                     Science=colors.darkgreen,
                     Core=colors.karky,
                     Chess=colors.burgundy,
                     computertime=colors.verydarkgrey,
                     Speech=colors.darkburgundy,
                     Student_News=colors.darkgrey,
                     Computer_Time=colors.brown,
                     Activity_Period=colors.mauve,
                     Melissa=colors.navyblue,
                     Amelia=colors.darkgreen,
                     Samantha=colors.darkyellow, 
                     Alexa=colors.paleblue, 
                     Paraic=colors.palegreen, 
                     Francisco=colors.cerise,
                     Rahul=colors.verydarkgrey,
                     Dylan=colors.verydarkgrey,
                     Moira=colors.verydarkgrey,
                     Issey=colors.verydarkgrey, 
                     Daryl=colors.verydarkgrey, 
                     Karolina=colors.verydarkgrey)

fontpalette = dict(Amelia=colors.green,
                   Paraic=colors.darkgreen,
                   Stan=colors.lavender,
                   Samantha=colors.lightgreen,
                   Alexa=colors.blue,
                   Francisco=colors.purple,
                   Melissa=colors.lightblue,
                   Rahul=colors.dirtyyellow,
                   Dylan=colors.dirtyyellow, 
                   Moira=colors.dirtyyellow,
                   Issey=colors.dirtyyellow, 
                   Daryl=colors.dirtyyellow, 
                   Karolina=colors.dirtyyellow,
                   Chess=colors.pink,
                   Student_News=colors.lightyellow,
                   subject=colors.blue)


def init_formats(dbname,_globals):
    
    _globals['colorpalette'] = dbformats_get(dbname,'bgcolor')
    _globals['fontpalette'] = dbformats_get(dbname,'fgcolor')
    _globals['colors'] = dbcolors_get(dbname)
    

def _color_get_multi(values):
    bgs=[]
    fgs=[]
    for value in values:
        #_bg,_fg = self.color_get(value)
        _bg,_fg = color_get(value)
        bgs.append(_bg)
        fgs.append(_fg)
    return(bgs,fgs)

def color_get(value):
    
    bg = colors.lightgrey
    fg = colors.black
        
    try:
        int(value)
        value = str(value)
    except ValueError:
        pass
    
    if value.count(" ") > 0:
        value= value.replace(" ","_")
        
    if value.count("[") == 1 and value.count("]") == 1:
        bg = colors.red
    
    if value.count(".") > 0:
        value = value.split(".")[0]
        
    #if self.colorpalette.has_key(value):
    if colorpalette.has_key(value):
        #bg = self.colorpalette[value]
        bg = colorpalette[value]
        
    #if self.fontpalette.has_key(value):
    if fontpalette.has_key(value):
        #fg = self.fontpalette[value]
        fg = fontpalette[value]
        
    return(bg,fg)   

def hex2rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb = tuple(int(value[i:i+lv//3],16) for i in range(0,lv,lv//3))
    return rgb

def color_db_load(dbname="test_ssloader"):
    
    tblname = "colors"
    
    colors_col_defn = [('name','text'),('hex','text'),('rgb','text'),('__id','text'),('__timestamp','text')]
    colors_col_names = [row[0] for row in colors_col_defn]
    
    dbrows=[]
    for key,value in colors.attr_get_keyval(include_callable=False,include_baseattr=False):
        rgb = hex2rgb(value)
        rgbstr = ",".join(map(str,rgb))
        __id = IDGenerator().getid()
        __timestamp = datetime.now().strftime("%H:%M:%S")  

        dbrows.append(["\""+key+"\"","\""+value+"\"","\""+rgbstr+"\"",
                       "\""+__id+"\"","\""+__timestamp+"\""])   
  
    database = Database(dbname)
    
    with database:
        if tbl_exists(database,tblname) == True:
            tbl_remove(database,tblname)
            
        tbl_create(database,tblname, colors_col_defn)
        exec_str, result = tbl_rows_insert(database,tblname,colors_col_names,dbrows)

def dbformats_get(dbname,colortype):

    results={}
    database = Database(dbname)
    with database:
        _,colors,_ = _formatsexecfunc(database,colortype)

    for color in colors:
        results[color[0]] = color[1]
        
    return(results)

def dbcolors_get(dbname):

    results = {}
    database = Database(dbname)
    with database:
        _,colors,_ = _colorexecfunc(database)

    for color in colors:
        results[color[0]] = color[1]
        
    return(enum(**results))
    
def formats_db_load(dbname="test_ssloader"):

    tblname = "formats"
    hex2name = {}    
    for key,value in colors.attr_get_keyval(include_callable=False,include_baseattr=False):
        hex2name[value] = key

    formats_col_defn = [('name','text'),('fgcolor','text'), ('bgcolor','text'),
                        ('__id','text'),('__timestamp','text')]
    
    formats_col_names = [row[0] for row in formats_col_defn]
    
    dbrows=[]
    for name,bg in colorpalette.iteritems():
        if fontpalette.has_key(name):
            fg = fontpalette[name]
        else:
            fg = '#000000'

        __id = IDGenerator().getid()
        __timestamp = datetime.now().strftime("%H:%M:%S") 

        dbrows.append(["\""+name+"\"",
                       "\""+hex2name[fg]+"\"",
                       "\""+hex2name[bg]+"\"",
                       "\""+__id+"\"","\""+__timestamp+"\""]) 
    
    database = Database(dbname)
    with database:
        if tbl_exists(database,tblname) == True:
            tbl_remove(database,tblname)
        
        tbl_create(database,tblname, formats_col_defn)
        exec_str, result = tbl_rows_insert(database,tblname,formats_col_names,dbrows)
            
if __name__ <> "__main__":
    
    dbname,_ = sswizard_utils.getdatabase()
    
    colorpalette = dbformats_get(dbname,'bgcolor')
    fontpalette = dbformats_get(dbname,'fgcolor')
    colors = dbcolors_get(dbname)

if __name__ == "__main__":
    
    dbname,_ = sswizard_utils.getdatabase()
    
    color_db_load(dbname)
    formats_db_load(dbname)
    
    #globals()['colorpalette'] = dbformats_get('test_ssloader','bgcolor')
    #globals()['fontpalette'] = dbformats_get('test_ssloader','fgcolor')
    #globals()['colors'] = dbcolors_get('test_ssloader')
    
    #for k,v in dict(globals()).iteritems():
    #    print k,v
        