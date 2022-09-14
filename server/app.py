from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/registerPlayer', methods=['POST'])
def registerPlayer():
    # TODO
    return 'YOU ARE PLAYER X'

@app.route("/checkMove", methods=["POST"])
def checkMove():
    return {"status": "ok"}