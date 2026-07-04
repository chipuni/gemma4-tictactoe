import json
import os

def save_game(session, slot=1):
    filename = f"savegame_{slot}.json"
    data = {
        'board': session.board.to_dict(),
        'current_player': session.current_player,
        'mode': session.mode,
        'difficulty': session.difficulty,
        'markers': session.markers,
        'cpu_speed': session.cpu_speed
    }
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_game(session, slot=1):
    filename = f"savegame_{slot}.json"
    if not os.path.exists(filename):
        return False
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # We trust the laoder inside game_manager but can handle file path here
    # Actually for simplicity we'll just pass filename back to session.load_game()
    return filename

def list_save_slots():
    slots = []
    for i in range(1, 11):
        if os.path.exists(f"savegame_{i}.json"):
            slots.append(i)
    return slots
