import os
from flask import Flask, render_template

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():
    return render_template("index.html")

app.run(host='0.0.0.0', port=port, debug=True)
