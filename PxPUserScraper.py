# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""

from PxPGoogleUser import GoogleUserScraper
from datetime import datetime, timedelta
import pyautogui
import argparse
import csv
from termcolor import colored
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


ind = {'most_relevant' : 0 , 'newest' : 1, 'highest_rating' : 2, 'lowest_rating' : 3 }
HEADER = ['title', 'location', 'caption', 'response', 'rating', 'relative_date', 'retrieval_date', "absolute_date"]

def csv_writer(urls, path='User/'):
    outfile = path + 'user_reviews.xlsx'
    writer = pd.ExcelWriter(outfile, engine = 'xlsxwriter')
    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=80, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls_user.txt', help='target URLs file')
    parser.add_argument('--source', dest='source', default=True, action='store_true', help='Add source url to CSV file (for multiple urls in a single file)')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    # store reviews in CSV file
    writer = csv_writer(args.i)

    loc_temp = ("data/deehurst_newest_gm_reviews.xlsx")
    count = 0
    df_temp = pd.read_excel(loc_temp, index_col=1)
    for index in range(0, len(df_temp)):
        print(df_temp["username"].iloc[index])
        url = df_temp['url_user'].iloc[index]
        if url.find("www.google.com") == -1:
            continue;
            
        n = 0
        list_reviews = list()
        
        scraper = GoogleUserScraper(debug=args.debug)
        try: 
            scraper.driver.get(url)
            time.sleep(4)
        except:
            pyautogui.click(2025, 2100)
            pyautogui.click(x=3050, y=1200)
            time.sleep(1)
            pyautogui.click(x=3050, y=1200)
            time.sleep(10)
            scraper.driver.get(url)
            time.sleep(4)
            
        user = scraper.parse_user()
        print(user)
        args.N = user["total"]
        while n < args.N:
            print(colored('[Review ' + str(n) + ']', 'cyan'))
            reviews = scraper.get_reviews(n)
            for r in reviews:
                row_data = list(r.values())
                if args.source:
                    row_data.append(url[:-1])
                list_reviews.append(row_data)
            n += len(reviews)
            
            if len(reviews) == 0:
                n += 1
            
        if len(list_reviews) > 0:
            sheet = np.array(list_reviews)
            temp_dataframe = pd.DataFrame(sheet, columns=HEADER)
            username = df_temp["username"].iloc[index].replace(" ", "-")
            contribution = user["contributions"].replace(" ", "")
            string = username[:12] + "_" + contribution
            temp_dataframe.to_excel(writer, sheet_name=string)

        scraper.driver.close()
        scraper.driver.quit()
        count += 1
    
    writer.save()
    writer.close()
