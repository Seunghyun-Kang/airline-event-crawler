from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd

class EventCrawler:
    def __init__(self, tag):
        self.tag = tag
        if tag == "jejuair":
            self.url = "https://www.jejuair.net/ko/event/event.do"
        elif tag == "airbusan":
            self.url = "https://www.airbusan.com/content/common/flynjoy/flyNEvent/"
        elif tag == "tway":
            self.url = "https://twayair.com/app/promotion/event/being?"
        elif tag == "airseoul":
            self.url = "https://flyairseoul.com/CW/ko/ingEvent.do"
        elif tag == "jinair":
            self.url = "https://www.jinair.com/promotion/nowLeave"

        options = Options()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))

        #location of chromedriver
        self.driver = webdriver.Chrome('/Users/seun9.kang/Downloads/chromedriver',options=options)
        self.driver.get(url = self.url)

        self.driver.delete_all_cookies()

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
                    new_df = [(airline, url, date, header, content)]
                    dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                    df = pd.concat([df,dfNew])
                return df
            else:
                return
        elif "airbusan" in self.driver.current_url:
            print("This is AirBusan events :")
            tag = "airbusan"
            event_list = self.driver.find_elements(by=By.XPATH, value="//ul[@id='nav_2']//li//a")
            print(f"Find {len(event_list)} lists of event")

            if event_list != None:
                df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content'])    
                for event in event_list:
                    airline = tag
                    url = event.get_attribute('href')
                    header = event.find_element(by=By.TAG_NAME, value="strong").get_attribute('innerText')
                    content = event.find_element(by=By.TAG_NAME, value="strong").get_attribute('innerText')
                    date = event.find_element(by=By.TAG_NAME, value="span").get_attribute('innerText')
                    new_df = [(airline, url, date, header, content)]
                    dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                    df = pd.concat([df,dfNew])
                return df
            else:
                return
        elif "twayair" in self.driver.current_url:
            print("This is Tway events :")
            tag = "tway"
            time.sleep(3)
            page_buttons = self.driver.find_elements(by=By.XPATH, value="//article//a[@class='num']")
            page_num = len(page_buttons) + 1
            print(f"Total page in Tway event site : {page_num}")
            
            df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content']) 
            for page in range(page_num):
                self.driver.get(url = f"https://twayair.com/app/promotion/event/being?page={page}")
                event_list = self.driver.find_elements(by=By.XPATH, value="//ul[@class='evt_list']//li//a")
                print(f"Find {len(event_list)} lists of event in page {page}")
                
                if event_list != None:   
                    for event in event_list:
                        airline = tag
                        code = event.get_attribute('href').split('\'')[1]
                        url = "https://twayair.com/app/promotion/event/retrieve/($code))/being/n?".replace('($code)',code)
                        header = event.find_element(by=By.TAG_NAME, value="strong").get_attribute('innerText')
                        content = event.find_element(by=By.CLASS_NAME, value="sbj_sub").get_attribute('innerText')
                        date = event.find_elements(by=By.TAG_NAME, value="p")[1].get_attribute('innerText')
                        new_df = [(airline, url, date, header, content)]
                        dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                        df = pd.concat([df,dfNew])
                    return df
                else:
                    return
        elif "airseoul" in self.driver.current_url:
            print("This is Airseoul events :")
            tag = "airseoul"
            time.sleep(3)
            page_buttons = self.driver.find_elements(by=By.XPATH, value="//ul[@class='page_navi']//li")
            page_num = len(page_buttons)
            print(f"Total page in Airseoul event site : {page_num}")
            
            df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content']) 
            for page in range(page_num):
                self.driver.get(url = f"https://flyairseoul.com/CW/ko/ingEvent.do?pageNo={page+1}")
                event_list = self.driver.find_elements(by=By.XPATH, value="//ul[@class='event_list']//li//a")
                print(f"Find {len(event_list)} lists of event in page {page}")
                
                if event_list != None:   
                    for event in event_list:
                        airline = tag
                        code = event.get_attribute('href')
                        url = "https://flyairseoul.com/" + code
                        header = event.find_element(by=By.CLASS_NAME, value="noti").get_attribute('innerText')
                        content = event.find_element(by=By.CLASS_NAME, value="txt").get_attribute('innerText')
                        date = event.find_element(by=By.CLASS_NAME, value="date").get_attribute('innerText')
                        new_df = [(airline, url, date, header, content)]
                        dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                        df = pd.concat([df,dfNew])
                    return df
                else:
                    return
        elif "jinair" in self.driver.current_url:
            print("This is Jinair events :")
            tag = "jinair"
            time.sleep(2)
            try:
                button = self.driver.find_element(by=By.XPATH, value="//fieldset//button")
                if(button):
                    print("Button Exist")
                    self.driver.execute_script("arguments[0].click();", button)
            except:
                print("Error")
                
            time.sleep(3)
            df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content']) 
            event_list = self.driver.find_elements(by=By.XPATH, value="//ul[@class='eventList']//li//a")
                
            if event_list != None:   
                for event in event_list:
                    airline = tag
                    code = event.get_attribute('href')
                    header = event.find_element(by=By.CLASS_NAME, value="tit").get_attribute('innerText')
                    content = event.find_element(by=By.CLASS_NAME, value="tit").get_attribute('innerText')
                    date = event.find_element(by=By.CLASS_NAME, value="date").get_attribute('innerText')
                    new_df = [(tag, code, date, header, content)]
                    dfNew = pd.DataFrame(new_df, columns=['airline', 'url', 'date',  'header','content'])
                    df = pd.concat([df,dfNew])
                return df
            else:
                return

#TEST
# jejuAir = EventCrawler("https://www.jejuair.net/ko/event/event.do")
# a= EventCrawler("https://www.jejuair.net/ko/event/event.do").getEventList()
# a= EventCrawler("https://www.airbusan.com/content/common/flynjoy/flyNEvent/").getEventList()
# a= EventCrawler("https://twayair.com/app/promotion/event/being?").getEventList()
# a= EventCrawler("https://flyairseoul.com/CW/ko/ingEvent.do").getEventList()
# a= EventCrawler("https://www.jinair.com/promotion/nowLeave").getEventList()
