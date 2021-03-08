# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""
import argparse
import numpy as np
import pandas as pd
from itertools import cycle
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import requests
from lxml.html import fromstring
from webdriver_manager.firefox import GeckoDriverManager
import time
from PxPDynamicDriver import DynamicDriver
from itertools import cycle
from termcolor import colored
from PxPGoogleMaps import GoogleMapsScraper

ind = {'most_relevant': 0, 'newest': 1, 'highest_rating': 2, 'lowest_rating': 3}
HEADER = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
          'n_review_user', 'n_photo_user', 'url_user']
HEADER_W_SOURCE = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
                   'n_review_user', 'n_photo_user', 'url_user', 'url_source']


def csv_writer(urls, source_field, ind_sort_by, path='data/'):
    outfile = path + '_' + ind_sort_by + urls[:-4] + '_gm_reviews.xlsx'
    writer = pd.ExcelWriter(outfile)
    return writer


if __name__ == '__main__':

    f = open("https10k_pxp.txt")
    doc = f.read()
    lines = doc.split('\n')
    iter = cycle(lines)
    i = 0
    while i < 10:
        print(next(iter).split(":"))
        i+=1

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    driver.get("https://whatismyip.com")
    time.sleep(5)
    set_proxy(driver, http_addr="93.113.63.144", http_port=31596)

    driver.get("https://whatismyip.com")"""
