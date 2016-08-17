from Tkinter import *
from ttk import *

import tkFont
import sys

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
    