#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import requests
import re
import sys
from collections import OrderedDict
sys.path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import get_log_handle

class YellDataitems(list):
    def __init__(self,cpy,loc):
        self._gen_url(cpy,loc)
        self._text = requests.get(self._url).text
        self._doc = self._text.split("<div class=\"parentListing\"")
        
    def bs_prettify(self):
        bs = BeautifulSoup(self._text)
        print bs.prettify()

    def _gen_url(self,cpy,loc):

        self._url = "http://www.yell.com/ucs/UcsSearchAction.do?keywords="
        self._url += cpy
        self._url += "&location="
        self._url += loc
        self._url += "&scrambleSeed=58471740&searchType=&M=&bandedclarifyResults=&ssm=1"

    def pprint(self,count=100):
        i=0
        for res in self:
            if i>=count:
                return
            else:
                for key,value in res.iteritems():
                    print key.ljust(15),
                    if value: print value[0].lstrip(),
                    print
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
        return(r.findall("".join(m for m in text)))

    def scrape(self,dataitems):
        for para in self._doc:
            # remove any unwanted chrs/strs
            para = re.sub("\&amp","",para)

            res = {}

            for dataitem,match_method in dataitems.iteritems():
                mypara = para # create a local cp
                for tag,item,regex in match_method:
                    mypara = self.search_for_tag(tag,item,regex,dataitem,mypara)
                res.__setitem__(dataitem,mypara)
                
            if res.__getitem__('offscreen')[0] != 'Search':
                self.append(res)

if __name__ == '__main__':

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

    

    yd = YellDataitems(cpy,loc)
    yd.scrape(d)
    yd.pprint()

    sys.stdout = get_log_handle("./yell.htm")
    print yd.bs_prettify()
