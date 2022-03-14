from feed import *

class Ticker:
    def __init__(self,savefile):
        self.viewport_width = 95 #f(SCREEN_WIDTH,FONT_SIZE)
        '''Average number of characters to fill up the viewport'''
        
        self.text_speed = 5 #f(ticker_width,
        '''Average new characters introduced per second. Horizontal scroll speed in OBS set to 40.'''
        
        self.savefile = 'feed_text_dev.txt'
        
        self.empty_time = 3
        '''Amount of time in secs we want to ticker to go blank in order'''

        self.SCREEN_WIDTH = None
        self.FONT_SIZE = None
        self.OBS_HORIZONTAL_SCROLL = 40

    def start(self):
        pass

    def switchToNextFeed(self):
        pass

    def addFeed(self,Feed):
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
    
with open('feed_text.txt','r') as txt:
    text = txt.read()
    print(len(text))

update_ticker( "https://www.theonion.com/content/feeds/daily","The Onion",ticker_text_path,cpv)
export_json("https://babylonbee.com/feed")