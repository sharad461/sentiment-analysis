from json import loads
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from os import getenv

TWIT_API = getenv('TWIT_API', 'UdBwYOS9iyz2AKM2XlVLj041v')
TWIT_SECRET = getenv('TWIT_SECRET', 'mFnjIkKlqOIFEF8pLS8JKNUaNmzIdJPl5KD8evx2ijbVZ8Im2N')
TWIT_ACCESS_TOKEN = getenv('TWIT_ACCESS_TOKEN', '1074976321523146757-tEPhRk2TTSoQ9QQoYQSUY2RxwNAtAe')
TWIT_ACCESS_SECRET = getenv('TWIT_ACCESS_SECRET', 'f4ed2V4B72aBxMo3Hy0ezPIJ5UIqc8SORUs0nSUBvA3lX')

class listener(StreamListener):
	# Currently reads only the tweet text. Also see if metadata can improve analysis.

    def on_data(self, data):
        tw_element = loads(data)
        tweet = tw_element["text"]
        print(tweet)
        return True

    def on_error(self, status):
         app.logger.info("Error! %", (status))

def stream(tag):
	'''
	A stream is probably better with single keywords. Multiple keywords ("apple", "android") will shift live sentiment badly.
	'''
	stream = Stream(auth, listener())
	stream.filter(languages=["en"], track=[tag])


auth = OAuthHandler(TWIT_API,TWIT_SECRET)
auth.set_access_token(TWIT_ACCESS_TOKEN,TWIT_ACCESS_SECRET)

if __name__ == "__main__":
	stream("apple")