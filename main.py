from ticker import Ticker
from feed import Feed
from threading import Thread
from extrafunctions import *   

def buildTicker():
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    feeds =['https://babylonbee.com/feed', 'https://www.theonion.com/content/feeds/daily', 'http://newsthump.com/feed/', 'https://www.betootaadvocate.com/feed/']
    threads =[]
    for rss_url in feeds:
        thread = Thread(target=addFeedToTicker,args=(rss_url,t))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return(t)

def addFeedToTicker(url:str,ticker:Ticker):
    f = Feed(url)
    ticker.addFeed(f)        

def main():
    t = buildTicker()
    t.connect()
    t.start()
if __name__ == '__main__':
    main()