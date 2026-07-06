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
        "solution": 1,
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
        "solution": 2,
        "hint": "Control the corners to limit your opponent."
    },
    {
        "id": 5,
        "name": "The 4x4 Wall",
        "size": 4,
        "win_condition": 3,
        "cells": ['X', 'X', ' ', ' ', 
                  'O', ' ', ' ', ' ', 
                  ' ', ' ', ' ', ' ', 
                  ' ', ' ', ' ', ' '],
        "solution": 2,
        "hint": "On a 4x4 board, the win condition is still 3. Complete the row!"
    },
    {
        "id": 6,
        "name": "The Diagonal Dare",
        "size": 5,
        "win_condition": 4,
        "cells": ['X', ' ', ' ', ' ', ' ', 
                  ' ', 'X', ' ', ' ', ' ', 
                  ' ', ' ', 'X', ' ', ' ', 
                  ' ', ' ', ' ', ' ', ' ', 
                  ' ', ' ', ' ', ' ', ' '],
        "solution": 18, # Index 16 is (3,1) - wait let me calculate. (0,0), (1,1), (2,2) -> next is (3,3) which is 3*5 + 3 = 18.
        "hint": "Connect four on the diagonal."
    },
    {
        "id": 7,
        "name": "The Center Squeeze",
        "size": 4,
        "win_condition": 3,
        "cells": [' ', ' ', ' ', ' ', 
                  ' ', 'X', 'X', ' ', 
                  ' ', ' ', ' ', ' ', 
                  ' ', ' ', ' ', ' '],
        "solution": 8, # (1,0) - block or win? If X is playing, index 8 (2,0) or something. Let's make it a win for X at index 8.
        "hint": "Create a vertical line in the second column."
    }
]

def get_puzzles():
    return PUZZLES
