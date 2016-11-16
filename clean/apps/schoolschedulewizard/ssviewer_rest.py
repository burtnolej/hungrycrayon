
import web
import xml_utils
#from ssviewer_headless import SSViewer
from misc_utils_objectfactory import ObjFactory
import xml.etree.ElementTree as xmltree
from database_util import Database, tbl_create
import ssviewer_utils
import sswizard_utils
import sswizard_query_utils

urls = (
    #'/(.*)', 'student','subject','adult','period','dow'
    '/(\w+)', 'Student',
    '/student/(\w+)', 'Student',
    '/subject/(\w+)', 'Subject',
    '/adult/(\w+)', 'Adult',
    '/list/(\w+)', 'List',
    '/id/(\w+)', 'RefID'
)
    
app = web.application(urls, globals())

dbname='test_ssloader'
refdbname='test_ssloader'

database = Database(dbname)
refdatabase = Database(refdbname)
of = ObjFactory(True)
enums = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)

args = dict(database=database,refdatabase=refdatabase,saveversion=1,of=of,enums=enums)

ssviewer_utils.dataset_load(**args)

# get a mapping of userobjid to db refid (__id) as of uses the former to index but the web page
# uses __id as they are easier to pass in URL
with database:
    dbidlookup = sswizard_query_utils._dbid2userdefid(database,asdict=True)

class Student:
    def GET(self,id):
        
        source_type="student"
        source_value=id
        
        if source_value=="all": source_value=""
        
        data = web.input(id='')

        ztypes=data.ztypes.split(",")
        xaxis=data.xaxis
        yaxis=data.yaxis
        
        values = ssviewer_utils.dataset_pivot(of,enums,yaxis,xaxis,ztypes, source_type,source_value,formatson=True)
        grid = ssviewer_utils.dataset_serialize(values,formatson=True,schema = dict(xaxis=xaxis,yaxis=yaxis,ztypes=ztypes))
        xml = xml_utils.grid2xml(grid,shrinkfont=5)
        
        return xmltree.tostring(xml)
    
class Subject:
    #def GET(self,id):
    def GET(self,id):
        
        #data = web.input(id='')

        #id = int(id)
        
        id = "foobar"
        
        return '<root><row id="1"><cell id="1.1"><value>' + id + '</value></row></root>'
    
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
        xml = xml_utils.grid2xml(grid,shrinkfont=5)
        return xmltree.tostring(xml)
    
class List:
    def GET(self,objtype):
        data = web.input(id='')

        pagenum=int(data.pagenum)
        pagelen=int(data.pagelen)
        
        values,colnames = ssviewer_utils.dataset_list(of,enums,pagelen=pagelen,pagenum=pagenum)
        
        schema = dict(xaxis='row',yaxis='col',colnames=list(colnames))
        
        _values = ssviewer_utils.dataset_serialize(values,formatson=True,schema = schema)
        xml = xml_utils.grid2xml(_values)
        
        return xmltree.tostring(xml)
    
class RefID:
    def GET(self,id):
        
        source_type="lesson"
        
        dbid = dbidlookup[id]
        
        _values = ssviewer_utils.dataset_record(of,source_type,dbid)
        
        header = "<root><parser><value>drawform</value></parser></root>"
        
        xml=xml_utils.record2xml(_values,header=header)
        
        print source_type,dbid,_values, xmltree.tostring(xml)
        
        return xmltree.tostring(xml)
    
        #xml = "<root><parser><value>drawform</value></parser><item><valuetype>period</valuetype><value>830-910</value></item><item><valuetype>dow</valuetype><value>MO</value></item></root>"
    
        #return(xml)
        
if __name__ == "__main__":
    import os
    app.run()
