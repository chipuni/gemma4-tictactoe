# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"

from typing import Optional, List

class Board:
    def __init__(self, size: int = 3):
        self.size = size
        self.cells = [' ' for _ in range(size * size)]

    def display(self):
        print("\n")
        cell_width = 3
        # Top border
        top_border = "  " + "---+" * (self.size - 1) + "---"
        print(top_border)
        
        for row in range(self.size):
            row_cells = []
            for col in range(self.size):
                cell = self.cells[row * self.size + col]
                if cell == 'X': 
                    formatted = f"{Colors.BLUE}{cell}{Colors.RESET}"
                elif cell == 'O': 
                    formatted = f"{Colors.RED}{cell}{Colors.RESET}"
                else: 
                    # Use coordinates for empty cells in larger boards to help user
                    formatted = " " if self.size == 3 else str(row * self.size + col)
                row_cells.append(f" {formatted} ")
            
            print(f"|{'|'.join(row_cells)}|")
            if row < self.size - 1:
                print("  " + "---+" * (self.size - 1) + "---")
        
        print(top_border + "\n")

    def make_move(self, position: int, player: str) -> bool:
        if 0 <= position < len(self.cells) and self.cells[position] == ' ':
            self.cells[position] = player
            return True
        return False

    def check_winner(self) -> Optional[str]:
        # Check rows
        for row in range(self.size):
            start = row * self.size
            if all(self.cells[start + i] == self.cells[start] != ' ' for i in range(self.size)):
                return self.cells[start]

        # Check columns
        for col in range(self.size):
            if all(self.cells[col + i * self.size] == self.cells[col] != ' ' for i in range(self.size)):
                return self.cells[col]

        # Main diagonal
        if all(self.cells[i * (self.size + 1)] == self.cells[0] != ' ' for i in range(self.size)):
            return self.cells[0]

        # Anti-diagonal
        if all(self.cells[(i + 1) * self.size - 1] == self.cells[self.size - 1] != ' ' for i in range(self.size)):
            return self.cells[self.size - 1]

        if ' ' not in self.cells:
            return 'Draw'
        
        return None
