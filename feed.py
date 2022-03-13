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