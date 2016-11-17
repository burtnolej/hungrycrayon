from selenium import webdriver
import os
import time

baseurl = "http://192.168.1.154/login.php"

'''firefox_profile = webdriver.FirefoxProfile()

firefox_profile.set_preference('browser.download.folderList', 2)
firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
firefox_profile.set_preference('browser.download.dir', os.getcwd())
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'tcx')
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))

'''

#firefox_profile.get(baseurl)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get(baseurl)
#assert 'Yahoo' in browser.title