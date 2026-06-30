import random
from typing import List, Optional

# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"

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

class TicTacToe:
    def __init__(self, mode='PvP'):
        self.board = Board()
        self.current_player = 'X' # X always goes first
        self.mode = mode 

    def minimax(self, board_cells: List[str], depth: int, is_maximizing: bool) -> int:
        # Helper to check winner on a temporary state
        temp_board = Board()
        temp_board.cells = board_cells[:]
        winner = temp_board.check_winner()

        if winner == 'O': return 10 - depth
        if winner == 'X': return depth - 10
        if winner == 'Draw': return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board_cells[i] == ' ':
                    board_cells[i] = 'O'
                    score = self.minimax(board_cells, depth + 1, False)
                    board_cells[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board_cells[i] == ' ':
                    board_cells[i] = 'X'
                    score = self.minimax(board_cells, depth + 1, True)
                    board_cells[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def get_cpu_move(self) -> int:
        best_score = -float('inf')
        best_move = -1
        available_moves = [i for i, x in enumerate(self.board.cells) if x == ' ']
        
        for move in available_moves:
            self.board.cells[move] = 'O'
            score = self.minimax(self.board.cells, 0, False)
            self.board.cells[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move if best_move != -1 else random.choice(available_moves)

    def play(self):
        print(f"{Colors.BOLD}Welcome to Tic Tac Toe!{Colors.RESET}")
        print("Positions are 0-8, starting from top-left.")
        
        while True:
            self.board.display()
            
            if self.current_player == 'X' or (self.mode == 'PvP' and self.current_player == 'O'):
                try:
                    prompt = f"Player {Colors.BOLD}{self.current_player}{Colors.RESET}, enter move (0-8): "
                    move = int(input(prompt))
                except ValueError:
                    print(f"{Colors.RED}Invalid input. Please enter a number between 0-8.{Colors.RESET}")
                    continue
            else:
                print(f"{Colors.CYAN}CPU is thinking...{Colors.RESET}")
                move = self.get_cpu_move()
                print(f"CPU chose position {Colors.BOLD}{move}{Colors.RESET}")

            if self.board.make_move(move, self.current_player):
                winner = self.board.check_winner()
                if winner:
                    self.board.display()
                    if winner == 'Draw':
                        print(f"{Colors.YELLOW}{Colors.BOLD}It's a draw!{Colors.RESET}")
                    else:
                        print(f"{Colors.GREEN}{Colors.BOLD}Player {winner} wins!{Colors.RESET}")
                    return winner
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            else:
                print(f"{Colors.RED}Invalid move. Position occupied or out of bounds.{Colors.RESET}")

def main():
    scores = {'X': 0, 'O': 0, 'Draw': 0}
    
    while True:
        print("\n" + "="*30)
        print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}")
        print("1. Play Human vs Human (PvP)")
        print("2. Play Human vs CPU (PvE)")
        print("3. View Scores")
        print("4. Quit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            game = TicTacToe(mode='PvP')
            result = game.play()
            if result and result != 'Draw': scores[result] += 1
            elif result == 'Draw': scores['Draw'] += 1
        elif choice == '2':
            game = TicTacToe(mode='PvE')
            result = game.play()
            if result and result != 'Draw': scores[result] += 1
            elif result == 'Draw': scores['Draw'] += 1
        elif choice == '3':
            print(f"\n{Colors.BOLD}Current Scores:{Colors.RESET}")
            print(f"Player X: {scores['X']}")
            print(f"Player O: {scores['O']}")
            print(f"Draws:    {scores['Draw']}")
        elif choice == '4':
            print("Thanks for playing!")
            break
        else:
            print(f"{Colors.RED}Invalid selection.{Colors.RESET}")

if __name__ == "__main__":
    main()
