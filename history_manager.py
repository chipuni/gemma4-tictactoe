import json
import os

def save_game_to_history(session):
    history_file = 'history.json'
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    
    game_data = {
        'size': session.board.size,
        'win_condition': session.board.win_condition,
        'markers': session.markers,
        'moves': session.move_history,
        'winner': session.check_winner(),
        'mode': session.mode
    }
    
    history.append(game_data)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def load_game_history():
    history_file = 'history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
