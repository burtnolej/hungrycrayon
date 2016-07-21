import Tkinter as tk
import tkFont

master = tk.Tk()

class generic:
    def __init__(self,**args):
	for key,value in args.iteritems():
	    setattr(self,key,value)

class color_enum:    
    black='#000000'
    white='#fff'
    grey='#d3d3d3'
    pink='#ff69b4'

color = color_enum()

label4 = tk.PhotoImage(file='label4.gif')
label12 = tk.PhotoImage(file='label12.gif')

class font_enum:
    ubuntumono14b=tkFont.Font(master,family='Ubuntu Mono',size=14, weight='bold')
    ubuntumono14i=tkFont.Font(master,family='Ubuntu Mono',size=14, weight='normal')
    
font = font_enum()

origincfg=generic(bg=color.grey,
               fg=color.black,
               width=3,
               height=2,
               num=1,
               font=font.ubuntumono14b,
               pic=label4,
               bd=0)

xlabelcfg=generic(bg=color.black,
               fg=color.grey,
               width=6,
               height=3,
               num=5,
               font=font.ubuntumono14b,
               pic=label4,
               bd=0)

ylabelcfg=generic(bg=color.black,
               fg=color.grey,
               width=3,
               height=6,
               num=8,
               font=font.ubuntumono14b,
               pic=label4,
               bd=0)

cellcfg=generic(bg=color.grey,
               fg=color.black,
               width=6,
               height=3,
               num=16,
               font=font.ubuntumono14b,
               pic=label12,
               bd=0.5)


def button(parent,config,scale,width=0,height=0):
    
    if width==0: width=config.width*scale
    if height==0: height=config.height*scale
    
    return(tk.Button(parent,
                     image=config.pic,
                     width=width,
                     height=height,
                     background=config.bg,
                     foreground=config.fg,
                     font=config.font,
                     bd=config.bd))
   
def button_factory(parent,
                   packside, 
                   config, 
                   sizes,
                   scale=1):
    
	''' sizes add up to 100% ; if scale is 1 then total size will be 100 pixels '''
	cellwid = []
	if len(sizes)==0:
	    for i in range(config.num):
		_button = button(parent,
		       config,
		       scale)
		_button.pack(fill="both",
		                   expand=True,
		                   side=packside)
		cellwid.append(_button)
	else:
	    for size in sizes:
		_button = button(parent,
		       config,
		       scale,
		       size*scale,
		       size*scale)
		_button.pack(fill="both",
		                        expand=True,
		                        side=packside)
		cellwid.append(_button)
		
	return cellwid

def merge_cells(cellwid, config, scale, column,cell,last_cell):
    num_rows = last_cell - cell
    for row in range(cell+1,last_cell+1):
	cellwid[column][row].destroy()
    
    border_width=6
    new_height = config.height*(num_rows+1)*scale+(border_width*num_rows)
    
    cellwid[column][cell].configure(height=new_height,
                                    background=color.pink)
	
    
def init_grid():

    ylabel = tk.Frame(master)
    ylabelwid=button_factory(ylabel,
                             "bottom",
                             ylabelcfg,
                             [],
                             10)
    ylabelwid.append(button_factory(ylabel,
                                    "bottom",
                                    origincfg,
                                    [],
                                    10))
    ylabel.pack(side="left",
                fill="y",
                expand=False)
		    
    
    
    xlabel = tk.Frame(master)
    xlabelwid = button_factory(xlabel,
                               "right",
                               xlabelcfg,
                               [],
                               10)
    xlabel.pack(side="top",fill="x",expand=False)
    
    cellwid=[]
    for i in range(20):
	gridcolumn = tk.Frame(master)
	cellwid.append(button_factory(gridcolumn,
	                              "bottom",
	                              cellcfg,[],
	                              10))
	gridcolumn.pack(side="right",fill="both",expand=True)

    return cellwid

cellwid = init_grid()

merge_cells(cellwid,cellcfg,10,3,4,7)
merge_cells(cellwid,cellcfg,10,1,2,4)
merge_cells(cellwid,cellcfg,10,4,2,7)
merge_cells(cellwid,cellcfg,10,2,4,5)
merge_cells(cellwid,cellcfg,10,0,7,12)
master.mainloop()
