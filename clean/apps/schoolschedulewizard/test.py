


from selenium import webdriver
import os
import time

baseurl = "http://www.hungrycrayon.com"
page="dpivot.php"

args = dict(source_type = "student",source_value = "Vonda",xaxis="period",
            yaxis="dow",ztypes="subject",source="56newworkp",
            cnstr_subject="NotSelected",cnstr_dow="NotSelected",cnstr_period="NotSelected",
            cnstr_student="NotSelected",cnstr_adult="NotSelected",cnstr_prep="NotSelected",
            formats="on",rollup="on",status="on",subject="on",adult="on",student="on")

params = "&".join([k + "=" + v for k,v in args.iteritems()])
_url = [baseurl,page]
url = "/".join(_url) + "?" + params


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get(url)

elem = browser.find_elements_by_class_name("table")

print elem
#elem.send_keys("period")
#elem.send_keys(Keys.RETURN)

#assert "doobar" in browser.page_source
browser.close