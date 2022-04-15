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
        self.transform_changed = self.ws.register(self.transformChanged,events.SceneItemTransformChanged)
        self.text_changed = Event()
        self.visibility_changed = self.ws.register(self.visibilityChanged,events.SceneItemVisibilityChanged)
        self.tickertext_visibility_changed = Event()
        self.filter_visibility_changed = self.ws.register(self.scrollChanged,events.SourceFilterVisibilityChanged)
        self.scroll_changed = Event()
        print('All events registered')

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
    
    def waitForScrollChange(self):
        self.scroll_changed.wait()
        self.scroll_changed.clear()
        

    def waitForUpdate(self,timeout=None):
        set_before_timeout = self.text_changed.wait(timeout)
        if not set_before_timeout:
            print('Timed out')
        # print('event set')
        self.text_changed.clear()

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
        OBSdict = {**prop.datain,**settings.datain,**filters.datain}
        # print(OBSdict)
        convertObjectToJson(OBSdict,filepath)
    
    def getVideoBaseWidth(self):
        response = self.ws.call(requests.GetVideoInfo())
        baseWidth = response.getBaseWidth()
        return(baseWidth)
    
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
        self.waitForUpdate(5) #if text not updated within x seconds code will continue. This should be enough time if new and old text render to same size.
        self.write = False
    
    def refreshSource(self):
        self.ws.call(requests.SetSceneItemRender(self.sourcename,False))
        self.waitForVisibilityChange()
        self.ws.call(requests.SetSceneItemRender(self.sourcename,True))
        self.waitForVisibilityChange()
    
    def startScroll(self):
        self.ws.call(requests.SetSourceFilterVisibility(self.sourcename,self.filtername,True))
        self.waitForScrollChange()
        print('scroll unhidden')

    def stopScroll(self):
        self.ws.call(requests.SetSourceFilterVisibility(self.sourcename,self.filtername,False))
        self.waitForScrollChange()
        print('scroll hidden')

def main():
    # test0()
    # test1()
    # test2()
    test3()
    
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
    s1.refreshSource()
    s1.disconnect()

if __name__ == '__main__':
    main()