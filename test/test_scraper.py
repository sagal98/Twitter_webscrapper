from webscraper import Scraper
import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.bot = Scraper()
    

    def test_page(self):
        self.bot.driver.maximize_window()
        time.sleep(1)
        self.bot.driver.find_element(By.XPATH, '//*[@aria-label="Twitter"]') # checks for the twitter logo if this changes the scraper will need to be updated
        self.bot.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[1]') # checks for username entry 
        self.bot.driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]') #checks for the next botton to make sure the login page has the same format username and then password

    def test_login(self):
        self.bot.login_username()
        self.bot.login_password()
        self.bot.login()
        self.bot.accept_cookies()
        time.sleep(1)
        actual_value = self.bot.driver.current_url
        expected_value ='https://twitter.com/home'
        self.assertEqual(actual_value,expected_value)

    def search(self):
        self.bot.search()
        
    def teardown(self):
        time.sleep(1)
        self.bot.driver.close()


if __name__ == '__main__':
    unittest.main()