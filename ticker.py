

from feed import Feed


class Ticker:
    def __init__(self,savetextfile,saveimgfile):
        self.viewport_width = 93 #f(SCREEN_WIDTH,FONT_SIZE)
        '''Average number of characters to fill up the viewport'''
        
        self.text_speed = 6 #f(ticker_width,
        '''Average new characters introduced per second.'''
        
        self.empty_time = 3
        '''Amount of time in seconds we want to ticker to go blank in order to switch feeds.'''
        
        self.textcontainer = savetextfile
        self.imgcontainer = saveimgfile
        
        self.feeds = []

        self.SCREEN_WIDTH = 1205 #pixels
        self.FONT_SIZE = 22
        self.OBS_HORIZONTAL_SCROLL = 80
    
    def recalculateViewportWidth(self):
        pass
    
    def recalculateTextSpeed(self):
        pass

    def updateTextContainer(self,feed:Feed):
        with open(self.textcontainer,"w") as tickertext:
            tickertext.write(feed.text)

    def updateImageContainer(self,feed:Feed):
        pass


    def start(self):
        while(True):
            for feed in self.feeds:
                self.updateTextContainer(feed)
                self.udpateImageContainer(feed)
                switchToNextFeed()

    def switchToNextFeed(self):
        pass

    def addFeed(self,feed:Feed):
        self.feeds.append(Feed)
        pass
    
    def removeFeed(self,Feed):
        pass

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
    


def main():
    update_ticker( "https://www.theonion.com/content/feeds/daily","The Onion",ticker_text_path,cpv)
    export_json("https://babylonbee.com/feed") 
    with open('feed_text.txt','r') as txt:
        text = txt.read()
        print(len(text))   

if __name__ == '__main__':
    main()
