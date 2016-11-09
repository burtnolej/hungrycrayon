
import web
import xml_utils
from ssviewer_headless import SSViewer
from misc_utils_objectfactory import ObjFactory
import xml.etree.ElementTree as xmltree

urls = (
    '/(.*)', 'page'
)
app = web.application(urls, globals())

ssviewer = SSViewer('test_ssloader','test_ssloader')

args = dict(saveversion=1)
print "loading with args=",args,
ssviewer.load(**args)
print "done"

class page(object):
    def GET(self,name):
        
        data = web.input(id='')

        ztypes=data.ztypes.split(",")
        source_type=data.source_type
        source_value=data.source_value
        xaxis=data.xaxis
        yaxis=data.yaxis
        
        grid = ssviewer.viewer(xaxis,yaxis,ztypes,source_type,source_value,formatson=True)
        xml = xml_utils.grid2xml(grid)
        return xmltree.tostring(xml)
        
if __name__ == "__main__":
    import os
    app.run()
