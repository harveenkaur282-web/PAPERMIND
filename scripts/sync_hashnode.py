import feedparser
from pprint import pprint

RSS_URL = "https://buildingthings.hashnode.dev/rss.xml"

feed = feedparser.parse(RSS_URL)

print("Feed keys:")
pprint(feed.feed)

print("\nEntries:", len(feed.entries))

print("\nFirst entry:")
pprint(feed.entries[0])