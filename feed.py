import feedparser
import json

def extract_headlines(url):
    headlines = []
    feed = feedparser.parse(url)
    
    for newsitem in feed['entries']:
        
        punctuated_headline = newsitem['title']+'.'
        headlines.append(punctuated_headline)
    
    return(headlines)

def export_json(url):
    feed = feedparser.parse(url)
    with open("newsfeed.json","w") as jsonfile:
        json.dump(feed,jsonfile, indent=4)

def export_text(headline_list):
    with open('feed_text.txt',"a") as txtfile:
            txtfile.writelines(headline_list)           

def empty_txtfile():
    with open('feed_text.txt',"w") as txtfile:
            txtfile.write('')           

def main():
    feed_urls = ["https://babylonbee.com/feed","https://www.theonion.com/content/feeds/daily"]
    empty_txtfile()
    for url in feed_urls:
        hl = extract_headlines(url)
        export_text(hl)
        # print(hl)

if __name__=='__main__':
    main()