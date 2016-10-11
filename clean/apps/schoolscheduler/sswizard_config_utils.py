import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)


def set_configs(style):
    style.configure('ConfigPanel.TFrame',background='blue')
    style.configure('ControlPanel.TFrame',background='red')
    style.configure('EntryGrid.TFrame',background='green')
    
