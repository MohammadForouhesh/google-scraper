# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""
import os
import argparse
import numpy as np
import pandas as pd
import PxPDynamicProxy
from pathlib import Path
from itertools import cycle
from termcolor import colored
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

    with GoogleMapsScraper(debug=args.debug) as scraper:
        with open(args.i, 'r') as urls_file:
            count = 0
            for url in urls_file:
                index = url.find("/", 34)
                print(url[34:index] + str(count))
                # store reviews in CSV file
                writer, path = csv_writer(url[34:index], args.channel, args.sort_by)

                if args.place:
                    print(scraper.get_account(url))

                else:
                    error = scraper.sort_by(url, ind[args.sort_by])
                    try: error = scraper.channeling(ref[args.channel])
                    except IndexError as e:
                        sheet = np.array(['error, no such channel'])
                        temp_dataframe = pd.DataFrame(sheet)
                        temp_dataframe.to_excel(writer, sheet_name=url[34:index] + str(count))
                        writer.close()
                        os.remove(path)
                        continue
                    print(error)

                if error == 0:

                    n = 0

                    # if ind[args.sort_by] == 0:
                    #    scraper.more_reviews()

                    list_reviews = list()
                    visited = 1
                    while n < args.N:
                        for iter_scroll in range(0, 20):
                            try:
                                scraper.scroll()
                            except:
                                pass

                        print(colored('[Review ' + str(n) + ']', 'cyan'))
                        reviews = scraper.get_reviews(n)
                        for r in reviews:
                            row_data = list(r.values())
                            if args.source:
                                row_data.append(url[:-1])
                            list_reviews.append(row_data)
                        n += len(reviews)

                        if len(reviews) == 0:
                            if visited < 100:
                                if visited % 10 == 0 or n > 1600:
                                    q = input("some error occurred, rotate IP?[y/N]:")
                                    if q.lower() == 'n': break
                                # scraper.driver.refresh()
                                # scraper.sort_by(url, ind[args.sort_by])
                                proxy = next(proxy_iter).split(":")
                                PxPDynamicProxy.set_proxy(scraper.driver, http_addr=proxy[0], http_port=int(proxy[1]))
                                visited += 1
                            else:
                                break
                        else:
                            visited = 1

                    print(list_reviews)
                    sheet = np.array(list_reviews)
                    temp_dataframe = pd.DataFrame(sheet, columns=HEADER)
                    temp_dataframe.to_excel(writer, sheet_name=url[34:index] + str(count))
                #writer.close()
                count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=200, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--all', dest='all', type=bool, default=False,
                        help="crawl over every possible option and choice.")
    parser.add_argument('--sort_by', type=str, default='highest_rating',
                        help='sort by most_relevant, newest, highest_rating or lowest_rating')
    parser.add_argument('--channel', dest='channel', type=str, default='trip',
                        help="change reviews channel by all_reviews, google, hotels.com, priceline, expedia, orbitz, "
                             "travelocity, wotif, ebookers and trip")
    parser.add_argument('--place', dest='place', default=True, action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', default=True, action='store_true',
                        help='Add source url to CSV file (for multiple urls in a single file)')
    parser.add_argument('--proxy', dest='proxy', default="https10k_pxp.txt",
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
