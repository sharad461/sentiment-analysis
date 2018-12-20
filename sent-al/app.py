from flask import Flask, render_template, request, url_for, redirect
from os import environ
import modules.forms as forms
import modules.twitter_stream as twstream

app = Flask(__name__)

# Key for CSRF
app.config["SECRET_KEY"] = '1f5aad569eef9cc369c32ec14f3d2cab'

port = int(environ.get("PORT", 5000))

@app.route('/')
def index():
    return render_template("home.html", title="Sentiment Analysis")

@app.route('/about')
def about():
    return render_template("about.html", title="About Sentiment Analysis",
    	name="Sentiment Analysis")

@app.route('/analyze/tweets', methods=["GET"])
def analyze_tweets():
	# try:
	# 	if request.method == "GET":
	# 		if request.args.getlist('keyword'):
	# 			keyword = request.args.getlist('keyword')[0]
	# 			twstream.stream(keyword)
	# 			return render_template("tweets.html", tweets = tweets)
	# except Exception as e:
	# 	print(e)

	kw_form = forms.KeywordSearch()
	if kw_form.validate_on_submit():
		# form validated
		pass
	return render_template("tweets.html", title="Live Sentiment", form=kw_form)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port, debug=True)
