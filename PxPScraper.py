# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""

import argparse
import os
from itertools import cycle
from pathlib import Path

from datetime import datetime

import numpy as np
import pandas as pd
from termcolor import colored


import PxPDynamicProxy
from PxPGoogleMaps import GoogleMapsScraper

ref = {'all_reviews': 0, 'google': 1, 'priceline': 2, 'expedia': 3, 'orbitz': 4, 'travelocity': 5, 'wotif': 6,
       'ebookers': 7, 'trip': 8, 'hotels.com': 9}
ind = {'most_relevant': 0, 'newest': 1, 'highest_rating': 2, 'lowest_rating': 3}
HEADER = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
          'n_review_user', 'n_photo_user', 'url_user']
HEADER_W_SOURCE = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
                   'n_review_user', 'n_photo_user', 'url_user', 'url_source']


def csv_writer(name, channel, ind_sort_by, path='data/'):
    name = name.replace("+", "").replace("%26", "")
    Path(path + name).mkdir(parents=True, exist_ok=True)
    outfile = path + name + "/" + channel + "_" + ind_sort_by + '_gm_reviews.xlsx'
    writer = pd.ExcelWriter(outfile)
    return writer, outfile


def crawler(args):
    # store reviews in CSV file
    # writer = csv_writer(args.i, args.channel, args.sort_by)

    proxy_file = open(args.proxy)
    doc = proxy_file.read()
    lines = doc.split('\n')
    proxy_iter = cycle(lines)

    with open(args.i, 'r') as urls_file:
        for url in urls_file:
            count = 0
            with GoogleMapsScraper(debug=args.debug) as scraper:
                index = url.find("/", 34)
                print(url[34:index] + str(count))
                # store reviews in CSV file
                writer, path = csv_writer(url[34:index], args.channel, args.sort_by)

                if args.place:
                    print(scraper.get_account(url))

                else:
                    error = scraper.sort_by(url, ind[args.sort_by])
                    try: error = scraper.channeling(ref[args.channel])
                    except:
                        sheet = np.array(['error, no such channel'])
                        temp_dataframe = pd.DataFrame(sheet)
                        temp_dataframe.to_excel(writer, sheet_name=url[34:index] + str(count))
                        writer.close()
                        os.remove(path)
                        continue
                    print(error)

                if error == 0:
                    n = 0
                    list_reviews = list()
                    visited = 1
                    try:
                        while n < args.N:
                            print(colored('[Review ' + str(n) + ']', 'cyan'))
                            delta_l, spinner = scraper.scroll()
                            print(colored("differential of height after scrolling: " + str(delta_l), 'magenta'))

                            reviews = scraper.get_reviews(n)
                            for r in reviews:
                                row_data = list(r.values())
                                if args.source:
                                    row_data.append(url[:-1])
                                list_reviews.append(row_data)
                            n += len(reviews)

                            if len(reviews) == 0:
                                visited += 1
                                if n >= 1500 or spinner or visited > 20:
                                    break
                                if visited % 5 == 0:
                                    proxy = next(proxy_iter)
                                    print("rotating ip")
                                    proxy = proxy.split(":")
                                    PxPDynamicProxy.set_proxy(scraper.driver, http_addr=proxy[0], http_port=int(proxy[1]))
                            else:
                                visited = 1
                    except Exception as e:
                        print(colored("ERROR:" + e.code, 'red'))

                    print(list_reviews)
                    if len(list_reviews) > 0:
                        sheet = np.array(list_reviews)
                        temp_dataframe = pd.DataFrame(sheet, columns=HEADER)
                        temp_dataframe.to_excel(writer, sheet_name=url[34:index] + str(count))
                    scraper.driver.refresh()
                writer.close()
                count += 1


if __name__ == '__main__':
    startTime = datetime.now()
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=2000, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--all', dest='all', type=bool, default=True,
                        help="crawl over every possible option and choice.")
    parser.add_argument('--sort_by', type=str, default='most_relevant',
                        help='sort by most_relevant, newest, highest_rating or lowest_rating')
    parser.add_argument('--channel', dest='channel', type=str, default='all_reviews',
                        help="change reviews channel by all_reviews, google, hotels.com, priceline, expedia, orbitz, "
                             "travelocity, wotif, ebookers and trip")
    parser.add_argument('--place', dest='place', default=True, action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', default=True, action='store_true',
                        help='Add source url to CSV file (for multiple urls in a single file)')
    parser.add_argument('--proxy', dest='proxy', default="refined_proxies.txt",
                        help='Add proxy file to rotate IP address dynamically.')

    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()
    if not args.all: crawler(args)
    else:
        for channel in ref:
            for sort in ind:
                args.channel = channel
                args.sort_by = sort
                crawler(args)

    print(colored(datetime.now() - startTime, 'cyan'))

# errors:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSDidNotSucceed
