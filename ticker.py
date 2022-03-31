from feed import Feed
from time import sleep
from shutil import copyfile
from threading import Event,Thread

class Ticker:
    def __init__(self,savetextfile,saveimgfile):
        self.viewport_width = 93 #f(SCREEN_WIDTH,FONT_SIZE)
        '''Average number of characters to fill up the viewport'''
        
        self.text_speed = 6.155 #6.1575 #6.15 #f(FONT_SIZE,OBS_HORIZONTAL_SCROLL)
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
        self.logo_size = (32,32) #(width,height)
        self.start_thread = None
        self.stop_event = Event()
    
    def recalculateViewportWidth(self):
        pass
    
    def recalculateTextSpeed(self):
        pass

    def updateTextContainer(self,feed:Feed):
        with open(self.textcontainer,"w") as tickertext:
            tickertext.write(feed.text.raw_string)

    def updateImageContainer(self,feed:Feed):
        if feed.logo.savefile != None:
            copyfile(feed.logo.savefile,self.imgcontainer)
        else:
            print(f'{feed.name} has no image source')


    def startTickerLoop(self):
        while(True):
            for feed in self.feeds:
                if(self.stop_event.isSet()):
                    return()
                print(feed.returnFeedSummary())
                self.updateTextContainer(feed)
                self.updateImageContainer(feed)
                self.switchToNextFeed(feed)
                
        
    def start(self):
        self.stop_event.clear() #clearing stop event just in case you are restarting after stopping
        self.start_thread = Thread(target=self.startTickerLoop,name='Ticker thread') #reinitializing thread because a thread can be started only once.
        self.start_thread.start()
        

    def switchToNextFeed(self,feed:Feed):
        sleep_time = (feed.calculateSize()/self.text_speed)
        print(f'Going to sleep for {sleep_time:.2f} seconds')
        self.stop_event.wait(sleep_time)

    def addFeed(self,feed:Feed):
        self.addPaddingToFeed(feed)
        self.resizeFeedLogo(feed)
        self.feeds.append(feed)

    
    def removeFeed(self,Feed):
        pass


    def addPaddingToFeed(self,feed:Feed):
        size = feed.calculateSize()
        if feed.calculateSize()+self.padding>self.max_text_size:
            print(f'for {feed.name}: Feed text too large. Reducing number of headlines. Original Headline Count : {feed.headlines_count}')
            self.reduceFeedSizeToFit(feed)
        
        feed.text.raw_string = self.padding*" "+feed.text.raw_string

           
    def reduceFeedSizeToFit(self,feed:Feed):
        while(feed.calculateSize()+self.padding>self.max_text_size):
            new_hl_count = feed.headlines_count - 1
            feed.updateHeadlinesCount(new_hl_count)
        
        print(f'Final headline count:{feed.headlines_count}')
    
    def resizeFeedLogo(self,feed):
        feed.logo.resize(self.logo_size)
    
    def stop(self):
        print('Stopping ticker')
        self.stop_event.set()

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
    f1 =Feed("https://www.betootaadvocate.com/feed/")
    f2 =Feed("https://www.theonion.com/content/feeds/daily")
    t.addFeed(f1)
    t.addFeed(f2)
    t.start()
    print('Stopping in 10 seconds')
    sleep(10)
    t.stop()
    print('starting again in 5 seconds')
    sleep(5)
    t.start()
    
if __name__ == '__main__':
    main()
