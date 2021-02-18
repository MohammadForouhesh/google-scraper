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

url = "https://www.google.com/travel/hotels/deerhurst%20resort/entity/CgoI6fnlocXKyPgPEAE/reviews?g2lb=2502548%2C4258168%2C4271060%2C4306835%2C4317915%2C4322823%2C4328159%2C4330862%2C4371334%2C4401769%2C4419364%2C4424916%2C4429191%2C4433754%2C4435907%2C4436127%2C4441383%2C4443999%2C4270859%2C4284970%2C4412693&hl=en&gl=ca&un=1&q=deerhurst%20resort&rp=EOn55aHFysj4DxDp-eWhxcrI-A84AkAASAHAAQI&ictx=1&utm_campaign=sharing&utm_medium=link&utm_source=htls&ved=0CAAQ5JsGahcKEwiglLTVt-vuAhUAAAAAHQAAAAAQAg&ts=CAESABogCgIaABIaEhQKBwjlDxADGAESBwjlDxADGAIYATICEAAqCQoFOgNDQUQaAA"
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








