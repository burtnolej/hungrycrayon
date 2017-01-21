
import os
import time

from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

__all__ = ['full_url','set_select_element','set_select_element', 
           'click_menu_element','set_checkbox_element', 
           'set_input_text_element','get_table_values', 
           '_macro_add_new_record','_macro_menu_click', 
           '_macro_list_objects','_macro_update_field','webdriver',
           'Keys', 'DesiredCapabilities','ActionChains','get_elements',
           '_macro_do_pivot']

def full_url():
    args = dict(source_type = "student",source_value = "Clayton",xaxis="period",
                yaxis="dow",ztypes="subject",
                #source="56newworkp",
                
                cnstr_subject="NotSelected",cnstr_dow="NotSelected",cnstr_period="NotSelected",
                cnstr_student="NotSelected",cnstr_adult="NotSelected",cnstr_prep="NotSelected",
                formats="on",rollup="on",status="on",subject="on",adult="on",student="on")

    params = "&".join([k + "=" + v for k,v in args.iteritems()])
    _url = [baseurl,page]
    url = "/".join(_url) + "?" + params
    
    return url

# simple wrappers to run commands on DOM elements
def set_select_element(name,value,browser):    
    browser.find_element_by_xpath("//select[@name=\""+name+"\"]/option[text()=\""+value+"\"]").click()

def click_menu_element(href,browser):
    element = browser.find_element_by_xpath('//*[@href="'+href+'"]')
    element.click()
    
def set_checkbox_element(name,browser):    
    element = browser.find_element_by_xpath("//*[@name=\""+name+"\"]")
    browser.execute_script("arguments[0].click();", element)
        
def set_input_text_element(id,value,browser):
    element = browser.find_element_by_xpath("//*[@id=\""+id+"\"]")
    element.send_keys(value)
    
def get_table_values(browser,xpathstr="//td/a",suppressid=False,onlyid=False):
    if suppressid==False and onlyid==False:
        elements = browser.find_elements_by_xpath(xpathstr)
        return[el.text for el in elements]
    else:
        row_elements = browser.find_elements_by_xpath("//tr")
        
        # get the col idx of id
        hdrs = [hdr.text for hdr in row_elements[0].find_elements_by_xpath("."+xpathstr)]
        ididx = hdrs.index('id')
        width = len(hdrs)
        
        _l = []
        for row_element in row_elements:
            
            row_text = [row.text for row in row_element.find_elements_by_xpath("."+xpathstr)]
            
            if onlyid==True:
                _l.append(row_text[ididx])
            else:
                for i in range(width):
                    if i <> ididx:
                        _l.append(row_text[i])
            
        return(_l)

def get_elements(browser,clsname,attr,attrval=None,inputtype=None):
    
    # get_elements(self.browser,'select','period')
    # get_elements(self.browser,'input')
    
    if attrval==None:
        if inputtype==None:
            elements = browser.find_elements_by_xpath("//"+clsname)
        else:
            elements = browser.find_elements_by_xpath("//"+clsname+"[@type=\""+inputtype+"\"]")
            
        return dict((element.get_attribute(attr),element.text.split("\n")) for element in elements)
    else:        
        element = browser.find_element_by_xpath("//"+clsname+"[@"+attr+"=\""+attrval+"\"]")
        return dict(name = element.text.split("\n"))
    return 

# macros to do functions on the UI
def _macro_add_new_record(browser,objtype,fields):
    
    sleeptime=0.1
    click_menu_element("dnew.php",browser)
    time.sleep(sleeptime)
    set_select_element("source_value",objtype,browser)

    for k,v in fields.iteritems():
        set_input_text_element(k,v,browser)
        time.sleep(sleeptime)
        
    element = browser.find_element_by_xpath("//*[@name='button']")
    element.click()
    time.sleep(sleeptime)

def _macro_menu_click(browser,steps):
    menu = browser.find_element_by_xpath('//*['+steps[0]+']')
    hidden_submenu = browser.find_element_by_xpath('//*['+steps[1]+']')
    ActionChains(browser).move_to_element(menu).perform()
    time.sleep(0.1)
    hidden_submenu.click()
    
def _macro_list_objects(browser,objtype,filter={},):
    
    sleeptime=0.1
    _macro_menu_click(browser,['text()="search"','@href="dsearch.php"'])
       
    if filter <> {}:
        
        for k,v in filter.iteritems():
            set_select_element("cnstr_"+k,v,browser)
    
    time.sleep(sleeptime)
    
    browser.execute_script("var el = document.getElementsByName('source_value');el[0].value = '"+objtype+"';")
    time.sleep(sleeptime)
    
    browser.execute_script("url = buildurl();get(url);")
    time.sleep(sleeptime)
    
    
def _macro_update_field(browser,id,fields):
    _macro_menu_click(browser,['text()="edit"','@href="dedit.php"'])
    
    sleeptime=0.1
    time.sleep(sleeptime)
    set_input_text_element("source_value",id,browser)
    time.sleep(sleeptime)
    set_input_text_element("source_value",Keys.RETURN,browser)
    time.sleep(sleeptime)
    
    for k,v in fields.iteritems():
        set_select_element(k,v,browser)
        #set_input_text_element(k,v,browser)
        
    time.sleep(sleeptime)
    
    element = browser.find_element_by_xpath("//*[@name='button']")
    element.click()
    
def _macro_do_pivot(browser,source_type,source_value,ztypes):
    
    sleeptime=0.1
    click_menu_element("dpivot.php",browser)
    time.sleep(sleeptime)
    set_select_element("source_type",source_type,browser)
    time.sleep(sleeptime)
    set_select_element("source_value",source_value,browser) 

    for ztype in ztypes:
        set_checkbox_element(ztype,browser)
        time.sleep(sleeptime)

    