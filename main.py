from ticker import Ticker
from feed import Feed
import os
from obswebsocket import obsws,requests,exceptions,events
from dotenv import load_dotenv
from threading import Thread,Event
import json

def abs_path(filename:str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return(os.path.join(dir_path,filename))

class Session:
    """start a new session every time you run OBS"""
    def __init__(self):
        self.host = 'localhost'
        self.port = 4444
        load_dotenv()
        self._password = os.getenv('obswspass')
        self.ticker = buildTicker()
        self.ws = None
        self.ticker_scenes = []
        self.obs_quit_event  = Event()

    def startOrStopTicker(self,transition_event:events.TransitionBegin):
        # print(self.ticker_scenes)
        if(transition_event.getFromScene() not in self.ticker_scenes and transition_event.getToScene() in self.ticker_scenes):
            print('start ticker')
            self.ticker.start()
        elif(transition_event.getFromScene() in self.ticker_scenes and transition_event.getToScene() not in self.ticker_scenes):
            print('stop Ticker')
            self.ticker.stop()

    def startSession(self):
        self.ws = obsws(self.host,self.port,self._password)
        self.ws.connected = False
        try:
            self.ws.connect()
            self.ws.connected = True
        except exceptions.ConnectionFailure:
            print('Unable to connect to OBS')
            return()
        if(self.ws.connected):
            self.ws.register(self.startOrStopTicker,events.TransitionBegin)
            self.ws.register(self.stopSession,events.Exiting)# register() passes events.Exiting as a parameter to stopSession()
            self.importTickerScenes()
            print('Connected to OBS')
            self.obs_quit_event.wait()
            self.ws.disconnect()

    def stopSession(self,obs_event):
        print('OBS closed.')
        self.obs_quit_event.set()
        pass


    def importTickerScenes(self):
        scenes = self.ws.call(requests.GetSceneList())
        for scene in scenes.getScenes():
            # exportDictToJSON(scene,f'scene-{scene.get("name")}.json')
            for source in scene['sources']:
                if source.get("name")=="TIcker-tape" and source.get("render"):
                    self.ticker_scenes.append(scene["name"])
                    break
        return(self.ticker_scenes)
   



def buildTicker():
    t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
    feeds =['https://babylonbee.com/feed', 'https://www.theonion.com/content/feeds/daily', 'http://newsthump.com/feed/', 'https://www.betootaadvocate.com/feed/']
    threads =[]
    for rss_url in feeds:
        thread = Thread(target=addFeedToTicker,args=(rss_url,t))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return(t)

def addFeedToTicker(url:str,ticker:Ticker):
    f = Feed(url)
    ticker.addFeed(f)        

def exportDictToJSON(dictionary,savefile):
        with open(savefile,'w') as jsonfile:
            json.dump(dictionary,jsonfile,indent=4)
def main():
    # t = buildTicker()
    # # start the websocket and wait for scene switch
    # t.start()
    s = Session()
    s.startSession()

if __name__ == '__main__':
    main()