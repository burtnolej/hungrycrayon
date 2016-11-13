

from misc_utils_enum import enum

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
        bg = red
    
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