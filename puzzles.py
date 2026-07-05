import json

PUZZLES = [
    {
        "id": 1,
        "name": "The Simple Win",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', 'X', ' ', 
                 'O', 'O', ' ', 
                 ' ', ' ', ' '],
        "solution": 2, # X wins at index 2
        "hint": "Look at the top row!"
    },
    {
        "id": 2,
        "name": "The Block",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', ' ', 'O', 
                 ' ', 'X', ' ', 
                 ' ', ' ', 'O'],
        "solution": 8, # O must block X at index 8 (diag)
        "hint": "Don't let X take the bottom right corner!",
        "player": 'O'
    },
    {
        "id": 3,
        "name": "The Fork",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', ' ', ' ', 
                 ' ', 'O', ' ', 
                 ' ', ' ', 'X'],
        "solution": [1, 3, 5, 7], # Any move that doesn't lose immediately? No, let's simplify for this tool.
        "hint": "Play strategically to create two winning paths."
    }
]

# Actually let's just use a few clear ones.
PUZZLES = [
    {
        "id": 1,
        "name": "The First Step",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', 'X', ' ', 
                  'O', ' ', ' ', 
                  ' ', ' ', ' '],
        "solution": 2,
        "hint": "Complete the row."
    },
    {
        "id": 2,
        "name": "The Guardian",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', ' ', 'O', 
                  ' ', 'X', ' ', 
                  ' ', ' ', ' '],
        "solution": 8,
        "hint": "Block the diagonal win."
    },
    {
        "id": 3,
        "name": "The Fork",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', ' ', ' ', 
                  ' ', 'O', ' ', 
                  ' ', ' ', 'X'],
        "solution": 1, # Simplified for this implementation
        "hint": "Create a double-threat situation."
    },
    {
        "id": 4,
        "name": "The Corner Trap",
        "size": 3,
        "win_condition": 3,
        "cells": ['X', ' ', ' ', 
                  ' ', 'O', ' ', 
                  ' ', ' ', ' '],
        "solution": 2, # X taking another corner
        "hint": "Control the corners to limit your opponent."
    }
]

def get_puzzles():
    return PUZZLES
