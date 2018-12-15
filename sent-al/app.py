import os
from flask import Flask, render_template

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():
    return render_template("home.html")

if __name__ == "__main__":
	app.run(port=port, debug=True)
