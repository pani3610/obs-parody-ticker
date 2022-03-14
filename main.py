from ticker import Ticker
from feed import Feed

def main():
    f = Feed('The Onion',"https://www.theonion.com/content/feeds/daily",'src/onion.png')
    print(f.name)
    t = Ticker('feed_text_dev.txt')
    t.addFeed(f)
    t.start()

if __name__ == '__main__':
    main()