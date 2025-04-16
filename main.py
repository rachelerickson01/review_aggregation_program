from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path="/Users/rachelerickson/repos/review_aggregation_program/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

time.sleep(5)

driver.quit()