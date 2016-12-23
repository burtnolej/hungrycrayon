import os
import ssviewer_rest_utils  
import xml.etree.ElementTree as xmltree
from time import sleep

#curl --get -d "ztypes=subject;xaxis=period;yaxis=dow;dow=MO" http://0.0.0.0:8080/student/Clayton
#curl --get http://0.0.0.0:8080/update/lesson?id=054C4D26\&subject=doodah
#curl --get http://0.0.0.0:8080/command/stop
#curl --get -d "pagenum=1;pagelen=20;rawdata=True" http://0.0.0.0:8080/list/lesson

APPROOT = os.environ['APPROOT']

restservice = ssviewer_rest_utils.RestService("http://0.0.0.0:8080/",
                                              "ssviewer_rest",
                                              os.path.join(APPROOT,"clean","apps","schoolschedulewizard"),
                                              "test_ssviewer_service.sqlite",
                                              keepversion=True,unknown='Y')

with restservice:
    
    URL =  "http://0.0.0.0:8080/"
    
    # get student pivot data
    buf = ssviewer_rest_utils.restquery(URL + "student/Clayton",xaxis="period",
                         yaxis="dow",ztypes="subject",source_type="student",
                         source_value="Clayton")
    
    
    try: # avoid spurious error due to threading problem when service is stopped
        tree = xmltree.fromstring(buf) 
    except xmltree.ParseError:
        pass
    
    try: # avoid spurious error due to threading problem when service is stopped
        for element in tree.findall(".//value"):
            print element.text
    except NameError:
        pass
    
    
    # update and id
    #print ssviewer_rest_utils.restquery(URL + "update/lesson",subject="doodah",id="046CE5DA"))
    
    # list
    #print ssviewer_rest_utils.restquery(URL + "list/lesson",pagenum=1,pagelen=20,rawdata=True)
    
    # stats
    #print ssviewer_rest_utils.restquery(URL + "command/stats")
