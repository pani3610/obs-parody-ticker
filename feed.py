import feedparser
import json

# feed_url = "https://babylonbee.com/feed"
feed_url = "https://www.theonion.com/content/feeds/daily"

feed = feedparser.parse(feed_url)
# print(feed)
with open("newsfeed.json","w") as jsonfile:
    json.dump(feed,jsonfile, indent=4)

# with open("newsfeed.json","r") as jsonfile:
#     feed_dict = json.load(jsonfile)

# feed_dict = json.loads('newsfeed.json')
# print(feed_dict)
with open('feed_text.txt',"w") as txtfile:
    for newsitem in feed['entries']:
        # txtfile.write(newsitem['title'])
        # txtfile.write('. <> ')
        print(newsitem['title'])

    