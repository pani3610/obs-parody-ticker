from ticker import Ticker
from feed import Feed
import os
import timeit
# def create_ticker():
#     t = Ticker('a','b')

# print(timeit.timeit(stmt='create_ticker()',setup='from __main__ import create_ticker'))



def abs_path(filename:str):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # return(os.path.join(dir_path,filename))
    return(filename)

def main():
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    feeds ={"https://babylonbee.com/feed":'src/babylonbee.png',
            "https://www.theonion.com/content/feeds/daily":'src/onion.png',
            "http://newsthump.com/feed/":'src/newsthump.png',            
            "https://www.betootaadvocate.com/feed/":'src/betoota.png'}

    for rss_url,logo_location in feeds.items():        
        f = Feed(rss_url,feed_img_path=abs_path(logo_location))
        t.addFeed(f)
    
    # t.start()

def main_alt():
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    f1 = Feed("https://babylonbee.com/feed",feed_img_path='src/babylonbee.png')
    f2 = Feed("https://babylonbee.com/feed",feed_img_path='feed_img_dev.png')
    f3 = Feed("https://babylonbee.com/feed",feed_img_path='feed_img_dev.png')
    t.addFeed(f1)
    t.addFeed(f2)
    t.addFeed(f3)


print(timeit.timeit(stmt='main()',setup='from __main__ import main',number=1))
