# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 02:33:00 2021

@author: Mohammad.FT
"""
import gc
from excelStorage import PlaceInfo
from termcolor import colored
from PxPGoogleMaps import GoogleMapsScraper


gc.enable()

ref = {'all_reviews': 0, 'google': 1, 'priceline': 2, 'expedia': 3, 'orbitz': 4, 'travelocity': 5, 'wotif': 6,
       'ebookers': 7, 'trip': 8, 'hotels.com': 9}
ind = {'most_relevant': 0, 'newest': 1, 'highest_rating': 2, 'lowest_rating': 3}
HEADER = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
          'n_review_user', 'n_photo_user', 'url_user']
HEADER_W_SOURCE = ['id_review', 'caption', 'relative_date', 'retrieval_date', "absolute_date", 'rating', 'username',
                   'n_review_user', 'n_photo_user', 'url_user', 'url_source']


def crawler(args, storage):
    global MAX_REVIEW_COUNT_PER_URL
    MAX_REVIEW_COUNT_PER_URL = args.N
    with open(args.i, 'r') as urls_file:
        for url in urls_file:
            with GoogleMapsScraper(debug=args.debug) as scraper:
                name, location = get_place_info(url)
                
                place_info = PlaceInfo(name, location, args.channel, args.sort_by)
                if not storage.continue_process(place_info): continue

                list_reviews = scraper_review(scraper, url, args.channel, args.sort_by)
                if len(list_reviews) > 0:
                    storage.save_reviews(place_info, list_reviews)
                scraper.driver.refresh()


def get_place_info(url):
    index = url.find("/", 34)
    index_latitude = url.find("@", index)
    index_longitude = url.find(",", index_latitude)
    name = url[34:index].replace("+", "").replace("%26", "")
    location = (url[index_latitude:index_longitude], url[index_longitude:url.find(",", index_longitude)])
    return name, location


def scraper_review(scraper, url, channel, sort_by):
    # if args.place: print(scraper.get_account(url))
    sortby_button_not_available = scraper.sort_by(url, ind[sort_by])
    scraper.channeling(ref[channel])
    
    if sortby_button_not_available == 1: return list()
    n = 0
    list_reviews = list()
    visited = 1
    while n < MAX_REVIEW_COUNT_PER_URL:
        print(colored('[Review ' + str(n) + ']', 'cyan'))
        delta_l, spinner = scraper.scroll()
        print(colored("differential of height after scrolling: " + str(delta_l), 'magenta'))
        
        reviews = scraper.get_reviews(n)
        for r in reviews:
            row_data = list(r.values())
            row_data.append(url[:-1])
            list_reviews.append(row_data)
        n += len(reviews)
        
        if len(reviews) == 0:
            visited += 1
            if n >= 1500 or spinner or visited > 4:
                break
        else:
            visited = 1
    print(list_reviews)
    return list_reviews

