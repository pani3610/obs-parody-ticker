from ticker import Ticker
from feed import Feed
from main import abs_path
import os


def run():
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    feeds ={"https://babylonbee.com/feed":'src/babylonbee.png',
            "https://www.theonion.com/content/feeds/daily":'src/onion.png',
            "http://newsthump.com/feed/":'src/newsthump.png',            
            "https://www.betootaadvocate.com/feed/":'src/betoota.png'}

    for rss_url,logo_location in feeds.items():        
        f = Feed(rss_url,feed_img_path=abs_path(logo_location))
        t.addFeed(f)
    
    # t.start()
def calculateExecutionTime(function):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        function()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')

if __name__ == '__main__':
    calculateExecutionTime(run)
    