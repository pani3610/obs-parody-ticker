from feed import *

cpv = 95 #average number of characters to fill up the viewport
cps = 5 #average new characters intrpduced per second. Horizontal scroll speed in OBS set to 40.


# feed_urls = {"The Babylon Bee" : "https://babylonbee.com/feed"}
feed_urls = {"The Onion": "https://www.theonion.com/content/feeds/daily"}
empty_txtfile()
for news_source,url in feed_urls.items():
    headlines_list = extract_headlines(url,3)
    courtesy_text = f"This news is brought to you by '{news_source}'"
    display_text = [courtesy_text]
    display_text.extend(headlines_list)
    display_text.append(courtesy_text)
    display_text.append(" "*(cpv*3))
    print(display_text)
    export_text(display_text)
    
with open('feed_text.txt','r') as txt:
    text = txt.read()
    print(len(text))