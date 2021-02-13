# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import csv
import time


options = Options()
options.add_argument("--lang=en")
driver = webdriver.Edge(EdgeChromiumDriverManager().install())

url = "https://www.google.it/maps/place/Pantheon/@41.8986108,12.4746842,17z/data=!3m1!4b1!4m7!3m6!1s0x132f604f678640a9:0xcad165fa2036ce2c!8m2!3d41.8986108!4d12.4768729!9m1!1b1"
driver.get(url)

wait = WebDriverWait(driver, 10)
menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Sort")]')))  

menu_bt.click()

# =============================================================================
# recent_rating_bt = driver.find_elements_by_xpath("/div[@id='menuitem']")
# recent_rating_bt.click()
# 
# time.sleep(5)
# =============================================================================

response = BeautifulSoup(driver.page_source, 'html.parser')
rlist = response.find_all('div', class_='section-review-content')

#r = requests.get(url)

id_r = response.find('button', 
              class_='section-review-action-menu')['data-review-id']
username = response.find('div', 
                  class_='section-review-title').find('span').text
try:
    review_text = response.find('span', class_='section-review-text').text
except Exception:
    review_text = None
rating = response.find('span', class_='section-review-stars')['aria-label']
rel_date = response.find('span', class_='section-review-publish-date').text








