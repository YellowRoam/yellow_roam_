from flask import Flask
app = Flask(__name__)
@app.route("/")@app.route("/")
def home():
    return "YellowRoam is live!"
