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
        print('Connected! Navigating to https://google.com')
        driver.get('https://google.com')
        
        # Wait for the search input to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "APjFqb"))
        )

        # Do your search like before
        input_element = driver.find_element(By.ID, "APjFqb")
        input_element.clear()
        #input_element.send_keys("scileppi's castle rock" + Keys.ENTER)

        # Wait a bit to see what happens
        time.sleep(20)


if __name__ == '__main__':
  main()