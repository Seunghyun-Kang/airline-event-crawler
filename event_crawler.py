from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

class EventCrawler:
    def __init__(self, url):
        #location of chromedriver
        self.driver = webdriver.Chrome('/Users/seun9.kang/Downloads/chromedriver')
        self.driver.get(url = url)

    def __del__(self):
        self.driver.close()

    def getEventList(self):
        if "jejuair" in self.driver.current_url:
            print("This is JejuAir events :")
            tag = "jejuair"
            try:
                print("find more button")
                more_button = self.driver.find_element(by=By.CLASS_NAME, value='more__button')
                more_button.click()
                time.sleep(2)
            except:
                print("No more button")
        
            event_list = self.driver.find_elements(by=By.CLASS_NAME, value='search-result__item')
            print(f"Find {len(event_list)} lists of event")

            if event_list != None:
                df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content'])    
                for event in event_list:
                    airline = tag
                    url = event.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                    header = event.find_element(by=By.CLASS_NAME, value='event-banner__text').get_attribute('innerText')
                    content = event.find_element(by=By.CLASS_NAME, value='event-banner__title').get_attribute('innerText')
                    date = event.find_element(by=By.CLASS_NAME, value='event-banner__date').get_attribute('innerText')
                    new_df = [(airline, url, header, date, content)]
                    dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                    df = pd.concat([df,dfNew])
                print(df)
            else:
                return
        elif "airbusan" in self.driver.current_url:
            print("This is AirBusan events :")
            tag = "jejuair"
            event_list = self.driver.find_elements(by=By.TAG_NAME, value='li')
            print(f"Find {len(event_list)} lists of event")

            if event_list != None:
                df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content'])    
                for event in event_list:
                    airline = tag
                    url = event.find_element(by=By.XPATH, value="//ul[@id='nav_2']//a").get_attribute('href')
                    header = event.find_element(by=By.XPATH, value="//ul[@id='nav_2']//strong").get_attribute('innerText')
                    content = event.find_element(by=By.XPATH, value="//ul[@id='nav_2']//strong").get_attribute('innerText')
                    date = event.find_element(by=By.XPATH, value="//ul[@id='nav_2']//span").get_attribute('innerText')
                    new_df = [(airline, url, header, date, content)]
                    dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                    df = pd.concat([df,dfNew])
                print(df)
            else:
                return


#TEST
# a= EventCrawler("https://www.jejuair.net/ko/event/event.do").getEventList()
a= EventCrawler("https://www.airbusan.com/content/common/flynjoy/flyNEvent/").getEventList()
