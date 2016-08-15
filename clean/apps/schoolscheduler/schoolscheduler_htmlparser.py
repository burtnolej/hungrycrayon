from lxml import etree

__all__ = ['students_get_from_html','htmlschedule_parse']

def students_get_from_html(htmldoc):
    students=[]
    for _s in htmldoc.xpath('//body')[0].getchildren():
        
        if _s.tag == "p":
            for item in _s.iter():
                if len(item)==0:
                    if item.text <> None:
                        students.append(item.text.replace("\n",""))
    return(students)

def htmlschedule_parse(filename):
    
    data = open(filename,'r').read()
    htmldoc = etree.HTML(data)    

    students = students_get_from_html(htmldoc)
    table = [table for table in htmldoc.xpath('//table')]    
    
    schedule=[]
    for _table in table:
        row = [row for row in _table.xpath('.//tr')]
        rw=[]
        for _row in row:
            item = [item for item in _row.xpath('.//td')]   
            i =[]
            for _item in item:
                _str=""
                for part in _item.iter():
                    try:
                        _str = _str + part.text.replace("\n","").replace("\t"," ")
                    except AttributeError:
                        pass
                    
                _i = _str.split(" ")
    
                __str=""
                for __i in _i:
                    if __i <> "":
                        if _str == "":
                            _str = __i
                        else:
                            __str = __str + " " + __i
    
                i.append(__str.strip())
            rw.append(i)
        schedule.append(rw)
        
    return schedule, students