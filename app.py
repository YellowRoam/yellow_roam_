app = Flask(__name__)

@app.route("/")
def home():
    return "YellowRoam is live!"
