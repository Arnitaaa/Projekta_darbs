pip install Flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preili")
def preili():
    return render_template("preili.html")

@app.route("/pasaule")
def pasaule():
    return render_template("pasaule.html")

if __name__ == "__main__":
    app.run(debug=True)
