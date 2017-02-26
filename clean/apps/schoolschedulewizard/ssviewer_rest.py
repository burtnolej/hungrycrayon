import sys
import os
from misc_utils_log import Log, logger, thisfuncname
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
from copy import deepcopy
from inspect import getmembers
from threading import Lock
from copy import deepcopy

import os
import os.path


class Add:
    def GET(self,objtype):
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')
        
        _dm = web.input()
        
        datamembers = dict(zip(_dm.keys(),_dm.values()))  
        
        # these are not required to build the new record and
        # the service takes ALL members of datamembers and adds them to
        # the new message payload
        try:
            datamembers.pop('page_status')
            datamembers.pop('source_type')
            datamembers.pop('source_value')
        except:
            pass

        try:
            newobj = ssviewer_utils.dataset_add(database,database,of,enums,prepmap,
                                            datamembers,objtype,keepversion=True)
        except ssviewer_utils.OFDuplicateRecord:
            return "-1"
        
        header = "<root><parser><value>drawform</value></parser></root>"
        
        if hasattr(newobj.userobjid,"name"):
            _userobjid = newobj.userobjid.name
        else:
            _userobjid = newobj.userobjid
            
        if hasattr(newobj.objtype,"name"):
            _objtype = newobj.objtype.name
        else:
            _objtype = newobj.objtype

        return "id="+_userobjid+","+",".join([k + "=" + _dm[k] for k in _dm.keys()])
    
        #values =dict(objtype =_objtype,userobjid=_userobjid)
        
        #xml=xml_utils.record2xml(_values,header=header)
        
        #globals()['dbidlookup'][newobj.id] = _userobjid
        #print "added to dbid",newobj.id,_userobjid
        
        #return xmltree.tostring(xml)
    
        
class New:
    def GET(self,objtype):
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')
                
        _values = ssviewer_utils.dataset_new(objtype)
        
        if objtype == "lesson":
            # lessson record can only be created from defined values (those specified in the individual ref tables
            header = "<root><parser><value>drawform</value></parser></root>"
        else:
            # a new on any other record is to create new defined values for lesson
            header = "<root><parser><value>drawentryform</value></parser></root>"
            
        xml=xml_utils.record2xml(_values,header=header)
        
        print xmltree.tostring(xml)
        return xmltree.tostring(xml)
    
def _pivot(data,source_type,source_value):

    if source_value=="all": source_value=""
    
    if hasattr(data,'ztypes') == False:
        ztypes = ['subject','adult']
    else:
        ztypes = data.ztypes.split(",")
    
    if len(ztypes) == 0:
        return "-1"
        
    formatson=False
    header=None
    
    if "formats" in ztypes: 
        formatson=True
    else:            
        header = "<root><parser><value>drawnoformatgrid</value></parser></root>"
        
    if "count" in ztypes: 
        ztypes=["*"]

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
    
class Student:
    def GET(self,id):
        
        data = web.input(id='')
        source_type="student"
        source_value=id
        return (_pivot(data,source_type,source_value))
    
class Subject:
    def GET(self,id):
        
        source_type="subject"
        source_value=id        
        data = web.input(id='')
        return (_pivot(data,source_type,source_value))

class Adult:
    def GET(self,id):
        
        source_type="adult"
        source_value=id
        data = web.input(id='')
        return (_pivot(data,source_type,source_value))

class Schema:
    def GET(self,objtype):
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')
        
        source_objs = of.query_advanced(objtype,[])
        colnames = list(source_objs[0].dm.keys())
        return ",".join(colnames)
       
class Refdata:
    def GET(self,objtype):

        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')
        
        reftree = ssviewer_utils.dataset_refdata(globals()['database'])
        
        #xml = xml_utils.tree2xml(reftree)
        
        xml = xml_utils.tree2xml(reftree,tag="refitem")
        
        return xmltree.tostring(xml)
    
class List:
    def GET(self,objtype):
        
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')
        
        data = web.input(id='')

        pagenum=int(data.pagenum)
        pagelen=int(data.pagelen)
                
        constraints=[]
        for attr,attr_val in data.iteritems():
            if attr.startswith('cnstr_') == True:
                if str(attr_val) <> "NotSelected":
                    constraints.append((attr[6:],str(attr_val)))
                
        columns=[]
        if hasattr(data,'ztypes'):
            columns = data.ztypes.split(",")
        
        
        values,colnames = ssviewer_utils.dataset_list(of,enums,objtype,pagelen=pagelen,
                                                      pagenum=pagenum,
                                                      constraints=constraints,
                                                      columns=columns)
        
        # if rawdata flag is present just return the values list
        # row 1 is the column headings
        if data.has_key('rawdata'):
            return values
            
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))

        
        _values = ssviewer_utils.dataset_serialize(values,formatson=True,schema = schema)
        xml = xml_utils.grid2xml(_values)
        
        return xmltree.tostring(xml)
    
class Load:
    def GET(self,objtype):
        data = web.input()
        
        args = dict(database=database,refdatabase=database,
                    objtype=str(objtype),of=of,saveversion=1,unknown='N',
                    keepversion=False)
        
        whereclause=[]
        for attr,attr_val in data.iteritems():
            whereclause.append([attr,"=",attr_val])
            
        print whereclause
        args['whereclause'] = whereclause
        
        ssviewer_utils.dataset_loadref(**args)  
        
class SearchID:
    def GET(self,id):
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')

        source_type="lesson"
        
        dbid = dbidlookup[id]
        
        _values = deepcopy(ssviewer_utils.dataset_record(of,source_type,dbid))
        
        header = "<root><parser><value>drawform</value></parser></root>"
        
        # only allow editing of adult,period,dow,recordtype,student,subject
        
        for k in list(_values.keys()):
            if k not in ['adult','period','dow','recordtype','student','subject']:
                _values.pop(k)
        
            
        # get values for this particular record        
        xml=xml_utils.record2xml(_values,header=header)

        # get refdata in case the UI wants to build selects
        reftree = ssviewer_utils.dataset_refdata(globals()['database'])
        refxml = xml_utils.tree2xml(reftree,xml,"refitem")

        return xmltree.tostring(refxml)

def _update(obj,_value_changes):
    
    value_changes = {}
    
    for i in range(0,len(_value_changes),2):
        value_changes[_value_changes[i]] = _value_changes[i+1]
        
    for attr,attr_val in value_changes.iteritems():
        
        obj.keepversion=True
        obj.customtimestamp = "%y%m%d_%H%M%S"
        
        
        newid = obj.update(of,attr,attr_val,dbname)
        
        
        if attr == "teacher": attr = "adult"
        
        logstr = "for record "+ str(obj.objid) + " updating " + str(attr)," from " + str(getattr(obj,attr).name) + " to " + str(attr_val)
        log.log(thisfuncname(),3,msg=logstr)
            
    return newid    
    
class UpdateUID:
    
    def GET(self,id):
        
        data = web.input()
        
        obj = of.object_get('lesson',id)
        
        newid = _update(obj,data['value_changes'].split(","))
        
        if newid <> -1:
            globals()['dbidlookup'][newid] = id
            globals()['dbidlookup'].pop(obj.id)
            log.log(thisfuncname(),3,msg=str(dbid) + " updated")
        else:
            log.log(thisfuncname(),2,msg="value to update to is not found",value=attr_val)
            
        return newid
    
class UpdateID:
    
    #lets pass in the id as a param; clsname not necessar
    #probably need an object_get that does not need clsname
    
    #def GET(self,clsname):
    def GET(self,id):
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')
        
        data = web.input()
        
        dbid = dbidlookup[id]
        
        obj = of.object_get('lesson',dbid)
        
        ssviewer_utils._lesson_change(obj,delete=True)
        newid = _update(obj,data['value_changes'].split(","))
        ssviewer_utils._lesson_change(obj)
        
        if newid <> -1:
            globals()['dbidlookup'][newid] = dbid
            globals()['dbidlookup'].pop(id)
            log.log(thisfuncname(),3,msg=str(dbid) + " updated")
        else:
            log.log(thisfuncname(),2,msg="value to update to is not found",value=data['value_changes'])
    
        if hasattr(obj.userobjid,"name"):
            _userobjid = obj.userobjid.name
        else:
            _userobjid = obj.userobjid
        
        return "id="+_userobjid+",value_changes="+data['value_changes']

        
class Command:
    def GET(self,cmd):
        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Credientials','true')

        if cmd=="stop":
            print "bringing down service...."
            app.stop()
        elif cmd=="ping":
            return("ping")
        elif cmd=="stats":
            return(len(of.query('lesson')))
        elif cmd=="config":
            return(len(of.query('lesson')))
        elif cmd=="reload":
            
            data = web.input()
            
            xtraargs={}
            for attr,attr_val in data.iteritems():
                xtraargs[attr] = attr_val
    
            #globals()['dbname'] = _dbname
            globals()['database'] = Database(globals()['dbname'])
            refdatabase = globals()['database']

            globals()['of'] = ObjFactory(True)
            globals()['enums'] = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
            globals()['prepmap'] = sswizard_utils._loadprepmapper(database)
             
            args = dict(database=database,refdatabase=refdatabase,
                         saveversion=1,of=of,enums=enums,keepversion=True)
         
            if xtraargs<>{}:
                for k,v in xtraargs.iteritems():
                    args[k] = v
                     
            ssviewer_utils.dataset_load(**args)
         
            logstr = "reloading " + globals()['dbname']
            log.log(thisfuncname(),3,msg=logstr)            

            # get a mapping of userobjid to db refid (__id) as of uses the former to index but the web page
            # uses __id as they are easier to pass in URL
            with database:
                globals()['dbidlookup'] = sswizard_query_utils._dbid2userdefid(database,asdict=True)
            
        elif cmd=="dump":
            
            data = web.input()
            

            #objtypes = data['objtypes'].split(",")
            #fields = data['fields'].split(",")
            #pprint = data['pprint'].split(",")
            
            
            listfields = ['objtypes','omitfields','fields']
            dictfields = ['constraints']
            boolfields = ['fieldnames','objref']
            urldict = {}
            
            for field in listfields:
                try:
                    urldict[field] = data[field].split(",")
                except:
                    pass
                
            for field in boolfields:
                urldict[field] = False
                try:
                    if data[field] == "1":
                        urldict[field] = True
                        print field
                except:
                    pass
                
            for field in dictfields:
                try:
                    _urldict = {}
                    for nvp in data[field].split(","):
                        k,v = nvp.split("=")
                        _urldict[k]=v

                    urldict[field] = _urldict
                except:
                    pass
                
            if data.has_key('pprint'):
                if data['pprint']=="0":
                    pprint=False
                else:
                    pprint=True

            results = of.dumpobjrpt(**urldict)
            
            if data.has_key('count'):
                if data['count']=="0":
                    return(len(results))
                
            css = "body { width:3000px;}"
            css += "table { border: 1px solid #f00;}"
            css += "td {border: 1px solid #000;word-wrap:break-word;}"
           
            if pprint == True:
                #_o_str = "<html><style>"+css+"</style><body><table>"
                _o_str = "<table>"

                for _output in results:
                    _o_str = _o_str + "<tr>"
                    for _o in _output:
                        _o_str+="<td>"+str(_o)+"</td>"
                        #.ljust(15)[:15]
                    _o_str += "</tr>"
                #return _o_str+"</table></body></html>"
                return _o_str+"</table>"
            else:
                return(results)

        
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
        '/load/(\w+)', 'Load',
        '/schema/(\w+)', 'Schema',
        '/id/(\w+)', 'SearchID',
        '/criteria/(\w+)', 'SearchCriteria',
        '/add/(\w+)', 'Add',
        '/new/(\w+)', 'New',
        '/command/(\w+)','Command',
        '/update/(\w+)','UpdateID',
        '/updateuid/(\w+)','UpdateUID',
        '/refdata/(\w+)','Refdata'
    )
    
    globals()['database'] = Database(dbname)
    refdatabase = Database(refdbname)
    #of = ObjFactory(True)
    #enums = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
    
    globals()['of'] = ObjFactory(True)
    globals()['enums'] = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)
    globals()['prepmap'] = sswizard_utils._loadprepmapper(database)
    
    args = dict(database=database,refdatabase=refdatabase,
                saveversion=1,of=of,enums=enums,keepversion=True)

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
        if sys.argv[1] == "--custom-source":
            args['source'] = sys.argv[2]
            sys.argv.pop(1)
            sys.argv.pop(1)
    except:
        pass
    
    #args['source'] = '56m'
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
