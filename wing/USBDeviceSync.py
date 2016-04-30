import unittest
import sys
sys.path.append("/home/burtnolej/pythonapps3/utils")

import commands
import os
import re
from datetime import datetime

class USBDeviceSync():
    def __init__(self,mount_point, source_path, target_path_suffix):
        self.mount_point = mount_point
        self.source_path = source_path
        self.target_path_suffix = target_path_suffix
    
    def _get_now():
        return(datetime.now().strftime("%m%d%y"))
    
    def _exec_cmd(self,cmd):
        return(commands.getstatusoutput(cmd))
    
    def mount(self):
        pass
    
    def unmount(self):
        pass
    
    def get_device_name(self):
        pass
    
    def set_target_path(self):
        pass
    
    def sync():
        pass
    
class iPhonePicSync(USBDeviceSync):
    
    def sync(self):
        self.unmount()
        self.pair()
        self.get_device_name()
        self.set_target_path()
        self.mount()
    
    def _mount_success(self):
        pass
    
    def mount(self):
        cmd="ifuse " + self.mount_point
        code, text = self._exec_cmd(cmd)
        
        put code in here to determine if successfull or not
        
        return(code,text)
    
    def _unmount_success():
        pass
    
    def unmount(self):
        cmd="fusermount -u " + self.mount_point
        code, text = self._exec_cmd(cmd)
        
        put code in here to determine if successfull or not
        
        return(code,text)
    
    def _pair_success(self,return_text):    
        if hasattr(re.search("SUCCESS",output),"pos"):
            return True
        return False
        
    def pair(self):
        cmd_iphone_pair="idevicepair pair"
        return_code, return_text = self._exec_cmd(cmd)
        
        if not _pairsuccess(return_text):
            raise Exception("failed to pair with device")
        
        return(True)
    
    def get_device_name(self,text):
        self.device_name = "unknown"
        UDID = text.split(" ")[4]
        if not device_UDID.has_key(UDID):
            raise Exception("unable to get device name")
        self.device_name = device_UDID[UDID]
        return(self.device_name)
    
    def set_target_path(self):
        today=datetime.now().strftime("%m%d%y")
        self.target_path = os.path.join(self.target_path_suffix + self.device_name,today)
        return(self.target_path)
    
class Test_iPhonePicSync(unittest.TestCase):
    
    def test_mount(self):
        
        tarantula.xml
  
            
        iphonepicsync = iPhonePicSync(mount_point,source_path,target_path_suffix)
    
    if __name__ == "__main__":
        
        suite = unittest.TestSuite()
    
        suite.addTest(Test_iPhonePicSync("test_mount"))
        
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)    