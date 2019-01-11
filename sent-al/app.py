from gevent.monkey import patch_all
patch_all()

from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit
from os import environ
import modules.forms as forms
import modules.twitter_stream as twstream
from modules.load_model import LoadModel
from threading import Thread

thread, tag, run = None, None, True

app = Flask(__name__)

# Key against CSRF
app.config["SECRET_KEY"] = '1f5aad569eef9cc369c32ec14f3d2cab'
socketio = SocketIO(app)

port = int(environ.get("PORT", 5000))

model = LoadModel("NaiveBayes")

class Listener(twstream.listener):
	def on_data(self, data):
		tweet = twstream.loads(data)["text"]
		polarity = model.polarity(tweet)
		socketio.emit("new tweet", {'tweet': tweet, 'polarity': polarity})
		return run

def stream(tag):
	stream = twstream.Stream(twstream.auth, Listener())
	stream.filter(languages=["en"], track=[tag])

def changeState(P):
	global thread
	global run

	if P == 0:
		run = False
		thread = False
	elif P == 1:
		run = True
		thread = True

@app.route('/')
def index():
    return render_template("home.html", title="Sentiment Analysis")

@app.route('/about')
def about():
    return render_template("about.html", title="About Sentiment Analysis",
    	name="Sentiment Analysis")

@app.route('/analyze/tweets')
def analyze_tweets():
	return render_template("tweets.html", title="Live Sentiment", form=forms.KeywordSearch())

@app.route('/analyze/tweets/<string:kw>', methods=["GET","POST"])
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
	return render_template("tweets.html", title="Live Sentiment", form=forms.KeywordSearch(data={"keyword": tag}))

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
