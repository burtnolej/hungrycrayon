from selenium import webdriver
import os
import time

baseurl = "http://192.168.1.154/test_selenium.php"

'''firefox_profile = webdriver.FirefoxProfile()

firefox_profile.set_preference('browser.download.folderList', 2)
firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
firefox_profile.set_preference('browser.download.dir', os.getcwd())
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'tcx')
firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))
'''
'''    <body>
        <form action='foobar.php' method='post' accept-charset='UTF-8'>	
            <fieldset >
                <input type='hidden' name='submitted' id='submitted' value='1'/>
                <div>
                  <div id='one'>
                    <div class="container">
                      <label for="xaxis" >xaxis</label>
                      <input type="text" name="xaxis" id="xaxis" list="suggestions0">
                      <datalist id="suggestions0">
                        <option>period</option>
                        <option>dow</option>
                        <option>adult</option>
                        <option>subject</option>
                      </datalist>
                    </div>
                  <div class="container">
                    <label for="yaxis" >yaxis</label>
                    <input type="text" name="yaxis" id="yaxis" list="suggestions1">
                    <datalist id="suggestions1">
                      <option>period</option>
                      <option>dow</option>
                      <option>adult</option>
                      <option>subject</option>
                    </datalist>
                  </div>
                 <div class="container">
                  <label for="source_type" >source_type</label>
                  <input type="text" name="source_type" id="source_type" list="suggestions2">
                    <datalist id="suggestions2">
                      <option>student</option>
                      <option>adult</option>
                    </datalist>
                </div>
                <div class="container">
                  <label for="source_value" >source_value</label>
                  <input type="text" name="source_value" id="source_value" list="suggestions3">
                  <datalist id="suggestions3">
                    <option>Peter</option>
                  </datalist>
                </div><input type="submit" name="submit" value="go" />				
              </div>
            </fieldset>
        </form>
    </body>
</html>
'''

#firefox_profile.get(baseurl)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get(baseurl)

elem = browser.find_element_by_name("xaxis")
elem.send_keys("period")
elem.send_keys(Keys.RETURN)

assert "doobar" in browser.page_source
browser.close()