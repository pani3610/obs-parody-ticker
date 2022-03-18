from feed import Feed
from time import sleep
from shutil import copyfile


class Ticker:
    def __init__(self,savetextfile,saveimgfile):
        self.viewport_width = 93 #f(SCREEN_WIDTH,FONT_SIZE)
        '''Average number of characters to fill up the viewport'''
        
        self.text_speed = 6.1575 #6.15 #f(FONT_SIZE,OBS_HORIZONTAL_SCROLL)
        '''Average new characters introduced per second.'''
        
        self.empty_time = 5
        '''Amount of time in seconds we want to ticker to go blank in order to switch feeds.'''

        self.padding = round(self.viewport_width + self.text_speed*self.empty_time)
        
        self.textcontainer = savetextfile
        self.imgcontainer = saveimgfile
        
        self.feeds = []

        self.SCREEN_WIDTH = 1205 #pixels
        self.FONT = {'Type':'Roboto Mono','Size':22}
        self.OBS_HORIZONTAL_SCROLL = 80
        self.max_text_size = 1260
    
    def recalculateViewportWidth(self):
        pass
    
    def recalculateTextSpeed(self):
        pass

    def updateTextContainer(self,feed:Feed):
        with open(self.textcontainer,"w") as tickertext:
            tickertext.write(feed.text.raw_string)

    def updateImageContainer(self,feed:Feed):
        if feed.image_path != None:
            copyfile(feed.image_path,self.imgcontainer)
        else:
            print(f'{feed.name} has no image source')


    def start(self):
        while(True):
            for feed in self.feeds:
                print(feed.name)
                self.updateTextContainer(feed)
                self.updateImageContainer(feed)
                self.switchToNextFeed(feed)

    def switchToNextFeed(self,feed:Feed):
        sleep_time = (feed.calculateSize()/self.text_speed)
        print(f'Going to sleep for {sleep_time:.2f} seconds')
        sleep(sleep_time)

    def addFeed(self,feed:Feed):
        self.addPaddingToFeed(feed)
        self.feeds.append(feed)

    
    def removeFeed(self,Feed):
        pass


    def addPaddingToFeed(self,feed:Feed):
        size = feed.calculateSize()
        if feed.calculateSize()+self.padding>self.max_text_size:
            print(f'for {feed.name}: Feed text too large. Reducing number of headlines')
            self.reduceFeedSizeToFit(feed)
        
        feed.text.raw_string = self.padding*" "+feed.text.raw_string

           
    def reduceFeedSizeToFit(self,feed:Feed):
        while(feed.calculateSize()+self.padding>self.max_text_size):
            new_hl_count = feed.headlines_count - 1
            feed.updateHeadlinesCount(new_hl_count)
        
        print(f'Final headline count:{new_hl_count}')

'''
screen_width = None
font_size = None

cpv = 95 #average number of characters to fill up the viewport
cps = 5 #average new characters intrpduced per second. Horizontal scroll speed in OBS set to 40.
obs_horizontal_scroll = None

ticker_text_path = 'feed_text_dev.txt'

feed_urls = {"The Babylon Bee" : "https://babylonbee.com/feed"}
# feed_urls = {"The Onion": "https://www.theonion.com/content/feeds/daily"}

def update_ticker(url,news_source,target_file,cpv):
    headlines_list = extract_headlines(url,10)
    courtesy_text = f"This newsreel is brought to you by '{news_source}'"
    display_text = [courtesy_text]
    display_text.extend(headlines_list)
    display_text.append(courtesy_text)
    print(display_text)
    export_text(display_text,target_file,3*cpv)

def switch_source():
    pass
    
'''

def main():
    t =Ticker('feed_text_dev.txt','feed_img_dev.png')
    f1 =Feed("https://www.betootaadvocate.com/feed/",None,'src/betoota.png')
    f2 =Feed("https://www.theonion.com/content/feeds/daily",None,'src/onion.png')
    t.addFeed(f1)
    t.addFeed(f2)
    t.start()
if __name__ == '__main__':
    main()
