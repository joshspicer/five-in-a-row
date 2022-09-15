from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route('/registerPlayer', methods=['POST'])
# def register_player():
#     # TODO
#     return 'YOU ARE PLAYER X'


# @app.route("/checkMove", methods=["POST"])
# def check_move():
#     j = request.get_json()
#     client_board = j['board']
#     client_turn = j['turn']
#     return j