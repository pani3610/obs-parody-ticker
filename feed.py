import feedparser
import json
from ticker import Ticker
class Feed(Ticker):
    def __init__(self,feed_name,feed_url,feed_img_path):
        self.name = feed_name
        self.url = feed_url
        self.image_path = feed_img_path
        self.size = 0
    
    def calculateSize(self):
        pass
    
    def calculateTimeToCycle(self,size):#,Ticker.viewport_width,Ticker.text_speed):
        pass

    class FeedText():
        def __init__(self,headline_count,separator):
            self.headlines_list = []
            self.headline_count = headline_count
            self.separator = separator
            self.courtesy_text = f'This newsreel is brought to you by {Feed.name}'
            self.raw_string = ''
        
        def extractHeadlines(self):
            self.headlines_list = []
            pass

        def calculatePadding(self):#,Ticker.empty_time):
            pass

        def changeCourtesyText():
            pass


    #Following code is a mockup.

    # def createFeedText(self,headline_count):
    #     ft = FeedText(headline_count,' //  ')
    #     ft.extractHeadlines()
    #     ft.addCourtesyText()
    #     ft.calculatePadding()
    #     ft.addpadding()
    #     return (ft.raw_string)

        
def extract_headlines(url,count=10): #extracts 10 recent headlines by default. Limited to 10 because long files breaks OBS.
    headlines = []
    feed = feedparser.parse(url)
    count = min(count,len(feed['entries'])) #to avoid IndexOutofRange
    for newsitem in feed['entries'][:count]:
        punctuated_headline = newsitem['title']
        headlines.append(punctuated_headline.upper())
    print('hl-count:',len(headlines))
    return(headlines)

def export_json(url):
    feed = feedparser.parse(url)
    with open("newsfeed.json","w") as jsonfile:
        json.dump(feed,jsonfile, indent=4)

def export_text(headline_list,target_file,padding=0,file_mode="w"): #TODO:add padding implicitly

    with open(target_file,file_mode) as txtfile:
            txtfile.write(" "*(padding//2))
            for headline in headline_list:
                txtfile.write(headline)
                txtfile.write('  //  ')
            txtfile.write(" "*(padding//2))           

def empty_txtfile(target_file):
    with open(target_file,"w") as txtfile:
            txtfile.write('')           

def main():
    feed_urls = ["https://babylonbee.com/feed","https://www.theonion.com/content/feeds/daily"]
    empty_txtfile()
    for url in feed_urls[0:1]:
        hl = extract_headlines(url,15)
        export_text(hl)
        print(hl)
    with open('feed_text.txt','r') as txt:
        text = txt.read()
        print(len(text))
if __name__=='__main__':
    main()