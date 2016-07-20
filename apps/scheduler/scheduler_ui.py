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

class grid_init_cfg_enum:
    columns=5
    rows=36
    item_height=2
    item_width=40
    item_text='not scheduled'
    item_bg=color.grey
    item_fg=color.black
    item_font=font.ubuntumono14i
    
grid_init_cfg = grid_init_cfg_enum()

colwid = []
butwid = []

def button_factory(parent, row,cfg,label=""):

    button = tk.Button(parent,
                       text=cfg.item_text+"("+str(label)+")",
                       width=cfg.item_width,
                       height=cfg.item_height,
                       background=cfg.item_bg,
                       foreground=cfg.item_fg,
                       font=cfg.item_font,
                       bd=0.5)
    
    button.grid(row=row,column=1,sticky=tk.N)
    return button

def column_factory(parent,col):
    
    column = tk.Frame(parent)
    column.grid(row=1,column=col,sticky = tk.W)
    return column
    
for columnid in range(grid_init_cfg.columns):
    _colwid = column_factory(master,columnid)
    colwid.append(_colwid)
    butwid.append([])
    
    for rowid in range(grid_init_cfg.rows):
        _butwid = button_factory(_colwid,rowid,grid_init_cfg,rowid)
        butwid[columnid].append(_butwid)
        

def merge_cells(start_row,end_row, column):
    num_rows = end_row - start_row
    for row in range(start_row+1,end_row+1):
        print row
        butwid[column][row].destroy()
        
    butwid[column][start_row].configure(height=grid_init_cfg.item_height*(num_rows+1),
                                        background=color.pink)
    
    c = tk.Canvas(colwid[column],width=380,height=14,
                  background=color.grey,
                  bd=0, highlightthickness=0, relief='ridge')
    c.grid(row=start_row+1,column=column)

        
    
info = colwid[0].grid_info()

merge_cells(2,3,1)

# making an item twice as big
#butwid[0][3].destroy()
#butwid[0][2].configure(height=4)


#c = tk.Canvas(colwid[0],width=380,height=14,background=grid_init_cfg.item_bg,
#              bd=0, highlightthickness=0, relief='ridge')
#c.grid(row=3,column=1)


master.mainloop()