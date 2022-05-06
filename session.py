from random import randrange
from re import S
from time import sleep, time
from obswebsocket import obsws,requests,exceptions,events
import os
from dotenv import load_dotenv
from requests import session
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
        # self.sources = ['LOGO', 'CIRCLE', 'TICKER', 'STRIP']
        # self.name ='TICKER'
        # self.scenename ='Coding'
        # self.connect()
        # return(self.ws)
    def connect(self):
        self.ws = obsws(self.host,self.port,self._password)
        try:
            self.ws.connect()
            print('Connected to OBS')
            self.connected = True
            self.registerEvents()
        except exceptions.ConnectionFailure:
            print('Unable to connect to OBS')
            sys.exit()
    def registerEvents(self):
        self.scene_changed = Event()
        self.ws.register(lambda event: self.scene_changed.set(),events.SwitchScenes)

    def disconnect(self):
        self.ws.disconnect()
    
    def getSceneList(self):
        response = self.ws.call(requests.GetSceneList())
        scene_list = [ scene.get('name') for scene in response.getScenes()]
        return(scene_list)
    
    def addSource(self,name,type,settings=None,filters=None):
        source = OBSSource(self.ws,name,type,settings,filters)
        return(source) 

    def exportVideoData(self,filepath):
        response = self.ws.call(requests.GetVideoInfo())
        convertObjectToJson(response.datain,filepath)

    
    def exportSourceData(self,sourcename,filepath):
        prop=self.ws.call(requests.GetSceneItemProperties(sourcename))
        settings = self.ws.call(requests.GetSourceSettings(sourcename))
        filters = self.ws.call(requests.GetSourceFilters(sourcename))
        # OBSdict = {**prop.datain,**settings.datain,**filters.datain}
        OBSdict = {'properties':prop.datain,'settings':settings.getSourceSettings(),'filters':filters.getFilters()}
        # print(OBSdict)
        convertObjectToJson(OBSdict,filepath)
    
    
    def exportSourceSettings(self,filepath='source-settings.json'):
        OBSsettings = dict()
        for source in self.sources:
            response = self.ws.call(requests.GetSourceSettings(source))
            OBSsettings.update({source:response.getSourceSettings()})
        convertObjectToJson(OBSsettings,filepath)
    
    def exportSourceFilters(self,filepath='source-filters.json'):
        OBSsettings = dict()
        for source in self.sources:
            response = self.ws.call(requests.GetSourceFilters(source))
            OBSsettings.update({source:response.getFilters()})
        convertObjectToJson(OBSsettings,filepath)
        
    def getVideoBaseWidth(self):
        response = self.ws.call(requests.GetVideoInfo())
        baseWidth = response.getBaseWidth()
        return(baseWidth)
    def getVideoBaseHeight(self):
        response = self.ws.call(requests.GetVideoInfo())
        baseHeight = response.getBaseHeight()
        return(baseHeight)

    def setCurrentScene(self,scenename):
        if(scenename!=self.getCurrentScene()):
            self.ws.call(requests.SetCurrentScene(scenename))
            self.waitForUpdate(self.scene_changed)

    def waitForUpdate(self,event:Event,timeout=None):
        set_before_timeout = event.wait(timeout)
        if not set_before_timeout:
            print('Timed out')
        event.clear()
        return(set_before_timeout)
        
    def getCurrentScene(self):
        scene = self.ws.call(requests.GetCurrentScene())
        scenename = scene.getName()
        return(scenename)
    
class OBSSource():
    def __init__(self,ws:obsws,name,type,settings=None,filters=None):
        self.ws = ws
        self.name = name
        self.type = type
        self.settings = dict() if settings == None else settings
        self.filters = [] if filters == None else filters
        self.write = None
        self.registerEvents()
        if self.name not in self.getSourceList():
            self.createSource()


    def getSourceList(self): 
        response = self.ws.call(requests.GetSceneItemList())
        source_list = [source.get('sourceName') for source in response.getSceneItems()]
        return(source_list)
    
    def registerEvents(self):
        self.ws.register(self.transformChanged,events.SceneItemTransformChanged)
        self.content_changed = Event()
        self.ws.register(self.visibilityChanged,events.SceneItemVisibilityChanged)
        self.visibility_changed = Event()
        self.ws.register(self.scrollChanged,events.SourceFilterVisibilityChanged)
        self.scroll_changed = Event()
        self.ws.register(self.sourceCreated,events.SourceCreated)
        self.source_created = Event()
        print('All events registered')
    def sourceCreated(self,event):
        if event.getSourceName() == self.name:
            self.source_created.set()

    def transformChanged(self,event):
        # print(event.getItemName(),end=', ')
        if (self.write and event.getItemName() == self.name):
            # print('width changed')
            self.content_changed.set()
    def visibilityChanged(self,event):
        if event.getItemName() == self.name:
            self.visibility_changed.set()
    
    def scrollChanged(self,event):
        if event.getSourceName() == self.name:
            self.scroll_changed.set()
    
    def waitForUpdate(self,event:Event,timeout=None):
        set_before_timeout = event.wait(timeout)
        if not set_before_timeout:
            print('Timed out')
        event.clear()
        return(set_before_timeout)

    def getPositionX(self):
        position = self.getPosition()
        xcor = position['x']
        return(xcor)
    
    def getPositionY(self):
        position = self.getPosition()
        ycor = position['y']
        return(ycor)

    def getPosition(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.name))
        position = response.getPosition()
        return(position)

    def getScrollSpeed(self):
        response = self.ws.call(requests.GetSourceFilters(self.name))
        filters = response.getFilters()
        scroll_speed = 0
        for filter in filters:
            if (filter['type'] == "scroll_filter" and filter['enabled']):
                scroll_speed = filter['settings']['speed_x']
        return(scroll_speed)

    def getSourceWidth(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.name))
        sourceWidth  = response.getSourceWidth()
        return(sourceWidth)
    
    def getHeight(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.name))
        height  = response.getHeight()
        return(height)
    def updateContent(self,string):
        self.write = True
        with open(str(self.settings.get('text_file')),"r+") as txtfile:
            if txtfile.read() == string:
                print('Same text')
                self.write = False
                return()
            txtfile.seek(0)
            txtfile.truncate()
            txtfile.write(string)
        self.waitForUpdate(self.content_changed,5) #if text not updated within x seconds code will continue. This should be enough time if new and old text render to same size.
        self.write = False
    
    def refreshSource(self):
        self.hideSource()
        self.showSource()
    
    def hideSource(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.name))
        source_visible = response.getVisible()
        if source_visible:
            self.ws.call(requests.SetSceneItemRender(self.name,False))
            self.waitForUpdate(self.visibility_changed)

    def showSource(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.name))
        source_visible = response.getVisible()
        if not source_visible:
            self.ws.call(requests.SetSceneItemRender(self.name,True))
            self.waitForUpdate(self.visibility_changed)

    def startScroll(self):
        scroll_filter = list(filter(lambda item:item.get("type")=="scroll_filter",self.filters)).pop()
        response = self.ws.call(requests.GetSourceFilterInfo(self.name,scroll_filter.get('name')))
        if not response.getEnabled():
            self.ws.call(requests.SetSourceFilterVisibility(self.name,scroll_filter.get('name'),True))
            self.waitForUpdate(self.scroll_changed)
            print('scroll unhidden')

    def stopScroll(self):
        scroll_filter = list(filter(lambda item:item.get("type")=="scroll_filter",self.filters)).pop()
        response = self.ws.call(requests.GetSourceFilterInfo(self.name,scroll_filter.get('name')))
        if response.getEnabled():
            self.ws.call(requests.SetSourceFilterVisibility(self.name,scroll_filter.get('name'),False))
            self.waitForUpdate(self.scroll_changed)
            print('scroll hidden')

    def createSource(self):
        scene = self.ws.call(requests.GetCurrentScene())
        scenename = scene.getName()
        self.ws.call(requests.CreateSource(self.name,self.type,scenename,self.settings,False))
        self.waitForUpdate(self.source_created,timeout=3)
        self.lockSource()
        self.applyFilters()
        
    def applyFilters(self):
        for filter in self.filters: 
            self.ws.call(requests.AddFilterToSource(self.name,filter.get('name'),filter.get('type'),filter.get('settings')))
    def repositionSource(self,position):
        self.ws.call(requests.SetSceneItemProperties(self.name,position=position))
    
    def lockSource(self):
        self.ws.call(requests.SetSceneItemProperties(self.name,locked=True))

    def exportSourceData(self,filepath):
        prop=self.ws.call(requests.GetSceneItemProperties(self.name))
        settings = self.ws.call(requests.GetSourceSettings(self.name))
        filters = self.ws.call(requests.GetSourceFilters(self.name))
        # OBSdict = {**prop.datain,**settings.datain,**filters.datain}
        OBSdict = {'properties':prop.datain,'settings':settings.getSourceSettings(),'filters':filters.getFilters()}
        # print(OBSdict)
        convertObjectToJson(OBSdict,filepath)
    
    def duplicateSource(self,scene_list):
        for scene in scene_list:
            self.ws.call(requests.DuplicateSceneItem(self.name,None,scene))
    
def main():
    # test0()
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    test7()
    
def test0():
    s= OBSSession()
    s.connect()
    source = s.addSource('altu','image_source',{"file": "/Users/pani3610/code/parody-ticker/circle.png"})
    print(source.getPositionX())
    print(source.getScrollSpeed())
    print(source.getSourceWidth())
    s.disconnect()
    
def test1():
    s= OBSSession()
    s.connect()
    source = s.addSource('TICKER','text_ft2_source_v2',convertJSONToDict('source-settings.json').get('TICKER'))
    charlist = ['F','D']#['O','I']
    for i in range(10):
        size = 100#randrange(1,1260)
        char = charlist[i%len(charlist)]#chr(randrange(65,81))
        print(f'Round {i}',end = ' ')
        print('expected value:',char,size*13,end=' ')
        source.updateContent(char*size)
        print('output value:',source.getSourceWidth())
        # if ( size*13 == s.getSourceSourceWidth()):
        #     print('Match')
        # else:
        #     print('Not match')
    s.disconnect()
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
    tickertext = s1.addSource('TICKER','text_ft2_source_v2',convertJSONToDict('source-settings.json').get('TICKER'))
    tickerlogo = s1.addSource('LOGO','image_source',convertJSONToDict('source-settings.json').get('LOGO'))
    strip = s1.addSource('STRIP','image_source',convertJSONToDict('source-settings.json').get('STRIP'))
    circle = s1.addSource('CIRCLE','image_source',convertJSONToDict('source-settings.json').get('CIRCLE'))
    # s1.exportSourceSettings('source-settings.json')
    # s1.exportSourceFilters()
    # s1.refreshSource()
    s1.disconnect()

def test4():
    s1= OBSSession()
    s1.connect()
    source = s1.addSource('TICKER','text_ft2_source_v2',convertJSONToDict('source-settings.json').get('TICKER'),convertJSONToDict('source-filters.json').get('TICKER'))
    source.updateContent('nanachi tang')
    sleep(3)
    source.hideSource()
    sleep(3)
    source.showSource()
    sleep(3)
    source.stopScroll()
    sleep(3)
    source.startScroll()
    s1.disconnect()

def test5():
    s =OBSSession()
    s.connect()
    print(s.getSceneList())
    # response = s.ws.call(requests.GetSceneItemList())
    # source_list = [source.get('sourceName') for source in response.getSceneItems()]
    # print(source_list)
    s.disconnect()
def test6():
    s = OBSSession()
    s.connect()
    print(s.getSceneList())
    # for scene in s.getSceneList():
    #     s.setCurrentScene(scene)
    #     s.getCurrentScene()
    s.setCurrentScene('Scene 5')
    print(s.getCurrentScene())
    s.setCurrentScene('Scene 3')
    print(s.getCurrentScene())
    s.setCurrentScene('Scene 4')
    print(s.getCurrentScene())
    # sleep(10)
    s.disconnect()

def test7():
    s = OBSSession()
    s.connect()
    strip = s.addSource('STRIP','image_source',{'file':abs_path('strip.png')})
    strip.duplicateSource(['Scene 5','Scene 6'])
if __name__ == '__main__':
    main()