from ticker import Ticker
from feed import Feed

def main():
    t =Ticker('feed_text_dev.txt','feed_img_dev.png')
    f1 =Feed("https://babylonbee.com/feed",None,'src/babylonbee.png')
    f2 =Feed("https://www.theonion.com/content/feeds/daily",None,'src/onion.png')
    t.addFeed(f1)
    t.addFeed(f2)
    t.start()

if __name__ == '__main__':
    main()