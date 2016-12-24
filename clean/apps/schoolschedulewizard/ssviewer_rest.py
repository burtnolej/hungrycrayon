import sys
import os
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)

import web
import xml_utils
#from ssviewer_headless import SSViewer
from misc_utils_objectfactory import ObjFactory
import xml.etree.ElementTree as xmltree
from database_util import Database, tbl_create
import ssviewer_utils
import sswizard_utils
import sswizard_query_utils
from ssviewer_utils_palette import *
from time import sleep

from inspect import getmembers
from threading import Lock

import os
import os.path

class Student:
    def GET(self,id):
        
        source_type="student"
        source_value=id
        if source_value=="all": source_value=""
        
        data = web.input(id='')

        ztypes = data.ztypes.split(",")
        formatson=False
        rollupson=False
        header=None
        if "formats" in ztypes: 
            formatson=True
        else:            
            header = "<root><parser><value>drawnoformatgrid</value></parser></root>"

        if "rollup" in ztypes: 
            rollupson=True
            ztypes.remove("rollup")

        constraints=[]
        for attr,attr_val in data.iteritems():
            if attr.startswith('cnstr_') == True:
                if str(attr_val) <> "NotSelected":
                    constraints.append((attr[6:],str(attr_val)))

        values = ssviewer_utils.dataset_pivot(of,enums,data.yaxis,data.xaxis,
                                              ztypes, source_type,source_value,
                                              constraints=constraints,
                                              formatson=True,rollupson=rollupson)
        

        grid = ssviewer_utils.dataset_serialize(values,formatson=formatson,
                                                schema = dict(xaxis=data.xaxis,
                                                              yaxis=data.yaxis,
                                                              ztypes=ztypes))
        
        xml = xml_utils.grid2xml(grid,header=header)

        return xmltree.tostring(xml)
    
class Add:
    def GET(self,objtype):
        
        _dm = web.input()

        datamembers = dict(zip(_dm.keys(),_dm.values()))  
        
        args = dict(database=database,refdatabase=database,
                    prepmap=prepmap,of=of,enums=enums,
                    datamembers=datamembers)
    
        newobj = ssviewer_utils.dataset_add(**args)
        
class New:
    def GET(self,objtype):
        
        #source_type="lesson"
        
        _values = ssviewer_utils.dataset_new(objtype)
        
        header = "<root><parser><value>drawform</value></parser></root>"
        
        xml=xml_utils.record2xml(_values,header=header)
        
        return xmltree.tostring(xml)
    
class Subject:
    def GET(self,id):
        
        source_type="subject"
        source_value=id
        
        data = web.input(id='')

        ztypes = data.ztypes.split(",")
        xaxis="period"
        yaxis="dow"
        
        formatson=False
        header=None
        if "formats" in ztypes: 
            formatson=True
        else:            
            header = "<root><parser><value>drawnoformatgrid</value></parser></root>"

        constraints=[]
        for attr,attr_val in data.iteritems():
            if attr.startswith('cnstr_') == True:
                if str(attr_val) <> "NotSelected":
                    constraints.append((attr[6:],str(attr_val)))
        
        values = ssviewer_utils.dataset_pivot(of,enums,data.yaxis,data.xaxis,
                                              ztypes, source_type,source_value,
                                              constraints=constraints,
                                              formatson=True)
        
        
        
        
        grid = ssviewer_utils.dataset_serialize(values,formatson=formatson,
                                                schema = dict(xaxis=data.xaxis,
                                                              yaxis=data.yaxis,
                                                              ztypes=ztypes))
        
        xml = xml_utils.grid2xml(grid,header=header)
        return xmltree.tostring(xml)

class Adult:
    def GET(self,id):
        
        source_type="adult"
        source_value=id

        data = web.input(id='')

        ztypes=data.ztypes.split(",")
        xaxis=data.xaxis
        yaxis=data.yaxis
        
        values = ssviewer_utils.dataset_pivot(of,enums,yaxis,xaxis,ztypes, source_type,source_value,formatson=True)
        grid = ssviewer_utils.dataset_serialize(values,formatson=True,schema = dict(xaxis=xaxis,yaxis=yaxis,ztypes=ztypes))

        xml = xml_utils.grid2xml(grid)
        
        return xmltree.tostring(xml)
    
class List:
    def GET(self,objtype):
        data = web.input(id='')

        pagenum=int(data.pagenum)
        pagelen=int(data.pagelen)
                
        constraints=[]
        for attr,attr_val in data.iteritems():
            if attr.startswith('cnstr_') == True:
                if str(attr_val) <> "NotSelected":
                    constraints.append((attr[6:],str(attr_val)))
        
        values,colnames = ssviewer_utils.dataset_list(of,enums,pagelen=pagelen,
                                                      pagenum=pagenum,
                                                      constraints=constraints)
        
        # if rawdata flag is present just return the values list
        # row 1 is the column headings
        if data.has_key('rawdata'):
            return values
            
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        
        _values = ssviewer_utils.dataset_serialize(values,formatson=True,schema = schema)
        xml = xml_utils.grid2xml(_values)
        
        return xmltree.tostring(xml)
    
class SearchID:
    def GET(self,id):
        
        source_type="lesson"
        
        dbid = dbidlookup[id]
        
        _values = ssviewer_utils.dataset_record(of,source_type,dbid)
        
        header = "<root><parser><value>drawform</value></parser></root>"
        
        xml=xml_utils.record2xml(_values,header=header)
        
        return xmltree.tostring(xml)

class UpdateID:
    def GET(self,clsname):
        
        data = web.input()
        
        dbid = dbidlookup[data['id']]
        data.pop('id')
        
        obj = of.object_get(clsname,dbid)
        
        for attr,attr_val in data.iteritems():            
            print "for record",dbid,"update",attr,"from",getattr(obj,attr).name,"to",attr_val
            obj.keepversion=True
            obj.customtimestamp = "%y%m%d_%H%M%S"
            obj.update(attr,attr_val,dbname)
    
class Command:
    def GET(self,cmd):
        
        #data = web.input(id='')
        
        if cmd=="stop":
            print "bringing down service...."
            app.stop()
            
            #exit("stopping")

        elif cmd=="ping":
            return("ping")
        elif cmd=="stats":
            return(len(of.query('lesson')))
        
        
class SearchCriteria:
    def GET(self,id):
        
        data = web.input(id='')
        
        pagenum=1;
        pagelen=10000;
        
        constraints=[]
        for attr,attr_val in data.iteritems():
            if attr.startswith('cnstr_') == True:
                if str(attr_val) <> "NotSelected":
                    constraints.append((attr[6:],str(attr_val)))
        
        ids,colnames = ssviewer_utils.dataset_list(of,enums,pagelen=pagelen,
                                                      pagenum=pagenum,
                                                      constraints=constraints,
                                                      columns=['id'])
        
        if len(ids) < 20:
            root = xmltree.Element('root')
        
            for i in range(1,len(ids)):
                
                source_type="lesson"
                
                dbid = dbidlookup[ids[i][0]]
            
                _values = ssviewer_utils.dataset_record(of,source_type,dbid)
                
                xml_utils.record2xml(_values,root=root,name='record')
            
        
            header = "<root><parser><value>drawmultirecordform</value></parser></root>"
            xml = xml_utils._addxmlheader(root,header)
            
            print xmltree.tostring(xml)
            
            return xmltree.tostring(xml)
        
def mutex_processor():
    mutex = Lock()
    
    def processor_func(handle):
        mutex.acquire()
        try:
            return handle()
        finally:
            mutex.release()
    return processor_func

def _run(port,**xtraargs):
    
    print "launching service... pid=",os.getpid()
    
    _dbname,refdbname = sswizard_utils.getdatabase()

    globals()['dbname'] = _dbname

    urls = (
        '/(\w+)', 'Student',
        '/student/(\w+)', 'Student',
        '/subject/(\w+)', 'Subject',
        '/adult/(\w+)', 'Adult',
        '/list/(\w+)', 'List',
        '/id/(\w+)', 'SearchID',
        '/criteria/(\w+)', 'SearchCriteria',
        '/add/(\w+)', 'Add',
        '/new/(\w+)', 'New',
        '/command/(\w+)','Command',
        '/update/(\w+)','UpdateID'
    )
    
    globals()['database'] = Database(dbname)
    refdatabase = Database(refdbname)
    #of = ObjFactory(True)
    #enums = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
    
    
    globals()['of'] = ObjFactory(True)
    globals()['enums'] = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
    globals()['prepmap'] = sswizard_utils._loadprepmapper(database)
    
    args = dict(database=database,refdatabase=refdatabase,
                saveversion=1,of=of,enums=enums)

    if xtraargs<>{}:
        for k,v in xtraargs.iteritems():
            args[k] = v
            
    ssviewer_utils.dataset_load(**args)

    # get a mapping of userobjid to db refid (__id) as of uses the former to index but the web page
    # uses __id as they are easier to pass in URL
    with database:
        globals()['dbidlookup'] = sswizard_query_utils._dbid2userdefid(database,asdict=True)

    #app = web.application(urls, locals())
    globals()['app'] = web.application(urls, globals())
    #globals()['app'].add_processor(mutex_processor())
    
    sys.argv.append(str(port))    
    app.run()
    
def run(port=8080,**xtraargs):
    pid = os.fork()
    
    if pid==0:
        _run(port,**xtraargs)
    
if __name__ == "__main__":
    
    #run(dict(source='56n,4n,4s,5s,6s'))

    args={}
    try:
        if sys.argv[1] == "--allow-unknown":
            args['unknown'] = 'Y'
            sys.argv.pop(1)
    except:
        pass
    
    run(**args)
    
    '''dbname,refdbname = sswizard_utils.getdatabase()

    urls = (
        #'/(.*)', 'student','subject','adult','period','dow'
        '/(\w+)', 'Student',
        '/student/(\w+)', 'Student',
        '/subject/(\w+)', 'Subject',
        '/adult/(\w+)', 'Adult',
        '/list/(\w+)', 'List',
        '/id/(\w+)', 'SearchID',
        '/criteria/(\w+)', 'SearchCriteria',
        '/new/', 'New',
        '/command/(\w+)','Command'
    )
    
    
    database = Database(dbname)
    refdatabase = Database(refdbname)
    of = ObjFactory(True)
    enums = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
    
    #args = dict(database=database,refdatabase=refdatabase,saveversion=1,of=of,enums=enums,source='56n,4n,4s,5s,6s')
    args = dict(database=database,refdatabase=refdatabase,saveversion=1,of=of,enums=enums)

    
    ssviewer_utils.dataset_load(**args)

    # get a mapping of userobjid to db refid (__id) as of uses the former to index but the web page
    # uses __id as they are easier to pass in URL
    with database:
        dbidlookup = sswizard_query_utils._dbid2userdefid(database,asdict=True)

    app = web.application(urls, locals())
    app.run()'''
