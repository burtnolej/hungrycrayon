
import os
import ssviewer_rest
import pycurl
import cStringIO
import urllib
from time import sleep

def launchservice(dbpath,dbname,**args):
    os.environ['DBPATH'] = dbpath
    os.environ['DBNAME'] = dbname
    ssviewer_rest.run(**args)
    sleep(1)


def restquery(url,**params):
    
    buffer = cStringIO.StringIO()
    curl = pycurl.Curl()
    
    if params <> {}:
        url = url + "?" + urllib.urlencode(params)
    
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, buffer.write)
    
    # avoid spurious error due to threading problem when service is stopped
    try:
        curl.perform()
    except pycurl.error:
        pass    
    
    _buffer = buffer.getvalue()

    buffer.close()
    curl.close()
    
    return(_buffer)

class RestService():
    def __init__(self,port,url,runcmd,dbpath,dbname,**args):
        self.dbpath = dbpath
        self.dbname = dbname
        self.args = args
        self.url = url
        self.runcmd = runcmd
        self.port = port

        os.environ['DBPATH'] = dbpath
        os.environ['DBNAME'] = dbname

    def __enter__(self):
        globals()[self.runcmd].run(self.port,**self.args)
        sleep(1)
        
    def __exit__(self,type,value,traceback):
        restquery(self.url + "command/stop")
        
        