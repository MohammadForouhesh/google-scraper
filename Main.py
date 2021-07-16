from datetime import datetime
from PxPScraper import crawler, ref, ind
import argparse
from termcolor import colored


def main(args):
    startTime = datetime.now()
    if not args.all: crawler(args)
    else:
        for channel in ref:
            for sort in ind:
                args.channel = channel
                args.sort_by = sort
                crawler(args)

    print(colored(datetime.now() - startTime, 'cyan'))
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=2000, help='Number of reviews to scrape') # to constants
    parser.add_argument('--i', type=str, default='LCBO-ReviewsLink.txt', help='target URLs file')
    parser.add_argument('--all', dest='all', type=bool, default=False,
                        help="crawl over every possible option and choice.")
    parser.add_argument('--sort_by', type=str, default='most_relevant',
                        help='sort by most_relevant, newest, highest_rating or lowest_rating')
    parser.add_argument('--channel', dest='channel', type=str, default='all_reviews',
                        help="change reviews channel by all_reviews, google, hotels.com, priceline, expedia, orbitz, "
                             "travelocity, wotif, ebookers and trip")
    parser.add_argument('--place', dest='place', default=False, action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true',
                        help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', default=False, action='store_true',
                        help='Add source url to CSV file (for multiple urls in a single file)')
    parser.add_argument('--proxy', dest='proxy', default="refined_proxies.txt",
                        help='Add proxy file to rotate IP address dynamically.')
    
    args = parser.parse_args()
    main(args);
