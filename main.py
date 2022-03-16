from ticker import Ticker
from feed import Feed
import os

def abs_path(filename:str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return(os.path.join(dir_path,filename))

def main():
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    feeds ={"https://babylonbee.com/feed":'src/babylonbee.png',
            "https://www.theonion.com/content/feeds/daily":'src/onion.png',
            "http://newsthump.com/feed/":'src/newsthump.png',}
            # "https://www.betootaadvocate.com/feed/":'src/betoota.png'}

    for rss_url,logo_location in feeds.items():        
        f = Feed(rss_url,feed_img_path=abs_path(logo_location))
        t.addFeed(f)
    
    t.start()

if __name__ == '__main__':
    main()