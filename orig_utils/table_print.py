#!/usr/bin/python

from os import getpid
from os import getlogin, path
from inspect import stack,getmembers, ismethod
from time import strftime
from time import time
from datetime import datetime
from sys import exc_info, exit
from sys import stdout
from collections import OrderedDict
from linecache import getline

from misc_util import get_terminal_size, compare_arrays,print_dict_basic,items_allsame_length,_GetchUnix, in_method_log
from types import FileType,IntType,LongType,FloatType,BooleanType,InstanceType,ClassType, ModuleType,ListType,DictType,NoneType, FunctionType, BuiltinFunctionType,BuiltinMethodType,TupleType

'''class TableCell(object)
         def printout
   class TableRow(object)
         def get_cells
         def get_cell_widths
         def add_cell_widths
         def printouut
   class Table(object)
         def _set_stats
         def _get_rows
         def _get_slice_cell_iter
         def _get_row_slice_iter
         def add_rows
         def _set_col_widths
         def _get_table_width
         def printout
         def print_stats
'''  
class TableStats():
    def __init__(self,**kwargs):
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

class TableCell(object):
    def __init__(self,cell_value,row,table):
        self._cell_value=cell_value
        self._cell_width=len(str(cell_value))
        self._row=row
        self._row._num_cells+=1
        self._table=table
        
    def printout(self,lh,col_width=None):

        spacer = self._table._spacer
        pad_char = self._table._pad_char
        term_width = self._table._term_width

        if not self._row._full:
            if col_width == None:
                lh.write(str(self._cell_value) + spacer)
                self._row._row_cursor_x += col_width+len(spacer) + 1
            else:
                #print "(" + str(self._row._row_cursor) + ")",
                if (self._row._row_cursor_x + col_width+len(spacer)) < term_width:
                    lh.write(str(self._cell_value).ljust(col_width,pad_char) + spacer)
                    self._row._row_cursor_x += col_width+len(spacer) + 1
                else:
                    remaining_space = term_width - self._row._row_cursor_x
                    if remaining_space < len(str(self._cell_value)):
                        lh.write(str(self._cell_value)[0:remaining_space])
                    else:
                        lh.write(str(self._cell_value).ljust(remaining_space,pad_char))
                    self._row._full = True
        
class TableRow(object):
    def __init__(self,table,row_slice):
        self._cells = list()
        self._column_widths = list()
        self._num_cells=0
        self._table=table
        self._table._num_rows+=1
        self._row=row_slice
        self._row_cursor_x=0
        self._full = False
        self.add_cells()

    def get_cells(self):
        return(self._cells)

    def get_cell_widths(self):
        return[c._cell_width for c in self.get_cells()]

    def add_cells(self):
        [self._cells.append(TableCell(cell_value,self,self._table)) for cell_value in self._row]   

    def printout(self,lh):
        if self._table._page:
            if (self._table._num_rows_printed%(self._table._term_height-1)) == 0 and self._table._num_rows_printed>0:
                print "**** HIT ANY KEY FOR MORE ****\r",
                getch = _GetchUnix()
                getch()
                #print "\r"

        # this is for recursive prints where an indent/prefix is used to show where an object is in the tree
        TableCell(self._table._prefix,self,self._table).printout(lh,len(self._table._prefix))

        [self.get_cells()[i].printout(lh,self._table._column_widths[i]) for i in range(0,self._table._num_cols)]
        lh.write("\n")
        self._table._num_rows_printed+=1

class Table(object):
    '''
    args
    _seed         = object or list(dict) to print
    _depth        = int,current depth if this is part of a recursive tree (deep print)
    _max_depth    = int,maximum depth to let the tree go to. if frames are involved it can go very deep
    _start_depth  = int,where to start displaying, this with max_depth is useful if only certain depths are interesting
    _show_summary = boolean, True/False, supress detail and just print header for each table object, useful for debugging
    _show_dirty   = boolean,True/False, print header for Tables that have been skipped becaause they have been parsed once already
    _prefix       = gets added to start of each line output, useful for indenting to show depth as part of a recursive print
    _descr        = to print in addition to args so the run is identifiable in the log file 
    '''
    dirty_object = []
    printed_object_count = 0
            
    def __init__(self,_seed,_depth=0,_max_column_width=35,_max_depth=10,_start_depth=0,_show_summary=False,_show_dirty=False,_page=True,_prefix="",_descr=""):
        
        ###############
        # here are the configurable bits
        self._seed = _seed
        self._max_column_width = _max_column_width
        self._max_cell_depth = 6
        self._pad_char = " "
        self._table_pad_char= "_"
        self._spacer = " |"
        self._depth= _depth
        self._max_depth = _max_depth
        self._start_depth = _start_depth
        self._show_summary = _show_summary
        self._show_dirty = _show_dirty
        self._prefix = _prefix
        self._descr = _descr
        self._page = _page

        ################

        self._num_rows=0
        self._num_rows_printed=1 # add one for the title
        self._num_cols=0
        self._table_width=0
        self._column_widths = ()
        self._rows=list()
        self._stats_dict = OrderedDict()        

        self._term_width,self._term_height = get_terminal_size()
        self._start_time,self._end_time=time(),0

        self._set_name()
        self.add_rows()
        self._num_cols = len(self._column_widths)
        self._set_stats()

    #@in_method_log
    def _set_name(self):
        '''
        change the name used in the heading for the report when self
        is of type list or dict other it will be the literal contents and long
        '''
        first_val = ""
        type_string = ""
        obj_len = 0
        type_string = str(self._seed)

        if isinstance(self._seed,(ListType,TupleType)):
            type_string = "List"
            obj_len = len(self._seed)
            if obj_len > 0:
                first_val = str(self._seed[0])
                first_val = first_val.rstrip("\n")
    
        elif isinstance(self._seed,DictType):
            type_string = "Dict"
            obj_len = len(self._seed)
            if obj_len > 0:
                first_val = str(self._seed.keys()[0])
                first_val = first_val.rstrip("\n")
    
        self._name = type_string+":"+str(obj_len)+":"+first_val
        return(self._seed,self._name)

    def print_stats(self):
        print_dict_basic(self._stats_dict)

    def _set_stats(self):
        self._stats = TableStats(_num_cols = self._num_cols,
            _width_chars = self._get_table_width(),
            _num_rows = self._num_rows,
            _term_width = self._term_width,
            _term_height = self._term_height,
            _build_time_ms = round((time()-self._start_time)*1000,1))

    def _get_rows(self):
        return(self._rows)

    def _get_slice_cell_iter(self,row,slice_range,max_column_width):
        '''
        type: generator
        args: row=Row instance, slice_range=starting char of the slice
              max_column_width=max allowed width
        return: yields all cells of a row slice

        example row: 'aaaaaa','bbbb','ccccccccccc'
        _slice_range=4           _slice_range=9 
        _max_column_width=4      _max_column_width=3
        2 'aa  ','    ','cccc'   4 '   ','   ','c  '
        '''
        l=list()
        blank_flag=False
        for cell_value in row:
            slice_cell_value=str(cell_value)[slice_range:slice_range+max_column_width]
            l.append(slice_cell_value)
            if slice_cell_value != "":
                 blank_flag=True
        return(blank_flag,l)

    def _get_row_slice_iter(self,row): 
        '''
        type: generator
        args: row=Row instance, self=Table instance
        return: yields all the slices for a row

        example row: 'aaaaaa','bbbb','ccccccccccc'
        _max_column_width=4      _max_column_width=3 
        _max_cell_depth=2        _max_cell_depth=5
        would create 2 slices:   would create 4 slices
        1 'aaaa','bbbb','cccc'   1 'aaa','bbb','ccc'  
        2 'aa  ','    ','cccc'   2 'aaa','b  ','ccc'
                                 3 '   ','   ','ccc'
                                 4 '   ','   ','c  '
        '''
        max_column_width = self._max_column_width
        max_cell_area = self._max_cell_depth*max_column_width # area=depth*width
        max_cell_depth = self._max_cell_depth

        for slice_range in range(0,max_cell_area,max_column_width):
            (blank_flag,slice) = self._get_slice_cell_iter(row,slice_range,max_column_width)
            if blank_flag==False:
                raise StopIteration
            yield slice
        # we have hit max_no_lines so yield how many rows left
        yield [ (len(str(cell_value))/max_column_width)/max_cell_depth for cell_value in row ]

    def add_rows(self):
        for row in self._cell_generator(self._seed): # get a row from the generator
            for row_slice in self._get_row_slice_iter(row): # take a slice of the row 
                self._rows.append(self._set_col_widths(TableRow(self,row_slice))) # create row, add to table, expand widths

    # does adding this row mean we have to change the column widths
    def _set_col_widths(self,table_row):
        '''
        args:table_row:._cells,_column_widths,_num_cells,_table,row_slice
        '''
        if self._num_rows == 1: # if its the first row nothing to compare with
            self._column_widths = table_row.get_cell_widths()
        else:
            self._column_widths = compare_arrays(self._column_widths,table_row.get_cell_widths())
        return(table_row)

    def _get_table_width(self):
        return sum([column_width + len(self._pad_char) for column_width in self._column_widths])

    def print_header(self,lh):
        lh.write(" descr:"+str(self._descr))
        lh.write(" seed:"+str(self._seed))
        lh.write(" depth:"+str(self._depth))
        lh.write(" max_depth:"+str(self._max_depth))
        lh.write(" start_depth:"+str(self._start_depth))
        lh.write(" show_summary:"+str(self._show_summary))
        lh.write(" show_summry:"+str(self._show_dirty))
        lh.write(" prefix:"+str(self._prefix))
        
    def printout(self,lh=None):
        if not lh:
            import sys
            lh = sys.stdout
        
        # if its the first object (i.e in a tree)
        #if Table.printed_object_count == 0:
        #    self.print_header(lh)
        
        Table.printed_object_count+= 1
        #lh.write(self._prefix+str(self._name).upper().center(self._term_width-len(self._prefix),"*"))
        if not self._show_summary:
            [table_row.printout(lh) for table_row in self._get_rows()]
 
    def _cell_generator(self,object):
        column_titles = ["callable","name","getattr()","type","[]Flag","[]Len","[]content"]
        yield column_titles

        for e in dir(object):
            mylistcontent=None
            mylistattr,mylistlen=False,0
            method_flag=callable(getattr(object,e))
            attr=getattr(object,e)
            attr_type=type(getattr(object,e))
            if isinstance(attr,list) and len(attr)>0:
                mylistattr=True
                mylistcontent=attr[0]
            if mylistattr:
                mylistlen=len(attr)
            (yield [method_flag,e,attr,attr_type,mylistattr,mylistlen,mylistcontent])

    #@in_method_log
    def _is_list_item_iterable(self,name):
        non_iter_types = (FileType,NoneType,IntType,LongType,FloatType,BooleanType,basestring,FunctionType,ModuleType,BuiltinFunctionType,BuiltinMethodType)
        if not isinstance(name,non_iter_types):
            return(True)
        return(False)

    #@in_method_log
    def _is_member_iterable(self,name,object=None):
        non_iter_types = (FileType,NoneType,IntType,LongType,FloatType,BooleanType,FunctionType,basestring,ModuleType,BuiltinFunctionType,BuiltinMethodType)
        if object != None:
            attr = getattr(object,name)
        else:
            attr = getattr(self._seed,name)
            
        if name[-2:] != "__" and not isinstance(attr,non_iter_types) and not callable(attr) and name != "f_builtins" and name != "f_code":
        #if name[-2:] != "__" and not isinstance(attr,non_iter_types) and not callable(attr) and name != "f_builtins":
            return(True)
        return(False)
        
    #@in_method_log
    def _isa_class_instance(self,name):
        return(isinstance(getattr(self._seed,name),(object,InstanceType)))
        
    #@in_method_log
    def _is_member_a_list(self,name):
        return(isinstance(getattr(self._seed,name),(ListType,TupleType)))

    #@in_method_log
    def _not_dirty(self,value):
        if value in self.dirty_object:
            return(False)
        return(True)

    #@in_method_log
    def _set_dirty(self,value=None):
        if value==None:
            value = self._seed
        self.dirty_object.append(value)
        return(value,len(self.dirty_object))
        
    #@in_method_log
    def _deep_print_next(self,value):
        if self._not_dirty(value):
            new_table = self.__class__(value,self._depth,self._max_depth,self._start_depth,self._show_summary,self._show_dirty,str(self._depth)+"".ljust(self._depth*4," "),self._descr)
            new_table.deep_print()
        elif self._show_dirty:
            print self._prefix+str(self._name).upper().center(self._term_width-len(self._prefix),"D")
                                
    def deep_print(self):
        '''
        function to print out any member attributes or list items
        that are iterable themselves. traverses the tree until hits
        the bottom global dirty_object or hits max_depth

        args: start_depth - min depth to print out, ie a non zero value
        will not print out anyt depths lower
        '''
        if self._depth >= self._start_depth and self._depth < self._max_depth:
            self.printout()
        elif self._depth >= self._max_depth:
            return
        
        self._set_dirty()
        self._depth+=1
                
        if isinstance(self._seed,(ListType,TupleType)):
            for i in range(0,len(self._seed)):
                if self._is_list_item_iterable(self._seed[i]):
                    self._deep_print_next(self._seed[i])
        elif isinstance(self._seed,DictType):
            for key,value in self._seed.iteritems():
                if self._is_list_item_iterable(value):
                    self._deep_print_next(value)
        else:
            for name, value in getmembers(self._seed):
                if self._is_member_iterable(name):
                    self._deep_print_next(value)

        # using class static variable so need to clear them out in case of another run
        if self._depth == 1:
                self._reset()

    def _reset(self):
        Table.dirty_object = []
        Table.printed_object_count = 0

class SimpleTable(Table):
    ''''
    prints tables in the form 'name','value','Y/N' where bool is
    whether item is iterable further or not
    knows how to handle recursion for lists, dicts and object members
    and any combo thereof
    '''
    def __init__(self,*args):
        '''
        can overide any config variables after super constructor called
        '''
        super(SimpleTable,self).__init__(*args)
        
    def _cell_generator(self,object):
        column_titles = ["name","value","o"]
        yield column_titles
        if isinstance(object,(ListType,TupleType)):
            for i in range(0,len(object)):
                if self._is_list_item_iterable(object[i]):
                    yield [i,object[i],"Y"]
                else:
                    yield [i,object[i],"N"]
        elif isinstance(object,dict):
            for name,value in object.iteritems():
                if self._is_list_item_iterable(value):
                    yield [name,value,"Y"]
                else:
                    yield [name,value,"N"]
        else:
            for name,value in getmembers(object):
                if self._is_member_iterable(name):
                    yield [name,value,"Y"]
                else:
                    if name[-2:] != "__": # never want to see __xyz__ builtins
                        yield [name,value,"N"]


            
class ObjectTablePrint(Table):
    def __init__(self,obj,*args,**kwargs):
        self.data = []
        self.obj = obj
        self.get_data()
    
        super(ObjectTablePrint,self).__init__(self.data,*args,**kwargs)

    def _cell_generator(self,object):
        for i in object:
            yield [j for j in i]

    def get_data(self):
        self.data.append(self.get_attr_keys(self.obj))
        self.data.append(self.get_attr_values(self.obj))

    def get_attr_keys(self,object):
        l=[]
        for k,v in getmembers(object):
            if not str(k).startswith("__") and not callable(v):
                l.append(k)
        return(l)
    
    def get_attr_values(self,object):
        l=[]
        for k,v in getmembers(object):
            if not str(k).startswith("__") and not callable(v):
                l.append(v)
        return(l)

    def get_methods(self,object):
        for k,v in getmembers(object):
            if not str(k).startswith("__") and callable(v):
                yield k,v

class HashObjectTablePrint(ObjectTablePrint):
    def get_data(self):
        item1 = self.obj.values()[0]
        self.data.append(self.get_attr_keys(item1))
        
        for v in self.obj.values():
            self.data.append(self.get_attr_values(v))

        
if __name__ == '__main__':

    # 1st run is just to create an object instance (table) thats
    # exciting enough to act as a test

    tmp_table = Table(Table)
    
    table = Table(tmp_table)
    table.printout()
    
    stats_table = Table(table._stats)
    stats_table.printout()
