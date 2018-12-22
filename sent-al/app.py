from gevent.monkey import patch_all
patch_all()

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, url_for, redirect
from os import environ
import modules.forms as forms
import modules.twitter_stream as twstream
from threading import Thread

thread = None

app = Flask(__name__)

# Key against CSRF
app.config["SECRET_KEY"] = '1f5aad569eef9cc369c32ec14f3d2cab'
socketio = SocketIO(app)

port = int(environ.get("PORT", 5000))

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

@app.route('/analyze/tweets/<string:kw>')
def analyze_tweets_keyword(kw):
	try:
		global thread
		if thread == None:
			thread = Thread(target=twstream.stream, args=(kw, socketio))
			thread.daemon = True
	except Exception as e:
		print("Error: ", e)
	thread.start()
	return render_template("tweets.html", title="Live Sentiment", form=forms.KeywordSearch())

if __name__ == "__main__":
	socketio.run(app, host='0.0.0.0', port=port, debug=True)
