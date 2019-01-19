import analyze
import re
handle = "SkyNews"
tweets = [tweet["full_text"] for tweet in twitter.getTweets(handle, 1000)]

with open(handle+".txt", "a", encoding="utf-8") as f:
	for tweet in tweets:
		if not tweet[:2] == "RT":
			tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
			f.write(tweet + "\n")