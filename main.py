from ticker import Ticker
from feed import Feed
import os

def abs_path(filename:str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return(os.path.join(dir_path,filename))

def main():
    
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    f1 =Feed("https://babylonbee.com/feed",None,abs_path('src/babylonbee.png'))
    f2 =Feed("https://www.theonion.com/content/feeds/daily",None,abs_path('src/onion.png'))
    t.addFeed(f1)
    t.addFeed(f2)
    t.start()

if __name__ == '__main__':
    main()