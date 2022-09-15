from tkinter import E
from flask import Flask
from flask import request
from flask_socketio import SocketIO, emit


EMPTY = 0
BLACK = 1
BLUE = 2

initial_state = {
    'board' : [[EMPTY for col in range(19)] for row in range(19)],
    'turn' : BLACK
}

# Store WebSocket session ID to authenticate user.
player_black = None
player_blue = None

initial_state['board'][5][5] = BLACK

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# A client request to join the game.
@socketio.event
def join_game():
    global player_black, player_blue
    print("Session ID: " + request.sid)

    if player_black is None:
        player_black = request.sid
        emit('accept_player', BLACK, broadcast=False)
    elif player_blue is None:
        player_blue = request.sid
        emit('accept_player', BLUE, broadcast=False)
    else:
        emit('reject_player', broadcast=False)

    # Emit the initial game state
    emit('state', initial_state)



if __name__ == '__main__':
    socketio.run(app)