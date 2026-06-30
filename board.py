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
        # Using Unicode box-drawing characters for a professional look
        top_left = "┌" 
        top_right = "┐"
        bottom_left = "└"
        bottom_right = "┘"
        horizontal = "───"
        vertical = "│"
        t_junction = "┬"
        b_junction = "┴"
        cross_junction = "┼"

        # Adjust content width based on board size (numbers might take more space)
        content_width = 3 if self.size < 10 else len(str(self.size * self.size - 1)) + 2
        horizontal_line = "─" * content_width

        # Top border
        print(f"{top_left}{horizontal_line}{t_junction}" * (self.size - 1) + f"{top_left if False else '┌'}{horizontal_line}{top_right}")
        # Fixed the top border logic slightly to be a single string
        # print(f"{top_left}{horizontal_line}{t_junction}" * (self.size - 1) + f"{horizontal_line}{top_right}")
        # Let's use a simpler cleaner approach:
        
    def display_fixed(self):
        print("\n")
        w = 3 if self.size < 10 else len(str(self.size * self.size - 1)) + 2
        h = "─" * w
        
        # Top
        border_top = f"┌{'┬'.join([h]*self.size)}┐"
        print(border_top)
        
        for r in range(self.size):
            row_str = "│"
            for c in range(self.size):
                cell = self.cells[r * self.size + c]
                if cell == 'X': 
                    fmt = f"{Colors.BLUE}{cell}{Colors.RESET}"
                elif cell == 'O': 
                    fmt = f"{Colors.RED}{cell}{Colors.RESET}"
                else: 
                    fmt = " " if self.size == 3 else str(r * self.size + c)
                
                # Center the content in the width w
                row_str += f" {fmt.center(w-2)} " + "│"
            print(row_str)
            if r < self.size - 1:
                border_mid = f"├{'┼'.join([h]*self.size)}┤"
                print(border_mid)
        
        border_bot = f"└{'┴'.join([h]*self.size)}┘"
        print(border_bot + "\n")

    def make_move(self, position: int, player: str) -> bool:
        if 0 <= position < len(self.cells) and self.cells[position] == ' ':
            self.cells[position] = player
            return True
        return False

    def check_winner(self) -> Optional[str]:
        for row in range(self.size):
            start = row * self.size
            if all(self.cells[start + i] == self.cells[start] != ' ' for i in range(self.size)):
                return self.cells[start]

        for col in range(self.size):
            if all(self.cells[col + i * self.size] == self.cells[col] != ' ' for i in range(self.size)):
                return self.cells[col]

        if all(self.cells[i * (self.size + 1)] == self.cells[0] != ' ' for i in range(self.size)):
            return self.cells[0]

        if all(self.cells[(i + 1) * self.size - 1] == self.cells[self.size - 1] != ' ' for i in range(self.size)):
            return self.cells[self.size - 1]

        if ' ' not in self.cells:
            return 'Draw'
        
        return None
