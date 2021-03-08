# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 23:36:58 2021

@author: Mohammad.FT
"""

import logging
import time
import traceback
from datetime import datetime

import parsedatetime as pdt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored
from webdriver_manager.chrome import ChromeDriverManager

GM_WEBPAGE = 'https://www.google.com/maps/'
MAX_WAIT = 10
MAX_RETRY = 5
MAX_SCROLLS = 40

class GoogleUserScraper:
    def __init__(self, debug=False):
        self.debug = debug
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        self.driver.close()
        self.driver.quit()

        return True

    def parse_user(self):
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        user = {}
        try: 
            user_unreachable = response.find('span', class_="section-empty-tab").text
            user['total'] = 0
        except:            
            try:
                user['reviews'] = response.find('span', class_="section-tab-info-stats-label").text.replace(' · ', ' ').replace(',','').split(' ')[0]
            except Exception as e:
                print(e)
                user['reviews'] = 0
                
            try:
                user['ratings'] = response.find('span', class_='section-tab-info-stats-label').text.replace('·', '').replace(',','').split(' ')[3]
            except Exception as e:
                print(e)
                user['ratings'] = 0
                
            user['contributions'] = response.find_all('div', class_="section-profile-header-line")[1].text
            print(colored(user, 'green'))
            user['total'] = int(user['ratings']) + int(user['reviews'])
            
            return user
    
    
    def get_reviews(self, offset):
        # scroll to load reviews

        self.__scroll()
        # expand review text
        self.__expand_reviews()
        # parse reviews
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        rblock = response.find_all('div', class_='section-review-content')
        parsed_reviews = []
        for index, review in enumerate(rblock):
            if index >= offset:
                parsed_reviews.append(self.__parse(review))
                print(self.__parse(review))

        return parsed_reviews


    def get_account(self, url):
        resp = BeautifulSoup(self.driver.page_source, 'html.parser')

        place_data = self.__parse_place(resp)

        return place_data


    def __parse(self, review):

        item = {}
        title = review.find('div', class_="section-review-title section-review-title-consistent-with-review-text").find('span').text
        location = review.find('div', class_="section-review-subtitle section-review-subtitle-nowrap").find_all('span')[0].text
        try:
            review_text = self.__filter_string(review.find('span', class_='section-review-text').text)
        except Exception as e:
            review_text = None
            
        try:
            response_text = self.__filter_string(review.find('div', class_='section-review-owner-response').text)
            # response_text = self.__filter_string(review.find("(//button[@class=\'section-expand-review blue-link\'])[position()=2]"))
        except Exception as e:
            response_text = None
        
        try:
            rating = float(review.find('span', class_='section-review-stars')['aria-label'].split(' ')[1])
            relative_date = review.find('span', class_='section-review-publish-date').text
        except:
            __rating = review.find('span', class_='section-review-numerical-rating').text
            relative_date = review.find('span', class_='section-review-publish-date-and-source').find('span').text
            numerator = int(__rating[0])
            denominator = int(__rating[2])
            rating = (numerator/denominator)*5
            
        c = pdt.Constants()
        p = pdt.Calendar(c)
        absolute_date = datetime(*p.parse(relative_date)[0][:6])
        try:
            n_reviews_photos = review.find('div', class_='section-review-subtitle').find_all('span')[1].text
            metadata = n_reviews_photos.split('\xe3\x83\xbb')
            if len(metadata) == 3:
                n_photos = int(metadata[2].split(' ')[0].replace('.', ''))
            else:
                n_photos = 0

            idx = len(metadata)
            n_reviews = int(metadata[idx - 1].split(' ')[0].replace('.', ''))

        except Exception as e:
            n_reviews = 0
            n_photos = 0
        
        item['title'] = title
        item['location'] = location
        item['caption'] = review_text
        item['response'] = response_text
        item['rating'] = rating
        # depends on language, which depends on geolocation defined by Google Maps
        # custom mapping to transform into date shuold be implemented
        item['relative_date'] = relative_date
        # store datetime of scraping and apply further processing to calculate
        # correct date as retrieval_date - time(relative_date)
        item['retrieval_date'] = datetime.now()
        item['absolute_date'] = absolute_date

        return item


    # expand review description
    def __expand_reviews(self):
        # use XPath to load complete reviews
        while True:
            try:
                links = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@class=\'section-expand-review blue-link\'])[position()=1]")))
                print(colored(links, 'red'))
                links.click()
            except:
                break;

    # load more reviews
    def more_reviews(self):
        # use XPath to load complete reviews
        #allxGeDnJMl__text gm2-button-alt
        #<button ved="1i:1,t:18519,e:0,p:kPkcYIz-Dtql-QaL1YawDw:1969" jstcache="1202" jsaction="pane.reviewChart.moreReviews" class="gm2-button-alt jqnFjrOWMVU__button-blue" jsan="7.gm2-button-alt,7.jqnFjrOWMVU__button-blue,0.ved,22.jsaction">14 reviews</button>
        #<button aria-label="14 reviews" vet="3648" jsaction="pane.rating.moreReviews" jstcache="1010" class="widget-pane-link" jsan="7.widget-pane-link,0.aria-label,0.vet,0.jsaction">14 reviews</button>
        links = self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.reviewChart.moreReviews\']')
        print('LINKS HERE', links)
        for l in links:
            l.click()
        time.sleep(2)


    def __scroll(self):
        scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def __get_logger(self):
        # create logger
        logger = logging.getLogger('googlemaps-scraper')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        fh = logging.FileHandler('gm-scraper.log')
        fh.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(fh)

        return logger


    def __get_driver(self, debug=False):
        options = Options()

        if not self.debug:
            options.add_argument("--headless")
        else:
            options.add_argument("--window-size=1366,768")

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=en-GB")
        input_driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        # input_driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        return input_driver


    # util function to clean special characters
    def __filter_string(self, str):
        strOut = str.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        return strOut
