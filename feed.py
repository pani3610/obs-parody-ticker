import feedparser
import favicon
import requests
import shutil
import json
from PIL import Image,ImageDraw,ImageChops
from io import BytesIO
from extrafunctions import abs_path,convertObjectToJson
import pickle
class Feed():
    def __init__(self,feed_url,feed_name=None,feed_img_path=None,hl_count=None):
        self.url = feed_url
        self.data = feedparser.parse(self.url)#self.importData()

        self.name = self.data.feed.title if feed_name == None else feed_name
        self.subtitle = self.data.feed.subtitle
        
        self.logo = FeedLogo(feed_url) if feed_img_path == None else FeedLogo(feed_img_path)

        self.headlines_count = len(self.data.entries) if hl_count==None else min(hl_count,len(self.data.entries))#to avoid IndexOutofRangeheadline_count

        
        self.text = FeedText(self)
        
        self.size = len(self.text.raw_string)
        
        self.data_update_time = self.findDataUpdateTime()

    # def importData(self): #Not Required as feedparser.parse returns a FeedParserDict not a traditional dict. FeedParserDict is already an Object.
    #     '''This function converts a dictionary into an Object'''
    #     class Data:
    #         def __init__(self,dictionary):
    #             self.__dict__.update(dictionary)
        
    #     data_dict = feedparser.parse(self.url)
    #     return(json.loads(json.dumps(data_dict),object_hook=Data))

    def findDataUpdateTime(self):
        try:
            return(self.data.feed.updated)
        except:
            # return(self.data.headers.date)
            return(None)
    
    def exportFeedDataJson(self,savefile_location):
        convertObjectToJson(self.data,savefile_location)

    def calculateSize(self):
        self.size  = len(self.text.raw_string)
        return(self.size)
    
    def updateHeadlinesCount(self,new_count:int):
        self.headlines_count = min(new_count,len(self.data.entries))
        self.text.updateFeedText()

    def returnFeedSummary(self):
        return(f'{self.name} | {self.headlines_count} headlines | Feed data latest by {self.data_update_time} | {self.size} characters long')
    
    def extractHeadlines(self):
        hl = [entry.title.upper() for entry in self.data.entries[:self.headlines_count]] 
        return(hl)
        for entry in self.data.entries[:self.headlines_count]:
            punctuated_headline = entry.title.upper()
            hl.append(punctuated_headline)
        return(hl)

    def saveToPickleFile(self,picklefile,filemode='a'):
        with open(picklefile,f'{filemode}b') as pf:
            pickle.dump(self,pf,protocol=4)

    

class FeedLogo():
    def __init__(self,source_loc:str,width=None,height=None,format='png'):
        # self.feed = feed
        self.name = source_loc.replace('.','_').replace('/','-')#feed.name.replace(' ','')
        self.format = format
        # self.savefile= abs_path(f'{savefile_loc}{self.name}.{self.format}')
        try:
            self.image = Image.open(source_loc)
            print('local file used')
        except Exception:
            self.main_url = '/'.join(source_loc.split('/')[:3])
            self.image = self.fetchLogoFromURL()
        # print('try works')
        self.circular_crop()
        # self.save()
        if None not in (width,height):
            self.resize((width,height))

    def fetchLogoFromURL(self):
        icons = favicon.get(self.main_url)
        for icon in icons:
            if icon.format == self.format:
                response = requests.get(icon.url,stream=True)
                if(response.status_code==200):
                    img = Image.open(BytesIO(response.content))
                    img = img.convert('RGBA')
                    
                    # with open(self.savefile,'wb') as img_file:
                    #     response.raw.decode_content = True
                    #     shutil.copyfileobj(response.raw,img_file)
                    # img = Image.open(self.savefile)
                    return(img)
        else:
            print(f'No logo retrieved for {self.name}')
            return(None)
    
    def save(self,file_loc=None):
        self.image.save(abs_path(file_loc))

    def resize(self,new_size:tuple):
        if(self.image == None):
            print(f"Image is not defined for logo for {self.name}")
            return()
        self.image = self.image.resize(new_size)
        # self.save()
    
    def circular_crop(self):
        if(self.image == None):
            print(f"Image is not defined for logo for {self.name}")
            return()
        mask = Image.new('L', self.image.size , 0)
        
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0)+self.image.size,fill=255)

        mask = ImageChops.darker(mask,self.image.split()[-1])
        self.image.putalpha(mask)
        # self.save()
class FeedText():
    def __init__(self,feed:Feed):
        self.feed = feed
        self.separator = " * "
        self.courtesy_text = f'This newsreel is brought to you by \"{feed.name}: {feed.subtitle}\"'
        self.raw_string = self.generateText()
    
    def generateText(self):
        raw_list = [self.courtesy_text]*2
        raw_list[1:1] = self.feed.extractHeadlines()
        raw_text = self.separator.join(raw_list)      

        return(raw_text)
        
    def updateFeedText(self):
        self.raw_string = self.generateText()
  
 
    def updateCourtesyText(self,courtesy_input:str):
        self.courtesy_text = courtesy_input
        self.updateFeedText()
        
    def updateSeparator(self,separator_input:str):
        self.separator = separator_input
        self.updateFeedText()

    def __str__(self):
        return(self.raw_string)

        
def main1():
    f = Feed("https://www.betootaadvocate.com/feed/",hl_count=4)
    f.logo.save('betoota.png')
    # f = Feed("https://babylonbee.com/feed")#,feed_img_path='src/https:--babylonbee_com-feed.png')
    # f.text.updateCourtesyText('hello')
    # f.text.updateSeparator('#')
    # print(f.text)
    # print(f.headlines_count)
    # f.updateHeadlinesCount(f.headlines_count//2)
    # print(f.text)

    # f = Feed("https://www.theonion.com/content/feeds/daily",hl_count=4)
    # f.saveToPickleFile('feed_examples.pkl')
    # print(f.text.raw_string)
    print(f.extractHeadlines())
    # f.text.updateSeparator(' # ')
    
    # f.text.updateRawString(f)
    # print(f.text.raw_string)

    # f.text.updateCourtesyText("Hello")
    # f.text.updateRawString(f)
    # print(f.text.raw_string)


    # print(f.size)
    print(f.name,f.subtitle)
    # print(f.headlines_count)
    print(f.data_update_time)
    # f.getFeedLogo()
    # print(f.calculateSize())
    # print(f.returnFeedSummary())
    # f.exportFeedDataJson('onion.json')
if __name__=='__main__':
    main1()