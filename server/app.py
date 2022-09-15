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

state = initial_state

# Store WebSocket session ID to authenticate user.
player_black = None
player_blue = None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def validate_is_player_turn(session_id):
    global player_black, player_blue

    if player_black is None or player_blue is None:
        return False, "All players not yet connected"
    
    if session_id == player_black and state['turn'] == BLACK:
        return True, None
    elif session_id == player_blue and state['turn'] == BLUE:
        return True, None
    else:
        return False, "Not your turn!"

def reset_game():
    global state, player_black, player_blue
    player_black = None
    player_blue = None
    state = initial_state

def check_if_game_over():
    # Check horizontals for 5 in a row of the same color.
    for row in range(19):
        for col in range(15):
            if state['board'][row][col] == EMPTY:
                continue
            if state['board'][row][col] == state['board'][row][col+1] == state['board'][row][col+2] == state['board'][row][col+3] == state['board'][row][col+4]:
                return True, state['board'][row][col]
    # Check verticals for 5 in a row of the same color.
    for row in range(15):
        for col in range(19):
            if state['board'][row][col] == EMPTY:
                continue
            if state['board'][row][col] == state['board'][row+1][col] == state['board'][row+2][col] == state['board'][row+3][col] == state['board'][row+4][col]:
                return True, state['board'][row][col]
    # Check diagonals for 5 in a row of the same color.
    for row in range(15):
        for col in range(15):
            if state['board'][row][col] == EMPTY:
                continue
            if state['board'][row][col] == state['board'][row+1][col+1] == state['board'][row+2][col+2] == state['board'][row+3][col+3] == state['board'][row+4][col+4]:
                return True, state['board'][row][col]

    return False, None

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
        emit('reject_with_error', "Two players already connected", broadcast=False)

    # Emit the initial game state to the joined player
    emit('state', state)


# Handles a move made by a player
@socketio.event
def move(tile):
    print(tile)
    # Don't allow a move if it's not the player's turn,
    # or if there are not two connected players.
    result, msg = validate_is_player_turn(request.sid)
    if not result:
        emit('reject_with_error', msg, broadcast=False)
        return
 
    # Don't allow a move if the tile is already occupied.
    if state['board'][tile['xIdx']][tile['yIdx']] != EMPTY:
        emit('reject_with_error', "Tile already occupied, try again!", broadcast=False)
        return

    # Update the game state
    state['board'][tile['xIdx']][tile['yIdx']] = state['turn']
    state['turn'] = BLACK if state['turn'] == BLUE else BLUE

    # Broadcast the updated game state to all players
    emit('state', state, broadcast=True)

    # Check if the game is over
    result, msg = check_if_game_over()
    if result:
        emit('game_over', msg, broadcast=True)
        reset_game()

if __name__ == '__main__':
    socketio.run(app)