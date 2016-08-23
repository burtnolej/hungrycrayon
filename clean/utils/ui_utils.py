from Tkinter import *
from Tkinter import Button as Tkbutton
from Tkinter import Label as Tklabel
from ttk import *
import tkFont
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")

from image_utils import ImageCreate, rgbstr_get
ic = ImageCreate()
widget_config = {'cursor': 0, 
                 'style':0,
                 'height': 0,
                 'padding':0,
                 'width':0,
                 'borderwidth':0,  
                 'class': 0,
                 'takefocus':0, 
                 'relief':0}

sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_enum import enum


tkfrm_cfg= enum.datamembers(dm={'background':'#000000',
                                'borderwidth':1,
                                'width':20,
                                'height':10})

def tk_create_config(style,cfg,stylename):
    for k,v in cfg.attr_get_keyval(include_callable=False,
                                   include_nondataattr=False):
        style.configure(stylename,k=v)
        
def tk_create_frame(parent,stylename):
    return(Frame(parent,style=stylename))

def tk_label_get_image(widget,text,**kw):
    
    if kw.has_key('pointsize'):
        kw['pointsize'] = int((kw['pointsize']/3)*4)
        
    widget.update_idletasks()

    w = widget.winfo_width()
    h = widget.winfo_height()

    geom = "{0}x{1}".format(w,h)
    
    outputfiles = ic.create_image_file(text,
                                       size=geom,
                                       **kw)

    return(PhotoImage(file=outputfiles[0]))
    
class GridTableWidget(Frame):

    def __init__(self,master=None,logicalwidth=5,logicalheight=10):
        
        '''
        logicalheight = number of actual columns created from a greater number of sub cols
        '''
        
        self.logicalheight= logicalheight
        self.logicalwidth=logicalwidth
        # set the number of subrows within a logical cell;
        cellcolumnspan = 19 # num of sub columns within a logical column
        cellrowspan = 19 # num of sub rows
        cellgroupspan = 6 # (19-1)/6=3 so would create 3 sub rows
        self.cellrownum = (cellrowspan-1)/cellgroupspan
        
        gridwidth = (logicalwidth*cellcolumnspan)+1 # +1 for left header
        gridheight =  (logicalheight*cellrowspan)+1 # +1 for top headers
       
        headerbg='#%02x%02x%02x' % (214, 210, 208)
        labelbg='white'

        headerbw = 1 # borderwidth for the headers
        headerhtness = 0 # highlightthickness for headers

        
        cellwidth = 25 # pixel width of a cell
        cellheight = 5 # pixel height - helvetica
        #cellheight = 10 # pixel height
        
        cellbw = 1 # borderwidth for the headers
        cellhtness = 1 # highlightthickness for headers
        
        self.rowheaderwidget=[]
        self.columnheaderwidget=[]
        
        # stores the refs to each of the label widgets
        # 3d array [#row][#col][#cellrow]
        self.widget=[]
        
        _style = Style()
        _style.configure('mystyle.TFrame',background=headerbg)
        Frame.__init__(self, master,style='mystyle.TFrame')
        self.grid(rows=gridheight, columns=gridwidth)
        
        # draw top column headers
        for column in range(1,gridwidth-1,cellcolumnspan):
            colhdrlbl=Tklabel(self,text='',
                              bg=headerbg,
                              width=cellwidth,
                              height=cellheight/(cellrowspan-1),
                              #height=1,
                              borderwidth=headerbw,
                              highlightthickness=headerhtness,
                              name="{0},{1}".format(0,column))
            colhdrlbl.grid(row=0,
                           column=column,
                           columnspan=cellcolumnspan-1)
            
            photo = PhotoImage(file="ic_082316/Thursday-Helvetica-16-center-#d6d2d0-204x19.gif")
            colhdrlbl.config(image=photo)
            colhdrlbl.config(width=204)
            colhdrlbl.config(height=19)
            
            #colhdrlbl.config(name="colhdr.{0}.{1}".format(0,column))
            
            self.columnheaderwidget.append(colhdrlbl)
            
            # add a spacer to the last column of the grid
            colhdrspc=Tklabel(self,text='',
            #colhdrspc=Tklabel(self,
                            bg='red',
                            width=cellwidth/(cellcolumnspan-1),
                            height=cellheight/(cellrowspan-1),
                            borderwidth=headerbw,
                            highlightthickness=headerhtness)

            colhdrspc.grid(row=0,column=column+cellcolumnspan-1)    
            
            
        # draw row headers
        for row in range(1,gridheight-1,cellrowspan):

            # add label that spans all but 1 row
            rowhdrbut=Tklabel(self,text='', 
                              bg=headerbg,
                              width=cellwidth/cellcolumnspan,
                              height=cellheight,
                              borderwidth=headerbw,
                              highlightthickness=headerhtness,
                              name="rowhdrbut {0}:{1}".format(row,0))
            rowhdrbut.grid(row=row,
                           column=0,
                           rowspan=cellrowspan-1)
            
            photo = PhotoImage(file="ic_082316/1215-1300-90-16-center-#d6d2d0-Helvetica-12x79.gif")
            rowhdrbut.config(image=photo)
            rowhdrbut.config(width=12)
            rowhdrbut.config(height=79)
            
            #rowhdrbut.config(name="rowhdrbut.{0}.{1}".format(row,1))

            self.rowheaderwidget.append(rowhdrbut)
            
            # add a spacer to the last row of the grid
            rowhdrspc=Tklabel(self,text='',
                            bg='red',
                            width=cellwidth/cellcolumnspan,
                            height=cellheight/cellrowspan,
                            borderwidth=headerbw,
                            highlightthickness=headerhtness)
            
            rowhdrspc.grid(row=row+cellrowspan-1,
                         column=0)     
        
        # draw cells
        for row in range(1,gridheight-1,cellrowspan):
            columnwidget=[]
            for column in range(1,gridwidth-1,cellcolumnspan):
                
                
                # for all but 1 subrow draw a label
                cellrowwidget=[]
                for subrow in range(row,row+cellrowspan-1,cellgroupspan):
                    
                    celllbl=Tklabel(self,text='',
                                    bg=labelbg,
                                    width=cellwidth,
                                    height=cellheight/(cellrowspan/cellgroupspan),
                                    borderwidth=cellbw,
                                    highlightthickness=cellhtness,
                                    name="{0},{1},{2}".format(row,column,subrow))

                    celllbl.grid(row=subrow,column=column,
                                 columnspan=cellcolumnspan-1,
                                 rowspan=cellgroupspan)
                    
                    #celllbl.config(name="celllbl.{0}.{1}".format(row,column))
                    
                    cellrowwidget.append(celllbl)
                columnwidget.append(cellrowwidget)

                # for the last subrow draw a spacer
                cellspc=Tklabel(self,text='',
                                bg=headerbg,
                                width=cellwidth,
                                height=cellheight/cellrowspan,
                                borderwidth=headerbw,
                                highlightthickness=headerhtness)
                
                cellspc.grid(row=row+cellrowspan-1,
                             column=column,
                             columnspan=cellcolumnspan)
                
                # for the last subcol draw a spacer
                cellspc=Tklabel(self,text='',
                                bg=headerbg,
                                width=cellwidth/cellcolumnspan,
                                height=cellheight,
                                borderwidth=headerbw,
                                highlightthickness=headerhtness)
                
                cellspc.grid(row=row,
                             column=column+cellcolumnspan-1,
                             rowspan=cellrowspan)
                
                
            self.widget.append(columnwidget)
        
    
    # decorator / iterator to parse a datagrid and call a func
    # for each item in the grid with the corresponding widget handle
    def datatable_iter(func):
        def inner(*args):
            tablewgt=args[0]
            datagrid = args[1]
            
            for row in range(len(datagrid)):
                for cell in range(len(datagrid[row])):
                    for cellrow in range(len(datagrid[row][cell])):
                        item = datagrid[row][cell][cellrow]
                        wgt = tablewgt.widget[row][cell][cellrow]
                        func(tablewgt,datagrid,wgt,item)
        return inner
    
    # decorator / iterator to run a function on each widget
    def widget_iter(func):
        def inner(*args):
            tablewgt=args[0]
            try:
                item = args[1]
            except:
                item = None
                              
            try:
                attr = args[2]
            except:
                attr = 'widget'
            
            widgets = getattr(tablewgt,attr)
            for row in range(len(widgets)):
                for cell in range(len(widgets[row])):
                    for cellrow in range(len(widgets[row][cell])):
                        wgt = widgets[row][cell][cellrow]
                        func(tablewgt,wgt,item)
        return inner


    @widget_iter
    def table_update_all_text(self,wgt,text):
        wgt.config(text=text)
        
    @widget_iter
    def table_update_all_fonts(self,wgt,font):
        wgt.config(font=font)
        
    @datatable_iter
    def table_update_content(self,datagrid,wgt,text=None):
        wgt.config(text=text)
        
    def widget_dump_info(self,wgt):
        wgt.update_idletasks()
        print "name",str(wgt),
        print "height",wgt.winfo_height(),
        print "width",wgt.winfo_width()        \
              
    def table_dump_header_info(self):
        for header in self.columnheaderwidget:
            self.widget_dump_info(header)
            
        for header in self.rowheaderwidget:
            self.widget_dump_info(header)
    
    @widget_iter
    def table_dump_info(self,wgt,item=None):        
        self.widget_dump_info(wgt)
        
    @datatable_iter 
    def table_update_colors(self,datagrid,wgt,colorpair=None):
        if colorpair <> '':
            bg = colorpair.BACKGROUND_COLOR
            fg = colorpair.COLOR
            wgt.config(bg=bg)            
            wgt.config(fg=fg)
            
    @datatable_iter
    def table_update_font(self,datagrid,wgt,font=None):
        if font <> '':
            wgt.config(font=font)     
            #wgt.config(width=30)
            #wgt.config(height=1)

    def table_get_content(self):
        widgettext=[]
        for row in range(len(self.widget)):
            columnwidget=[]
            for column in range(len(self.widget[row])):
                cellrowwidget=[]
                for cellrow in range(3):
                    cellrowwidget.append(self.widget[row][column][cellrow].cget('text'))
                columnwidget.append(cellrowwidget)
            widgettext.append(columnwidget)
        return widgettext

    def _init_datagrid(self,value=''):
        grid = []
        for row in range(self.logicalheight):
            columnwidget=[]
            for column in range(self.logicalwidth):
                cellrowwidget=[]
                for cellrow in range(self.cellrownum):
                    cellrowwidget.append('')
                columnwidget.append(cellrowwidget)
            grid.append(columnwidget)
        return grid  
        
if __name__ == '__main__':
    master = Tk()
    wgt = GridTableWidget(master,5,8)
    master.mainloop()
    
    import pprint
    
    pprint.pprint(wgt.widget)