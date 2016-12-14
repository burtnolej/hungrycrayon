import sys
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

from inspect import getmembers

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
        
        print ztypes
        print xmltree.tostring(xml)

        return xmltree.tostring(xml)
    
class New:
    def GET(self):
        
        print web.input(id='')
    
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
        
        
if __name__ == "__main__":
        
    dbname,refdbname = sswizard_utils.getdatabase()
    
    '''
    DBPATH = os.environ['DBPATH']
    DBNAME = os.environ['DBNAME']

    if DBNAME <> "":
        dbname=os.path.join(DBPATH,DBNAME)
        refdbname=os.path.join(DBPATH,DBNAME)
    elif len(sys.argv) == 2:
        dbname=os.path.join(DBPATH,sys.argv[1])
        refdbname=os.path.join(DBPATH,sys.argv[1])
        sys.argv.pop(1)
    else:
        raise Exception("provide a database name on cndline or set $DBNAME/$DBPATH")
        
    '''

    urls = (
        #'/(.*)', 'student','subject','adult','period','dow'
        '/(\w+)', 'Student',
        '/student/(\w+)', 'Student',
        '/subject/(\w+)', 'Subject',
        '/adult/(\w+)', 'Adult',
        '/list/(\w+)', 'List',
        '/id/(\w+)', 'SearchID',
        '/criteria/(\w+)', 'SearchCriteria',
        '/new/', 'New'
    )
    
    
    database = Database(dbname)
    refdatabase = Database(refdbname)
    of = ObjFactory(True)
    enums = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
    
    args = dict(database=database,refdatabase=refdatabase,saveversion=1,of=of,enums=enums,source='56n,4n,4s,5s,6s')
    
    ssviewer_utils.dataset_load(**args)

    # get a mapping of userobjid to db refid (__id) as of uses the former to index but the web page
    # uses __id as they are easier to pass in URL
    with database:
        dbidlookup = sswizard_query_utils._dbid2userdefid(database,asdict=True)

    app = web.application(urls, locals())
    app.run()
