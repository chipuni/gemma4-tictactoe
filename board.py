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
    def __init__(self, size: int = 3, win_condition: int = 3):
        self.size = size
        self.win_condition = win_condition
        self.cells = [' ' for _ in range(size * size)]
        self.history = [] # For undo functionality

    def display_fixed(self, markers: dict = {'X': 'X', 'O': 'O'}, highlight_line: List[int] = None):
        print("\n")
        w = 3 if self.size < 10 else len(str(self.size * self.size - 1)) + 2
        h = "─" * w
        
        # Print column headers (A, B, C...)
        headers = "  " + " ".join([chr(65 + i) if i < 26 else f"{i//26+1}{chr(65 + i%26)}" for i in range(self.size)])
        print(headers)

        border_top = f"┌{'┬'.join([h]*self.size)}┐"
        print(border_top)
        
        for r in range(self.size):
            # Print row header (1, 2, 3...)
            row_label = f"{r + 1} " if r < 10 else f"{r + 1:2}"
            row_str = f"{row_label}│"
            for c in range(self.size):
                idx = r * self.size + c
                cell = self.cells[idx]
                
                # Colors for markers
                if cell == 'X': 
                    fmt = f"{Colors.BLUE}{markers.get('X', 'X')}{Colors.RESET}"
                elif cell == 'O': 
                    fmt = f"{Colors.RED}{markers.get('O', 'O')}{Colors.RESET}"
                else: 
                    fmt = " " if self.size == 3 else str(idx)

                # Highlight winning line in yellow background or bold
                if highlight_line and idx in highlight_line:
                    fmt = f"{Colors.YELLOW}{Colors.BOLD}{fmt}{Colors.RESET}"
                
                row_str += f" {fmt.center(w-2)} " + "│"
            print(row_str)
            if r < self.size - 1:
                border_mid = f"├{'┼'.join([h]*self.size)}┤"
                print(border_mid)
        
        border_bot = f"└{'┴'.join([h]*self.size)}┘"
        print(border_bot + "\n")

    def make_move(self, position: int, player: str) -> bool:
        if 0 <= position < len(self.cells) and self.cells[position] == ' ':
            self.history.append((position, self.cells[position]))
            self.cells[position] = player
            return True
        return False

    def undo_move(self):
        if not self.history:
            return False
        pos, old_val = self.history.pop()
        self.cells[pos] = old_val
        return True

    def get_winning_lines(self) -> List[List[int]]:
        lines = []
        k = self.win_condition
        s = self.size

        # Horizontal lines of length k
        for r in range(s):
            for c in range(s - k + 1):
                lines.append([r * s + (c + i) for i in range(k)])
        
        # Vertical lines of length k
        for c in range(s):
            for r in range(s - k + 1):
                lines.append([(r + i) * s + c for i in range(k)])
        
        # Diagonal lines (\) of length k
        for r in range(s - k + 1):
            for c in range(s - k + 1):
                lines.append([(r + i) * s + (c + i) for i in range(k)])
        
        # Anti-diagonal lines (/) of length k
        for r in range(s - k + 1):
            for c in range(k - 1, s):
                lines.append([(r + i) * s + (c - i) for i in range(k)])

        return lines

    def get_winning_line(self) -> Optional[List[int]]:
        """Returns the indices of the winning line if one exists."""
        for line in self.get_winning_lines():
            if all(self.cells[i] == self.cells[line[0]] != ' ' for i in line):
                return line
        return None

    def check_winner(self) -> Optional[str]:
        winning_line = self.get_winning_line()
        if winning_line:
            return self.cells[winning_line[0]]
        if ' ' not in self.cells:
            return 'Draw'
        return None

    def to_dict(self) -> dict:
        return {
            'size': self.size,
            'win_condition': self.win_condition,
            'cells': self.cells,
            'history': self.history
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        board = cls(size=data['size'], win_condition=data.get('win_condition', 3))
        board.cells = data['cells']
        board.history = data['history']
        return board
