
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# java -jar selenium-server-standalone-2.53.0.jar -Dwebdriver.gecko.driver=/usr/local/bin/geckodriver

import os
import time

baseurl = "http://www.hungrycrayon.com"
page="dpivot.php"

def full_url():
    args = dict(source_type = "student",source_value = "Vonda",xaxis="period",
                yaxis="dow",ztypes="subject",source="56newworkp",
                cnstr_subject="NotSelected",cnstr_dow="NotSelected",cnstr_period="NotSelected",
                cnstr_student="NotSelected",cnstr_adult="NotSelected",cnstr_prep="NotSelected",
                formats="on",rollup="on",status="on",subject="on",adult="on",student="on")

    params = "&".join([k + "=" + v for k,v in args.iteritems()])
    _url = [baseurl,page]
    url = "/".join(_url) + "?" + params
    
    return url

def set_select_element(name,value,browser,url):    
    browser.find_element_by_xpath("//select[@name=\""+name+"\"]/option[text()=\""+value+"\"]").click()

def set_checkbox_element(name,browser,url):    
    element = browser.find_element_by_xpath("//*[@name=\""+name+"\"]")
    browser.execute_script("arguments[0].click();", element)
        
def get_table_values(browser):
    elements = browser.find_elements_by_xpath("//td/a")
    
    return[el.text for el in elements]

browser = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.FIREFOX)

_url = [baseurl,page]
url = "/".join(_url)

browser.get(url)

#set_select_element("xaxis","subject",browser,url)
set_select_element("source_value","Donny",browser,url)
set_checkbox_element("subject",browser,url)

time.sleep(2)
print get_table_values(browser)