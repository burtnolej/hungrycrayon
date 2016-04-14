#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import requests
import re
import sys
from collections import OrderedDict
sys.path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import get_log_handle
from error_util import Notification, MyException, MyAlert, MyComment

class URLSearchStringAlert(MyAlert):
    pass

class URLFindallLenAlert(MyAlert):
    pass

class URLFindall0LenAlert(MyAlert):
    pass

class URLDataItems(list):
    def get_url(self,url):
        self.doc = requests.get(url).text
        self._stdout = sys.stdout
        #sys.stdout = get_log_handle("/tmp/output.htm")
        #print self.bs_prettify()
        #sys.stdout = self._stdout
        
    def bs_prettify(self):
        bs = BeautifulSoup(self.doc)
        print bs.prettify()

    def pprint(self,count=100):
        i=0
        for res in self:
            if i>=count:
                return
            else:
                for key,value in res.iteritems():
                    print key.ljust(15), value
                print 
            i+=1

    def search_for_tag(self,tag,item,regex,dataitem,text):
        re_str =  "<"
        re_str += tag
        if item != "":
            re_str += " "
            re_str += item
            re_str += r"\""
            re_str += dataitem
            re_str += r"\""
        elif regex != "":
            re_str += regex
        re_str += ">"
        re_str += "(.*?)<\/"
        re_str += tag
        re_str +=">"


        r = re.compile(re_str)
        res = r.findall("".join(m for m in text))
        return(res)

    def scrape(self,dataitems,seed):
        i=1
        for para in self.doc:
            # remove any unwanted chrs/strs
            para = re.sub("\&amp","",para)

            res = {}

            for dataitem,match_method in dataitems.iteritems():
                mypara = para # create a local cp
                for tag,item,regex in match_method:
                    mypara = self.search_for_tag(tag,item,regex,dataitem,mypara)
                if not len(mypara) < 2:
                    Notification.myraise(URLFindallLenAlert(seed))
                elif len(mypara) == 0:
                    res.__setitem__(dataitem,"")
                    #Notification.myraise(URLFindall0LenAlert(seed))
                else:
                    res.__setitem__(dataitem,str(mypara[0].lstrip().rstrip()))

            res.__setitem__('result_count',i) # keep track of order/priority of results
            i+=1
            
            try:
                if res.__getitem__('offscreen')[0] != 'Search':
                    self.append(res)
            except:
                Notification.myraise(URLSearchStringAlert(seed))

if __name__ == '__main__':
    
    class YellDataItems(URLDataItems):
        def __init__(self,cpy,loc):
            self.get_url(self._gen_url(cpy,loc))
            # modify _doc
            self.doc = self.doc.split("<div class=\"parentListing\"")
        
        def _gen_url(self,cpy,loc):
            url = "http://www.yell.com/ucs/UcsSearchAction.do?keywords="
            url += cpy
            url += "&location="
            url += loc
            url += "&scrambleSeed=58471740&searchType=&M=&bandedclarifyResults=&ssm=1"
            return(url)

    cpy = sys.argv[1]
    loc = sys.argv[2]

    d = OrderedDict({'offscreen':[('span','class=','')],
                     'streetAddress':[('span','itemprop=','')],
                     'addressLocality':[('span','itemprop=',''),
                                        ('strong','','')],
                     'addressLocality':[('span','itemprop=',''),
                                        ('strong','','')],

                     'postalCode':[('span','itemprop=','')],
                     'keywords':[('div','class=',''),
                                 ('p','',''),
                                 ('strong','','')],
                     'keywords snippet':[('div','class=',''),
                                 ('p','',''),
                                 ('a','','[^>]*')]})

    yd = YellDataItems(cpy,loc)
    yd.scrape(d)
    yd.pprint()

