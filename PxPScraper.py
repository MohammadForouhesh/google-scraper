# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""
# -*- coding: utf-8 -*-
from PxPGoogleMaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import csv
from termcolor import colored
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager




ind = {'most_relevant' : 0 , 'newest' : 1, 'highest_rating' : 2, 'lowest_rating' : 3 }
HEADER = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user']
HEADER_W_SOURCE = ['id_review', 'caption', 'relative_date','retrieval_date', "absolute_date", 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user', 'url_source']

def csv_writer(urls, source_field, ind_sort_by, path='data/'):
    outfile = path + '_' + ind_sort_by + urls[:-4] + '_gm_reviews.xlsx'
    writer = pd.ExcelWriter(outfile)
    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=200, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--sort_by', type=str, default='newest', help='sort by most_relevant, newest, highest_rating or lowest_rating')
    parser.add_argument('--place', dest='place', default=True, action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', default=True, action='store_true', help='Add source url to CSV file (for multiple urls in a single file)')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    # store reviews in CSV file
    writer = csv_writer(args.i, args.source, args.sort_by)

    with GoogleMapsScraper(debug=args.debug) as scraper:
        with open(args.i, 'r') as urls_file:
            count = 0
            for url in urls_file:
                index = url.find("/", 34)
                print(url[34:index] + str(count))
                
                if args.place:
                    print(scraper.get_account(url))
                else:
                    error = scraper.sort_by(url, ind[args.sort_by])
                    print(error)

                if error == 0:

                    n = 0

                    if ind[args.sort_by] == 0:
                        scraper.more_reviews()
                    
                    list_reviews = list()
                    while n < args.N:
                        print(colored('[Review ' + str(n) + ']', 'cyan'))
                        reviews = scraper.get_reviews(n)
                        for r in reviews:
                            row_data = list(r.values())
                            if args.source:
                                row_data.append(url[:-1])
                            list_reviews.append(row_data)
                        n += len(reviews)
                        
                    print(list_reviews)
                    sheet = np.array(list_reviews)
                    temp_dataframe = pd.DataFrame(sheet, columns=HEADER)
                    temp_dataframe.to_excel(writer, sheet_name=url[34:index]+str(count))
                count += 1
                    
                        
    writer.close()
