from obswebsocket import obsws,requests,exceptions,events
import os
from dotenv import load_dotenv
from extrafunctions import * 
import sys
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
        return(response.getBaseWidth())
    
    def getSourcePositionX(self):
        response=self.ws.call(requests.GetSceneItemProperties(self.sourcename,self.scenename))

