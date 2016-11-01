"""mimerender example for web.py. Run this server and then try:

    $ curl -iH "Accept: application/html" localhost:8080/x
    ...
    Content-Type: text/html
    ...
    <html><body>Hello, x!</body></html>

    $ curl -iH "Accept: application/xml" localhost:8080/x
    ...
    Content-Type: application/xml
    ...
    <message>Hello, x!</message>

    $ curl -iH "Accept: application/json" localhost:8080/x
    ...
    Content-Type: application/json
    ...
    {"message": "Hello, x!"}

    $ curl -iH "Accept: text/plain" localhost:8080/x
    ...
    Content-Type: text/plain
    ...
    Hello, x!

"""
import web
try:
    import simplejson as json
except ImportError:
    import json
import mimerender

import xml_utils

mimerender = mimerender.WebPyMimeRender()

#render_xml = lambda message: '<message>%s</message>'%message
render_xml = lambda message: xml_utils.grid_to_xml(message)
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message
urls = (
    '/(.*)', 'greet'
)
app = web.application(urls, globals())

grid = [[dict(A=1,B=2)],[dict(C=3,D=4)]]
xml = xml_utils.grid2xml(grid)
xmlstr = xml_utils.xml2string(xml)

'''class greet:
    @mimerender(
        default = 'xml',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
    )
    def GET(self, name):
        if not name: 
            name = 'world'
        #return {'message': 'Hello, ' + name + '!'}
        
        
        return {'message': grid }'''

class greet:
    def GET(self,name):
        return {'message': xmlstr }
        
        
if __name__ == "__main__":
    import os
    #os.environ["PORT"] = "8008"
    app.run()


    def test_alllist_content(self):
        
        grid = [[["A",1],["B",2]],[["C",3],["D",4]]]
        
        expected_results = "<root><row><cell><subcell>A</subcell><subcell>1</subcell></cell><cell><subcell>B</subcell><subcell>2</subcell></cell></row><row><cell><subcell>C</subcell><subcell>3</subcell></cell><cell><subcell>D</subcell><subcell>4</subcell></cell></row></root>"
        xml = grid_to_xml(grid)
         
        self.assertEqual(xmltree.tostring(xml),expected_results)