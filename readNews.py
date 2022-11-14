import feedparser
import pandas as ps
from pandas import DataFrame


def getnews():
    NewsFeed = feedparser.parse("https://agriculture.einnews.com/rss/CHGZ74Uzpfp_XXUK")
    entry = NewsFeed.entries
    # print ("******")
    # print (entry.published)
    # print ("******")
    # print (entry.title)
    # print ("...")
    # print (entry.description)
    # print ("------News Link--------")
    # print (entry.link)
    return entry;


# appp = DataFrame(getnews())

# print(getnews())