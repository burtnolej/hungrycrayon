
import web
import xml_utils
#from ssviewer_headless import SSViewer
from misc_utils_objectfactory import ObjFactory
import xml.etree.ElementTree as xmltree
from database_util import Database, tbl_create
import ssviewer_utils
import sswizard_utils

urls = (
    #'/(.*)', 'student','subject','adult','period','dow'
    '/(\w+)', 'Student',
    '/student/(\w+)', 'Student',
    '/subject/(\w+)', 'Subject',
    '/adult/(\w+)', 'Adult'
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

class Student:
    def GET(self,id):
        
        source_type="student"
        source_value=id

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
    
if __name__ == "__main__":
    import os
    app.run()
