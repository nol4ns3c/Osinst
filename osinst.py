from selenium import webdriver as web
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

bot_username = ''    # Your instagram username
bot_password = ''    # Your instagram password
profiles = ['']      # Instagram usernames you want to intersect
PATH = ""            # Path to the chromedriver
class Instagram():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = web.Chrome(PATH)

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        try:
            browser.get('https://www.instagram.com')
            time.sleep(random.randrange(4, 8))

            #allow cookie:

            try:
                cookie = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Allow essential and optional cookies']"))
                )
                time.sleep(random.randrange(3, 6))
                cookie.click()
            except:
                print("There is a problem")

            #Enter username:

            username_input = browser.find_element(By.XPATH,"(//input[@name='username'])[1]")
            username_input.clear()
            username_input.send_keys(self.username)
            time.sleep(random.randrange(2, 4))

            # Enter password:

            password_input = browser.find_element(By.XPATH,"(//input[@name='password'])[1]")
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(random.randrange(5, 7))
            password_input.send_keys(Keys.ENTER)
            time.sleep(random.randrange(9, 11))
            print(f'[{self.username}] Successfully logged on!')
        except Exception as ex:
            print(f'[{self.username}] Authorization fail')
            #self.close_browser()


        #save your login page

        try:
            save = WebDriverWait(browser, 7).until(
                EC.presence_of_element_located((By.XPATH, "(//button[normalize-space()='Not Now'])[1]"))
            )
            time.sleep(random.randrange(2, 5))
            save.click()
        except:
            print("There is a problem")

    #Getting follow list

    def get_followers(self, users, amount):
        amount = 100
        browser = self.browser
        followers_list = []
        names = []
        res = []
        for user in users:
            browser.get('https://instagram.com/' + user)
            time.sleep(random.randrange(5, 9))
            followers_button = browser.find_element(By.XPATH, "(//div[@class='_aacl _aacp _aacu _aacx _aad6 _aade'])[2]")

            countt = followers_button.text

            def parsing(countt):

                if 'K' in countt:
                    countf = float((countt.split('K')[0])) * 1000
                    countl = int(countf)
                else:
                    countf = float((countt.split(' ')[0]))
                    countl = int(countf)
                return countl

            count = parsing(countt)



            if amount > count:
                print(f'You set amount = {amount} but there are {count} followers, then amount = {count}')
                amount = count
            followers_button.click()
            loops_count = int(count / 12)
            print(f'Scraping. Total: {count} usernames. Wait {loops_count} iterations')
            time.sleep(random.randrange(9, 13))
            followers_ul = browser.find_element(By.XPATH, "//div[@class='_aano']")
            time.sleep(random.randrange(5, 7))
            try:
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(3, 5))
                    all_div = followers_ul.find_elements(By.TAG_NAME, "a")
                    names = [name.text for name in all_div if name.text != '']
                followers_list.append(names)
                res = list(set.intersection(*map(set, followers_list)))
            except Exception as ex:
                print(ex)
                self.close_browser()

        return res

bot = Instagram(bot_username, bot_password)
bot.login()
followers = bot.get_followers(profiles, 100)
print(followers)


