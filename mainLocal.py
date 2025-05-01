from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Remote, ChromeOptions, ActionChains
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from browser_manager import BrowserSessionManager

# see class file for information on connecting to remote browser
manager = BrowserSessionManager(
    use_brightdata=False,
)

driver = manager.start_session()

# insert url for the google maps page for business location
url = "https://www.google.com/maps/place/Bien+Y+Tu/@39.3734649,-104.8628896,17z/data=!3m1!4b1!4m6!3m5!1s0x876c99be1478395b:0x95c8d18822604bc7!8m2!3d39.3734608!4d-104.8603147!16s%2Fg%2F11lymnnzn6?entry=ttu&g_ep=EgoyMDI1MDQyMC4wIKXMDSoASAFQAw%3D%3D"
driver.get(url)
time.sleep(3)

wait = WebDriverWait(driver, 20) # setting wait condition
totalRev = "button.GQjSyb.fontTitleSmall.rqjGif" # This says "x reviews" and is clickable to navigate to all reviews
usernameClassName = ".d4r55" # username locator
reviewsClassName = "jftiEf"  # review container locator; use "wiI7pd" for review text

totalRevCount = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, totalRev))).get_attribute("textContent").split(' ')[0].replace(',','').replace('.','')
print(f"Found some reviews! This business currently has {totalRevCount} reviews.") # confirm correct count

time.sleep(5) # ideally change EC to accomodate clickability
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, totalRev))).click()
time.sleep(5)

mydict = {} # we will make key-value pair from reviewer's username and review content
previous_count = 0 # to track reviews that have been accessed as we scroll

scroll_box = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")

while True: #int(totalRevCount): 
          
    #stores a list of review elements if found
    review_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, reviewsClassName))) #By.CLASS_NAME, "jftiEf"
    #stores a list of usernames if found
    reviewer_names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, usernameClassName)))

    previous_count = len(mydict)

    for rev, name in zip(review_elements, reviewer_names):
        if name.text not in mydict:  # skip username duplicates -- what if someone leaves multiple reviews??
            mydict[name.text] = rev.text # allows for reviews with no text -- should I change this since it grabs all the html?

    print(f"Currently found {len(mydict)} reviews")
    print(mydict)
    print("---------------------------------------------------------------")

    # to print review text only:
    # reviews = [element.text for element in review_elements]
    # print(reviews)

    if len(mydict) == previous_count:
        print("No new reviews loaded. Exiting scroll loop.")
        print("Total found: ", len(mydict))
        break

    # Scroll the container down
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
    time.sleep(3) # wait a couple seconds for more reviews to load


manager.close_session()