#!/usr/bin/python

import sys
sys.path.append("/home/burtnolej/pythonapps3/utils")

import commands
import os
import re
from datetime import datetime
#import datetime_util

device_UDID = {"990c2407137d91ea7c7553bb8cb529f76610fd6b":"Tarantula"}

mount_point = "/media/iPhone"
iphone_pic_path = os.path.join(mount_point,"DCIM")
target_path_root = "/home/burtnolej/Pictures/iPhone-sync-"

today=datetime.now().strftime("%m%d%y")

cmd_iphone_pair="idevicepair pair"
cmd_iphone_mount="ifuse " + mount_point
cmd_iphone_unmount="fusermount -u " + mount_point
cmd_iphone_ls="find " + iphone_pic_path + " -name \"*\" -print | xargs stat -c \"%y %s %n\""

log=[]

def exec_cmd(cmd,log):
    
    return(commands.getstatusoutput(cmd))
    
def parse_output(output):
    search_result = re.search("SUCCESS",text)

    if hasattr(search_result,"pos"):
        return(0)
    else:
        return(code)

def get_device_name(text):
    UDID = text.split(" ")[4]
    if device_UDID.has_key(UDID):
        return(device_UDID[UDID])
    else:
        return("UNKNOWN")

# unmount 
_,return_text = exec_cmd(cmd_iphone_unmount,log)

# pair with iPhone - hit OK on device
_,return_text = exec_cmd(cmd_iphone_pair,log)
return_val = parse_output(return_text)
device_name = get_device_name(return_text)

# set target based on device name and date
target_pic_path = os.path.join(target_path_root + device_name,today)

# make todays dir if it doesnt exist


# mount iPhone user directories to local mount point 
code,text = exec_cmd(cmd_iphone_mount,log)
print text

# list files to move
code,text = exec_cmd(cmd_iphone_ls,log)

#print text
# unmount 
#exec_cmd(cmd_iphone_unmount,log)


exit()

#cp -r /media/iPhone/DCIM/* ~/Pictures/iPhones-sync/"DCIM-" + [phone name]
#phone name = tarantula
