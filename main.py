from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# connecting to BrightData API
AUTH = 'brd-customer-hl_95d5726c-zone-scraping_browser1:pf55bbw07stq'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    
    # using API's Scraping Browser as driver 
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to the Google Maps page for business')
        url = "https://www.google.com/maps/place/Scileppi's+at+The+Old+Stone+Church/@39.3720661,-104.8714116,15z/data=!3m1!4b1!4m6!3m5!1s0x876c99212e83407f:0x2a5eaab168c360e4!8m2!3d39.37205!4d-104.8611333!16s%2Fg%2F11f5pfgpyc?entry=ttu&g_ep=EgoyMDI1MDQxNi4xIKXMDSoASAFQAw%3D%3D"
        driver.get(url)
        
        # Wait for review elements to appear and test for presence
        wait = WebDriverWait(driver, 10)
        review_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "wiI7pd")))

        reviews = [element.text for element in review_elements]

        print(reviews)

        # Wait a bit to see what happens
        time.sleep(20)


if __name__ == '__main__':
  main()