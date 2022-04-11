from time import sleep
from obswebsocket import obsws,requests,exceptions,events
import os
from dotenv import load_dotenv
from extrafunctions import * 
import sys
from tickertextmod import fill
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
    def registerEvents(self):
        self.transform_changed = self.ws.register(self.inform,events.SceneItemTransformChanged)

    def inform(self,event):
        print('width changed')
        print(event.getItemName())
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
    events.SceneItemTransformChanged()
def main():
    s= OBSSession()
    s.connect()
    s.registerEvents()
    print(s.getSourcePositionX())
    print(s.getScrollSpeed())
    print(s.getSourceSourceWidth())
    fill('I'*100)
    sleep(3)
    fill('X'*1000)
if __name__ == '__main__':
    main()