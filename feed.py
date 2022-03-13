import feedparser
import json

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

def export_text(headline_list):
    with open('feed_text.txt',"a") as txtfile:
            for headline in headline_list:
                txtfile.write(headline)
                txtfile.write('  //  ')           

def empty_txtfile():
    with open('feed_text.txt',"w") as txtfile:
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