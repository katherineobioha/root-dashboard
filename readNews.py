import feedparser



NewsFeed = feedparser.parse("https://agriculture.einnews.com/rss/CHGZ74Uzpfp_XXUK")
entry = NewsFeed.entries[1]
print ("******")
print (entry.published)
print ("******")
print (entry.title)
print ("...")
print (entry.description)
print ("------News Link--------")
print (entry.link)
