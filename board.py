# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"

from typing import Optional

class Board:
    def __init__(self):
        self.cells = [' ' for _ in range(9)]

    def display(self):
        print("\n")
        for i in range(0, 9, 3):
            row = self.cells[i:i+3]
            formatted_row = []
            for cell in row:
                if cell == 'X': formatted_row.append(f"{Colors.BLUE}X{Colors.RESET}")
                elif cell == 'O': formatted_row.append(f"{Colors.RED}O{Colors.RESET}")
                else: formatted_row.append(" ")
            
            print(f" {formatted_row[0]} | {formatted_row[1]} | {formatted_row[2]} ")
            if i < 6:
                print("-----------")
        print("\n")

    def make_move(self, position: int, player: str) -> bool:
        if 0 <= position < 9 and self.cells[position] == ' ':
            self.cells[position] = player
            return True
        return False

    def check_winner(self) -> Optional[str]:
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Cols
            [0, 4, 8], [2, 4, 6]             # Diags
        ]
        for condition in win_conditions:
            if self.cells[condition[0]] == self.cells[condition[1]] == self.cells[condition[2]] != ' ':
                return self.cells[condition[0]]
        
        if ' ' not in self.cells:
            return 'Draw'
        
        return None
