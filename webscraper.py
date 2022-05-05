# import csv
# import selenium
# from selenium import webdriver
# from getpass import getpass 
# from time import sleep
# #from webbrowser import Chrome 
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver import Chrome 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import csv
from getpass import getpass 
import time 
from time import sleep 

from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#depending on the browser used 
#from msedge.selenium_tools import Edge, EdgeOptions
#from selenium.webdriver import Chrome 
#from selenium.webdriver import Firefox 
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
import uuid
import pandas as pd


class Scraper:
    """This class is used to scrape tweets from twitter
    Attributes:
    -Twitter URL
    """

    def __init__(self,url: str = 'https://twitter.com/login'):
        self.driver_path = "C:/Users/sagal/OneDrive/Documents/AiCore/miniconda3/condabin/chromedriver.exe"
        self.service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        #self.driver = webdriver.Chrome(executable_path="C:/Users/sagal/OneDrive/Documents/AiCore/miniconda3/condabin/chromedriver.exe")
        self.driver.get(url)
        self.driver.maximize_window()
        # self.dict_data = {'UUID': [],'twitter_username':[] , 'twitter_handle': [] ,'twitter_postdate': [],'twitter_comment':[],'twitter_reply_cnt':[],'twitter_like_cnt':[],'twitter_retweet_cnt':[]}
        time.sleep(2)

    def login_username (self,username_xpath: str ='//input[@name="text"]' ):

        """This function is used to enter username handle"""

        username= self.driver.find_element(By.XPATH , username_xpath)
        twitter_username =getpass()
        username.send_keys(twitter_username)
        username.send_keys(Keys.RETURN)
        time.sleep(2)
    
    def login_password (self,password_xpath: str ='//input[@name="password"]'):
        """This function is used to """
        password= self.driver.find_element(By.XPATH , password_xpath)
        my_password = getpass()
        password.send_keys(my_password)
        time.sleep(2)
        
    def login (self,click_passowrd: str ='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]'):
        login_to_twitter = self.driver.find_element(By.XPATH,click_passowrd ).click()

    def accept_cookies(self,xpath: str ='//*[@id="layers"]/div/div[2]/div/div/div/div[2]/div[1]'):
        try:    
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH , xpath).click()
        except TimeoutException:
            print('No Cookies Found')
        time.sleep(2)
    
    def search(self,search_xpath: str = '//input[@aria-label="Search query"]'):
        user_search = self.driver.find_element(By.XPATH, search_xpath)
        request = input('What would you like to search?')
        user_search.send_keys(request)
        user_search.send_keys(Keys.RETURN)
        self.driver.find_element(By.LINK_TEXT, 'Latest').click()
        time.sleep(3)

    # dict_data = {'UUID': [],'twitter_username':[] , 'twitter_handle': [] ,'twitter_postdate': [],'twitter_comment':[],'twitter_reply_cnt':[],'twitter_like_cnt':[],'twitter_retweet_cnt':[]}

#    def find_container(self, xpath: str ="//div[@aria-label='Timeline: Search timeline']//article"):
    def find_container(self,xpath: str = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div'):
        time.sleep(1)
        container = self.driver.find_element(By.XPATH,xpath)
        twitter_list = container.find_elements(By.XPATH, './div')
        last_postion = self.driver.execute_script("return window.pageYOffset;")
        scrolling = True
        dict_data = {'UUID': [],'twitter_username':[] , 'twitter_handle': [] ,'twitter_postdate': [],'twitter_comment':[],'twitter_reply_cnt':[],'twitter_like_cnt':[],'twitter_retweet_cnt':[]}

        last_postion = self.driver.execute_script("return window.pageYOffset;")
        scrolling = True
        
        while True:
            container = self.driver.find_element(By.XPATH,xpath)
            twitter_list = container.find_elements(By.XPATH, './div')
            print(dict_data)

            for tweet in twitter_list:
                try:
                    dict_data['twitter_username'].append(tweet.find_element_by_xpath('.//span').text)
                    dict_data['twitter_handle'].append(tweet.find_element_by_xpath('.//span[contains(text(),"@")]').text)
                    try:
                        dict_data['twitter_postdate'].append(tweet.find_element_by_xpath('.//time').get_attribute('datetime'))
                    except NoSuchElementException:
                        dict_data['twitter_postdate'].append('advert')
                    # dict_data['twitter_comment'].append(tweet.find_element_by_xpath('.//div[2]/div[2]/div[1]').text)
                #responding =container.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
                #text=comment + responding
                    #dict_data['twitter_comment'].append(tweet.find_element_by_xpath('//div[@lang ="en"]').text)
                    dict_data['twitter_comment'].append(tweet.find_element_by_xpath('//div[@class ="css-1dbjc4n"]').text)
                    dict_data['twitter_reply_cnt'].append(tweet.find_element_by_xpath('//div[@data-testid ="reply"]').text)

                    dict_data['twitter_like_cnt'].append(tweet.find_element_by_xpath('//div[@data-testid ="like"]').text)

                    dict_data['twitter_retweet_cnt'].append(tweet.find_element_by_xpath('//div[@data-testid ="retweet"]').text)
                    dict_data['UUID'].append(uuid.uuid4()) 
                except StaleElementReferenceException or NoSuchElementException:
                    sleep(4)  
          
            Scroll_attempt = 0
            while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(1)
                curr_position = self.driver.execute_script("return window.pageYOffset;")
                if last_postion == curr_position:
                    Scroll_attempt += 1
                    if Scroll_attempt >= 3:
                        scrolling=False
                        break
                    else:
                        sleep(2)
                else:
                    last_postion =curr_position
                    break
                    
                  






        
print (__name__)
if __name__ == '__main__':
    bot = Scraper()
    bot.login_username()
    bot.login_password()
    bot.login()
    bot.accept_cookies()
    bot.search()
    bot.find_container()
    #bot.tweets()
    #bot.get_tweet_data()

