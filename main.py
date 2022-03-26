from time import sleep
from ticker import Ticker
from feed import Feed
import os
from obswebsocket import obsws,requests,exceptions,events
from dotenv import load_dotenv
from threading import Thread
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
            self.importTickerScenes()
            print('Connected to OBS')
            input('Press enter to close')
            self.ws.disconnect()


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
    feeds ={"https://babylonbee.com/feed":'src/babylonbee.png',
            "https://www.theonion.com/content/feeds/daily":'src/onion.png',
            "http://newsthump.com/feed/":'src/newsthump.png',            
            "https://www.betootaadvocate.com/feed/":'src/betoota.png'}

    threads =[]
    for rss_url,logo_location in feeds.items():
        thread = Thread(target=addFeedToTicker,args=(rss_url,logo_location,t))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return(t)

def addFeedToTicker(url:str,image_loc:str,ticker:Ticker):
    f = Feed(url,feed_img_path=abs_path(image_loc))
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