from gevent.monkey import patch_all
patch_all()

from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit
from os import environ

import modules.forms as forms
import modules.analyze as tw
from modules.load_model import LoadModel

from threading import Thread
from json import dumps, loads
from math import floor
from random import shuffle

thread, tag, run = None, None, True

app = Flask(__name__)

# Key against CSRF
app.config["SECRET_KEY"] = '1f5aad569eef9cc369c32ec14f3d2cab'

socketio = SocketIO(app)

port = int(environ.get("PORT", 5000))

model = LoadModel("NaiveBayes")

def weigh(topics):
	'''
	Assigns weights to topics for tag cloud
	'''
	maximum = topics[0][1]
	shuffle(topics)
	topics = dict(topics)

	for key in topics:
		topics[key] = floor(topics[key]/maximum*5)
	return topics

def changeState(P):
	'''
	Function to stop the twitter stream
	'''
	global thread
	global run

	if P == 0:
		run = False
		thread = False
	elif P == 1:
		run = True
		thread = True

class Listener(tw.listener):
	def on_data(self, data):
		tweet = loads(data)["text"]
		polarity = model.polarity(tweet)
		socketio.emit("new tweet", {'tweet': tweet, 'polarity': polarity})
		self.count += 1
		if self.count > 100:
			changeState(0)
		return run

def stream(tag):
	'''
	Function to start a twitter stream on keyword `tag`
	'''
	stream = tw.Stream(tw.auth, Listener())
	stream.filter(languages=["en"], track=[tag])

@app.route('/')
def index():
    return render_template("home.html", title="Sentiment Analysis")

@app.route('/analyze/text', methods=["GET", "POST"])
def text():
	text = request.form.get("text")
	topics, polarities, sentences, f = None, None, None, None
	if text:
		f = 1
		topics = tw.getTopics([text], 10)
		topics = weigh(topics) if topics else None
		sentences = tw.textTokenize(text)
		text_polarity = model.label(text)

		sentences = tw.group_by_polarity([(model.label(sentence), sentence) for sentence in sentences])

		polarities = {}
		for polarity, sentence in sentences.items():
			polarities[polarity] = len(sentence)
	return render_template('text.html',title="Text Analysis", form=forms.TextClassification(data={"text":text}), topics=topics, polarities=polarities, sentences=sentences, f=f)

@app.route('/about')
def about():
    return render_template("about.html", title="About Sentiment Analysis", name="Sentiment Analysis")

@app.route('/analyze/tweets')
def tweets():
	return render_template("tweets.html", title="Twitter Analysis")

@app.route('/analyze/keyword')
def analyze_tweets():
	return render_template("keywords.html", title="Live Sentiment", form=forms.KeywordSearch())

@app.route('/analyze/keyword/<string:kw>')
def analyze_tweets_keyword(kw):
	try:
		global tag
		tag = kw
		changeState(1)
		thread = Thread(target=stream, args=(tag,))
		thread.daemon = True
	except Exception as e:
		print("Error: ", e)
	thread.start()
	return render_template("keywords.html", title="Live Sentiment", form=forms.KeywordSearch(data={"keyword": tag}), live=1)

@app.route('/analyze/twitter')
def analyze_twitter():
	return render_template("people.html", title="Profile Sentiment", form=forms.ProfileSearch())

@app.route('/analyze/twitter/<string:st>')
def analyze_twitter_st(st):
	searchResults = tw.profilesearch(st, 12)
	return render_template("people.html", title="Profile Sentiment", form=forms.ProfileSearch(data={"searchTerm":st}), results=searchResults)

@app.route('/analyze/people/<string:name>')
def analyze_people(name):
	error = None
	try:
		tweets = list(reversed(tw.getTweets(name, 65)))		
		topics = weigh(tw.getTopics([tweet["full_text"] for tweet in tweets], 15))
		polarity = []
		for tweet in tweets:
			polarity.append(model.polarity(tweet["full_text"]))

		t = {}
		for sn, tweet in enumerate(tweets): t[str(sn+1)] = tweet
		tweets = t
	except Exception as e:
		tweets, polarity, topics = None, None, None
		error = "That twitter handle doesn't seem to exist!"
	return render_template("profile.html", title=(name+" - Profile Sentiment"), tweets=tweets, polarities=polarity, n=name, topics=topics, error=error)

@socketio.on("stop-stream")
def stop(data):
	changeState(0)

@socketio.on("continue-stream")
def cont(data):
	changeState(1)
	thread = Thread(target=stream, args=(tag,))
	thread.daemon = True
	thread.start()

if __name__ == "__main__":
	socketio.run(app, host='0.0.0.0', port=port, debug=True)