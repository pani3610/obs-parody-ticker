from feed import Feed
from time import sleep
from shutil import copyfile
from threading import Event,Thread,activeCount
from obswebsocket import obsws,requests,exceptions,events
import os
from dotenv import load_dotenv
from extrafunctions import * 
import sys

class Ticker:
    def __init__(self,savetextfile,saveimgfile):
        # self.viewport_width = 93 #f(SCREEN_WIDTH,FONT_SIZE)
        '''Average number of characters to fill up the viewport'''
        
        # self.text_speed = 6.155 #6.1575 #6.15 #f(FONT_SIZE,OBS_HORIZONTAL_SCROLL)
        '''Average new characters introduced per second.'''
        
        self.empty_time = 5
        '''Amount of time in seconds we want to ticker to go blank in order to switch feeds.'''

        self.padding = None#round(self.viewport_width + self.text_speed*self.empty_time)
        
        self.textcontainer = savetextfile
        self.imgcontainer = saveimgfile
        
        self.feeds = []

        self.SCREEN_WIDTH = 1205 #pixels
        self.FONT = {'Type':'Roboto Mono','Size':22}
        self.OBS_HORIZONTAL_SCROLL = 80
        self.max_size = 16380
        self.logo_size = (32,32) #(width,height)
        self.play_thread = None
        self.pause_event = Event()
    
        self.ticker_scenes = []
        self.obs_quit_event  = Event()

    def connect(self,host=None,port=None,password=None):
        self.obs = OBSSession(host,port,password)
        self.obs.connect()
    
    
    def start(self):
        #getOBSTickerObject details or create if required
        # self.video_info = self.getObsVideoData()
        # self.obs_text = self.getObsSourceData()
        # print(self.obs.getVideoData().baseWidth)
        #calculateviewportwidth
        self.calculatePadding()
        # self.checkAllFeedSize()
        #calculate padding based on font and viewportwidth
        #startsession
        pass
    def calculateViewportWidth(self):
        self.viewport_width = self.obs.getVideoData().baseWidth - self.obs.getSourceData().position.x
        return(self.viewport_width)
    
    def calculatePadding(self):
        self.calculateViewportWidth()
        self.getScrollSpeed()
        resolution = 100
        with open(self.textcontainer,"w") as txtfile:
            txtfile.write(resolution*" ")
        sleep(1)
        single_space_width = self.obs.getSourceData().sourceWidth/resolution
        print('SSW',single_space_width)
        self.padding = round((self.viewport_width + self.empty_time*self.scroll_speed)/single_space_width)
        return(self.padding)

    def getScrollSpeed(self):
        filters = self.obs.getSourceData().filters
        self.scroll_speed = 0
        for filter in filters:
            print(filter.__dict__)
            if (filter.type == "scroll_filter" and filter.enabled):
                self.scroll_speed = filter.settings.speed_x
        return(self.scroll_speed)

    def updateTextContainer(self,feed:Feed):
        with open(self.textcontainer,"w") as tickertext:
            tickertext.write(self.padding*" ")
            tickertext.write(feed.text.raw_string)

    def updateImageContainer(self,feed:Feed):
        if feed.logo.savefile != None:
            copyfile(feed.logo.savefile,self.imgcontainer)
        else:
            print(f'{feed.name} has no image source')


    def startTickerLoop(self):
        while(True):
            for feed in self.feeds:
                if(self.pause_event.isSet()):
                    return()
                print(feed.returnFeedSummary())
                self.updateTextContainer(feed)
                self.updateImageContainer(feed)
                self.switchToNextFeed(feed)
                
        
    def play(self):
        self.pause_event.clear() #clearing stop event just in case you are restarting after stopping
        self.play_thread = Thread(target=self.startTickerLoop,name='Ticker thread') #reinitializing thread because a thread can be started only once.
        self.play_thread.start()
        

    def switchToNextFeed(self,feed:Feed):
        sleep_time = (feed.calculateSize()/self.text_speed)
        print(f'Going to sleep for {sleep_time:.2f} seconds')
        self.pause_event.wait(sleep_time)

    def addFeed(self,feed:Feed):
        #self.addPaddingToFeed(feed) #Padding to be added to the containerfile and NOT to modify feedtext
        self.resizeFeedLogo(feed) #Maybe resize the containerfile than the feedlogo file
        self.feeds.append(feed)

    
    def removeFeed(self,Feed):
        pass


    def checkAllFeedSize(self):
        for feed in self.feeds:
            self.updateTextContainer(feed)
            print(feed.name,self.obs.getSourceData().sourceWidth)
            if(self.obs.getSourceData().sourceWidth > self.max_size):
                print(f'for {feed.name}: Feed text too large. Reducing number of headlines. Original Headline Count : {feed.headlines_count}')
                self.reduceFeedSizeToFit(feed)
            sleep(1)

           
    def reduceFeedSizeToFit(self,feed:Feed):
        while(self.obs.getSourceData().sourceWidth > self.max_size):
            new_hl_count = feed.headlines_count - 1
            feed.updateHeadlinesCount(new_hl_count)
            self.updateTextContainer(feed)
        
        print(f'Final headline count:{feed.headlines_count}')
    
    def resizeFeedLogo(self,feed):
        feed.logo.resize(self.logo_size)
    
    def pause(self):
        print('Stopping ticker')
        self.pause_event.set()
        self.play_thread.join()

    def startOrStopTicker(self,transition_event:events.TransitionBegin):
        # print(self.ticker_scenes)
        if(transition_event.getFromScene() not in self.ticker_scenes and transition_event.getToScene() in self.ticker_scenes):
            print('start ticker')
            self.ticker.start()
        elif(transition_event.getFromScene() in self.ticker_scenes and transition_event.getToScene() not in self.ticker_scenes):
            print('stop Ticker')
            self.ticker.stop()

    def startSession(self):
        if(self.connected):
            self.ws.register(self.startOrStopTicker,events.TransitionBegin)
            self.ws.register(self.stopSession,events.Exiting)# register() passes events.Exiting as a parameter to stopSession()
            print('All events registered.')
            self.obs_quit_event.wait()
            self.ws.disconnect()

    def stopSession(self,obs_event):
        print('OBS closed.')
        self.obs_quit_event.set()


    def importTickerScenes(self):
        scenes = self.ws.call(requests.GetSceneList())
        for scene in scenes.getScenes():
            #convertObjectToJson(scene,f'scene-{scene.get("name")}.json')
            for source in scene['sources']:
                if source.get("name")=="TIcker-tape" and source.get("render"):
                    self.ticker_scenes.append(scene["name"])
                    break
        return(self.ticker_scenes)
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
class OBSSession:
    """start a new session every time you run OBS"""
    def __init__(self,host=None,port=None,password=None):
        self.host = 'localhost' if host == None else host
        self.port = 4444 if port == None else port
        load_dotenv()
        self._password = os.getenv('obswspass')
        self.ws = None
        self.connected = False
        # self.connect()
        # return(self.ws)

    def connect(self):
        self.ws = obsws(self.host,self.port,self._password)
        try:
            self.ws.connect()
            print('Connected to OBS')
            self.connected = True
        except exceptions.ConnectionFailure:
            print('Unable to connect to OBS')
            sys.exit()

    def getVideoData(self):
        response = self.ws.call(requests.GetVideoInfo())
        self.video = convertDictToObject(response.datain)
        return(self.video)
    
    def getSourceData(self,sourcename='tickertext',scenename='Coding'):
        prop=self.ws.call(requests.GetSceneItemProperties(sourcename,scenename))
        settings = self.ws.call(requests.GetSourceSettings(sourcename))
        filters = self.ws.call(requests.GetSourceFilters(sourcename))
        OBSdict = {**prop.datain,**settings.datain,**filters.datain}
        # print(OBSdict)
        convertObjectToJson(OBSdict,'obssourcedata.json')
        self.source = convertDictToObject(OBSdict)
        return(self.source)

   
def main():
    # t =Ticker('feed_text_dev.txt','feed_img_dev.png')
    # f1 =Feed("https://www.betootaadvocate.com/feed/","australia")
    # f2 =Feed("https://www.theonion.com/content/feeds/daily","US")
    # t.addFeed(f1)
    # t.addFeed(f2)
    # t.start()
    # print('Stopping in 10 seconds')
    # sleep(10)
    # t.stop()
    # print('starting again in 5 seconds')
    # sleep(5)
    # t.start()
    t =Ticker('feed_text_dev.txt','feed_img_dev.png')
    f1 =Feed("https://www.betootaadvocate.com/feed/")
    f2 =Feed("https://www.theonion.com/content/feeds/daily")
    t.addFeed(f1)
    t.addFeed(f2)
    t.connect()
    print('testing')
    t.start() #within start loop through all the feeds once,render them,get their size and reduce headlines accordingly
    # print(t.padding)
    # print(t.viewport_width)
    # print(t.getScrollSpeed())
    # t.calculatePadding()
    # print(t.padding)
    # t.play()
    # t.pause()
    # t.stop()
    # t.disconnect()
if __name__ == '__main__':
    main()
