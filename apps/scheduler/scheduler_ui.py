import Tkinter as tk
import tkFont


#print tkFont.families(tk.Tk())

master = tk.Tk()

class color_enum:    
    black='#000000'
    white='#fff'
    grey='#d3d3d3'
    pink='#ff69b4'

color = color_enum()

class font_enum:
    ubuntumono14b=tkFont.Font(master,family='Ubuntu Mono',size=14, weight='bold')
    ubuntumono14i=tkFont.Font(master,family='Ubuntu Mono',size=14, weight='normal')
    
font = font_enum()


class grid_config:
    def __init__(self,**args):
        for key,value in args.iteritems():
            setattr(self,key,value)
            
grid_init_cfg = grid_config(columns=5,
                            rows=36,
                            item_height=2,
                            item_width=40,
                            item_text='not scheduled',
                            item_bg=color.grey,
                            item_fg=color.black,
                            item_font=font.ubuntumono14i,
                            item_bd=0.5)

column_header_cfg=grid_config(columns=5,
                           rows=9,
                           item_height=8,
                           item_width=5,
                           item_text='hour',
                           item_bg=color.black,
                           item_fg=color.grey,
                           item_font=font.ubuntumono14b,
                           item_bd=0)

row_header_cfg=grid_config(columns=5,
                            rows=1,
                            item_height=2,
                            item_width=40,
                            item_text='day',
                            item_bg=color.black,
                            item_fg=color.grey,
                            item_font=font.ubuntumono14b,
                            item_bd=0)


def cell_factory(parent, row,cfg,vertical=True):

    button = tk.Button(parent,
                       text=cfg.item_text,
                       width=cfg.item_width,
                       height=cfg.item_height,
                       background=cfg.item_bg,
                       foreground=cfg.item_fg,
                       font=cfg.item_font,
                       bd=cfg.item_bd,
                       highlightbackground=cfg.item_bg)
    
    if vertical==False:
        button.grid(row=1,column=row,sticky=tk.N)
    else:
        button.grid(row=row,column=1,sticky=tk.N)
    return button

def column_factory(parent,col):
    column = tk.Frame(parent)
    column.grid(row=1,column=col,sticky = tk.W)
    return column

def merge_cells(start_row,end_row, column):
    num_rows = end_row - start_row
    for row in range(start_row+1,end_row+1):
        print row
        cellwid[column][row].destroy()
        
    cellwid[column][start_row].configure(height=grid_init_cfg.item_height*(num_rows+1),
                                        background=color.pink)
    
    c = tk.Canvas(colwid[column],width=380,height=14,
                  background=color.grey,
                  bd=0, highlightthickness=0, relief='ridge')
    c.grid(row=start_row+1,column=column)

def init_cells(master):     
    for columnid in range(grid_init_cfg.columns):
        _colwid = column_factory(master,columnid)
        colwid.append(_colwid)
        cellwid.append([])
        
        for rowid in range(grid_init_cfg.rows):
            _cellwid = cell_factory(_colwid,rowid,grid_init_cfg)
            cellwid[columnid].append(_cellwid)
   
colwid = []
cellwid = []

# add row for column titles
col_title_row = tk.Frame(master)
col_title_row.grid(row=1,column=2,sticky = tk.N)

for colid in range(0,5*2,2):
    cell_factory(col_title_row,colid,row_header_cfg,False)
    
    
    c = tk.Canvas(col_title_row,width=2,height=50,
                  background=color.black,
                  bd=0, highlightthickness=0)
    colid = colid +1 
    c.create_line(2,0,2,50,fill=color.pink,width=3)
    c.grid(row=1,column=colid)

    
# add column for row titles
row_title_column = tk.Frame(master)
row_title_column.grid(row=2,column=1,sticky = tk.W)

grid_frame = tk.Frame(master)
grid_frame.grid(row=2,column=2,sticky = tk.W)

for rowid in range(0,column_header_cfg.rows*2,2):
    cell_factory(row_title_column,rowid,column_header_cfg)
    
    c = tk.Canvas(row_title_column,width=71,height=44,
                  background=color.black,
                  bd=0, highlightthickness=0)
    rowid = rowid+1
    c.create_line(0,44,71,44,fill=color.pink,width=3)
    c.grid(row=rowid,column=1)



init_cells(grid_frame)

merge_cells(2,3,1)

master.mainloop()
