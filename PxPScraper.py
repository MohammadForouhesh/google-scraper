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


def set_proxy(driver, http_addr='', http_port=0, ssl_addr='', ssl_port=0, socks_addr='', socks_port=0):
    driver.execute("SET_CONTEXT", {"context": "chrome"})

    try:
        driver.execute_script("""
          Services.prefs.setIntPref('network.proxy.type', 1);
          Services.prefs.setCharPref("network.proxy.http", arguments[0]);
          Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
          Services.prefs.setCharPref("network.proxy.ssl", arguments[2]);
          Services.prefs.setIntPref("network.proxy.ssl_port", arguments[3]);
          Services.prefs.setCharPref('network.proxy.socks', arguments[4]);
          Services.prefs.setIntPref('network.proxy.socks_port', arguments[5]);
          """, http_addr, http_port, ssl_addr, ssl_port, socks_addr, socks_port)

    finally:
        driver.execute("SET_CONTEXT", {"context": "content"})


if __name__ == '__main__':

    f = open("https10k_pxp.txt")
    doc = f.read()
    lines = doc.split('\n')
    iter = cycle(lines)
    i = 0
    while i < 10:
        print(next(iter).split(":"))
        i+=1
    """driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    #set_proxy(driver, http_addr="93.113.63.144", http_port=37833)
    #91.251.104.220
    driver.get("https://whatismyip.com")
    time.sleep(5)
    set_proxy(driver, http_addr="93.113.63.144", http_port=31596)

    driver.get("https://whatismyip.com")"""
