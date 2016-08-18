from lxml import etree

__all__ = ['students_get_from_html','htmlschedule_parse','htmlschedule_slice']

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

    '''students = students_get_from_html(htmldoc)'''
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
        
    return schedule

def htmlschedule_slice(filename,num_days=-1,num_periods=-1,num_students=-1):
    ''' -1 means return all '''
    
    schedule = htmlschedule_parse(filename)
    
    if num_days == -1:
        num_days = 5
    if num_periods == -1:
        num_periods = 10
    if num_students == -1:
        num_students = len(schedule)
    
    _schedule_slice = []
    
    _slice=[]
    for student in range(num_students):
        _student=[]
        for period in range(1,num_periods+1):
            _period=[]
            for day in range(2,num_days+2):
                lesson = schedule[student][period][day]
                #if lesson == 'SS':
                #    lesson = 'Social Studies'
                if lesson.find('SS:') == 0:
                    lesson = 'Social Studies'+lesson[3:]
                if lesson.find('SS') == 0:
                    lesson = 'Social Studies'+lesson[2:]
                    
                if lesson.find('Social S') == 0 and lesson[8:14] <> 'tudies':
                    lesson = lesson.replace('Social S','Social Studies')
                
                lesson = lesson.replace('Francisco','Fran')
                
                lesson = lesson.replace('Lunch Computer Time','LCT')
                lesson = lesson.replace('Computer Time','End Computer Time')
                lesson = lesson.replace('LCT','Lunch Computer Time')
                _period.append(lesson)
            _student.append(_period)
        _slice.append(_student)
        
    return(_slice)
                