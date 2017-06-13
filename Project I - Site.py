from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/account')
def account():
    return render_template("account.html")

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host="0.0.0.0"
    app.run(host=host, port=port, debug=True)

