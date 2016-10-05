import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

__all__ = ['_execfunc','_rowheaderexecfunc','_columnheaderexecfunc','_dowexecfunc']

def _dowexecfunc(database,value,prep,*args):
    exec_str = "select code from dow "
    return(tbl_query(database,exec_str))

def _colorexecfunc(database,value):
    exec_str = "select rgb from {0} ".format(value)
    return(tbl_query(database,exec_str))

def _execfunc(database,value,prep,dow):
    exec_str = "select s.code "
    exec_str += "from session as s,adult as a "
    #exec_str += "where a.prep = {0} and ".format(prep)
    exec_str += "where s.prep = {0} and ".format(prep)
    exec_str += "a.name = s.teacher and "
    exec_str += "s.period = {0} and ".format(value)
    #exec_str += "s.day = \"{0}\"".format(dow)
    exec_str += "s.dow = \"{0}\"".format(dow)
    
    return(tbl_query(database,exec_str))

def _rowheaderexecfunc(database):
    exec_str = "select name from period"
    return(tbl_query(database,exec_str))

def _columnheaderexecfunc(database,pred=None,predvalue=None):
    exec_str = "select name from student"
    if pred <> None:
        exec_str = exec_str + " where {0} = {1}".format(pred,predvalue)
    return(tbl_query(database,exec_str))

def _pivotexecfunc(database,ycoltype,xcoltype,tblname,prep):
    
    headers = {}
    with database:
        for hdrtype in [ycoltype,xcoltype]:        
            _,headers[hdrtype],_ =  tbl_query(database,"select distinct({0}) from {1}".format(hdrtype,tblname))
            headers[hdrtype] = [_hdrtype[0] for _hdrtype in headers[hdrtype]]

    resulttable = []
    resulttable.append([""] + headers[ycoltype])
    with database:
        for xaxishdr in headers[xcoltype]:
            row=[]
            row.append(xaxishdr)
            for yaxishdr in headers[ycoltype]:
                exec_str = "select count(*) from {0} ".format(tblname)
                exec_str += "where {1} = {0} ".format("\""+str(yaxishdr)+"\"",ycoltype)
                exec_str += " and {1} = {0} ".format("\""+str(xaxishdr)+"\"",xcoltype)                
                
                _,results,_ = tbl_query(database,exec_str)
                try:
                    row.append(results[0][0])
                except:
                    row.append(0)
            resulttable.append(row)
            
    row=[""]      
    with database:
        for yaxishdr in headers[ycoltype]:
            exec_str = "select count(*) from {0} ".format(tblname)
            exec_str += "where {1} = {0} ".format("\""+str(yaxishdr)+"\"",ycoltype)                
            
            _,results,_ = tbl_query(database,exec_str)
            try:
                row.append(results[0][0])
            except:
                row.append(0)
    resulttable.append(row)
    
    return resulttable

if __name__ == "__main__":
    
    from pprint import pprint
    
    database = Database('quadref')
    with database:
        coldefn,values = _execfunc(database,6,5)
        
    pprint(values)
    
