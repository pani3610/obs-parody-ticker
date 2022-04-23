from feed import *
from session import OBSSession
from graphics import Strip,Circle
from time import sleep,time
from threading import Event,Thread,activeCount
from obswebsocket import obsws,requests,exceptions,events
from extrafunctions import *
from math import log2
import pickle

# time_start,time_stop = None,None
class Ticker:
    def __init__(self,savetextfile,saveimgfile):
        self.viewport_width = None #pixels
        '''Width of ticker text area in pixels'''
        
        self.scroll_speed,self.scroll_direction = None,None #pixels-per-second 
        '''New pixels introduced per second.'''
        
        self.empty_time = 3 #seconds
        '''Amount of time in seconds we want to ticker to go blank in order to switch feeds.'''

        self.ssw = None
        
        self.textcontainer = savetextfile
        self.imgcontainer = saveimgfile
        
        self.feeds = []

        self.max_size = 16380
        self.logo_size = (32,32) #(width,height)
        self.play_thread = None
        self.pause_event = Event()

        self.ticker_scenes = []
        self.obs_quit_event  = Event()

        self.tickertext = None
        self.tickerlogo = None
        self.strip = None
        self.circle = None

    def connect(self,host=None,port=None,password=None):
        self.obs = OBSSession(host,port,password)
        self.obs.connect()
    
    
    def start(self):
        #getOBSTickerObject details or create if required

        if (not self.obs.connected):
            return()
        #clear ticker text before all calculations
        self.clearTextContainer() 

        self.createOBSResource()
         
        #calculateviewportwidth
        self.viewport_width = self.calculateViewportWidth()
        self.scroll_speed,self.scroll_direction = self.getScrollVelocity()
        print(self.scroll_speed,self.scroll_direction)
        #calculate padding based on font and viewportwidth
        self.ssw = self.calculateSSW()
        
        # self.tickertext.hideSource()#self.obs.stopScroll()
        self.checkAllFeedSize()
        # self.obs.startScroll()

        self.obs.ws.register(self.playOrPauseTicker,events.TransitionBegin)
        self.obs.ws.register(self.stop,events.Exiting)# register() passes events.Exiting as a parameter to stopSession()
        print('Ready')
        # self.showOBSSources()
        self.showGraphics()
        self.importTickerScenes()
        self.play()
        self.obs_quit_event.wait()
        self.obs.disconnect()

    def addOBSSources(self):
        self.tickertext = self.obs.addSource('TICKER','text_ft2_source_v2',convertJSONToDict('source-settings.json').get('TICKER'),convertJSONToDict('source-filters.json').get('TICKER'))
        self.tickerlogo = self.obs.addSource('LOGO','image_source',convertJSONToDict('source-settings.json').get('LOGO'))
        self.strip = self.obs.addSource('STRIP','image_source',convertJSONToDict('source-settings.json').get('STRIP'))
        self.circle = self.obs.addSource('CIRCLE','image_source',convertJSONToDict('source-settings.json').get('CIRCLE'))

    def repositionOBSSources(self):
        position = {'x':0.05*self.obs.getVideoBaseWidth(),'y':self.obs.getVideoBaseHeight()-2*self.tickertext.getHeight(),'alignment':1}
        self.tickertext.repositionSource(position)

        position = {'x':self.tickertext.getPositionX()-self.tickerlogo.getHeight()/2,'y':self.tickertext.getPositionY(),'alignment':0}
        self.tickerlogo.repositionSource(position)

        position = {'x':0,'y':self.tickertext.getPositionY(),'alignment':1}
        self.strip.repositionSource(position)
        
        position = self.tickerlogo.getPosition()
        self.circle.repositionSource(position)

    def showOBSSources(self):
        self.tickertext.showSource()
        self.tickerlogo.showSource()
        self.strip.showSource()
        self.circle.showSource()

    def showGraphics(self):
        self.strip.showSource()
        self.circle.showSource()

    def reorderOBSSources(self):
        required_order = ['LOGO', 'CIRCLE', 'TICKER', 'STRIP']
        response = self.obs.ws.call(requests.GetCurrentScene())
        current_order = response.getSources()
        new_order = []
        for source in required_order:
            new_order.extend(list(filter(lambda item:item.get('name')==source,current_order)))
        
        print(self.obs.ws.call(requests.ReorderSceneItems(tuple(new_order))))
    def createOBSResource(self):
        self.addOBSSources()
        self.repositionOBSSources()
        self.reorderOBSSources()
    def createStrip(self):
        width = self.obs.getVideoBaseWidth()
        height = self.tickertext.getHeight()
        Strip(width,height)
    
    def createCircle(self):
        width = self.tickerlogo.getHeight()
        height = self.tickerlogo.getSourceWidth()
        Circle(width*1.5,height*1.5)

    def calculateViewportWidth(self):
        viewport_width = self.obs.getVideoBaseWidth() - self.tickertext.getPositionX()
        return(viewport_width)

    def getScrollVelocity(self):
        scroll_value = self.tickertext.getScrollSpeed()
        scroll_speed = abs(scroll_value)
        scroll_direction = 1 if scroll_value >= 0 else -1
        return(scroll_speed,scroll_direction)

    def calculateSSW(self):
        resolution = 100
        self.tickertext.updateContent(resolution*' ')
        source_width = self.tickertext.getSourceWidth()
        single_space_width = source_width/resolution
        print('SSW',single_space_width)
        return(single_space_width)

    def clearTextContainer(self):
        with open(self.textcontainer,'w') as txtfile:
            txtfile.write('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rerum eligendi, exercitationem fuga veniam adipisci natus nesciunt voluptatum? Maxime, deserunt ullam.')
        sleep(2)

    def updateTextContainer(self,feed:Feed):
        text = self.addPadding(feed.text.raw_string)
        self.tickertext.updateContent(text)

    def addPadding(self,string):
        if (self.scroll_direction>=0):
            padded_string = round(self.viewport_width/self.ssw)*' ' + round((self.empty_time*self.scroll_speed)/self.ssw)*' ' + string
        else:
            padded_string = round(self.viewport_width/self.ssw)*' ' + string + round((self.empty_time*self.scroll_speed)/self.ssw)*' ' 
        return(padded_string)


    def updateImageContainer(self,feed:Feed):
        if feed.logo.image != None:
            feed.logo.save(self.imgcontainer)
            # print(self.imgcontainer)
        else:
            print(f'{feed.name} has no image source')


    def startTickerLoop(self):
        # global time_start,time_stop
        while(True):
            for feed in self.feeds:
                if(self.pause_event.isSet()):
                    return()
                time_start = time()
                self.tickertext.refreshSource()
                print(feed.returnFeedSummary())
                self.updateTextContainer(feed)
                self.updateImageContainer(feed)
                self.tickerlogo.showSource()
                self.switchToNextFeed(feed,time_start)
                
        
    def play(self):
        self.pause_event.clear() #clearing stop event just in case you are restarting after stopping
        self.play_thread = Thread(target=self.startTickerLoop,name='Ticker thread') #reinitializing thread because a thread can be started only once.
        self.play_thread.start()
        

    def switchToNextFeed(self,feed:Feed,update_start_time=None):
        source_width = self.tickertext.getSourceWidth()
        sleep_time = (source_width/self.scroll_speed)
        # self.tickertext.refreshSource()
        print(f'Going to sleep for {sleep_time:.2f} seconds (minus execution time)')
        execution_time = 0
        if (update_start_time != None):
            stop_time = time()
            execution_time =stop_time-update_start_time
        self.pause_event.wait(sleep_time-execution_time+1)

    def addFeed(self,feed:Feed):
        #self.addPaddingToFeed(feed) #Padding to be added to the containerfile and NOT to modify feedtext
        self.resizeFeedLogo(feed) #Maybe resize the containerfile than the feedlogo file
        self.feeds.append(feed)

    
    def removeFeed(self,Feed):
        pass


    def checkAllFeedSize(self):
        for feed in self.feeds:
            self.updateTextContainer(feed)
            source_width = self.tickertext.getSourceWidth()
            print(feed.name,source_width)
            if(source_width > self.max_size):
                print(f'for {feed.name}: Feed text too large. Reducing number of headlines. Original Headline Count : {feed.headlines_count}')
                self.reduceFeedSizeToFit(feed)
            # sleep(1)

           
    def reduceFeedSizeToFit(self,feed:Feed): #modified binary search to find headlines count but ensure solution doesn't exceed target.
        source_width = self.tickertext.getSourceWidth()
        low = 0
        lowvalue = 0
        high = feed.headlines_count
        highvalue = source_width
        oldmid = None
        while(highvalue>lowvalue):
            mid = low + int((self.max_size-lowvalue)*(high-low)/(highvalue-lowvalue))
            if (mid == oldmid):
                break
            feed.updateHeadlinesCount(mid)
            self.updateTextContainer(feed)
            source_width = self.tickertext.getSourceWidth()
            print(f'Headline count: {mid}|Pixel Width: {source_width}')
            if(source_width>self.max_size):
                high = mid
                highvalue = source_width
            else:
                low = mid
                lowvalue = source_width
            oldmid = mid
                
        print(f'Final headline count:{feed.headlines_count}| {source_width} pixels')
    
    def resizeFeedLogo(self,feed:Feed):
        feed.logo.resize(self.logo_size)
    
    def pause(self):
        # print('Stopping ticker')
        self.pause_event.set()
        if self.play_thread != None:
            self.play_thread.join()

    def playOrPauseTicker(self,transition_event:events.TransitionBegin):
        # print(self.ticker_scenes)
        if(transition_event.getFromScene() not in self.ticker_scenes and transition_event.getToScene() in self.ticker_scenes):
            print('play ticker')
            self.play()
        elif(transition_event.getFromScene() in self.ticker_scenes and transition_event.getToScene() not in self.ticker_scenes):
            print('pause ticker')
            self.pause()


    def stop(self,obs_event):
        print('OBS closed.')
        self.pause()
        # self.activateTickerLoop()
        self.obs_quit_event.set()

    def activateTickerLoop(self):
        filters = convertJSONToDict('source-filters.json').get('TICKER')
        scroll_filter = list(filter(lambda item:item.get("type")=="scroll_filter",filters)).pop()
        scroll_filter['settings']['loop']=True
        self.tickertext.ws.call(requests.SetSourceFilterSettings(self.tickertext.name,scroll_filter.get('name'),scroll_filter.get('settings')))


    def importTickerScenes(self):
        scenes = self.obs.ws.call(requests.GetSceneList())
        for scene in scenes.getScenes():
            # convertObjectToJson(scene,f'scene-{scene.get("name")}.json')
            for source in scene['sources']:
                if source.get("name")==self.tickertext.name and source.get("render"):
                    self.ticker_scenes.append(scene["name"])
                    break
        return(self.ticker_scenes)
    def disconnect(self):
        self.obs.disconnect()   

def loadFromPickle(picklefile):
    with open(picklefile,'rb') as pf:
        while True:
            try:
                yield pickle.load(pf)
            except EOFError:
                break


def main():
    t =Ticker('feed_text_dev.txt','feed_img_dev.png')
    # pickled_feeds = loadFromPickle('feed_examples.pkl')
    # f1 = next(pickled_feeds)
    # f2 = next(pickled_feeds)
    f1 = Feed("https://babylonbee.com/feed",hl_count=4)
    f2 = Feed("https://www.betootaadvocate.com/feed/",hl_count=4)
    print(f1.calculateSize())
    print(f2.calculateSize())
    t.addFeed(f1)
    t.addFeed(f2)
    t.connect()
    # t.importTickerScenes()
    # t.disconnect()
    # t.createStrip()
    t.start() #within start loop through all the feeds once,render them,get their size and reduce headlines accordingly
    # t.play()
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
