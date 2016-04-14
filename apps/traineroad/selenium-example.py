from selenium import webdriver
import os
import time

baseurl = "https://www.trainerroad.com/login"
username = "burtnolejusa"
password = "G0ldm@n1"

#firefox_profile = webdriver.FirefoxProfile()

#firefox_profile.set_preference('browser.download.folderList', 2)
#firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
#firefox_profile.set_preference('browser.download.dir', os.getcwd())
#firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'tcx')
#firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))

xpaths = {
        'usernameTxtBox' : "//input[@name='Username']",
        'passwordTxtBox' : "//input[@name='Password']",
        'submitButton' :   "//button[contains(text(),'Log In')]",
        'downloadButton' : "//button[contains(text(),'Download')]"
        }


chromedriver = "/home/burtnolej/Downloads/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

mydriver = webdriver.Chrome(chromedriver)
mydriver.get(baseurl)
#mydriver.maximize_window()

#Clear Username TextBox if already allowed "Remember Me"
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()

#Write Username in Username TextBox
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)

#Clear Password TextBox if already allowed "Remember Me"
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()

#Write Password in password TextBox
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)

#Click Login button
mydriver.find_element_by_xpath(xpaths['submitButton']).click()

for i in range(10):
	mydriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(0.5)

num_rides = len(mydriver.find_elements_by_class_name("header-text"))

print "downloading",num_rides,"rides"

rides = []
for i in range(num_rides):
	
	try:
		#Get link to the page for the next ride		
		nextRide = mydriver.find_elements_by_class_name("header-text")[i]
		attr = nextRide.find_element_by_css_selector("a").get_attribute("href")
		rides.append(attr)
		
	except:
		print "cannot get item",i
		

for ride in rides:

	try:
		mydriver.get(ride) 
		
		print "now getting",ride
			
		#Get link to the download button
		time.sleep(0.5)
		downloadButton = mydriver.find_element_by_class_name('btn-default')
		downloadButton.click()
		time.sleep(0.5)
		
		#Go  back to the list of rides page
		mydriver.back()
		time.sleep(0.5)
	except:
		print "cannot get item",i
		        
