from feed import *
from session import OBSSession
from graphics import Strip,Circle
from gui import *
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
        
        self.scroll_speed= None#pixels-per-second 
        '''New pixels introduced per second.'''
        
        self.empty_time = 0 #seconds
        '''Amount of time in seconds we want to ticker to go blank in order to switch feeds.'''

        self.text_direction = 1 # +1 for right-to-left and -1 for left-to-right
        
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

        self.gui = None
        
        self.status = 'not started'

    def connect(self,host=None,port=None,password=None):
        self.obs = OBSSession(host,port,password)
        self.obs.connect()
        self.obs.ws.register(self.playOrPauseTicker,events.TransitionBegin)
        self.obs.ws.register(lambda event: self.gui.destroy(),events.Exiting)# register() passes events.Exiting as a parameter to stopSession()
    
    def createGUI(self):
        self.gui = GUIApp('OBS Ticker')
        TickBoxList(self.gui,'Scene Checklist',self.obs.getSceneList())#
        EditableListBox(self.gui,'Feed List')#
        Font(self.gui,'Ticker Font')
        Slider(self.gui,'Text Scroll Speed',0,500)
        FloatEntry(self.gui,'Sleep time between feeds','seconds')#
        RadioList(self.gui,'Text Direction',['Right to Left','Left to Right'])#
        # tk.Button(self.gui,text='Start',command=self.start).pack()
        ToggleButton(self.gui,'Stop','Start',self.stop,self.start).pack()
        ToggleButton(self.gui,'⏸','▶️',lambda :self.pause(True),self.play).pack()
        # tk.Button(self.gui,text='Stop',command=self.stop).pack()
        tk.Button(self.gui,text='Reset',command=lambda: self.gui.importData('default-gui-data.json')).pack()
        # tk.Button(self.gui,text='Save',command=self.gui.exportData).pack()
        self.gui.onQuit(self.quit)
        self.gui.mainloop()

    def setBasicSettings(self):
        gui_settings = convertJSONToDict('gui-data.json')
        self.empty_time = gui_settings.get('sleep_time_between_feeds')
        text_direction = gui_settings.get('text_direction')
        self.text_direction = 1 if gui_settings.get('text_direction') == 'Right to Left' else -1
        self.ticker_scenes = gui_settings.get('scene_checklist')
        self.updateFeedList(gui_settings.get('feed_list'))

    def setSourceSettingsfromGUI(self):
        gui_settings = convertJSONToDict('gui-data.json')
        font = {'face':gui_settings.get('ticker_font')[0],
                        'size':gui_settings.get('ticker_font')[1],
                        'style':gui_settings.get('ticker_font')[2].title()}
        source_settings = {'TICKER':{'font':font,'from_file':True,'text_file':abs_path(self.textcontainer)}}
        convertObjectToJson(source_settings,'source-settings.json')
    
    def setSourceFiltersfromGUI(self):
        gui_settings = convertJSONToDict('gui-data.json')
        ticker_speed = gui_settings.get('text_scroll_speed')*{'Right to Left':1,'Left to Right':-1}[gui_settings.get('text_direction')]
        print(ticker_speed)
        filter_settings = {"TICKER":[{
                                    "enabled:":True,
                                    "name":"tickerscroll",
                                    "settings":{
                                        'loop':False,
                                        'speed_x':ticker_speed
                                    },
                                    'type':"scroll_filter"
                                    }]}
        convertObjectToJson(filter_settings,'source-filters.json')
        

    def start(self):
        #getOBSTickerObject details or create if required

        if (not self.obs.connected):
            return()
        #clear ticker text before all calculations
        self.gui.exportData('gui-data.json')
        self.clearTextContainer() 
        self.setBasicSettings()
        self.setSourceSettingsfromGUI()
        self.setSourceFiltersfromGUI()
        self.createOBSResource()
        
        #calculateviewportwidth
        self.viewport_width = self.calculateViewportWidth()
        self.scroll_speed = abs(self.tickertext.getScrollSpeed())
        print(self.scroll_speed,self.text_direction)
        #calculate padding based on font and viewportwidth
        self.ssw = self.calculateSSW()  
        # self.tickertext.hideSource()#self.obs.stopScroll()
        self.checkAllFeedSize()
        # self.obs.startScroll()

        # self.showOBSSources()
        self.showGraphics()
        # self.importTickerScenes()
        self.status = 'started'
        print('Ready to play')
        # self.play()
        # self.obs_quit_event.wait()
        # self.obs.disconnect()

    def addOBSSources(self):
        self.strip = self.obs.addSource('STRIP','image_source',{'file':abs_path('strip.png')})
        self.tickertext = self.obs.addSource('TICKER','text_ft2_source_v2',convertJSONToDict('source-settings.json').get('TICKER'),convertJSONToDict('source-filters.json').get('TICKER'))
        self.circle = self.obs.addSource('CIRCLE','image_source',{'file':abs_path('circle.png')})
        self.tickerlogo = self.obs.addSource('LOGO','image_source',{'file':abs_path(self.imgcontainer)})

    def repositionOBSSources(self):
        if self.text_direction == 1:
            position = {'x':0.05*self.obs.getVideoBaseWidth(),'y':self.obs.getVideoBaseHeight()-2*self.tickertext.getHeight(),'alignment':1}

        elif self.text_direction == -1:
            position = {'x':0.95*self.obs.getVideoBaseWidth(),'y':self.obs.getVideoBaseHeight()-2*self.tickertext.getHeight(),'alignment':2}
        self.tickertext.repositionSource(position)

        position = {'x':self.tickertext.getPositionX()-self.text_direction*self.tickerlogo.getHeight()/2,'y':self.tickertext.getPositionY(),'alignment':0}
        self.tickerlogo.repositionSource(position)

        position = {'x':0,'y':self.tickertext.getPositionY(),'alignment':1}
        self.strip.repositionSource(position)
        
        position = self.tickerlogo.getPosition()
        self.circle.repositionSource(position)
    
    def duplicateOBSSources(self,scene_list): #order should be as per per required_order
        self.strip.duplicateSource(scene_list)
        self.tickertext.duplicateSource(scene_list)
        self.circle.duplicateSource(scene_list)
        self.tickerlogo.duplicateSource(scene_list)
        
        for scene in scene_list:
            self.obs.setCurrentScene(scene)
            self.repositionOBSSources()
            self.lockOBSSources()
            self.showOBSSources()
           

    def lockOBSSources(self):
        self.tickertext.lockSource()
        self.tickerlogo.lockSource()
        self.strip.lockSource()
        self.circle.lockSource()


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
        self.obs.setCurrentScene(self.ticker_scenes[0])
        # print(self.obs.getCurrentScene())
        self.addOBSSources()
        self.repositionOBSSources()
        # self.reorderOBSSources()
        self.duplicateOBSSources(self.ticker_scenes[1:])
        self.obs.setCurrentScene(self.ticker_scenes[0])
    
    def removeOBSSources(self,scene_list):
        self.strip.removeSourceFromScenes(scene_list)
        self.tickertext.removeSourceFromScenes(scene_list)
        self.circle.removeSourceFromScenes(scene_list)
        self.tickerlogo.removeSourceFromScenes(scene_list)

    def createStrip(self):
        width = self.obs.getVideoBaseWidth()
        height = self.tickertext.getHeight()
        Strip(width,height)
    
    def createCircle(self):
        width = self.tickerlogo.getHeight()
        height = self.tickerlogo.getSourceWidth()
        Circle(width*1.5,height*1.5)

    def calculateViewportWidth(self):
        if self.text_direction == 1:
            viewport_width = self.obs.getVideoBaseWidth() - self.tickertext.getPositionX()
        elif self.text_direction == -1:
            viewport_width = self.tickertext.getPositionX()
        return(viewport_width)

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
        if (self.text_direction==1):
            # padded_string = round(self.viewport_width/self.ssw)*' ' + round((self.empty_time*self.scroll_speed)/self.ssw)*' ' + string
            padded_string = round(self.viewport_width/self.ssw)*' ' + string
        else:
            # padded_string = round(self.viewport_width/self.ssw)*' ' + string + round((self.empty_time*self.scroll_speed)/self.ssw)*' ' 
            padded_string = string + round(self.viewport_width/self.ssw)*' ' 
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
                print(feed.returnFeedSummary())
                self.updateTextContainer(feed)
                self.updateImageContainer(feed)
                self.tickertext.refreshSource()
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
        self.pause_event.wait(sleep_time-execution_time+self.empty_time+1)

    def addFeed(self,feed:Feed):
        #self.addPaddingToFeed(feed) #Padding to be added to the containerfile and NOT to modify feedtext
        self.resizeFeedLogo(feed) #Maybe resize the containerfile than the feedlogo file
        self.feeds.append(feed)

    
    def removeFeed(self,Feed):
        pass
    
    def updateFeedList(self,url_list):
        self.feeds = []
        threads =[]
        for rss_url in url_list:
            thread = Thread(target=self.addFeedToTicker,args=(rss_url,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def addFeedToTicker(self,url:str):
        f = Feed(url)
        self.addFeed(f)        


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
    
    def pause(self,hide_source=False):
        if hide_source:
            self.tickertext.hideSource()
            self.tickerlogo.hideSource()
        self.pause_event.set()
        if self.play_thread != None:
            self.play_thread.join()
        print('ticker paused')

    def playOrPauseTicker(self,transition_event:events.TransitionBegin):
        print(f'{transition_event.getFromScene()} -> {transition_event.getToScene()}')
        if(transition_event.getFromScene() not in self.ticker_scenes and transition_event.getToScene() in self.ticker_scenes):
            print('play ticker')
            self.play()
        elif(transition_event.getFromScene() in self.ticker_scenes and transition_event.getToScene() not in self.ticker_scenes):
            print('pause ticker')
            self.pause()


    def stop(self):
        if self.status == 'started':
            self.pause()
            self.removeOBSSources(self.obs.getSceneList())
            del self.tickertext
            del self.tickerlogo
            del self.strip
            del self.circle
            self.ticker_scenes = []
            self.status = 'not started'
            print('ticker stopped')
        # self.activateTickerLoop()
        # self.obs_quit_event.set()
        
    def quit(self):
        self.stop()
        self.obs.disconnect()
        print('ticker quit')

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
    t.connect()
    t.createGUI()
    return()
    pickled_feeds = loadFromPickle('feed_examples.pkl')
    f1 = next(pickled_feeds)
    f2 = next(pickled_feeds)
    # f1 = Feed("https://babylonbee.com/feed",hl_count=4)
    # f2 = Feed("https://www.betootaadvocate.com/feed/",hl_count=4)
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
