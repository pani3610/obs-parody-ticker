from time import sleep
from ticker import Ticker
from feed import Feed
import os
from obswebsocket import obsws,requests,exceptions,events
from dotenv import load_dotenv

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
        self.ticker = self.buildTicker()
    
    def startTicker(self,transition_event):
        if(transition_event.getFromScene()=='TheStart' and transition_event.getToScene()!='TheEnd'):
            print('restart ticker')

    def startSession(self):
        ws = obsws(self.host,self.port,self._password)
        ws.register(self.startTicker,events.TransitionBegin)
        ws.connected = False
        try:
            ws.connect()
            ws.connected = True
        except exceptions.ConnectionFailure:
            print('Unable to connect to OBS')
            return()
        if(ws.connected):
            print('Connected to OBS')
            sleep(60)
            ws.disconnect()
            # scene = ws.call(requests.GetCurrentScene())
            # ws.register(on_switch,events.SwitchScenes)


    def buildTicker(self):
        t =Ticker(abs_path('feed_text_dev.txt'),abs_path('feed_img_dev.png'))
        feeds ={"https://babylonbee.com/feed":'src/babylonbee.png',
                "https://www.theonion.com/content/feeds/daily":'src/onion.png',
                "http://newsthump.com/feed/":'src/newsthump.png',            
                "https://www.betootaadvocate.com/feed/":'src/betoota.png'}

        for rss_url,logo_location in feeds.items():        
            f = Feed(rss_url,feed_img_path=abs_path(logo_location))
            t.addFeed(f)
        
        return(t)

def main():
    # t = buildTicker()
    # # start the websocket and wait for scene switch
    # t.start()
    s = Session()
    s.startSession()

if __name__ == '__main__':
    main()