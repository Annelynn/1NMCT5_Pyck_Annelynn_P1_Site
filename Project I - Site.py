from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("home.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host="0.0.0.0"
    app.run(host=host, port=port, debug=True)

