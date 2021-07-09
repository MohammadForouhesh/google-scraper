# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:50:15 2021

@author: Mohammad.FT
"""

import logging
import time
import traceback
from datetime import datetime
import numpy as np
import parsedatetime as pdt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager

GM_WEBPAGE = 'https://www.google.com/maps/'
MAX_WAIT = 10
MAX_RETRY = 5
MAX_SCROLLS = 40


class GoogleMapsScraper:
    def __init__(self, debug=False):
        self.debug = debug
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()
        self.type = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:    traceback.print_exception(exc_type, exc_value, tb)

        self.driver.close()
        self.driver.quit()

        return True

    def sort_by(self, url, ind):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, MAX_WAIT)

        # open dropdown menu
        clicked = False
        tries = 0

        while not clicked and tries < MAX_RETRY:
            try:
                try:
                    menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-value=\'Sort\']')))
                    self.type = 1
                except:
                    menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class=\'gm2-body-1 k5lwKb\'])[position()=2]")))
                    self.type = 2
                    
                menu_bt.click()
                clicked = True
                time.sleep(3)
            except Exception as e:
                tries += 1
                self.logger.warning('Failed to click recent button')

            # failed to open the dropdown
            if tries == MAX_RETRY:
                return -1

        # element of the list specified according to ind
        time.sleep(1)
        tries = 0
        clicked = False
        while not clicked and tries < MAX_RETRY:
            try:
                recent_rating_bt = self.driver.find_elements_by_xpath('//li[@role=\'menuitemradio\']')[ind]
                clicked = True
            except:
                tries += 1
                self.logger.warning('Failed to click menu buttons')
        recent_rating_bt.click()

        # wait to load review (ajax call)
        time.sleep(5)

        return 0

    def channeling(self, ref):
        print(self.type)
        if self.type == 1: return 1
        wait = WebDriverWait(self.driver, MAX_WAIT)

        # open dropdown menu
        clicked = False
        tries = 0

        while not clicked and tries < MAX_RETRY:
            try:
                try:    menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class=\'gm2-body-1 k5lwKb\'])[position()=1]")))
                except: pass

                menu_bt.click()
                clicked = True
                time.sleep(3)
            except Exception as e:
                tries += 1
                self.logger.warning('Failed to click channeling button')

            # failed to open the dropdown
            if tries == MAX_RETRY:
                print(Exception("No such menu"))
                return -1

        # element of the list specified according to ref
        time.sleep(1)
        try:
            recent_rating_bt = self.driver.find_elements_by_xpath('//li[@role=\'menuitemradio\']')[ref]
            recent_rating_bt.click()

            # wait to load review (ajax call)
            time.sleep(5)
        except: pass

        return 0

    def get_reviews(self, offset):
        # scroll to load reviews
        # wait for other reviews to load (ajax)
        time.sleep(1)
        self.__scroll()
        # expand review text
        self.__expand_reviews()
        # parse reviews
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        rblock = response.find_all('div', class_='ODSEW-ShBeI-content')
        #section-review-content
        parsed_reviews = []
        for index, review in enumerate(rblock):
            if index >= offset:
                parsed_reviews.append(self.__parse(review))
                print(self.__parse(review))
                self.driver.execute_script("""
                    var element = document.querySelector(".ODSEW-ShBeI-content");
                    if (element)
                        element.parentNode.removeChild(element);
                    """)
        rblock.clear()

        return parsed_reviews

    def get_account(self, url):

        self.driver.get(url)

        # ajax call also for this section
        time.sleep(1)

        resp = BeautifulSoup(self.driver.page_source, 'html.parser')

        place_data = self.__parse_place(resp)

        return place_data

    def __parse(self, review):
        
        item = {}
        
        # section-review-action-menu
        try:    id_review = review.find('button', class_='ODSEW-ShBeI-JIbuQc-menu ODSEW-ShBeI-JIbuQc-menu-SfQLQb-title')['data-review-id']
        except: id_review = "Not a google review"

        # section-review-title
        username = review.find('div', class_='ODSEW-ShBeI-title').find('span').text
        
        # section-review-text
        try:                    review_text = self.__filter_string(review.find('span', class_='ODSEW-ShBeI-text').text)
        except Exception as e:  review_text = None
        # section-review-stars
        #
        # section-review-publish-date
        try:
            rating = float(review.find('span', class_='ODSEW-ShBeI-H1e3jb')['aria-label'].split(' ')[1])
            relative_date = review.find('span', class_='ODSEW-ShBeI-RgZmSc-date').text
        except:
            __rating = review.find('span', class_='ODSEW-ShBeI-RGxYjb-wcwwM').text
            relative_date = review.find('span', class_='ODSEW-ShBeI-RgZmSc-date-J42Xof-Hjleke').find('span').text
            __rating = __rating.split("/")
            numerator = float(__rating[0])
            denominator = float(__rating[1])
            rating = (numerator / denominator) * 5

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

        except Exception as e:
            n_photos = 0

        try:
            # section-review-subtitle
            n_reviews = review.find('div', class_='ODSEW-ShBeI-VdSJob').find_all('span')[1].text.replace("・", "")
            print(colored(n_reviews, 'red'))
            n_reviews = n_reviews[:-8]

        except:
            n_reviews = 0

        user_url = review.find('a')['href']

        item['id_review'] = id_review
        item['caption'] = review_text

        # depends on language, which depends on geolocation defined by Google Maps
        # custom mapping to transform into date shuold be implemented
        item['relative_date'] = relative_date
        # store datetime of scraping and apply further processing to calculate
        # correct date as retrieval_date - time(relative_date)
        item['retrieval_date'] = datetime.now()
        item['absolute_date'] = absolute_date
        item['rating'] = rating
        item['username'] = username
        item['n_review_user'] = n_reviews
        item['n_photo_user'] = n_photos
        item['url_user'] = user_url
        
        return item

    def __parse_place(self, response):
        place = {}
        try:    place['overall_rating'] = float(response.find('div', class_='gm2-display-2').text.replace(',', '.'))
        except: place['overall_rating'] = 'NOT FOUND'

        try:    place['n_reviews'] = int(response.find('div', class_='gm2-caption').text.replace('.', '').replace(',', '').split(' ')[0])
        except: place['n_reviews'] = 0

        return place

    # expand review description
    def __expand_reviews(self):
        # use XPath to load complete reviews
        temp_link = None
        visited = 0
        while True:
            try:
                links = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@jsaction=\'pane.review.expandReview\'])[position()=1]")))
                print(colored(links, 'red'))
                links.click()
                if links == temp_link:
                    visited += 1
                    if visited > 10:
                        # links.clear()
                        self.driver.execute_script("""
                            var element = document.querySelector(".ODSEW-KoToPc-ShBeI.gXqMYb-hSRGPd");
                            element.click()
                            if (element)
                                element.parentNode.removeChild(element);
                            """)
                        # raise Exception("")
                else: visited = 1
                temp_link = links
            except:
                break

    # load more reviews
    def more_reviews(self):
        # use XPath to load complete reviews
        # allxGeDnJMl__text gm2-button-alt
        # <button ved="1i:1,t:18519,e:0,p:kPkcYIz-Dtql-QaL1YawDw:1969" jstcache="1202" jsaction="pane.reviewChart.moreReviews" class="gm2-button-alt jqnFjrOWMVU__button-blue" jsan="7.gm2-button-alt,7.jqnFjrOWMVU__button-blue,0.ved,22.jsaction">14 reviews</button>
        # <button aria-label="14 reviews" vet="3648" jsaction="pane.rating.moreReviews" jstcache="1010" class="widget-pane-link" jsan="7.widget-pane-link,0.aria-label,0.vet,0.jsaction">14 reviews</button>
        links = self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.review.expandReview\']')
        print('LINKS HERE', links)
        for l in links:
            l.click()
        time.sleep(1)

    def scroll(self):
        height = list()
        height.append(self.__scroll())
        self.__expand_reviews()
        iter_index = 0
        spinner = False
        while height[-1] - height[0] < 50000000 and iter_index < 500000:
            try:
                height.append(self.__scroll())
                self.__expand_reviews()
            except Exception as e:
                print(e)
                pass
            iter_index += 1

            if not self.driver.find_elements_by_class_name("wo1ice-loading-aZ2wEe")[-1].is_displayed():
                #mapsConsumerUiSubviewSectionLoading__section-loading-spinner
                print(colored("End of document!", 'yellow'))
                spinner = True
                break
            np_height = np.array(height)
            if np_height[-300:].std() == 0 and iter_index > 300:
                break

        return height[-1] - height[0], spinner

    def __scroll(self):
        #scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.cYB2Ge-oHo7ed.cYB2Ge-ti6hGc')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        
        section_layout = self.driver.find_elements_by_class_name('section-layout')[-1]
        return section_layout.size['height']
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

    def __get_driver(self):
        chrome_options = Options()
        
        if self.debug: chrome_options.add_argument("--window-size=1366,768")
        else:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        # input_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        input_driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        # input_driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        print("Chrome Headless Browser Invoked")

        return input_driver

    # util function to clean special characters
    def __filter_string(self, str):
        strOut = str.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        return strOut

    def __filter_digit(self, string: str):
        temp = str()
        for char in string:
            if 48 <= ord(char) <= 59:
                temp += char

        return temp