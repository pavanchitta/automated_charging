from requests import Session
from bs4 import BeautifulSoup

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    login_params = {
    }
    webdriver = login(login_params)
    print(webdriver.current_url)
    print("Successfully logged in")
    try:
        element = WebDriverWait(webdriver, 20).until(
            EC.presence_of_element_located((By.ID, "arrowBillPaymentHistory"))
        )
    finally:
        element.click()
    # bills_url = "https://m.pge.com/?_ga=2.13832887.1033180705.1651987363-1497019897.1627081963#myaccount/dashboard"
    # headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
    # res = SESS.get(bills_url, headers = headers)
    # print(res)
    # bills_site = BeautifulSoup(res.text, 'html.parser')
    # print(bills_site.prettify())
    # webdriver.close()


def login(params):
    # Common utility to login and initialize a webdriver
    """
    Perform manual proxy login using selenium
    """
    url = "https://www.pge.com/"

    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    driver.get(url)
    
    try:
        while True:
            u = driver.find_element_by_name('username')
            u.clear()
            u.send_keys(params['username'])
            p = driver.find_element_by_name('password')
            p.clear()
            p.send_keys(params['password'])
            p.send_keys(Keys.RETURN)
            time.sleep(5)
    except Exception:
        pass
    return driver

if __name__ == "__main__":
    main()