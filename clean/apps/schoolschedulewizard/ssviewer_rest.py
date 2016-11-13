
import web
import xml_utils
#from ssviewer_headless import SSViewer
from misc_utils_objectfactory import ObjFactory
import xml.etree.ElementTree as xmltree
from database_util import Database, tbl_create
import ssviewer_utils
import sswizard_utils

urls = (
    '/(.*)', 'page'
)
app = web.application(urls, globals())

#ssviewer = SSViewer('test_ssloader','test_ssloader')

dbname='test_ssloader'
refdbname='test_ssloader'

database = Database(dbname)
refdatabase = Database(refdbname)
of = ObjFactory(True)
enums = sswizard_utils.setenums(dow="all",prep=-1,database=refdatabase)

args = dict(database=database,refdatabase=refdatabase,saveversion=1,of=of,enums=enums)
#ssviewer.load(**args)

ssviewer_utils.dataset_load(**args)

class page(object):
    def GET(self,name):
        
        data = web.input(id='')

        ztypes=data.ztypes.split(",")
        source_type=data.source_type
        source_value=data.source_value
        xaxis=data.xaxis
        yaxis=data.yaxis
        
        values = ssviewer_utils.dataset_pivot(of,enums,yaxis,xaxis,ztypes, source_type,source_value,formatson=True)
        
        print values
        grid = ssviewer_utils.dataset_serialize(values,formatson=True)
        
        #grid = ssviewer.viewer(xaxis,yaxis,ztypes,source_type,source_value,formatson=True)
        xml = xml_utils.grid2xml(grid)
        return xmltree.tostring(xml)
        
if __name__ == "__main__":
    import os
    app.run()
