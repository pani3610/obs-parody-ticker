import feedparser
import json
class Feed():
    def __init__(self,feed_url,feed_name=None,feed_img_path=None):
        self.url = feed_url
        self.data = self.importData()

        self.name = self.data.feed.title if feed_name == None else feed_name
        self.subtitle = self.data.feed.subtitle
        
        self.image_path = feed_img_path

        self.headlines_count = 10



        self.text = FeedText(self)
        
        self.size = len(self.text.raw_string)
        

    def importData(self):
        class Data:
            def __init__(self,dictionary):
                self.__dict__.update(dictionary)
        
        data_dict = feedparser.parse(self.url)
        return(json.loads(json.dumps(data_dict),object_hook=Data))
    
    def exportFeedDataJson(self,savefile_location):
        data_dict = feedparser.parse(self.url)
        with open(savefile_location,'w') as jsonfile:
            json.dump(data_dict,jsonfile,indent=4)


    def calculateSize(self):
        self.size  = len(self.text.raw_string)
        return(self.size)
    
    def calculateTimeToCycle(self,size):#,Ticker.viewport_width,Ticker.text_speed):
        pass

    def createFeedText(self):
        return(FeedText(self))
    
    def updateFeedText(self):
        self.text = FeedText(self)

    
    def updateHeadlinesCount(self,new_count:int):
        self.headlines_count = new_count
        self.updateFeedText()

        
class FeedText():
    def __init__(self,feed:Feed):
        self.headlines_list = []
        self.headlines_count = min(feed.headlines_count,len(feed.data.entries)) #to avoid IndexOutofRangeheadline_count
        self.separator = " * "
        self.courtesy_text = f'This newsreel is brought to you by \"{feed.name}: {feed.subtitle}\"'
        self.raw_string = self.generateText(feed)
    
    
    def generateText(self,feed:Feed):
        raw_text = self.courtesy_text +self.separator
        self.headlines_list = self.extractHeadlines(feed)
        for headline in self.headlines_list:
            raw_text += headline+self.separator
        raw_text += self.courtesy_text

        return(raw_text)
        
    
    def extractHeadlines(self,feed):
        hl = []
        for entry in feed.data.entries[:self.headlines_count]:
            punctuated_headline = entry.title.upper()
            hl.append(punctuated_headline)
        return(hl)
 
    def updateCourtesyText(self,courtesy_input:str):
        self.courtesy_text = courtesy_input
        
        
    def updateSeparator(self,separator_input:str):
        self.separator = separator_input
        
    def updateRawString(self,feed:Feed):
        self.raw_string = self.generateText(feed)

def main1():
    f = Feed('https://www.thepoke.co.uk/category/news/feed/')
    f = Feed('https://www.betootaadvocate.com/feed/')
    # print(f.text.raw_string)

    # f.text.updateSeparator(' # ')
    
    # f.text.updateRawString(f)
    # print(f.text.raw_string)

    # f.text.updateCourtesyText("Hello")
    # f.text.updateRawString(f)
    # print(f.text.raw_string)


    # print(f.size)
    print(f.name,f.subtitle)
    f.exportFeedDataJson('onion.json')
if __name__=='__main__':
    main1()