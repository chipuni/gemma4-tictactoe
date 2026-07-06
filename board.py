# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"

class Themes:
    CLASSIC = {
        'X': Colors.BLUE,
        'O': Colors.RED,
        'border': Colors.RESET,
        'highlight': Colors.YELLOW
    }
    NEON = {
        'X': Colors.CYAN,
        'O': Colors.GREEN,
        'border': Colors.CYAN,
        'highlight': Colors.BOLD + Colors.CYAN
    }
    PASTEL = {
        'X': "\033[38;5;141m", 
        'O': "\033[38;5;213m", 
        'border': "\033[38;5;244m",
        'highlight': Colors.BOLD + "\033[38;5;226m"
    }
    
    @staticmethod
    def get(theme_name):
        themes = {
            'Classic': Themes.CLASSIC,
            'Neon': Themes.NEON,
            'Pastel': Themes.PASTEL
        }
        return themes.get(theme_name, Themes.CLASSIC)

from typing import Optional, List

class Board:
    def __init__(self, size: int = 3, win_condition: int = 3):
        self.size = size
        self.win_condition = win_condition
        self.cells = [' ' for _ in range(size * size)]
        self.history = [] # For undo functionality

    def display_fixed(self, markers: dict = {'X': 'X', 'O': 'O'}, highlight_line: List[int] = None, theme_name: str = 'Classic'):
        theme = Themes.get(theme_name)
        print("\n")
        w = 3 if self.size < 10 else len(str(self.size * self.size - 1)) + 2
        h = "─" * w
        
        # Print column headers (A, B, C...)
        headers = "    " + " ".join([chr(65 + i) if i < 26 else f"{i//26+1}{chr(65 + i%26)}" for i in range(self.size)])
        print(f"{theme['border']}{headers}{Colors.RESET}")
        
        border_top = f"  ┌{'┬'.join([h]*self.size)}┐"
        print(f"{theme['border']}{border_top}{Colors.RESET}")
        
        for r in range(self.size):
            # Print row header (1, 2, 3...)
            row_label = f"{r + 1} " if r < 10 else f"{r + 1:2}"
            row_str = f"{row_label} │"
            for c in range(self.size):
                idx = r * self.size + c
                cell = self.cells[idx]
                
                # Colors for markers
                if cell == 'X': 
                    fmt = f"{theme['X']}{markers.get('X', 'X')}{Colors.RESET}"
                elif cell == 'O': 
                    fmt = f"{theme['O']}{markers.get('O', 'O')}{Colors.RESET}"
                else: 
                    fmt = " " if self.size == 3 else str(idx)
                
                # Highlight winning line in yellow background or bold
                if highlight_line and idx in highlight_line:
                    fmt = f"{theme['highlight']}{fmt}{Colors.RESET}"
                
                row_str += f" {fmt.center(w-2)} " + "│"
            print(f"{theme['border']}{row_str}{Colors.RESET}")
            if r < self.size - 1:
                border_mid = f"├{'┼'.join([h]*self.size)}┤"
                print(f"{theme['border']}{border_mid}{Colors.RESET}")
        
        border_bot = f"└{'┴'.join([h]*self.size)}┘"
        print(f"{theme['border']}{border_bot}{Colors.RESET}\n")

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
    
    def get_coord(self, pos: int) -> str:
        row = pos // self.size
        col = pos % self.size
        col_char = chr(65 + col) if col < 26 else f"{col//26+1}{chr(65 + col%26)}"
        return f"{col_char}{row + 1}"
