from Tkinter import *
from ttk import *

import tkFont
import sys
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
    