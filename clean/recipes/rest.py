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

#grid = [[dict(A=1,B=2)],[dict(C=3,D=4)]]
#xml = xml_utils.grid2xml(grid)
#xmlstr = xml_utils.xml2string(xml)

xmlstr= "<root><row id='1'><cell id='1.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id='1.2'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>??</value></cell><cell id='1.3'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Karolina</value></cell><cell id='1.4'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Paraic</value></cell><cell id='1.5'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Issey</value></cell><cell id='1.6'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>[Paraic,Rahul]</value></cell><cell id='1.7'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Amelia</value></cell></row><row id='2'><cell id='2.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id='2.2' /><cell id='2.3' /><cell id='2.4' /><cell id='2.5' /><cell id='2.6' /><cell id='2.7'><subrow id='2.7.1'><subcell id='2.7.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='2.7.1.2'><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row><row id='3'><cell id='3.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>910-950</value></cell><cell id='3.2'><subrow id='3.2.1'><subcell id='3.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='3.2.1.2'><bgcolor>#666600</bgcolor><fgcolor>#ffffff</fgcolor><value>Core</value></subcell></subrow></cell><cell id='3.3' /><cell id='3.4' /><cell id='3.5' /><cell id='3.6' /><cell id='3.7' /></row><row id='4'><cell id='4.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>950-1030</value></cell><cell id='4.2' /><cell id='4.3' /><cell id='4.4'><subrow id='4.4.1'><subcell id='4.4.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='4.4.1.2'><bgcolor>#006600</bgcolor><fgcolor>#ffffff</fgcolor><value>Science</value></subcell></subrow></cell><cell id='4.5' /><cell id='4.6' /><cell id='4.7' /></row><row id='5'><cell id='5.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1030-1110</value></cell><cell id='5.2' /><cell id='5.3' /><cell id='5.4' /><cell id='5.5'><subrow id='5.5.1'><subcell id='5.5.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='5.5.1.2'><bgcolor>#ff99cc</bgcolor><fgcolor>#ffffff</fgcolor><value>History</value></subcell></subrow></cell><cell id='5.6' /><cell id='5.7' /></row><row id='6'><cell id='6.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1110-1210</value></cell><cell id='6.2'><subrow id='6.2.1'><subcell id='6.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='6.2.1.2'><bgcolor>#663300</bgcolor><fgcolor>#ffffff</fgcolor><value>Computer Time</value></subcell></subrow></cell><cell id='6.3' /><cell id='6.4' /><cell id='6.5' /><cell id='6.6' /><cell id='6.7' /></row><row id='7'><cell id='7.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1210-100</value></cell><cell id='7.2' /><cell id='7.3' /><cell id='7.4' /><cell id='7.5' /><cell id='7.6'><subrow id='7.6.1'><subcell id='7.6.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='7.6.1.2'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>??</value></subcell></subrow></cell><cell id='7.7' /></row><row id='8'><cell id='8.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>100-140</value></cell><cell id='8.2' /><cell id='8.3' /><cell id='8.4' /><cell id='8.5' /><cell id='8.6' /><cell id='8.7'><subrow id='8.7.1'><subcell id='8.7.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='8.7.1.2'><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row><row id='9'><cell id='9.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>140-220</value></cell><cell id='9.2' /><cell id='9.3'><subrow id='9.3.1'><subcell id='9.3.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='9.3.1.2'><bgcolor>#ccff99</bgcolor><fgcolor>#ffffff</fgcolor><value>Counseling</value></subcell></subrow></cell><cell id='9.4' /><cell id='9.5' /><cell id='9.6' /><cell id='9.7' /></row><row id='10'><cell id='10.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>220-300</value></cell><cell id='10.2'><subrow id='10.2.1'><subcell id='10.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='10.2.1.2'><bgcolor>#ff99cc</bgcolor><fgcolor>#ffffff</fgcolor><value>Movement</value></subcell></subrow></cell><cell id='10.3' /><cell id='10.4' /><cell id='10.5' /><cell id='10.6' /><cell id='10.7' /></row><row id='11'><cell id='11.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>300-330</value></cell><cell id='11.2'><subrow id='11.2.1'><subcell id='11.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='11.2.1.2'><bgcolor>#663300</bgcolor><fgcolor>#ffffff</fgcolor><value>Computer Time</value></subcell></subrow></cell><cell id='11.3' /><cell id='11.4' /><cell id='11.5' /><cell id='11.6' /><cell id='11.7' /></row></root>"

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
        return xmlstr
        #return {'message': xmlstr }
        
        
if __name__ == "__main__":
    import os
    #os.environ["PORT"] = "8008"
    app.run()
