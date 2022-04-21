from random import randrange
from time import sleep, time
from obswebsocket import obsws,requests,exceptions,events
import os
from dotenv import load_dotenv
from extrafunctions import * 
import sys
from threading import Event
class OBSSession:
    """start a new session every time you run OBS"""
    def __init__(self,host=None,port=None,password=None):
        self.host = 'localhost' if host == None else host
        self.port = 4444 if port == None else port
        load_dotenv()
        self._password = os.getenv('obswspass')
        self.ws = None
        self.connected = False
        self.sourcename ='tickertext'
        self.scenename ='Coding'
        self.sourceparentname = 'TIcker-tape'
        self.filtername = 'tickerscroll'
        self.textfile = 'feed_text_dev.txt'
        self.write = None
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
    def disconnect(self):
        self.ws.disconnect()
    def registerEvents(self):
        self.ws.register(self.transformChanged,events.SceneItemTransformChanged)
        self.text_changed = Event()
        self.ws.register(self.visibilityChanged,events.SceneItemVisibilityChanged)
        self.tickertext_visibility_changed = Event()
        self.ws.register(self.scrollChanged,events.SourceFilterVisibilityChanged)
        self.scroll_changed = Event()
        self.ws.register(self.sourceCreated,events.SourceCreated)
        self.source_created = Event()
        print('All events registered')

    def sourceCreated(self,event):
        if event.getSourceName() == 'TICKER':
            self.source_created.set()

    def transformChanged(self,event):
        # print(event.getItemName(),end=', ')
        if (self.write and event.getItemName() == self.sourceparentname):
            # print('width changed')
            self.text_changed.set()
    def visibilityChanged(self,event):
        if event.getItemName() == self.sourcename:
            self.tickertext_visibility_changed.set()
    
    def scrollChanged(self,event):
        if event.getSourceName() == self.sourcename:
            self.scroll_changed.set()
    
    def waitForCreateSource(self):
        self.source_created.wait()
        self.source_created.clear()
    def waitForScrollChange(self):
        self.scroll_changed.wait()
        self.scroll_changed.clear()
        

    def waitForUpdate(self,event,timeout=None):
        set_before_timeout = event.wait(timeout)
        if not set_before_timeout:
            print('Timed out')
        event.clear()
        return(set_before_timeout)

    def waitForVisibilityChange(self):
        self.tickertext_visibility_changed.wait()
        self.tickertext_visibility_changed.clear()

    def exportVideoData(self,filepath):
        response = self.ws.call(requests.GetVideoInfo())
        convertObjectToJson(response.datain,filepath)
    
    def exportSourceData(self,filepath):
        prop=self.ws.call(requests.GetSceneItemProperties(self.sourcename,self.scenename))
        settings = self.ws.call(requests.GetSourceSettings(self.sourcename))
        filters = self.ws.call(requests.GetSourceFilters(self.sourcename))
        # OBSdict = {**prop.datain,**settings.datain,**filters.datain}
        OBSdict = {'properties':prop.datain,'settings':settings.getSourceSettings(),'filters':filters.getFilters()}
        # print(OBSdict)
        convertObjectToJson(OBSdict,filepath)
    
    def getVideoBaseWidth(self):
        response = self.ws.call(requests.GetVideoInfo())
        baseWidth = response.getBaseWidth()
        return(baseWidth)
    def getVideoBaseHeight(self):
        response = self.ws.call(requests.GetVideoInfo())
        baseHeight = response.getBaseHeight()
        return(baseHeight)
    
    def getSourcePositionX(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.sourcename,self.scenename))
        position = response.getPosition()
        xcor = position['x']
        return(xcor)
    
    def getScrollSpeed(self):
        response = self.ws.call(requests.GetSourceFilters(self.sourcename))
        filters = response.getFilters()
        scroll_speed = 0
        for filter in filters:
            if (filter['type'] == "scroll_filter" and filter['enabled']):
                scroll_speed = filter['settings']['speed_x']
        return(scroll_speed)

    def getSourceSourceWidth(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.sourcename,self.scenename))
        sourceWidth  = response.getSourceWidth()
        return(sourceWidth)
    
    def updateText(self,string):
        self.write = True
        with open(self.textfile,"r+") as txtfile:
            if txtfile.read() == string:
                print('Same text')
                self.write = False
                return()
            txtfile.seek(0)
            txtfile.truncate()
            txtfile.write(string)
        self.waitForUpdate(self.text_changed,5) #if text not updated within x seconds code will continue. This should be enough time if new and old text render to same size.
        self.write = False
    
    def refreshSource(self):
        self.hideSource()
        self.showSource()
    
    def hideSource(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.sourcename,self.scenename))
        source_visible = response.getVisible()
        if source_visible:
            self.ws.call(requests.SetSceneItemRender(self.sourcename,False))
            self.waitForUpdate(self.tickertext_visibility_changed)

    def showSource(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.sourcename,self.scenename))
        source_visible = response.getVisible()
        if not source_visible:
            self.ws.call(requests.SetSceneItemRender(self.sourcename,True))
            self.waitForUpdate(self.tickertext_visibility_changed)

    def startScroll(self):
        self.ws.call(requests.SetSourceFilterVisibility(self.sourcename,self.filtername,True))
        self.waitForUpdate(self.scroll_changed)
        print('scroll unhidden')

    def stopScroll(self):
        self.ws.call(requests.SetSourceFilterVisibility(self.sourcename,self.filtername,False))
        self.waitForUpdate(self.scroll_changed)
        print('scroll hidden')

    def createTextSource(self):
        scene = self.ws.call(requests.GetCurrentScene())
        scenename = scene.getName()
        print(scenename)
        source_data = convertJSONToDict('source-data.json')
        self.ws.call(requests.CreateSource('TICKER','text_ft2_source_v2',scenename,source_data.get('settings')))
        self.waitForUpdate(self.source_created,timeout=5)
        prop = self.ws.call(requests.GetSceneItemProperties('TICKER'))
        text_height = prop.getSourceHeight()
        print(text_height)
        self.ws.call(requests.SetSceneItemPosition('TICKER',0.05*self.getVideoBaseWidth(),self.getVideoBaseHeight()-2*text_height))
        filter = source_data.get('filters').pop()
        print(filter)
        
        self.ws.call(requests.AddFilterToSource('TICKER',filter.get('name'),filter.get('type'),filter.get('settings')))
def main():
    # test0()
    # test1()
    # test2()
    test3()
    # test4()
    
def test0():
    s= OBSSession()
    s.connect()
    print(s.getSourcePositionX())
    print(s.getScrollSpeed())
    print(s.getSourceSourceWidth())
    
def test1():
    s= OBSSession()
    s.connect()
    s.registerEvents()
    charlist = ['F','D']#['O','I']
    for i in range(10):
        size = 100#randrange(1,1260)
        char = charlist[i%len(charlist)]#chr(randrange(65,81))
        print(f'Round {i}',end = ' ')
        print('expected value:',char,size*13,end=' ')
        s.updateText(char*size)
        # print('output value:',s.getSourceSourceWidth())
        if ( size*13 == s.getSourceSourceWidth()):
            print('Match')
        else:
            print('Not match')
    
def test2():
    e1 = Event()
    s1= OBSSession()
    s1.connect()
    s1.registerEvents()
    s2= OBSSession()
    s2.connect()
    s2.registerEvents()
    e1.wait()

def test3():
    s1= OBSSession()
    s1.connect()
    s1.registerEvents()
    # s1.exportSourceData('source-data.json')
    s1.createTextSource()
    # s1.refreshSource()
    s1.disconnect()

def test4():
    s1= OBSSession()
    s1.connect()
    s1.registerEvents()
    s1.updateText('nanachi tang')
    sleep(3)
    s1.hideSource()
    sleep(3)
    s1.showSource()
    sleep(3)
    s1.stopScroll()
    sleep(3)
    s1.startScroll()
if __name__ == '__main__':
    main()