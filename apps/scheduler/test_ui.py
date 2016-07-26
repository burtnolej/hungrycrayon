master,

from scheduler_util import generic

class config(generic):
    pass

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

origincfg=config(bg=color.grey,
               fg=color.black,
               width=3,
               height=2,
               num=1,
               font=font.ubuntumono14b,
               pic=label4,
               side="top",
               frameside="bottom",
               framefill="y",
               frameexpand=False,
               bd=0)

xlabelcfg=config(bg=color.black,
               fg=color.grey,
               width=6,
               height=3,
               num=20,
               font=font.ubuntumono14b,
               pic=label4,
               side="left",
               frameside="top",
               framefill="x",
               frameexpand=False,
               bd=0)

ylabelcfg=config(bg=color.black,
               fg=color.grey,
               width=3,
               height=6,
               num=8,
               font=font.ubuntumono14b,
               pic=label4,
               side="top",
               frameside="left",
               framefill="y",
               frameexpand=False,
               bd=0)

cellcfg=config(bg=color.grey,
               fg=color.black,
               width=6,
               height=3,
               num=16,
               font=font.ubuntumono14b,
               pic=label12,
               side="bottom",
               frameside="right",
               framefill="both",
               frameexpand=True,
               bd=0.5)


def cell(parent,config,scale,width=0,height=0):
    
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
   
def cell_factory(parent, 
                   config, 
                   sizes,
                   scale=1):
    
	''' sizes add up to 100% ; if scale is 1 then total size will be 100 pixels '''
	cellwid = []
	if len(sizes)==0:
	    for i in range(config.num):
		_cell = cell(parent,
		       config,
		       scale)
		_cell.pack(fill="both",
		                   expand=True,
		                   side=config.side)
		cellwid.append(_cell)
	else:
	    for size in sizes:
		_cell = cell(parent,
		       config,
		       scale,
		       size*scale,
		       size*scale)
		_cell.pack(fill="both",
		                        expand=True,
		                        side=config.side)
		cellwid.append(_cell)
		
	return cellwid

def merge_cells(cellwid, config, scale, column,cell,last_cell):
    num_rows = last_cell - cell
    for row in range(cell+1,last_cell+1):
	cellwid[column][row].destroy()
    
    border_width=6
    new_height = config.height*(num_rows+1)*scale+(border_width*num_rows)
    
    cellwid[column][cell].configure(height=new_height,
                                    background=color.pink)
	
    
def init_range(parent,config,scale,**args):
    _frame = tk.Frame(parent)
    
    for key,value in args.iteritems():
	setattr(config,key,value)
	
    cellwid = cell_factory(_frame,
                           config,
                           [],
                           scale)
    _frame.pack(side=config.frameside,
                fill=config.framefill,
                expand=config.frameexpand)
    
    return(cellwid)
    
def init_grid():

    init_range(master,ylabelcfg,10)
    #init_range(ylabel,origincfg,10)    
    init_range(master,xlabelcfg,10)
    init_range(master,xlabelcfg,10,num=4)
    
    cellwid=[]
    for i in range(20):
	cellwid.append(init_range(master,cellcfg,10))

    return cellwid

cellwid = init_grid()

merge_cells(cellwid,cellcfg,10,3,4,7)
merge_cells(cellwid,cellcfg,10,1,2,4)
merge_cells(cellwid,cellcfg,10,4,2,7)
merge_cells(cellwid,cellcfg,10,2,4,5)
merge_cells(cellwid,cellcfg,10,0,7,12)
master.mainloop()
