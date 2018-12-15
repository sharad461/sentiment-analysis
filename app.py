from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

@app.route('/')
def home():
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run(debug=True)
