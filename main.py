from selenium.webdriver import Remote, ChromeOptions, ActionChains
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

from browser_manager import BrowserSessionManager

#----------Helper Functions---------------#
        
def expand_all_reviews(driver, more_button_class="w8nwRe", delay=2):
    #Clicks all 'More' buttons in Google reviews to expand full text
    try:
        more_buttons = driver.find_elements(By.CLASS_NAME, more_button_class)
        for button in more_buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
            except (ElementClickInterceptedException, ElementNotInteractableException):
                continue
        time.sleep(delay)
    except Exception as e:
        print(f"[Warning] Failed to expand reviews: {e}")



def extract_reviews(review_elements, username_class, text_class):
    extracted = []
    for review_el in review_elements: 
        try:
            username_el = review_el.find_element(By.CSS_SELECTOR, username_class)
            text_el = review_el.find_elements(By.CLASS_NAME, text_class)  # use find_elements for safety

            username = username_el.text.strip()
            review_text = text_el[0].text.strip().replace('\n', ' ') if text_el else ""  # for empty reviews
            raw_profile_text = review_el.text.strip().replace('\n', ' ')
            cleaned_profile = raw_profile_text.replace(username, "").replace(review_text, "").strip() #we don't need username or review text again

            extracted.append({
                "username": username,
                "review": review_text,
                "profile_info": cleaned_profile
            })

            if review_text == "":
              print(f"[Notice] Empty review captured from: {username}")

        except Exception as e:
            print(f"[Skipping] Error parsing a review: {e}")
    
    return extracted

def normalize_text(text):
    return text.strip().lower()


#-------------Scraping Logic--------------------#


manager = BrowserSessionManager(
    use_brightdata=False,
)

def main():
    
  driver = manager.start_session()

  # insert url for the google maps page for business location
  url = "https://www.google.com/maps/place/Bien+Y+Tu/@39.3734649,-104.8628896,17z/data=!3m1!4b1!4m6!3m5!1s0x876c99be1478395b:0x95c8d18822604bc7!8m2!3d39.3734608!4d-104.8603147!16s%2Fg%2F11lymnnzn6?entry=ttu&g_ep=EgoyMDI1MDQyMC4wIKXMDSoASAFQAw%3D%3D"
  driver.get(url)

  wait = WebDriverWait(driver, 20) # setting wait condition
  totalRevSelector = "button.GQjSyb.fontTitleSmall.rqjGif" # This says "x reviews" and is clickable to navigate to all reviews
  usernameClassName = ".d4r55" # username locator
  reviewsClassName = "jftiEf"  # review container locator; use "wiI7pd" for review text
  textClassName = "wiI7pd" # for the review text specifically

  totalRevCount = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, totalRevSelector))).get_attribute("textContent").split(' ')[0].replace(',','').replace('.','')
  print(f"Found some reviews! This business currently has {totalRevCount} reviews.") # confirm correct count

  wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, totalRevSelector))).click()

  #scroll_box = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
  scroll_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")))

  review_data = []

  while True: 
            
      #stores a list of review elements
      review_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, reviewsClassName))) #By.CLASS_NAME, "jftiEf"

      # expand reviews before extracting data
      expand_all_reviews(driver)

      # extract review data
      new_reviews = extract_reviews(review_elements, usernameClassName, textClassName)

      # add only new reviews
      previous_count = len(review_data)

      review_data.extend([
          r for r in new_reviews
          if not any(
              r["username"] == existing["username"] and
              normalize_text(r["review"]) == normalize_text(existing["review"])
              for existing in review_data
          ) #allows for multiple reviews from same username if different text
      ])


      if len(review_data) == previous_count:
          print("No new reviews loaded. Exiting scroll loop.")
          print("Total found: ", len(review_data))
          break

      # Scroll the container down
      driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
      time.sleep(3) # wait a couple seconds for more reviews to load

  df = pd.DataFrame(review_data)

  print("DATAFRAME HEAD:")
  print(df.head())
  print("DATAFRAME TAIL:")
  print(df.tail())
  try:
      df.to_csv("reviews.csv", index=False)
      print("Dataframe exported to .csv")
  except: 
      print("Issue exporting to .csv")
 
  manager.close_session()


if __name__ == '__main__':
  main()